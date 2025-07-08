import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Configurações da aplicação Hotmart AI System"""

    # API Configuration
    API_HOST: str = "localhost"
    API_PORT: int = 8000
    API_VERSION: str = "v1"
    API_PREFIX: str = f"/api/{API_VERSION}"

    # Hugging Face Configuration
    HUGGINGFACE_API_KEY: Optional[str] = os.getenv("HF_TOKEN")
    HUGGINGFACE_MODEL: str = "meta-llama/Llama-3.3-70B-Instruct"    

    # ChromaDB Configuration
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "project_faq"

    # Embedding Configuration
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # Journey Agent Configuration
    JOURNEY_ELIGIBILITY_THRESHOLD: float = 1000.0  # Valor mínimo para elegibilidade
    JOURNEY_PREMIUM_THRESHOLD: float = 5000.0  # Valor para benefícios premium

    # Security
    SECRET_KEY: str = "hotmart-ai-system-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"

    # Testing
    TESTING: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True

# Instância global das configurações
settings = Settings()