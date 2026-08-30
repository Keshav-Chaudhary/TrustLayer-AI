import os
import sys
import json
import pytest
import psycopg2
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.config.config import settings
from scripts.ingestion.schema_contract import validate_record_contract
from scripts.ingestion.normalizer import normalize_hotel_record
from scripts.ingestion.deduplicator import deduplicate_records
from scripts.ingestion.diff_engine import compute_postgresql_diff
from scripts.ingestion.pipeline import execute_pipeline
from app.api.main import app

client = TestClient(app)

class TestSchemaContract:
    def test_valid_record(self):
        rec = {"hotel_id": "h123", "hotel_name": "Test Hotel", "rating": 4.5, "review_count": 100, "trust_score": 90.0, "latitude": 28.5, "longitude": 77.1}
        valid, errs = validate_record_contract(rec)
        assert valid
        assert len(errs) == 0

    def test_invalid_rating(self):
        rec = {"hotel_id": "h123", "hotel_name": "Test Hotel", "rating": 6.5}
        valid, errs = validate_record_contract(rec)
        assert not valid
        assert any("Rating out of bounds" in e for e in errs)

class TestNormalizer:
    def test_normalization_whitespace_and_types(self):
        raw = {"hotel_id": "  h123  ", "hotel_name": "  Test Hotel  ", "rating": "4.2", "review_count": "50.0", "amenities": "Wifi, Pool"}
        norm = normalize_hotel_record(raw)
        assert norm["hotel_id"] == "h123"
        assert norm["hotel_name"] == "Test Hotel"
        assert norm["rating"] == 4.2
        assert norm["review_count"] == 50
        assert norm["amenities"] == ["Wifi", "Pool"]

class TestDeduplicator:
    def test_deduplication(self):
        records = [
            {"hotel_id": "h1", "hotel_name": "Hotel 1"},
            {"hotel_id": "h2", "hotel_name": "Hotel 2"},
            {"hotel_id": "h1", "hotel_name": "Hotel 1 Duplicate"}
        ]
        deduped, rejs = deduplicate_records(records)
        assert len(deduped) == 2
        assert len(rejs) == 1
        assert rejs[0]["hotel_id"] == "h1"

class TestDiffEngine:
    def test_diff_against_postgres(self):
        canonical = [
            {"hotel_id": "ChIJCdCLTWgcDTkRgCe4U3CxnUo", "hotel_name": "Pullman New Delhi Aerocity", "rating": 4.7, "review_count": 4843, "city": "Delhi"},
            {"hotel_id": "NEW_TEST_HOTEL_999", "hotel_name": "Brand New Hotel", "rating": 5.0, "review_count": 10, "city": "Delhi"}
        ]
        diff = compute_postgresql_diff(canonical)
        assert diff["total_canonical"] == 2
        assert diff["new_count"] == 1
        assert diff["new_hotels"][0]["hotel_id"] == "NEW_TEST_HOTEL_999"

class TestDryRunSafety:
    def test_dry_run_zero_database_mutation(self):
        conn = psycopg2.connect(settings.DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM hotels;")
        count_before = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM embedding_documents;")
        vec_before = cur.fetchone()[0]

        # Execute dry-run
        res = execute_pipeline(mode="dry-run")
        assert res["mode"] == "dry-run"
        assert res["approved"] is False

        # Verify ZERO mutation in PostgreSQL
        cur.execute("SELECT COUNT(*) FROM hotels;")
        count_after = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM embedding_documents;")
        vec_after = cur.fetchone()[0]

        conn.close()

        assert count_before == count_after == 1661
        assert vec_before == vec_after == 7910

class TestPipelineIdempotency:
    def test_pipeline_dry_run_idempotent(self):
        res1 = execute_pipeline(mode="dry-run")
        res2 = execute_pipeline(mode="dry-run")
        assert res1["diff_summary"]["total_canonical"] == res2["diff_summary"]["total_canonical"] == 1661
        assert res1["diff_summary"]["new_count"] == res2["diff_summary"]["new_count"] == 0
        assert res1["diff_summary"]["updated_count"] == res2["diff_summary"]["updated_count"]

class TestAPIRegression:
    def test_api_serving_from_postgres(self):
        res = client.get("/api/v1/hotels?limit=5")
        assert res.status_code == 200
        assert len(res.json()["hotels"]) == 5
