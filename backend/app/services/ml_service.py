import re


# --------------------------------------------------
# ML Service
# --------------------------------------------------

def classify_medicine(medicine_info: dict) -> dict:
    """
    Classify the medicine information into a basic
    medicine category.

    This is a lightweight classification layer for
    the current MediLens prototype. It can later be
    replaced with a trained ML model.
    """

    medicine_name = medicine_info.get("medicine_name")

    if not medicine_name:
        return {
            "category": "Unknown",
            "confidence": 0.0,
        }

    medicine_name_lower = medicine_name.lower()

    # --------------------------------------------------
    # Medicine Categories
    # --------------------------------------------------

    categories = {
        "Antibiotic": [
            "amoxicillin",
            "azithromycin",
            "cephalexin",
            "ciprofloxacin",
            "doxycycline",
        ],
        "Pain Reliever": [
            "paracetamol",
            "acetaminophen",
            "ibuprofen",
            "naproxen",
        ],
        "Antihistamine": [
            "cetirizine",
            "loratadine",
            "fexofenadine",
            "levocetirizine",
        ],
        "Antacid": [
            "omeprazole",
            "pantoprazole",
            "esomeprazole",
            "famotidine",
        ],
    }

    # --------------------------------------------------
    # Classification
    # --------------------------------------------------

    for category, medicines in categories.items():

        for medicine in medicines:

            if re.search(
                rf"\b{re.escape(medicine)}\b",
                medicine_name_lower,
            ):
                return {
                    "category": category,
                    "confidence": 0.95,
                }

    # --------------------------------------------------
    # Unknown Medicine
    # --------------------------------------------------

    return {
        "category": "Other",
        "confidence": 0.50,
    }