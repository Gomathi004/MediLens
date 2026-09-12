import json
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

KNOWLEDGE_BASE_PATH = (
    BASE_DIR / "knowledge_base" / "medicines.json"
)

VECTOR_DB_PATH = BASE_DIR / "vector_db"


# --------------------------------------------------
# Vector Database
# --------------------------------------------------

embedding_function = (
    embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
)

client = chromadb.PersistentClient(
    path=str(VECTOR_DB_PATH)
)

collection = client.get_or_create_collection(
    name="medicine_knowledge",
    embedding_function=embedding_function,
)


# --------------------------------------------------
# Load Knowledge Base
# --------------------------------------------------

def load_knowledge_base() -> list:
    """
    Load medicine information from medicines.json.
    """

    if not KNOWLEDGE_BASE_PATH.exists():
        raise FileNotFoundError(
            f"Knowledge base not found: {KNOWLEDGE_BASE_PATH}"
        )

    with open(
        KNOWLEDGE_BASE_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


# --------------------------------------------------
# Create Searchable Documents
# --------------------------------------------------

def create_document(medicine: dict) -> str:
    """
    Convert a medicine record into searchable text.
    """

    important_information = medicine.get(
        "important_information",
        [],
    )

    return (
        f"Medicine Name: {medicine.get('medicine_name', '')}. "
        f"Generic Name: {medicine.get('generic_name', '')}. "
        f"Category: {medicine.get('category', '')}. "
        f"Dosage Form: {medicine.get('dosage_form', '')}. "
        f"Common Strengths: "
        f"{', '.join(medicine.get('common_strengths', []))}. "
        f"Route: {medicine.get('route', '')}. "
        f"Description: {medicine.get('description', '')}. "
        f"Simple Explanation: "
        f"{medicine.get('simple_explanation', '')}. "
        f"Important Information: "
        f"{' '.join(important_information)}."
    )


# --------------------------------------------------
# Index Knowledge Base
# --------------------------------------------------

def index_knowledge_base() -> int:
    """
    Add medicine knowledge to the vector database.
    """

    medicines = load_knowledge_base()

    if not medicines:
        return 0

    documents = []
    ids = []
    metadatas = []

    for index, medicine in enumerate(medicines):

        medicine_name = medicine.get(
            "medicine_name",
            f"medicine_{index}",
        )

        documents.append(
            create_document(medicine)
        )

        ids.append(
            medicine_name.lower().replace(" ", "_")
        )

        metadatas.append(
            {
                "medicine_name": medicine_name,
                "category": medicine.get(
                    "category",
                    "",
                ),
                "source": medicine.get(
                    "source",
                    "",
                ),
            }
        )

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )

    return len(documents)


# --------------------------------------------------
# Retrieve Relevant Information
# --------------------------------------------------

def retrieve_medicine_info(
    medicine_name: str,
    top_k: int = 3,
) -> list:
    """
    Retrieve the most relevant medicine information
    from the vector database.
    """

    if not medicine_name:
        return []

    results = collection.query(
        query_texts=[medicine_name],
        n_results=top_k,
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    retrieved_information = []

    for document, metadata in zip(
        documents,
        metadatas,
    ):
        retrieved_information.append(
            {
                "document": document,
                "metadata": metadata,
            }
        )

    return retrieved_information