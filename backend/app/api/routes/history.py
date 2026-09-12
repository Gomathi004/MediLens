from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import CurrentUser
from app.database import get_db
from app.models.analysis import MedicineAnalysis


# ==================================================
# Router
# ==================================================

router = APIRouter(
    prefix="/history",
    tags=["History"],
)


# ==================================================
# Get User History
# ==================================================

@router.get("/")
def get_history(
    user_id: CurrentUser,
    db: Session = Depends(get_db),
):
    """
    Return medicine analyses belonging only to the
    currently authenticated Clerk user.
    """

    try:
        analyses = (
            db.query(MedicineAnalysis)
            .filter(
                MedicineAnalysis.clerk_user_id == user_id
            )
            .order_by(
                MedicineAnalysis.created_at.desc()
            )
            .all()
        )

        return {
            "success": True,
            "count": len(analyses),
            "history": [
                {
                    "id": analysis.id,
                    "medicine_name": analysis.medicine_name,
                    "strength": analysis.strength,
                    "form": analysis.form,
                    "category": analysis.category,
                    "instructions": analysis.instructions,
                    "expiration_date": analysis.expiration_date,
                    "explanation": analysis.explanation,
                    "created_at": analysis.created_at.isoformat(),
                }
                for analysis in analyses
            ],
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve history: {str(e)}",
        )