import os
import sys
import json
import uuid
import hashlib
import argparse
from datetime import datetime
from typing import Dict, Any, Optional
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.config.config import settings
from scripts.ingestion.schema_contract import validate_record_contract
from scripts.ingestion.normalizer import normalize_hotel_record
from scripts.ingestion.deduplicator import deduplicate_records
from scripts.ingestion.diff_engine import compute_postgresql_diff
from scripts.ingestion.bootstrap_postgres import run_bootstrap
from scripts.ingestion.selective_vector_sync import sync_selective_vectors

DIFFS_DIR = os.path.abspath("data/diffs")
os.makedirs(DIFFS_DIR, exist_ok=True)

def execute_pipeline(
    mode: str = "dry-run",
    run_id: Optional[str] = None,
    source_csv: Optional[str] = None,
    db_url: Optional[str] = None
) -> Dict[str, Any]:
    target_csv = source_csv or settings.CSV_DATASET_PATH
    target_db_url = db_url or settings.DATABASE_URL
    assert target_db_url and "postgresql" in target_db_url, "DATABASE_URL must be configured for PostgreSQL"

    if mode == "dry-run":
        current_run_id = str(uuid.uuid4())[:8]
        df = pd.read_csv(target_csv)
        raw_records = df.to_dict(orient="records")

        # 1. Normalize & Validate
        normalized_records = []
        rejected_records = []
        for r in raw_records:
            norm = normalize_hotel_record(r)
            valid, errs = validate_record_contract(norm)
            if valid:
                normalized_records.append(norm)
            else:
                rejected_records.append({"record": norm, "errors": errs})

        # 2. Deduplicate
        canonical_records, dup_rejected = deduplicate_records(normalized_records)

        # 3. Compute Diff against live PostgreSQL
        diff_res = compute_postgresql_diff(canonical_records, db_url=target_db_url)

        report = {
            "run_id": current_run_id,
            "mode": "dry-run",
            "timestamp": datetime.utcnow().isoformat(),
            "source_file": target_csv,
            "raw_record_count": len(raw_records),
            "validated_count": len(normalized_records),
            "canonical_count": len(canonical_records),
            "rejected_validation_count": len(rejected_records),
            "rejected_duplicate_count": len(dup_rejected),
            "diff_summary": diff_res,
            "approved": False
        }

        # Save dry-run artifact to data/diffs/<run_id>/dry_run.json
        run_dir = os.path.join(DIFFS_DIR, current_run_id)
        os.makedirs(run_dir, exist_ok=True)
        artifact_path = os.path.join(run_dir, "dry_run.json")
        with open(artifact_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(f"=== PIPELINE DRY RUN SUCCESSFUL ===")
        print(f"Run ID      : {current_run_id}")
        print(f"New Hotels  : {diff_res['new_count']}")
        print(f"Updated     : {diff_res['updated_count']}")
        print(f"Unchanged   : {diff_res['unchanged_count']}")
        print(f"Artifact    : {artifact_path}")
        print(f"\nTo apply this run, execute: python -m scripts.ingestion.pipeline apply --run-id {current_run_id}")

        return report

    elif mode == "apply":
        if not run_id:
            raise ValueError("Error: --run-id is required for apply mode!")

        run_dir = os.path.join(DIFFS_DIR, run_id)
        artifact_path = os.path.join(run_dir, "dry_run.json")
        if not os.path.exists(artifact_path):
            raise FileNotFoundError(f"No valid dry-run artifact found for RUN_ID: '{run_id}'. Run dry-run first.")

        with open(artifact_path, "r", encoding="utf-8") as f:
            dry_report = json.load(f)

        print(f"=== APPLYING INGESTION RUN: {run_id} ===")
        # Execute PostgreSQL bootstrap apply
        bootstrap_res = run_bootstrap(mode="apply", csv_path=target_csv, db_url=target_db_url)

        # Selective vector update for affected hotels
        updated_hotels = [h["hotel_id"] for h in dry_report.get("diff_summary", {}).get("updated_hotels", [])]
        new_hotels = [h["hotel_id"] for h in dry_report.get("diff_summary", {}).get("new_hotels", [])]
        affected_ids = updated_hotels + new_hotels

        vec_res = sync_selective_vectors(affected_ids, mode="apply", db_url=target_db_url)

        # Update artifact to approved/applied
        dry_report["mode"] = "apply"
        dry_report["applied_at"] = datetime.utcnow().isoformat()
        dry_report["approved"] = True
        dry_report["bootstrap_result"] = bootstrap_res
        dry_report["vector_sync_result"] = vec_res

        with open(artifact_path, "w", encoding="utf-8") as f:
            json.dump(dry_report, f, indent=2)

        print(f"Successfully applied run '{run_id}' to PostgreSQL and synchronized selective vectors!")
        return dry_report

    else:
        raise ValueError(f"Unknown mode: {mode}")

def main():
    parser = argparse.ArgumentParser(description="TrustLayer-AI Data Ingestion Pipeline CLI")
    parser.add_argument("command", choices=["dry-run", "apply", "verify", "history"], help="Pipeline action")
    parser.add_argument("--run-id", help="Approved RUN_ID for apply mode")
    parser.add_argument("--source", help="Path to source CSV file")

    args = parser.parse_args()

    if args.command in ["dry-run", "apply"]:
        execute_pipeline(mode=args.command, run_id=args.run_id, source_csv=args.source)
    elif args.command == "verify":
        print("Running pipeline verification...")
        from scripts.verification.audit_postgres_runtime import run_runtime_audit
        run_runtime_audit()
    elif args.command == "history":
        runs = [d for d in os.listdir(DIFFS_DIR) if os.path.isdir(os.path.join(DIFFS_DIR, d))]
        print(f"=== INGESTION RUN HISTORY ({len(runs)} runs) ===")
        for r in runs:
            p = os.path.join(DIFFS_DIR, r, "dry_run.json")
            if os.path.exists(p):
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    print(f"Run ID: {r} | Mode: {data.get('mode')} | Timestamp: {data.get('timestamp')} | Approved: {data.get('approved')}")

if __name__ == "__main__":
    main()
