import os
import sys
import json
import pytest
import psycopg2
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.config.config import settings
from app.repositories.factory import get_hotel_repository, get_embedding_repository, get_trace_repository
from app.repositories.postgres_hotel_repository import PostgresHotelRepository
from app.repositories.pgvector_embedding_repository import PgVectorEmbeddingRepository
from app.services.recommendation_service import RecommendationService
from app.api.main import app

client = TestClient(app)

class TestRuntimeBackendProvenance:
    def test_settings_provenance(self):
        assert settings.DATA_BACKEND == "postgres"
        assert settings.VECTOR_BACKEND == "pgvector"
        assert settings.DATABASE_URL is not None
        assert "postgresql" in settings.DATABASE_URL

    def test_factory_provenance(self):
        h_repo = get_hotel_repository()
        e_repo = get_embedding_repository()
        assert type(h_repo).__name__ == "PostgresHotelRepository"
        assert type(e_repo).__name__ == "PgVectorEmbeddingRepository"

class TestPostgresConnectivity:
    def test_direct_postgres_connection(self):
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            row = conn.execute(text("SELECT current_database(), current_user, version();")).fetchone()
            assert row[0] == "trustlayer_db"
            assert "PostgreSQL 17" in row[2]

class TestDatabaseIntegrity:
    def test_table_counts_and_orphans(self):
        conn = psycopg2.connect(settings.DATABASE_URL)
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM hotels;")
        assert cur.fetchone()[0] == 1661

        cur.execute("SELECT COUNT(DISTINCT hotel_id) FROM hotels;")
        assert cur.fetchone()[0] == 1661

        cur.execute("SELECT COUNT(*) FROM hotel_locations l LEFT JOIN hotels h ON h.hotel_id = l.hotel_id WHERE h.hotel_id IS NULL;")
        assert cur.fetchone()[0] == 0

        cur.execute("SELECT COUNT(*) FROM hotel_scores s LEFT JOIN hotels h ON h.hotel_id = s.hotel_id WHERE h.hotel_id IS NULL;")
        assert cur.fetchone()[0] == 0

        conn.close()

class TestHotelRepository:
    def test_postgres_hotel_repo_methods(self):
        repo = PostgresHotelRepository()
        assert repo.count() == 1661
        
        sample = repo.get_by_id("ChIJCdCLTWgcDTkRgCe4U3CxnUo")
        assert sample is not None
        assert sample["name"] == "Pullman New Delhi Aerocity"

        filtered = repo.list_hotels(area="Aerocity")
        assert len(filtered) > 0

class TestEmbeddingRepository:
    def test_pgvector_embedding_repo_methods(self):
        repo = PgVectorEmbeddingRepository()
        assert repo.count() == 7910

        res = repo.query_vectors("clean hotel in Delhi", 3)
        assert len(res.get("ids", [[]])[0]) == 3

class TestVectorProvenance:
    def test_vector_table_integrity(self):
        conn = psycopg2.connect(settings.DATABASE_URL)
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM embedding_documents;")
        assert cur.fetchone()[0] == 7910

        cur.execute("SELECT COUNT(*) FROM embedding_documents WHERE embedding_vector IS NULL;")
        assert cur.fetchone()[0] == 0

        cur.execute("SELECT chunk_id, COUNT(*) FROM embedding_documents GROUP BY chunk_id HAVING COUNT(*) > 1;")
        assert len(cur.fetchall()) == 0

        conn.close()

class TestAPIEndpoints:
    def test_root_and_v1_endpoints(self):
        r_ready = client.get("/ready")
        assert r_ready.status_code == 200

        r_hotels = client.get("/api/v1/hotels?limit=5")
        assert r_hotels.status_code == 200
        assert len(r_hotels.json()["hotels"]) == 5

        r_single = client.get("/api/v1/hotel/ChIJCdCLTWgcDTkRgCe4U3CxnUo")
        assert r_single.status_code == 200
        assert r_single.json()["name"] == "Pullman New Delhi Aerocity"

class TestRecommendationSystem:
    def test_recommendation_query_processing(self):
        service = RecommendationService()
        recs, traces, meta = service.process_query("clean hotel in Delhi", 5)
        assert len(recs) == 5
        assert recs[0]["name"] is not None

class TestRAGGrounding:
    def test_retrieval_grounding_citations(self):
        repo = PgVectorEmbeddingRepository()
        res = repo.query_vectors("hotel with free wifi near airport", 3)
        docs = res.get("documents", [[]])[0]
        assert len(docs) == 3
        assert len(docs[0]) > 0

class TestOutboxPipeline:
    def test_domain_events_outbox(self):
        conn = psycopg2.connect(settings.DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM domain_events WHERE event_type = 'HOTEL_CREATED';")
        assert cur.fetchone()[0] == 1661
        conn.close()

class TestIdempotency:
    def test_idempotent_query_execution(self):
        repo = PostgresHotelRepository()
        cnt1 = repo.count()
        cnt2 = repo.count()
        assert cnt1 == cnt2 == 1661

class TestLegacyBackendIsolation:
    def test_api_matches_postgres_directly(self):
        res = client.get("/api/v1/hotels?limit=1")
        api_h = res.json()["hotels"][0]
        
        conn = psycopg2.connect(settings.DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT name, rating FROM hotels WHERE hotel_id = %s;", (api_h["hotel_id"],))
        db_row = cur.fetchone()
        conn.close()

        assert db_row is not None
        assert db_row[0] == api_h["name"]

class TestFailureResilience:
    def test_nonexistent_hotel_handling(self):
        res = client.get("/api/v1/hotel/NonExistentHotelID999")
        assert res.status_code == 404

    def test_invalid_limit_handling(self):
        res = client.get("/api/v1/hotels?limit=-5")
        assert res.status_code in (200, 422)

class TestSecurity:
    def test_sql_injection_resilience(self):
        res = client.get("/api/v1/hotel/' OR 1=1 --")
        assert res.status_code in (404, 422)

    def test_no_credential_leak_in_api(self):
        res = client.get("/ready")
        raw_text = res.text
        assert "postgres:postgres" not in raw_text

class TestConcurrency:
    def test_concurrent_postgres_reads(self):
        def fetch_hotel():
            repo = PostgresHotelRepository()
            return repo.get_by_id("ChIJCdCLTWgcDTkRgCe4U3CxnUo")

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(fetch_hotel) for _ in range(5)]
            results = [f.result() for f in futures]
            assert all(r["name"] == "Pullman New Delhi Aerocity" for r in results)
