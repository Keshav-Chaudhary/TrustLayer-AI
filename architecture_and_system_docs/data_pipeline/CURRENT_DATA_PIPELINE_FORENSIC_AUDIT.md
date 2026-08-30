# CURRENT DATA PIPELINE FORENSIC AUDIT — STAGE 26

## 1. Executive Summary

This forensic audit analyzes the existing data ingestion, bootstrapping, and vector backfill implementations in **TrustLayer-AI** (`scripts/ingestion/bootstrap_postgres.py` and `scripts/ingestion/backfill_pgvector.py`).

The existing system provides an initial bootstrap and validation mechanism, but lacks a structured multi-stage lifecycle (`raw -> normalized -> validated -> canonical -> diff -> approval -> apply -> selective vector update`).

---

## 2. Ingestion Pipeline Breakdown

| Pipeline Component | Existing Implementation | File Location | Audit Evaluation |
|---|---|---|---|
| **Source Data Input** | Static single CSV file | `data/exports/final_hotel_dataset.csv` | Static reference file; missing raw ingestion staging layer. |
| **Validation Rules** | Basic field check (`hotel_id`, `hotel_name`, bounds) | `bootstrap_postgres.py` (`validate_hotel_record`) | Functional but basic; needs schema contract validation. |
| **Content Hashing** | SHA-256 canonical string hashing | `app/repositories/db_schema.py` (`calculate_canonical_content_hash`) | Effective for change detection (`records_unchanged` vs `records_updated`). |
| **Database Application** | Full bootstrap or record upsert | `bootstrap_postgres.py` (`run_bootstrap`) | Writes `hotels` and 4 child tables (`locations`, `scores`, `sources`, `amenities`). |
| **Outbox Synchronization** | Domain event logging | `bootstrap_postgres.py` | Generates `HOTEL_CREATED` events in `domain_events` table. |
| **Vector Backfill** | ChromaDB to PostgreSQL sync | `backfill_pgvector.py` (`run_pgvector_backfill`) | Hashes vector snippets and backfills missing/changed chunks using SentenceTransformer (`all-MiniLM-L6-v2`). |

---

## 3. Key Pipeline Gaps & Requirements for Stage 26

1. **No Staging / Lifecycle Pipeline**: Currently, data must be manually saved into `final_hotel_dataset.csv`. A structured multi-directory staging area (`data/sources/raw`, `data/sources/normalized`, `data/sources/validated`, `data/canonical`) is needed.
2. **No Interactive Diff Engine**: Currently `bootstrap_postgres.py` shows counts (`inserted`, `updated`, `unchanged`), but does not display field-by-field value diffs (`rating: 4.2 -> 4.5`).
3. **No Human Approval Step**: Dry-run outputs summary counts, but there is no `--mode apply --run-id <RUN_ID>` approval enforcement.
4. **Selective Embedding Updates**: Vector updates currently read from ChromaDB (`backfill_pgvector.py`). Stage 26 must link canonical PostgreSQL changes directly to selective embedding document updates.
