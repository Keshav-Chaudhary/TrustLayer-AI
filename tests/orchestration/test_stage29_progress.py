import os
import sys
import json
import pytest
import psycopg2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.config.config import settings
from scripts.orchestration.progress import ProgressTracker
from scripts.orchestrator import MasterOrchestrator, validate_environment

class TestProgressTracker:
    def test_progress_tracker_transitions(self, tmp_path):
        log_file = os.path.join(tmp_path, "pipeline.log")
        tracker = ProgressTracker(run_id="test-run-123", total_stages=6, log_file=log_file)
        
        assert tracker.stages[0]["status"] == "PENDING"
        
        tracker.start_stage(0, "fetch_google_places.py")
        assert tracker.stages[0]["status"] == "RUNNING"
        
        tracker.complete_stage(0, records=1661, output_path="data/raw/test.csv")
        assert tracker.stages[0]["status"] == "COMPLETED"
        assert tracker.stages[0]["records"] == 1661

        assert os.path.exists(log_file)

    def test_progress_tracker_failure(self, tmp_path):
        log_file = os.path.join(tmp_path, "pipeline.log")
        tracker = ProgressTracker(run_id="test-run-fail", total_stages=6, log_file=log_file)
        
        tracker.start_stage(1, "clean_hotel_metadata.py")
        tracker.fail_stage(1, "File not found")
        assert tracker.stages[1]["status"] == "FAILED"

class TestOrchestratorSafety:
    def test_zero_mutation_during_dry_run(self):
        conn = psycopg2.connect(settings.DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM hotels;")
        h_before = cur.fetchone()[0]
        conn.close()

        orchestrator = MasterOrchestrator()
        res = orchestrator.run_dry_run()

        conn = psycopg2.connect(settings.DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM hotels;")
        h_after = cur.fetchone()[0]
        conn.close()

        assert res["mode"] == "dry-run"
        assert h_before == h_after == 1661

    def test_status_command_execution(self):
        env = validate_environment()
        assert env["postgres_connected"] is True
        assert env["hotels_count"] == 1661
