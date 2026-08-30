# DATA PIPELINE ARCHITECTURE — STAGE 26

```mermaid
graph TD
    RAW[data/sources/raw/] --> NORM[scripts/ingestion/normalizer.py]
    NORM --> VAL[scripts/ingestion/schema_contract.py]
    VAL --> DEDUP[scripts/ingestion/deduplicator.py]
    DEDUP --> CANON[data/canonical/final_hotel_dataset.csv]
    CANON --> DIFF[scripts/ingestion/diff_engine.py]
    
    DIFF --> DRYRUN[Dry Run Diff Report (data/diffs/<RUN_ID>/)]
    DRYRUN --> APPROVAL{Human Approval}
    
    APPROVAL -->|python -m scripts.ingestion.pipeline apply --run-id RUN_ID| APPLY[bootstrap_postgres.py]
    APPLY --> POSTGRES[(REAL PostgreSQL 17 'trustlayer_db')]
    APPLY --> OUTBOX[domain_events Table]
    
    APPLY --> SELECTIVE[scripts/ingestion/selective_vector_sync.py]
    SELECTIVE --> EMBEDDINGS[embedding_documents Table]
```

## Core Principles
1. **Multi-Stage Data Lifecycle**: Clean separation between `RAW -> NORMALIZED -> VALIDATED -> DEDUPLICATED -> CANONICAL -> DIFF -> APPROVAL -> APPLY`.
2. **PostgreSQL Runtime Authority**: PostgreSQL 17 `trustlayer_db` is the source of truth (`DATA_BACKEND=postgres`, `VECTOR_BACKEND=pgvector`).
3. **Selective Vector Sync**: Vector embeddings (`embedding_documents`) are regenerated ONLY for hotels with changed content hashes (`calculate_canonical_content_hash`).
