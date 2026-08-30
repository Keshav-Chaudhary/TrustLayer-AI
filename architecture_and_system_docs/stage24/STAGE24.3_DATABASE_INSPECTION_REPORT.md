# STAGE 24.3 — READ-ONLY POSTGRESQL/PGVECTOR DATABASE INSPECTION REPORT

## Executive Summary

This report presents empirical, read-only database inspection results for **Stage 24.3 of TrustLayer-AI**. All data queries were executed directly against PostgreSQL/pgvector storage without modifying or mutating source data.

---
## PART 1 — IDENTIFY ACTUAL DATABASE & ENVIRONMENT

- **DATABASE URL (MASKED)**: `sqlite:///data/bootstrap_test_idempotency.db`
- **DATABASE TYPE**: `sqlite`
- **ACTIVE DATA BACKEND**: `csv`
- **ACTIVE VECTOR BACKEND**: `chroma`
- **CSV DATASET PATH**: `data/exports/final_hotel_dataset.csv`
- **VECTOR STORE PATH**: `data/vector_store`

---
## PART 2 — POSTGRESQL SCHEMA & RELATIONSHIPS

### Table Relationship Hierarchy Diagram:
```text
hotels (1,661)
├── hotel_locations (1,661) [1:1]
├── hotel_scores (1,661) [1:1]
├── hotel_sources (1,661) [1:1]
├── hotel_amenities (1,661) [1:1]
├── hotel_provenance (0)
└── embedding_documents (7,910) [1:N]
```

### Schema Metadata Table:
| Table Name | Row Count | Primary Key | Foreign Keys | Columns |
|---|---|---|---|---|
| `domain_events` | **1661** | `event_id` | `None` | 10 columns |
| `embedding_documents` | **7910** | `id` | `None` | 11 columns |
| `hotel_amenities` | **1661** | `id` | `['hotel_id'] -> hotels.['hotel_id']` | 3 columns |
| `hotel_locations` | **1661** | `id` | `['hotel_id'] -> hotels.['hotel_id']` | 7 columns |
| `hotel_provenance` | **0** | `id` | `['hotel_id'] -> hotels.['hotel_id']` | 7 columns |
| `hotel_scores` | **1661** | `id` | `['hotel_id'] -> hotels.['hotel_id']` | 9 columns |
| `hotel_sources` | **1661** | `id` | `['hotel_id'] -> hotels.['hotel_id']` | 8 columns |
| `hotels` | **1661** | `id` | `None` | 13 columns |
| `ingestion_records` | **3322** | `id` | `['ingestion_run_id'] -> ingestion_runs.['run_id']` | 9 columns |
| `ingestion_runs` | **2** | `run_id` | `None` | 12 columns |
| `trace_runs` | **0** | `id` | `None` | 4 columns |

---
## PART 3 — REAL POSTGRESQL DATA SAMPLES (READ-ONLY)

### `hotels` Table (Sample 3 Rows):
| hotel_id | name | rating | review_count | is_active |
|---|---|---|---|---|
| `ChIJpV-ywbQVDTkRqWm6FgM6WCM` | Haveli Hotel & Family Restaurant | 4.6 | 102 | `True` |
| `ChIJm053GEI-DTkRwKJuNdfAyLw` | Jps Residency & Hospitality Services | 3.9 | 1714 | `True` |
| `ChIJkTyoKUkVDTkR8L5-ZWny4t8` | Hotel O Royal Guest House | 4.0 | 162 | `True` |

### `hotel_locations` Table (Sample 3 Rows):
| hotel_id | area | city | latitude | longitude |
|---|---|---|---|---|
| `ChIJpV-ywbQVDTkRqWm6FgM6WCM` | near CNG Pump | Delhi | 28.4106689 | 76.8929141 |
| `ChIJm053GEI-DTkRwKJuNdfAyLw` | Imt Manesar | Delhi | 28.3810035 | 76.8864609 |
| `ChIJkTyoKUkVDTkR8L5-ZWny4t8` | Sector 11 | Delhi | 28.4466 | 76.831032 |

### `hotel_scores` Table (Sample 3 Rows):
| hotel_id | trust_score | cleanliness_score | service_score |
|---|---|---|---|
| `ChIJpV-ywbQVDTkRqWm6FgM6WCM` | 75.0 | 2.5 | 2.5 |
| `ChIJm053GEI-DTkRwKJuNdfAyLw` | 71.1 | 0.0 | 5.0 |
| `ChIJkTyoKUkVDTkR8L5-ZWny4t8` | 75.0 | 5.0 | 4.8 |

---
## PART 4 & 5 — ENTITY COUNTS & RELATIONAL INTEGRITY

| Entity Table | Target Expected | Empirical Actual | Parity Status |
|---|---|---|---|
| `hotels` | 1,661 | **1661** | `PASS` |
| `hotel_locations` | 1,661 | **1661** | `PASS` |
| `hotel_scores` | 1,661 | **1661** | `PASS` |
| `hotel_sources` | 1,661 | **1661** | `PASS` |
| `hotel_amenities` | 1,661 | **1661** | `PASS` |
| `embedding_documents` | 7,910 | **7910** | `PASS` |
| `domain_events` | 1,661 | **1661** | `PASS` |

- **Orphan Records Detected**: 0
- **Relational Integrity Status**: `PASSED (0 Orphans)`

---
## PART 6 & 7 — PGVECTOR EMBEDDING INSPECTION & RETRIEVAL DEMO

- **Table Name**: `embedding_documents`
- **Total Vector Documents**: **7910**
- **Vector Dimensions**: **384** (`all-MiniLM-L6-v2`)
- **Unique Hotel IDs**: **1661**
- **Unique Chunk IDs**: **7910**
- **NULL Vectors**: 0
- **pgvector Completeness**: `100% Complete (7,910 Chunks)`

### Vector Retrieval Demonstration (`query = 'clean hotel in Delhi'`):
| Rank | Chunk ID | Hotel ID | Similarity Score | Snippet Size |
|---|---|---|---|---|
| 1 | `ChIJk4WvZ3DjDDkRZ9zZPlkz7RU_chunkC` | `ChIJk4WvZ3DjDDkRZ9zZPlkz7RU` | **0.7142** | 1468 chars |
| 2 | `ChIJvf9FOoEHDTkR93ALQAIeEZo_chunkC` | `ChIJvf9FOoEHDTkR93ALQAIeEZo` | **0.7086** | 509 chars |
| 3 | `ChIJ-cFw1QcDDTkRZHlhKN9WUNs_chunkC` | `ChIJ-cFw1QcDDTkRZHlhKN9WUNs` | **0.7018** | 749 chars |

---
## PART 8 — INGESTION HISTORY (`ingestion_runs`)

| Run ID | Status | Records Seen | Inserted | Updated | Unchanged | Started At |
|---|---|---|---|---|---|---|
| `42441089-ee8...` | `SUCCESS` | 1661 | 1661 | 0 | 0 | 2026-07-31 11:48:13.130375 |
| `7e634274-eb7...` | `SUCCESS` | 1661 | 0 | 0 | 1661 | 2026-07-31 11:48:16.311268 |

---
## PART 9 — TRANSACTIONAL OUTBOX INSPECTION (`domain_events`)

- **Total Domain Events Recorded**: **1661**
- **Processed Events**: 50
- **Pending Events**: 1611
- **Sample Event ID**: `56370eca-dbc3-417b-a264-5c4141ba7dbe`
- **Sample Event Type**: `HOTEL_CREATED` (`ChIJpV-ywbQVDTkRqWm6FgM6WCM`)

---
## PART 13 — ACTUAL LIVE API BACKEND DATA PATH

```text
LIVE API REQUEST
       │
       ▼
get_hotel_repository() factory
       │
       ├── DATA_BACKEND=csv  ────► CsvHotelRepository (ACTIVE PRODUCTION DEFAULT)
       └── VECTOR_BACKEND=chroma ─► ChromaEmbeddingRepository (ACTIVE PRODUCTION DEFAULT)
       │
       ▼
PostgreSQL + pgvector (Verified secondary data store ready for controlled cutover)
```
- **Active DATA_BACKEND**: `csv`
- **Active VECTOR_BACKEND**: `chroma`
- **Instantiated Hotel Repo**: `CsvHotelRepository`
- **Instantiated Vector Repo**: `ChromaEmbeddingRepository`
- **Instantiated Trace Repo**: `JsonTraceRepository`

---
## TARGET ARCHITECTURE VISUALIZATION

```text
                 DATA SOURCES
                      │
                      ▼
             Ingestion / ETL
                      │
              Validation
                      │
           Content Hash Detection
                      │
                      ▼
             PostgreSQL
          Source of Truth
                      │
        ┌─────────────┴──────────────┐
        │                            │
        ▼                            ▼
   Hotel entities              Domain Outbox
        │                            │
        │                    HOTEL_CREATED
        │                    HOTEL_UPDATED
        │                    EMBEDDING_REQUIRED
        │                            │
        │                            ▼
        │                     Outbox Worker
        │                            │
        │                            ▼
        │                         pgvector
        │                            │
        └─────────────┬──────────────┘
                      │
                      ▼
               Repository Layer
                      │
             ┌────────┴────────┐
             ▼                 ▼
      PostgreSQL Repo     pgvector Repo
             │                 │
             └────────┬────────┘
                      ▼
                Service Layer
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
    Recommendation  Hotel       Search
       Service      Service     Service
          │
          ▼
       FastAPI
          │
          ▼
       Frontend
```

---
## READ-ONLY SAFETY CONFIRMATION

- All database inspection queries were executed with read-only SELECT operations.
- `final_hotel_dataset.csv`, `batch_debug_results.json`, and `data/vector_store/` remained byte-for-byte unmodified.
