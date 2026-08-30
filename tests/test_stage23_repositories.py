import os
import pytest
from app.repositories.hotel_repository import CsvHotelRepository
from app.repositories.trace_repository import JsonTraceRepository
from app.repositories.embedding_repository import ChromaEmbeddingRepository
from app.services.data_integrity_service import DataIntegrityService
from app.config.config import settings

def test_csv_hotel_repository_read():
    repo = CsvHotelRepository()
    assert repo.count() > 0
    hotels = repo.get_all_hotels()
    assert len(hotels) == 1661

    # Check representative hotel identity
    sample_id = next(iter(hotels.keys()))
    hotel = repo.get_by_id(sample_id)
    assert hotel is not None
    assert "hotel_id" in hotel
    assert "name" in hotel
    assert "trust_score" in hotel
    assert "area" in hotel
    assert "city" in hotel

def test_json_trace_repository_read():
    repo = JsonTraceRepository()
    history = repo.get_history()
    assert isinstance(history, list)
    assert len(history) > 0

def test_chroma_embedding_repository_read():
    if os.path.exists(settings.VECTOR_STORE_PATH):
        repo = ChromaEmbeddingRepository()
        assert repo.count() == 7910

def test_data_integrity_service_verification():
    service = DataIntegrityService()
    all_passed, report = service.verify_integrity()
    assert all_passed is True
    assert report["checks"]["csv_sha_matches"] is True
    assert report["checks"]["csv_row_count_matches"] is True
    assert report["checks"]["json_run_count_matches"] is True
    assert report["checks"]["chromadb_document_count_matches"] is True
