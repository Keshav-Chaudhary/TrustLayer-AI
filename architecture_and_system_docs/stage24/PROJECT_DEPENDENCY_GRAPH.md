# TRUSTLAYER-AI PROJECT DEPENDENCY GRAPH

## 1. Core End-to-End Runtime Architecture

```mermaid
graph TD
    Client[HTTP Client / Frontend] --> API[FastAPI App (app/api/main.py)]
    API --> Router[API Routers (app/api/v1/endpoints/)]
    Router --> Service[Services (RecommendationService / HotelService)]
    Service --> Factory[Repository Factory (app/repositories/factory.py)]
    Factory -->|DATA_BACKEND=postgres| PostgresHotelRepo[PostgresHotelRepository]
    Factory -->|VECTOR_BACKEND=pgvector| PgVectorEmbeddingRepo[PgVectorEmbeddingRepository]
    Factory -->|TRACE_BACKEND=json| JsonTraceRepo[JsonTraceRepository]
    
    PostgresHotelRepo --> Engine[SQLAlchemy Engine (127.0.0.1:5432)]
    PgVectorEmbeddingRepo --> Engine
    Engine --> PostgresDB[(REAL PostgreSQL 17 'trustlayer_db')]
    
    PostgresDB --> HotelsTable[hotels table (1,661 records)]
    PostgresDB --> EmbeddingTable[embedding_documents table (7,910 chunks)]
    PostgresDB --> DomainEventsTable[domain_events table (Outbox)]
```
