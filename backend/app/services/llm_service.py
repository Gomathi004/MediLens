from groq import Groq

from app.config import settings


# --------------------------------------------------
# Groq Client
# --------------------------------------------------

client = Groq(
    api_key=settings.llm_api_key
)


# --------------------------------------------------
# LLM Service
# --------------------------------------------------

def generate_simplified_explanation(
    medicine_info: dict,
    classification: dict,
    retrieved_information: list,
) -> str:
    """
    Generate a simple medicine explanation using
    medicine information, ML classification,
    and RAG-retrieved context.
    """

    medicine_name = medicine_info.get(
        "medicine_name",
        "Unknown",
    )

    strength = medicine_info.get(
        "strength",
        "Not available",
    )

    form = medicine_info.get(
        "form",
        "Not available",
    )

    instructions = medicine_info.get(
        "instructions",
        "Not available",
    )

    expiration_date = medicine_info.get(
        "expiration_date",
        "Not available",
    )

    category = classification.get(
        "category",
        "Unknown",
    )

    # --------------------------------------------------
    # Prepare RAG Context
    # --------------------------------------------------

    rag_context = "\n\n".join(
        item.get("document", "")
        for item in retrieved_information
    )

    # --------------------------------------------------
    # Prompt
    # --------------------------------------------------

    prompt = f"""
You are MediLens, a medicine-label simplification
assistant.

Medicine information:

Medicine name: {medicine_name}
Strength: {strength}
Form: {form}
Label instructions: {instructions}
Expiration date: {expiration_date}
Category: {category}

Trusted retrieved information:

{rag_context}

Explain this medicine label in simple language.

Include:

1. What the medicine is
2. What it is commonly used for
3. What the label instructions say
4. Important safety information from the trusted information
5. Expiration date

Rules:

- Use only the information provided above.
- Do not invent medical facts.
- Do not diagnose the user.
- Do not recommend changing the dose.
- Do not recommend starting or stopping the medicine.
- Do not provide medical advice beyond the supplied information.

End with:

"This information is for understanding the medicine label
and is not a substitute for advice from a healthcare professional."
"""

    # --------------------------------------------------
    # Generate Groq Response
    # --------------------------------------------------

    response = client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are MediLens, a medicine-label "
                    "simplification assistant. Provide "
                    "clear and simple explanations based "
                    "only on the supplied information."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    result = response.choices[0].message.content

    if not result:
        raise ValueError(
            "Groq returned an empty response."
        )

    return result.strip()