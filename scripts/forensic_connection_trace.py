import os
import re

files_to_inspect = [
    'app/config/config.py',
    'app/repositories/db_schema.py',
    'app/repositories/postgres_hotel_repository.py',
    'app/repositories/pgvector_embedding_repository.py',
    'app/repositories/factory.py',
    'scripts/ingestion/bootstrap_postgres.py',
    'scripts/ingestion/backfill_pgvector.py',
    'scripts/workers/outbox_worker.py',
    'scripts/verification/parity_verification.py',
    'scripts/verification/test_realtime_isolated.py',
    'scripts/audit_stage24_1.py',
    'scripts/audit_stage24_3.py',
    'tests/test_stage24_database.py',
    'tests/test_stage24_ingestion.py'
]

keywords = ['DATABASE_URL', 'db_url', 'sqlite://', 'postgresql://', 'bootstrap_']

for rel_path in files_to_inspect:
    abs_path = os.path.abspath(rel_path)
    if os.path.exists(abs_path):
        print(f"\n==========================================")
        print(f"FILE: {rel_path}")
        print(f"==========================================")
        with open(abs_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for idx, line in enumerate(lines, 1):
            if any(k in line for k in keywords):
                print(f"Line {idx:<4}: {line.strip()}")
    else:
        print(f"FILE NOT FOUND: {rel_path}")
