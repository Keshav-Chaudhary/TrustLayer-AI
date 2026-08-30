# DATA PIPELINE FILE MAP

- `scripts/ingestion/schema_contract.py` — Schema Contract Validation
- `scripts/ingestion/normalizer.py` — Data Normalizer & Cleaner
- `scripts/ingestion/deduplicator.py` — Entity Resolution & Deduplication
- `scripts/ingestion/diff_engine.py` — PostgreSQL Diff Engine
- `scripts/ingestion/selective_vector_sync.py` — Selective Embedding Synchronizer
- `scripts/ingestion/pipeline.py` — Master Ingestion CLI Entrypoint
- `tests/ingestion/test_pipeline_stage26.py` — Stage 26 Test Suite (8/8 Passed)
