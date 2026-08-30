# STAGE 24 — PRODUCTION DATA PLATFORM ARCHITECTURE

## System Overview

Stage 24 establishes a professional production data platform for **TrustLayer-AI** introducing a normalized **PostgreSQL schema**, **pgvector vector storage adapter**, **idempotent ETL bootstrap pipeline**, **canonical content-hash change detection**, and an **atomic transactional outbox event framework** while preserving **100% data safety** and leaving current live CSV, JSON, and ChromaDB datasets read-only.

---

## Active Operational Configuration

```text
CURRENT ACTIVE PRODUCTION BACKEND:
  DATA_BACKEND=csv
  VECTOR_BACKEND=chroma

MIGRATION TARGET / SECONDARY VERIFIED STORE:
  DATA_BACKEND=postgres
  VECTOR_BACKEND=pgvector
```

> [!IMPORTANT]
> The active production backend remains `csv` + `chroma`. PostgreSQL + pgvector is configured as a secondary migration target and verified data store. Live API endpoints are not switched to PostgreSQL until explicit controlled cutover.

---

## Architecture Diagram

```text
External Source / CSV Reference Dataset
       │
       ▼
scripts/ingestion/bootstrap_postgres.py
       │ (Validate & Normalize -> SHA-256 Content Hash Change Detection)
       ▼
PostgreSQL Source of Truth (Database Session Transaction)
       ├── hotels (PK: id, Business Key: hotel_id)
       ├── hotel_locations
       ├── hotel_scores
       ├── hotel_amenities
       ├── hotel_sources
       ├── hotel_provenance
       ├── ingestion_runs & ingestion_records
       └── domain_events (Transactional Outbox)
             │
             ▼
       scripts/workers/outbox_worker.py
             │
             ▼
       embedding_documents (pgvector / vector(384))
       │
       ▼
Repository Abstraction Layer (app/repositories/factory.py)
       ├── BaseHotelRepository     ──> CsvHotelRepository (default) | PostgresHotelRepository
       ├── BaseTraceRepository     ──> JsonTraceRepository (default)| PostgresTraceRepository
       └── BaseEmbeddingRepository ──> ChromaEmbeddingRepository (default) | PgVectorEmbeddingRepository
       │
       ▼
Application Services & FastAPI Endpoints (RecommendationService, HotelService, SearchService, DebugService)
```

---

## Key Design Principles

1. **Backend Agnosticism**: Application services (`RecommendationService`, `HotelService`, `SearchService`, `DebugService`) interact strictly with abstract repository interfaces (`BaseHotelRepository`, `BaseTraceRepository`, `BaseEmbeddingRepository`). No PostgreSQL-specific SQL resides inside domain services.
2. **Canonical Content-Hash Change Detection**: Computes SHA-256 digests over standard normalized key-value representations of all entity fields. Identical re-ingestions bypass redundant DB writes and vector embeddings (`UNCHANGED`).
3. **Transactional Outbox Event Pattern**: Hotel mutations and domain events (`HOTEL_CREATED`, `HOTEL_UPDATED`, `EMBEDDING_REQUIRED`) are committed atomically within a single database transaction, guaranteeing event consistency.
4. **Idempotency Guarantee**: Running the bootstrap pipeline repeatedly produces zero duplicate hotels, zero duplicate vector embeddings, and zero duplicate domain events.
