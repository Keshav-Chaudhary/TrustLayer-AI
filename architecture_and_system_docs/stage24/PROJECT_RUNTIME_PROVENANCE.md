# PROJECT RUNTIME PROVENANCE DOCUMENTATION

## 1. Verified Environment Configuration
```env
DATA_BACKEND=postgres
VECTOR_BACKEND=pgvector
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/trustlayer_db
```

## 2. Dynamic Factory Resolution
- `get_hotel_repository()` ──► `app.repositories.postgres_hotel_repository.PostgresHotelRepository`
- `get_embedding_repository()` ──► `app.repositories.pgvector_embedding_repository.PgVectorEmbeddingRepository`
- `get_trace_repository()` ──► `app.repositories.postgres_trace_repository.PostgresTraceRepository`

## 3. Direct SQL Query Provenance (PostgreSQL 17.6 `trustlayer_db`)
- `hotels`: 1,661 records
- `hotel_locations`: 1,661 records (0 orphans)
- `hotel_scores`: 1,661 records (0 orphans)
- `hotel_sources`: 1,661 records (0 orphans)
- `hotel_amenities`: 1,661 records (0 orphans)
- `embedding_documents`: 7,910 records (0 NULL vectors)
- `domain_events`: 1,661 records (Outbox)

## 4. API Endpoint Matching Proof
Querying `GET /api/v1/hotels?limit=5` returns hotel ID `ChIJCdCLTWgcDTkRgCe4U3CxnUo`. Direct SQL query `SELECT name, rating FROM hotels WHERE hotel_id = 'ChIJCdCLTWgcDTkRgCe4U3CxnUo'` returns exact row `('Pullman New Delhi Aerocity', 4.7)`.
