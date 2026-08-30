import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.repositories.db_schema import Base, HotelModel, HotelLocationModel, HotelScoreModel, calculate_canonical_content_hash
from app.repositories.postgres_hotel_repository import PostgresHotelRepository
from app.repositories.pgvector_embedding_repository import PgVectorEmbeddingRepository
from app.repositories.postgres_trace_repository import PostgresTraceRepository

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_canonical_content_hash_deterministic():
    rec1 = {
        "hotel_id": "test_1",
        "name": "Hotel Test",
        "area": "Aerocity",
        "trust_score": 95.0,
        "amenities": ["Air Conditioning", "Free Wi-Fi"]
    }
    rec2 = {
        "hotel_id": "test_1",
        "name": "Hotel Test",
        "area": "Aerocity",
        "trust_score": 95.0,
        "amenities": ["Free Wi-Fi", "Air Conditioning"]
    }
    hash1 = calculate_canonical_content_hash(rec1)
    hash2 = calculate_canonical_content_hash(rec2)
    assert hash1 == hash2

def test_postgres_hotel_repository_crud(db_session):
    repo = PostgresHotelRepository(session=db_session)
    hotel_data = {
        "hotel_id": "hotel_101",
        "name": "Test Grand Hotel",
        "area": "Aerocity",
        "city": "Delhi",
        "rating": 4.8,
        "review_count": 120,
        "trust_score": 92.5,
        "aspect_scores": {"cleanliness": 4.9, "service": 4.8}
    }
    count = repo.bulk_upsert([hotel_data])
    assert count == 1
    assert repo.exists("hotel_101")
    retrieved = repo.get_by_id("hotel_101")
    assert retrieved is not None
    assert retrieved["name"] == "Test Grand Hotel"
    assert retrieved["trust_score"] == 92.5

def test_pgvector_embedding_repository(db_session):
    repo = PgVectorEmbeddingRepository(session=db_session)
    chunks = [
        {"chunk_id": "chk_1", "hotel_id": "h1", "snippet": "Clean hotel near Delhi airport", "content_hash": "hash1"},
        {"chunk_id": "chk_2", "hotel_id": "h2", "snippet": "Luxury beach resort with pool", "content_hash": "hash2"}
    ]
    upserted = repo.upsert_embeddings(chunks)
    assert upserted == 2
    assert repo.count() == 2

    res = repo.query_vectors(query_texts=["airport hotel"], n_results=1)
    assert len(res["documents"][0]) == 1
    assert "airport" in res["documents"][0][0].lower()

def test_postgres_trace_repository(db_session):
    repo = PostgresTraceRepository(session=db_session)
    run_data = {"run_id": "run_001", "queries": 10, "status": "SUCCESS"}
    saved = repo.save_run(run_data)
    assert saved is True
    history = repo.get_history(run_id="run_001")
    assert len(history) == 1
    assert history[0]["queries"] == 10
