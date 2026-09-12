from pathlib import Path

import pytesseract

from PIL import (
    Image,
    ImageEnhance,
    ImageOps,
)


# ==================================================
# Tesseract Configuration
# ==================================================

TESSERACT_PATH = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

if Path(TESSERACT_PATH).exists():
    pytesseract.pytesseract.tesseract_cmd = (
        TESSERACT_PATH
    )


# ==================================================
# Image Preprocessing
# ==================================================

def preprocess_image(
    image: Image.Image,
) -> Image.Image:
    """
    Prepare the uploaded image for OCR.

    A lightweight preprocessing pipeline is used
    to keep OCR reasonably accurate while reducing
    unnecessary processing time.
    """

    # --------------------------------------------------
    # Convert to RGB
    # --------------------------------------------------

    image = image.convert("RGB")

    # --------------------------------------------------
    # Resize small images
    # --------------------------------------------------

    width, height = image.size

    minimum_width = 1200

    if width < minimum_width:

        scale = (
            minimum_width / width
        )

        image = image.resize(
            (
                int(width * scale),
                int(height * scale),
            ),
            Image.Resampling.LANCZOS,
        )

    # --------------------------------------------------
    # Convert to grayscale
    # --------------------------------------------------

    image = ImageOps.grayscale(
        image
    )

    # --------------------------------------------------
    # Improve contrast
    # --------------------------------------------------

    image = ImageOps.autocontrast(
        image
    )

    image = ImageEnhance.Contrast(
        image
    ).enhance(1.4)

    # --------------------------------------------------
    # Slightly improve sharpness
    # --------------------------------------------------

    image = ImageEnhance.Sharpness(
        image
    ).enhance(1.5)

    return image


# ==================================================
# OCR Helper
# ==================================================

def run_ocr(
    image: Image.Image,
    psm_mode: int,
) -> str:
    """
    Run Tesseract OCR using the specified
    page segmentation mode.
    """

    try:

        text = pytesseract.image_to_string(
            image,
            config=f"--oem 3 --psm {psm_mode}",
        )

        return text.strip()

    except Exception:

        return ""


# ==================================================
# OCR Text Scoring
# ==================================================

def score_text(
    text: str,
) -> int:
    """
    Calculate a simple quality score for OCR text.

    Results with more readable words and
    alphanumeric characters receive a higher score.
    """

    if not text:
        return 0

    words = text.split()

    alphanumeric_characters = sum(
        character.isalnum()
        for character in text
    )

    return (
        len(words) * 10
        + alphanumeric_characters
    )


# ==================================================
# OCR Text Cleaning
# ==================================================

def clean_text(
    text: str,
) -> str:
    """
    Clean OCR output while preserving line structure.

    Keeping separate lines is important because
    the NLP service can use the original label layout
    to identify medicine names such as:

        BANABA
        BLEND
    """

    cleaned_lines = []

    for line in text.splitlines():

        line = " ".join(
            line.strip().split()
        )

        if line:
            cleaned_lines.append(
                line
            )

    return "\n".join(
        cleaned_lines
    )


# ==================================================
# OCR Service
# ==================================================

def extract_text(
    image_path: str,
) -> str:
    """
    Extract text from a medicine-label image.

    The service first performs one fast OCR pass
    using PSM 6.

    If the result is too weak, additional OCR modes
    are attempted.

    This reduces the previous 12 OCR operations
    to normally 1, and at most 3.
    """

    path = Path(image_path)

    # --------------------------------------------------
    # Validate image path
    # --------------------------------------------------

    if not path.exists():

        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    try:

        # --------------------------------------------------
        # Open image
        # --------------------------------------------------

        with Image.open(path) as image:

            # --------------------------------------------------
            # Preprocess image
            # --------------------------------------------------

            processed_image = (
                preprocess_image(
                    image.copy()
                )
            )

        # --------------------------------------------------
        # Fast OCR pass
        # --------------------------------------------------

        best_text = run_ocr(
            processed_image,
            6,
        )

        best_score = score_text(
            best_text
        )

        # --------------------------------------------------
        # Extra OCR passes only when needed
        # --------------------------------------------------

        # If the first OCR result is reasonably useful,
        # don't perform additional expensive OCR calls.

        if best_score < 80:

            for psm_mode in [
                11,
                12,
            ]:

                candidate_text = run_ocr(
                    processed_image,
                    psm_mode,
                )

                candidate_score = (
                    score_text(
                        candidate_text
                    )
                )

                if candidate_score > best_score:

                    best_text = (
                        candidate_text
                    )

                    best_score = (
                        candidate_score
                    )

        # --------------------------------------------------
        # Validate OCR result
        # --------------------------------------------------

        if not best_text.strip():

            raise ValueError(
                "No readable text found in the image. "
                "Please upload a clearer medicine-label image."
            )

        # --------------------------------------------------
        # Clean final OCR text
        # --------------------------------------------------

        final_text = clean_text(
            best_text
        )

        if not final_text:

            raise ValueError(
                "No readable text found in the image. "
                "Please upload a clearer medicine-label image."
            )

        return final_text

    except FileNotFoundError:

        raise

    except ValueError:

        raise

    except Exception as e:

        raise RuntimeError(
            f"OCR processing failed: {str(e)}"
        )