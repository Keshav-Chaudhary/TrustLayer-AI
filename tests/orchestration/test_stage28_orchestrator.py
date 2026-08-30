import os
import sys
import json
import pytest
import psycopg2
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.config.config import settings
from scripts.orchestrator import MasterOrchestrator, compute_sha256, validate_environment
from app.api.main import app

client = TestClient(app)

class TestOrchestratorValidation:
    def test_environment_validation(self):
        env = validate_environment()
        assert env["postgres_connected"] is True
        assert env["hotels_count"] == 1661
        assert env["embeddings_count"] == 7910

    def test_sha256_computation(self):
        csv_path = "data/exports/final_hotel_dataset.csv"
        sha = compute_sha256(csv_path)
        assert sha is not None
        assert len(sha) == 64

class TestOrchestratorExecution:
    def test_full_pipeline_dry_run_safety(self):
        conn = psycopg2.connect(settings.DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM hotels;")
        h_before = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM embedding_documents;")
        e_before = cur.fetchone()[0]

        orchestrator = MasterOrchestrator()
        # Test dry-run stage safety directly
        diff_res = orchestrator.run_dry_run()
        assert diff_res["mode"] == "dry-run"
        assert diff_res["approved"] is False

        cur.execute("SELECT COUNT(*) FROM hotels;")
        h_after = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM embedding_documents;")
        e_after = cur.fetchone()[0]
        conn.close()

        # Zero mutation proof
        assert h_before == h_after == 1661
        assert e_before == e_after == 7910

    def test_stale_run_id_rejection(self):
        with pytest.raises(Exception):
            from scripts.ingestion.pipeline import execute_pipeline
            execute_pipeline(mode="apply", run_id="INVALID_STALE_RUN_ID_999999")

class TestAPIRegression:
    def test_api_health_check(self):
        res = client.get("/ready")
        assert res.status_code == 200

    def test_api_hotels_retrieval(self):
        res = client.get("/api/v1/hotels?limit=5")
        assert res.status_code == 200
        assert len(res.json()["hotels"]) == 5
