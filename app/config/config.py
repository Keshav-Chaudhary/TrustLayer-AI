import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "TrustLayer-AI Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Active Storage Backend Configuration
    # Safe Production Default: DATA_BACKEND=csv, VECTOR_BACKEND=chroma
    DATA_BACKEND: str = Field(default="csv", validation_alias="DATA_BACKEND")
    VECTOR_BACKEND: str = Field(default="chroma", validation_alias="VECTOR_BACKEND")
    DATABASE_URL: Optional[str] = Field(default=None, validation_alias="DATABASE_URL")

    # Data Paths
    CSV_DATASET_PATH: str = Field(default="data/exports/final_hotel_dataset.csv", validation_alias="CSV_DATASET_PATH")
    BATCH_DEBUG_FILE_PATH: str = Field(default="data/exports/batch_debug_results.json", validation_alias="BATCH_DEBUG_FILE_PATH")
    VECTOR_STORE_PATH: str = Field(default="data/vector_store", validation_alias="VECTOR_STORE_PATH")
    
    # LLM & Vector Store Settings
    OLLAMA_ENDPOINT: str = Field(default="http://127.0.0.1:11434", validation_alias="OLLAMA_ENDPOINT")
    OLLAMA_MODEL: str = Field(default="qwen2.5:7b-instruct", validation_alias="OLLAMA_MODEL")
    EMBEDDING_MODEL: str = Field(default="all-MiniLM-L6-v2", validation_alias="EMBEDDING_MODEL")
    
    # Operational Limits & Thresholds
    RETRIEVAL_TOP_K: int = Field(default=10, validation_alias="RETRIEVAL_TOP_K")
    CANDIDATE_POOL_SIZE: int = Field(default=50, validation_alias="CANDIDATE_POOL_SIZE")
    QUALITY_GATE_TRUST_THRESHOLD: float = Field(default=70.0, validation_alias="QUALITY_GATE_TRUST_THRESHOLD")
    MAX_BATCH_QUERIES: int = Field(default=100, validation_alias="MAX_BATCH_QUERIES")
    CACHE_TTL_SECONDS: int = Field(default=3600, validation_alias="CACHE_TTL_SECONDS")
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
