# STAGE 26 — IMPLEMENTATION RECONCILIATION

## Executive Summary

This reconciliation document maps existing pipeline components in **TrustLayer-AI** (`bootstrap_postgres.py`, `backfill_pgvector.py`, `db_schema.py`) to the new repeatable ingestion architecture.

It ensures 100% code reuse for existing canonical hashing, SQLAlchemy schema models, domain event logging, and SentenceTransformer vector embeddings while extending the system with a multi-stage data lifecycle and interactive diff engine.

---

## Component Reconciliation Table

| Existing Implementation | Reusable Component | Required Modification | New Component | Architectural Reason |
|---|---|---|---|---|
| `scripts/ingestion/bootstrap_postgres.py` | Data validation, SHA256 file checksum, outbox logging (`domain_events`), database commit | Refactor into modular pipeline runner | `scripts/ingestion/pipeline.py` | Unifies CLI interface (`ingest`, `dry-run`, `apply`, `verify`, `history`). |
| `app/repositories/db_schema.py` | `calculate_canonical_content_hash`, SQLAlchemy models (`HotelModel`, `EmbeddingDocumentModel`, `DomainEventModel`) | None (Preserve byte-for-byte) | `scripts/ingestion/diff_engine.py` | Reuses canonical hashing algorithm for change detection. |
| `scripts/ingestion/backfill_pgvector.py` | Vector backfill, SentenceTransformer (`all-MiniLM-L6-v2`), batching | Integrate with content-hash diffs | `scripts/ingestion/selective_vector_sync.py` | Prevents unnecessary full embedding recalculation; updates only modified chunks. |
| Manual CSV editing | None | Standardize data lifecycle | `data/sources/` (`raw`, `normalized`, `validated`, `canonical`) | Establishes auditable staging layers. |
| Basic record check in `bootstrap_postgres.py` | Field checks | Expand validation rules & constraints | `scripts/ingestion/schema_contract.py` | Prevents malformed source records from entering PostgreSQL. |
| No deduplication | None | Implement multi-key entity resolution | `scripts/ingestion/deduplicator.py` | Prevents duplicate hotel insertion across multi-source datasets. |
| No diff visualization | Count summaries (`records_inserted`, `records_updated`) | Generate field-level diff reports (`old -> new`) | `scripts/ingestion/diff_engine.py` | Enables human-auditable dry-run reviews before applying changes. |
