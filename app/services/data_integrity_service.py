import os
import hashlib
import json
import logging
import pandas as pd
from typing import Dict, Any, Tuple
from app.config.config import settings

logger = logging.getLogger("trustlayer")

class DataIntegrityService:
    """
    Verification service checking baseline manifests against runtime datasets to guarantee zero data loss.
    """
    def __init__(self, baseline_path: str = "architecture_and_system_docs/stage23/data_integrity_baseline.json"):
        self.baseline_path = os.path.abspath(baseline_path)

    def generate_current_manifest(self) -> Dict[str, Any]:
        manifest = {}

        # 1. CSV Manifest
        csv_path = os.path.abspath(settings.CSV_DATASET_PATH)
        if os.path.exists(csv_path):
            with open(csv_path, 'rb') as f:
                csv_bytes = f.read()
            csv_sha = hashlib.sha256(csv_bytes).hexdigest()
            df = pd.read_csv(csv_path)
            hotel_ids = df['hotel_id'].dropna().astype(str).tolist()
            manifest['csv'] = {
                'file_path': csv_path,
                'sha256': csv_sha,
                'row_count': len(df),
                'unique_hotel_ids_count': len(set(hotel_ids))
            }

        # 2. JSON Manifest
        json_path = os.path.abspath(settings.BATCH_DEBUG_FILE_PATH)
        if os.path.exists(json_path):
            with open(json_path, 'rb') as f:
                json_bytes = f.read()
            json_sha = hashlib.sha256(json_bytes).hexdigest()
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            runs = data.get('runs', []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
            run_ids = [r.get('run_id') for r in runs if isinstance(r, dict)]
            manifest['json'] = {
                'file_path': json_path,
                'sha256': json_sha,
                'run_count': len(runs),
                'run_ids': run_ids
            }

        # 3. ChromaDB Manifest
        vector_dir = os.path.abspath(settings.VECTOR_STORE_PATH)
        if os.path.exists(vector_dir):
            import chromadb
            client = chromadb.PersistentClient(path=vector_dir)
            collection = client.get_collection(name='hotel_knowledge')
            doc_count = collection.count()
            manifest['chromadb'] = {
                'dir_path': vector_dir,
                'collection_name': 'hotel_knowledge',
                'document_count': doc_count
            }

        return manifest

    def verify_integrity(self) -> Tuple[bool, Dict[str, Any]]:
        current = self.generate_current_manifest()
        
        if not os.path.exists(self.baseline_path):
            logger.warning(f"Baseline file missing at {self.baseline_path}. Generating fresh snapshot.")
            os.makedirs(os.path.dirname(self.baseline_path), exist_ok=True)
            with open(self.baseline_path, 'w', encoding='utf-8') as f:
                json.dump(current, f, indent=2)
            return True, {"status": "baseline_created", "current": current}

        with open(self.baseline_path, 'r', encoding='utf-8') as f:
            baseline = json.load(f)

        checks = {
            "csv_sha_matches": current.get('csv', {}).get('sha256') == baseline.get('csv', {}).get('sha256'),
            "csv_row_count_matches": current.get('csv', {}).get('row_count') == baseline.get('csv', {}).get('row_count'),
            "json_run_count_matches": current.get('json', {}).get('run_count') == baseline.get('json', {}).get('run_count'),
            "chromadb_document_count_matches": current.get('chromadb', {}).get('document_count') == baseline.get('chromadb', {}).get('document_count')
        }

        all_passed = all(checks.values())
        report = {
            "all_passed": all_passed,
            "checks": checks,
            "baseline": baseline,
            "current": current
        }
        return all_passed, report
