from app.config.config import settings
from app.repositories.base import BaseHotelRepository, BaseTraceRepository, BaseEmbeddingRepository
from app.repositories.hotel_repository import CsvHotelRepository
from app.repositories.trace_repository import JsonTraceRepository
from app.repositories.embedding_repository import ChromaEmbeddingRepository
from app.repositories.postgres_hotel_repository import PostgresHotelRepository
from app.repositories.postgres_trace_repository import PostgresTraceRepository
from app.repositories.pgvector_embedding_repository import PgVectorEmbeddingRepository

def get_hotel_repository() -> BaseHotelRepository:
    """
    Returns the active Hotel Repository instance based on settings.DATA_BACKEND.
    Default safe production value: 'csv'
    """
    if settings.DATA_BACKEND.lower() == "postgres":
        return PostgresHotelRepository()
    return CsvHotelRepository()

def get_trace_repository() -> BaseTraceRepository:
    """
    Returns the active Trace Repository instance based on settings.DATA_BACKEND.
    Default safe production value: 'json' (or 'csv' default)
    """
    if settings.DATA_BACKEND.lower() == "postgres":
        return PostgresTraceRepository()
    return JsonTraceRepository()

def get_embedding_repository() -> BaseEmbeddingRepository:
    """
    Returns the active Embedding Repository instance based on settings.VECTOR_BACKEND.
    Default safe production value: 'chroma'
    """
    if settings.VECTOR_BACKEND.lower() == "pgvector":
        return PgVectorEmbeddingRepository()
    return ChromaEmbeddingRepository()
