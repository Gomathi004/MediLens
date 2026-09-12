from app.services.rag_service import (
    index_knowledge_base,
    retrieve_medicine_info,
)


# --------------------------------------------------
# Index Knowledge Base
# --------------------------------------------------

try:
    count = index_knowledge_base()

    print("\n--- KNOWLEDGE BASE ---")
    print(f"Indexed medicines: {count}")

    # --------------------------------------------------
    # Test RAG Retrieval
    # --------------------------------------------------

    results = retrieve_medicine_info(
        "Amoxicillin",
        top_k=3,
    )

    print("\n--- RAG RESULT ---")

    if not results:
        print("No relevant information found.")

    else:
        for index, result in enumerate(
            results,
            start=1,
        ):
            print(f"\nResult {index}")
            print("--------------------")

            print(
                "Medicine:",
                result["metadata"].get(
                    "medicine_name"
                ),
            )

            print(
                "Category:",
                result["metadata"].get(
                    "category"
                ),
            )

            print(
                "Source:",
                result["metadata"].get(
                    "source"
                ),
            )

            print("\nRetrieved Information:")
            print(result["document"])


except Exception as e:
    print("\n--- RAG ERROR ---")
    print(e)