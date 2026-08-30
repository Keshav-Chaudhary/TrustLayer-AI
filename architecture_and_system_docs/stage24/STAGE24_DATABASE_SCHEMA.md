# STAGE 24 — POSTGRESQL & PGVECTOR DATABASE SCHEMA

## Database Entity Relationship Overview

The PostgreSQL database schema decouples core entity identities, location attributes, normalized trust scores, amenities, provenance records, vector embeddings, ingestion audit runs, and domain event outbox records.

---

## Entity Definitions

### 1. `hotels` Table
- `id`: `INTEGER` (PRIMARY KEY AUTOINCREMENT)
- `hotel_id`: `VARCHAR(255)` (UNIQUE, NOT NULL, INDEXED) - Canonical external/business identifier
- `name`: `VARCHAR(255)` (NOT NULL)
- `address`: `TEXT`
- `rating`: `FLOAT`
- `review_count`: `INTEGER`
- `price`: `VARCHAR(100)`
- `budget_category`: `VARCHAR(50)`
- `hero_image`: `TEXT`
- `created_at`: `TIMESTAMP`
- `updated_at`: `TIMESTAMP`
- `version`: `INTEGER`
- `is_active`: `BOOLEAN`

### 2. `hotel_locations` Table
- `id`: `INTEGER` (PRIMARY KEY AUTOINCREMENT)
- `hotel_id`: `VARCHAR(255)` (FOREIGN KEY -> `hotels.hotel_id`, INDEXED)
- `area`: `VARCHAR(255)`
- `city`: `VARCHAR(255)`
- `destination`: `VARCHAR(255)`
- `latitude`: `FLOAT`
- `longitude`: `FLOAT`

### 3. `hotel_scores` Table
- `id`: `INTEGER` (PRIMARY KEY AUTOINCREMENT)
- `hotel_id`: `VARCHAR(255)` (FOREIGN KEY -> `hotels.hotel_id`, INDEXED)
- `trust_score`: `FLOAT`
- `cleanliness_score`: `FLOAT`
- `service_score`: `FLOAT`
- `location_score`: `FLOAT`
- `value_score`: `FLOAT`
- `staff_behavior_score`: `FLOAT`
- `updated_at`: `TIMESTAMP`

### 4. `hotel_sources` Table
- `id`: `INTEGER` (PRIMARY KEY AUTOINCREMENT)
- `hotel_id`: `VARCHAR(255)` (FOREIGN KEY -> `hotels.hotel_id`, INDEXED)
- `source`: `VARCHAR(255)`
- `source_id`: `VARCHAR(255)`
- `source_url`: `TEXT`
- `content_hash`: `VARCHAR(64)` (SHA-256 Digest, INDEXED)
- `ingested_at`: `TIMESTAMP`
- `last_seen_at`: `TIMESTAMP`

### 5. `hotel_amenities` Table
- `id`: `INTEGER` (PRIMARY KEY AUTOINCREMENT)
- `hotel_id`: `VARCHAR(255)` (FOREIGN KEY -> `hotels.hotel_id`, INDEXED)
- `amenities_json`: `TEXT` / `JSON`

### 6. `hotel_provenance` Table
- `id`: `INTEGER` (PRIMARY KEY AUTOINCREMENT)
- `hotel_id`: `VARCHAR(255)` (FOREIGN KEY -> `hotels.hotel_id`, INDEXED)
- `field_name`: `VARCHAR(100)`
- `source`: `VARCHAR(255)`
- `source_id`: `VARCHAR(255)`
- `content_hash`: `VARCHAR(64)`
- `created_at`: `TIMESTAMP`

### 7. `embedding_documents` Table (pgvector)
- `id`: `INTEGER` (PRIMARY KEY AUTOINCREMENT)
- `hotel_id`: `VARCHAR(255)` (FOREIGN KEY -> `hotels.hotel_id`, INDEXED)
- `chunk_id`: `VARCHAR(255)` (UNIQUE, NOT NULL, INDEXED)
- `chunk_type`: `VARCHAR(100)`
- `snippet`: `TEXT`
- `content_hash`: `VARCHAR(64)` (INDEXED)
- `embedding_model`: `VARCHAR(100)`
- `embedding_version`: `INTEGER`
- `embedding_dimension`: `INTEGER` (384)
- `embedding_vector`: `VECTOR(384)` / `TEXT`
- `created_at`: `TIMESTAMP`

### 8. `ingestion_runs` Table
- `run_id`: `VARCHAR(100)` (PRIMARY KEY)
- `source`: `VARCHAR(255)`
- `source_checksum`: `VARCHAR(64)`
- `started_at`: `TIMESTAMP`
- `completed_at`: `TIMESTAMP`
- `records_seen`: `INTEGER`
- `records_inserted`: `INTEGER`
- `records_updated`: `INTEGER`
- `records_unchanged`: `INTEGER`
- `records_rejected`: `INTEGER`
- `validation_errors`: `TEXT` / `JSON`
- `status`: `VARCHAR(50)`

### 9. `ingestion_records` Table
- `id`: `INTEGER` (PRIMARY KEY AUTOINCREMENT)
- `ingestion_run_id`: `VARCHAR(100)` (FOREIGN KEY -> `ingestion_runs.run_id`, INDEXED)
- `hotel_id`: `VARCHAR(255)` (INDEXED)
- `operation`: `VARCHAR(50)` (`CREATED`, `UPDATED`, `UNCHANGED`, `REJECTED`)
- `previous_hash`: `VARCHAR(64)`
- `new_hash`: `VARCHAR(64)`
- `changed_fields`: `TEXT` / `JSON`
- `timestamp`: `TIMESTAMP`

### 10. `domain_events` Outbox Table
- `event_id`: `VARCHAR(100)` (PRIMARY KEY)
- `event_type`: `VARCHAR(100)` (`HOTEL_CREATED`, `HOTEL_UPDATED`, `EMBEDDING_REQUIRED`)
- `aggregate_type`: `VARCHAR(100)`
- `aggregate_id`: `VARCHAR(255)` (INDEXED)
- `version`: `INTEGER`
- `payload`: `TEXT` / `JSON`
- `created_at`: `TIMESTAMP`
- `processed_at`: `TIMESTAMP`
- `attempt_count`: `INTEGER`
- `last_error`: `TEXT`
