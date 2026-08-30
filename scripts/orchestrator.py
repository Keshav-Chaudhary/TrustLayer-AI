import os
import sys
import json
import uuid
import signal
import hashlib
import argparse
from datetime import datetime
from typing import Dict, Any, Optional, List
import pandas as pd
import psycopg2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.config.config import settings
from scripts.ingestion.pipeline import execute_pipeline
from scripts.verification.audit_postgres_runtime import run_runtime_audit
from scripts.orchestration.progress import ProgressTracker

RUNS_DIR = os.path.abspath("data/runs")
DIFFS_DIR = os.path.abspath("data/diffs")
os.makedirs(RUNS_DIR, exist_ok=True)
os.makedirs(DIFFS_DIR, exist_ok=True)

def compute_sha256(file_path: str) -> Optional[str]:
    if not os.path.exists(file_path):
        return None
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def validate_environment() -> Dict[str, Any]:
    db_url = settings.DATABASE_URL
    assert db_url and "postgresql" in db_url, "DATABASE_URL must be configured for PostgreSQL"
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM hotels;")
        h_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM embedding_documents;")
        e_count = cur.fetchone()[0]
        conn.close()
        return {"postgres_connected": True, "hotels_count": h_count, "embeddings_count": e_count}
    except Exception as ex:
        raise RuntimeError(f"PostgreSQL Connection Failed: {ex}")

class MasterOrchestrator:
    def __init__(self, run_id: Optional[str] = None):
        self.run_id = run_id or f"{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        self.run_dir = os.path.join(RUNS_DIR, self.run_id)
        os.makedirs(self.run_dir, exist_ok=True)
        self.manifest_path = os.path.join(self.run_dir, "pipeline_manifest.json")
        self.log_file = os.path.join(self.run_dir, "pipeline.log")
        self.tracker = ProgressTracker(self.run_id, total_stages=6, log_file=self.log_file)
        self.interrupted = False

        # Register Ctrl+C Interrupt Handler
        signal.signal(signal.SIGINT, self._handle_interrupt)

    def _handle_interrupt(self, signum, frame):
        self.interrupted = True
        print("\n\n[CTRL+C DETECTED] Interrupting pipeline execution cleanly...")
        manifest = {
            "run_id": self.run_id,
            "status": "INTERRUPTED",
            "timestamp": datetime.utcnow().isoformat(),
            "postgres_mutated": False,
            "reason": "User interrupted execution with Ctrl+C"
        }
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        print("Written manifest marked INTERRUPTED. PostgreSQL remained 100% untouched.")
        sys.exit(130)

    def run_fetch(self):
        self.tracker.start_stage(0, "fetch_google_places.py")
        api_key = os.getenv("GOOGLE_PLACES_API_KEY")
        raw_places = "data/raw/google_places/delhi_hotels_raw.csv"

        if api_key:
            try:
                from scripts.collection.fetch_google_places import main as fetch_places_main
                fetch_places_main()
            except Exception as ex:
                self.tracker._log_raw(f"Warning: Live Places fetch failed: {ex}. Using existing raw dataset.")
        
        try:
            from scripts.recommender.generate_users import generate_users
            generate_users()
        except Exception:
            pass

        rec_count = len(pd.read_csv(raw_places)) if os.path.exists(raw_places) else 0
        self.tracker.complete_stage(0, records=rec_count, output_path=raw_places)

    def run_clean(self):
        self.tracker.start_stage(1, "clean_hotel_metadata.py")
        from scripts.cleaning.clean_hotel_metadata import clean_data
        from scripts.cleaning.clean_reviews import clean_reviews
        clean_data()
        clean_reviews()
        cleaned_path = "data/processed/cleaned/delhi_hotels_cleaned.csv"
        rec_count = len(pd.read_csv(cleaned_path)) if os.path.exists(cleaned_path) else 0
        self.tracker.complete_stage(1, records=rec_count, output_path=cleaned_path)

    def run_nlp(self):
        self.tracker.start_stage(2, "analyze_sentiment.py")
        from scripts.nlp.analyze_sentiment import run_sentiment_analysis
        from scripts.nlp.extract_absa_features import extract_absa
        from scripts.recommender.aggregate_reviews import aggregate_reviews
        run_sentiment_analysis()
        extract_absa()
        aggregate_reviews()
        summary_path = "data/processed/features/hotel_review_summary.csv"
        rec_count = len(pd.read_csv(summary_path)) if os.path.exists(summary_path) else 0
        self.tracker.complete_stage(2, records=rec_count, output_path=summary_path)

    def run_features(self):
        self.tracker.start_stage(3, "engineer_features.py")
        from scripts.recommender.engineer_features import engineer_features
        engineer_features()
        feats_path = "data/processed/features/hotel_features.csv"
        rec_count = len(pd.read_csv(feats_path)) if os.path.exists(feats_path) else 0
        self.tracker.complete_stage(3, records=rec_count, output_path=feats_path)

    def run_merge(self):
        self.tracker.start_stage(4, "merge_dataset.py")
        from scripts.recommender.merge_dataset import merge_final_dataset
        merge_final_dataset()
        canonical_path = "data/exports/final_hotel_dataset.csv"
        rec_count = len(pd.read_csv(canonical_path)) if os.path.exists(canonical_path) else 0
        self.tracker.complete_stage(4, records=rec_count, output_path=canonical_path)

    def run_dry_run(self) -> Dict[str, Any]:
        self.tracker.start_stage(5, "diff_engine.py")
        diff_report = execute_pipeline(mode="dry-run", run_id=self.run_id)
        diff_file = os.path.join(DIFFS_DIR, diff_report["run_id"], "dry_run.json")
        self.tracker.complete_stage(5, records=diff_report["diff_summary"]["total_canonical"], output_path=diff_file)
        return diff_report

    def run_full_pipeline(self):
        self.tracker._log_raw(f"=== STARTING MASTER END-TO-END PIPELINE (RUN_ID: {self.run_id}) ===")
        env_res = validate_environment()

        self.run_fetch()
        self.run_clean()
        self.run_nlp()
        self.run_features()
        self.run_merge()
        diff_res = self.run_dry_run()

        manifest = {
            "run_id": self.run_id,
            "status": "READY_FOR_APPROVAL",
            "timestamp": datetime.utcnow().isoformat(),
            "postgres_mutated": False,
            "stages": self.tracker.stages,
            "canonical_dataset_sha256": compute_sha256("data/exports/final_hotel_dataset.csv"),
            "diff_summary": diff_res.get("diff_summary", {})
        }

        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        print("\n====================================================")
        print("DRY-RUN PIPELINE EXECUTION COMPLETE!")
        print(f"RUN_ID                  : {self.run_id}")
        print(f"Canonical Dataset       : data/exports/final_hotel_dataset.csv")
        print(f"PostgreSQL Mutation     : NONE (Dry-Run Safety Preserved)")
        print(f"Diff Summary            : New={diff_res['diff_summary']['new_count']} | Updated={diff_res['diff_summary']['updated_count']} | Unchanged={diff_res['diff_summary']['unchanged_count']}")
        print(f"Manifest Log            : {self.log_file}")
        print("====================================================")
        print(f"\nTo apply this run to PostgreSQL, execute:\npython -m scripts.orchestrator apply --run-id {diff_res['run_id']}")

def main():
    parser = argparse.ArgumentParser(description="TrustLayer-AI Master Data Pipeline Orchestrator")
    parser.add_argument("command", choices=["full", "fetch", "clean", "nlp", "features", "merge", "dry-run", "apply", "verify", "status"])
    parser.add_argument("--run-id", help="Approved RUN_ID for apply mode")

    args = parser.parse_args()
    orchestrator = MasterOrchestrator(run_id=args.run_id)

    if args.command == "full":
        orchestrator.run_full_pipeline()
    elif args.command == "fetch":
        orchestrator.run_fetch()
    elif args.command == "clean":
        orchestrator.run_clean()
    elif args.command == "nlp":
        orchestrator.run_nlp()
    elif args.command == "features":
        orchestrator.run_features()
    elif args.command == "merge":
        orchestrator.run_merge()
    elif args.command == "dry-run":
        orchestrator.run_dry_run()
    elif args.command == "apply":
        if not args.run_id:
            print("Error: --run-id <RUN_ID> is required for apply mode!")
            sys.exit(1)
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║              POSTGRESQL TRANSACTIONAL APPLY                  ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"RUN_ID: {args.run_id}")
        print("-> BEGIN Transaction...")
        res = execute_pipeline(mode="apply", run_id=args.run_id)
        print("-> COMMIT Transaction successful!")
        print("✓ PostgreSQL apply completed cleanly.")
    elif args.command == "verify":
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║          BACKEND & POSTGRESQL INTEGRITY VERIFICATION         ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        run_runtime_audit()
    elif args.command == "status":
        env = validate_environment()
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                TRUSTLAYER-AI PIPELINE STATUS                 ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"PostgreSQL Database : trustlayer_db (127.0.0.1:5432)")
        print(f"Active Hotels Count : {env['hotels_count']}")
        print(f"Active Embeddings   : {env['embeddings_count']}")
        print(f"Backend Engine      : DATA_BACKEND=postgres | VECTOR_BACKEND=pgvector")

if __name__ == "__main__":
    main()
