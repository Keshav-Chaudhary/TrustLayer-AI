# STAGE 28 — ONE-COMMAND END-TO-END DATA PIPELINE ARCHITECTURE

```mermaid
graph TD
    subgraph 1_UPSTREAM_PIPELINE
        API[Google Places & Reviews API] --> RawData[data/raw/]
        RawData --> Clean[scripts/cleaning/]
        Clean --> NLP[scripts/nlp/ Sentiment & ABSA]
        NLP --> Feats[scripts/recommender/ Features]
        Feats --> Merge[scripts/recommender/merge_dataset.py]
        Merge --> Canonical[data/exports/final_hotel_dataset.csv]
    end

    subgraph 2_STAGE26_INGESTION_BOUNDARY
        Canonical --> DiffEngine[scripts/ingestion/diff_engine.py]
        DiffEngine --> DryRunArtifact[data/diffs/<RUN_ID>/dry_run.json]
        DryRunArtifact --> Manifest[data/runs/<RUN_ID>/pipeline_manifest.json]
    end

    subgraph 3_APPROVAL_SAFETY_BOUNDARY
        Manifest --> Approval{Explicit Human Approval}
        Approval -->|python -m scripts.orchestrator apply --run-id RUN_ID| Apply[bootstrap_postgres.py]
        Apply --> Postgres[(REAL PostgreSQL 17 'trustlayer_db')]
        Apply --> Outbox[domain_events Table]
        Apply --> VectorSync[selective_vector_sync.py] --> PgVector[(embedding_documents Table)]
    end
```

## Core Execution Semantics
- `python -m scripts.orchestrator full` — Executes upstream stages 1 through 5, generates `final_hotel_dataset.csv`, computes Stage 26 diff against PostgreSQL, produces `pipeline_manifest.json`, and **STOPS AT DRY-RUN**. Zero database mutation occurs during `full`.
- `python -m scripts.orchestrator apply --run-id <RUN_ID>` — Applies the approved `RUN_ID` transactionally to PostgreSQL and updates affected vector embeddings selectively.
