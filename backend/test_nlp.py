import sys
from pathlib import Path

from app.services.nlp_service import (
    extract_medicine_info,
)


# ==================================================
# Select Image
# ==================================================

if len(sys.argv) > 1:
    image_name = sys.argv[1]
else:
    image_name = "test_medicine.jpg"


# ==================================================
# Image Paths
# ==================================================

BACKEND_DIR = Path(__file__).resolve().parent

PROJECT_DIR = BACKEND_DIR.parent

IMAGE_PATH = PROJECT_DIR / "images" / image_name

BACKEND_IMAGE_PATH = BACKEND_DIR / image_name


if IMAGE_PATH.exists():
    selected_image = IMAGE_PATH

elif BACKEND_IMAGE_PATH.exists():
    selected_image = BACKEND_IMAGE_PATH

else:
    print(
        f"\nImage not found: {image_name}"
    )

    print("\nExpected locations:")

    print(IMAGE_PATH)

    print(BACKEND_IMAGE_PATH)

    raise SystemExit(1)


print(
    f"\nTesting image: {selected_image}"
)


# ==================================================
# OCR
# ==================================================

from app.services.ocr_service import extract_text


try:

    raw_text = extract_text(
        str(selected_image)
    )

except Exception as e:

    print("\n--- OCR ERROR ---")

    print(type(e).__name__)

    print(e)

    raise SystemExit(1)


# ==================================================
# NLP
# ==================================================

try:

    medicine_info = extract_medicine_info(
        raw_text
    )

except Exception as e:

    print("\n--- NLP ERROR ---")

    print(type(e).__name__)

    print(e)

    raise SystemExit(1)


# ==================================================
# Display Result
# ==================================================

print("\n--- OCR TEXT ---")

print(raw_text)


print("\n--- NLP RESULT ---")

print(
    "Medicine Name :",
    medicine_info.get(
        "medicine_name"
    ),
)

print(
    "Strength      :",
    medicine_info.get(
        "strength"
    ),
)

print(
    "Form          :",
    medicine_info.get(
        "form"
    ),
)

print(
    "Instructions  :",
    medicine_info.get(
        "instructions"
    ),
)

print(
    "Expiration    :",
    medicine_info.get(
        "expiration_date"
    ),
)


print("\n--- CLEANED TEXT ---")

print(
    medicine_info.get(
        "cleaned_text"
    )
)