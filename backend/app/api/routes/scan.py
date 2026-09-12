from pathlib import Path
import shutil
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.auth import CurrentUser
from app.config import settings
from app.database import get_db
from app.models.analysis import MedicineAnalysis

from app.services.llm_service import (
    generate_simplified_explanation,
)
from app.services.ml_service import classify_medicine
from app.services.nlp_service import extract_medicine_info
from app.services.ocr_service import extract_text
from app.services.rag_service import (
    index_knowledge_base,
    retrieve_medicine_info,
)


# ==================================================
# Router
# ==================================================

router = APIRouter(
    prefix="/scan",
    tags=["Scan"],
)


# ==================================================
# Upload Directory
# ==================================================

UPLOAD_DIR = Path(settings.upload_dir)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ==================================================
# Scan Medicine Label
# ==================================================

@router.post("/")
async def scan_medicine(
    user_id: CurrentUser,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload a medicine-label image and process it
    through the complete MediLens AI pipeline.

    The authenticated Clerk user ID is used to
    associate the analysis with the current user.

    The completed analysis is also stored in
    PostgreSQL for history.
    """

    # --------------------------------------------------
    # Validate File
    # --------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was provided.",
        )

    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    }

    file_extension = Path(
        file.filename
    ).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Please upload JPG, JPEG, PNG, or WEBP."
            ),
        )

    # --------------------------------------------------
    # Create Unique File Name
    # --------------------------------------------------

    unique_filename = (
        f"{uuid.uuid4()}{file_extension}"
    )

    image_path = UPLOAD_DIR / unique_filename

    # --------------------------------------------------
    # Save Uploaded Image
    # --------------------------------------------------

    try:
        with open(
            image_path,
            "wb",
        ) as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Failed to save uploaded image: {str(e)}"
            ),
        )

    # ==================================================
    # OCR
    # ==================================================

    try:
        raw_text = extract_text(
            str(image_path)
        )

    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"OCR processing failed: {str(e)}",
        )

    # ==================================================
    # NLP
    # ==================================================

    try:
        medicine_info = extract_medicine_info(
            raw_text
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"NLP processing failed: {str(e)}",
        )

    medicine_name = medicine_info.get(
        "medicine_name"
    )

    if not medicine_name:
        raise HTTPException(
            status_code=422,
            detail=(
                "Could not identify the medicine name "
                "from the uploaded label."
            ),
        )

    # ==================================================
    # ML Classification
    # ==================================================

    try:
        classification = classify_medicine(
            medicine_info
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Medicine classification failed: {str(e)}"
            ),
        )

    # ==================================================
    # RAG
    # ==================================================

    try:
        index_knowledge_base()

        retrieved_information = (
            retrieve_medicine_info(
                medicine_name,
                top_k=3,
            )
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=(
                f"RAG processing failed: {str(e)}"
            ),
        )

    # ==================================================
    # LLM
    # ==================================================

    try:
        explanation = (
            generate_simplified_explanation(
                medicine_info=medicine_info,
                classification=classification,
                retrieved_information=(
                    retrieved_information
                ),
            )
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=(
                f"LLM processing failed: {str(e)}"
            ),
        )

    # ==================================================
    # Save Analysis to PostgreSQL
    # ==================================================

    analysis = MedicineAnalysis(
        clerk_user_id=user_id,

        medicine_name=medicine_name,

        strength=medicine_info.get(
            "strength"
        ),

        form=medicine_info.get(
            "form"
        ),

        category=classification.get(
            "category"
        ),

        instructions=medicine_info.get(
            "instructions"
        ),

        expiration_date=medicine_info.get(
            "expiration_date"
        ),

        explanation=explanation,

        raw_text=raw_text,
    )

    try:
        db.add(analysis)

        db.commit()

        db.refresh(analysis)

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=(
                f"Failed to save analysis: {str(e)}"
            ),
        )

    # ==================================================
    # Response
    # ==================================================

    return {
        "success": True,

        "message": (
            "Medicine label processed successfully."
        ),

        "analysis_id": analysis.id,

        "user_id": user_id,

        "medicine": medicine_info,

        "classification": classification,

        "retrieved_information": (
            retrieved_information
        ),

        "explanation": explanation,
    }