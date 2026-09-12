from app.services.ml_service import classify_medicine


# --------------------------------------------------
# Sample NLP Result
# --------------------------------------------------

medicine_info = {
    "medicine_name": "Amoxicillin",
    "strength": "500 mg",
    "form": "Capsule",
    "instructions": (
        "TAKE 1 CAPSULE BY MOUTH "
        "THREE TIMES DAILY FOR 10 DAYS"
    ),
    "expiration_date": "09/06/2026",
}


# --------------------------------------------------
# Run ML Classification
# --------------------------------------------------

try:
    result = classify_medicine(medicine_info)

    print("\n--- ML RESULT ---")
    print(f"Category   : {result['category']}")
    print(f"Confidence : {result['confidence']}")

except Exception as e:
    print("\n--- ML ERROR ---")
    print(e)