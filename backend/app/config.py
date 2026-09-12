from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "MediLens API"
    app_version: str = "1.0.0"
    debug: bool = True

    # Clerk
    clerk_secret_key: str = ""
    clerk_publishable_key: str = ""
    clerk_jwt_key: str = ""

    # Database
    database_url: str = ""

    # File storage
    upload_dir: str = "uploads"

    # OCR
    ocr_engine: str = ""

    # ML
    ml_model_path: str = ""

    # RAG
    vector_db_path: str = ""
    knowledge_base_path: str = ""

    # LLM
    llm_api_key: str = ""
    llm_model: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()