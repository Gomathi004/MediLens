from app.services.llm_service import (
    generate_simplified_explanation,
)


print("Starting MediLens LLM test...")


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
# Sample ML Result
# --------------------------------------------------

classification = {
    "category": "Antibiotic",
    "confidence": 0.95,
}


# --------------------------------------------------
# Sample RAG Result
# --------------------------------------------------

retrieved_information = [
    {
        "document": (
            "Medicine Name: Amoxicillin. "
            "Generic Name: Amoxicillin. "
            "Category: Antibiotic. "
            "Dosage Form: Capsule. "
            "Common Strengths: 250 mg, 500 mg. "
            "Route: Oral. "
            "Description: Amoxicillin is a "
            "penicillin-class antibacterial medicine "
            "used to treat certain bacterial infections. "
            "Simple Explanation: Amoxicillin is an "
            "antibiotic used to treat certain bacterial "
            "infections. "
            "Important Information: Use this medicine "
            "only as directed by a healthcare professional."
        ),
        "metadata": {
            "medicine_name": "Amoxicillin",
            "category": "Antibiotic",
            "source": "DailyMed",
        },
    }
]


# --------------------------------------------------
# Run LLM
# --------------------------------------------------

try:

    print("Sending request to Groq...")

    explanation = generate_simplified_explanation(
        medicine_info=medicine_info,
        classification=classification,
        retrieved_information=retrieved_information,
    )

    print("\n--- LLM RESULT ---")
    print(explanation)

except Exception as e:

    print("\n--- LLM ERROR ---")
    print(type(e).__name__)
    print(e)