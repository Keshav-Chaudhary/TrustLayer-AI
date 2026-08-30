# 🔌 TrustLayer-AI REST API Reference

The TrustLayer-AI FastAPI backend exposes REST endpoints under both root compatibility paths and the `/api/v1/` versioned namespace.

Base URL: `http://127.0.0.1:8000`

---

## 🏥 System & Health Endpoints

### 1. Root / Ping
- **Endpoint**: `GET /`
- **Description**: Returns basic service identification and status.
- **Response**:
```json
{
  "name": "TrustLayer-AI Backend",
  "status": "healthy",
  "version": "1.0.0"
}
```

### 2. Health & Dependency Diagnostic
- **Endpoint**: `GET /api/v1/system/health`
- **Description**: Verifies status of ChromaDB vector store, Ollama LLM connectivity, and dataset cache.
- **Response**:
```json
{
  "status": "healthy",
  "chromadb": "connected",
  "ollama": "reachable",
  "dataset_loaded": true
}
```

---

## 🏨 Recommendation & Search Endpoints

### 3. Natural Language Hotel Recommendations
- **Endpoint**: `POST /api/v1/recommend/hotels` (or legacy `POST /recommend/hotels`)
- **Description**: Parses user query, retrieves candidate stays via hybrid ChromaDB search, evaluates aspect sentiment, and synthesizes grounded AI explanations.
- **Request Body**:
```json
{
  "query": "Looking for a quiet business stay in Aerocity with high cleanliness under 5000 INR",
  "top_k": 5
}
```
- **Response**:
```json
{
  "query": "Looking for a quiet business stay in Aerocity with high cleanliness under 5000 INR",
  "parsed_constraints": {
    "area": "Aerocity",
    "max_price": 5000,
    "persona": "business",
    "aspects": ["cleanliness", "quietness"]
  },
  "recommendations": [
    {
      "hotel_id": "ChIJ01RYkd0dDTkRcowtxjOpraI",
      "name": "Holiday Inn Express New Delhi International Airport",
      "locality": "Aerocity",
      "price_per_night": 4200,
      "trust_score": 91.4,
      "aspect_scores": {
        "cleanliness": 94.0,
        "service": 88.5,
        "location": 96.0,
        "value": 89.0,
        "staff": 90.0
      },
      "ai_grounded_summary": "Highly rated for soundproof rooms and pristine airport terminal accessibility with prompt check-in.",
      "evidence_badges": [
        "Verified Airport Transit Proximity",
        "Top Cleanliness Index (94%)",
        "Consistent High Service Rating"
      ],
      "cautions": []
    }
  ]
}
```

### 4. Structured Faceted Search
- **Endpoint**: `POST /api/v1/search/hotels`
- **Description**: Performs fast parametric filtering by area, price range, persona, and minimum trust score without LLM synthesis latency.
- **Request Body**:
```json
{
  "area": "Connaught Place",
  "min_price": 1000,
  "max_price": 6000,
  "min_trust_score": 80.0,
  "limit": 10
}
```

### 5. Hotel Detail by ID
- **Endpoint**: `GET /api/v1/hotels/{hotel_id}`
- **Description**: Retrieves exhaustive aspect breakdown, full review sentiment distribution, radar score metrics, and provenance chunks for a specific hotel ID.

---

## 🐞 Diagnostics & Debug Endpoints

### 6. RAG Retrieval Debugger
- **Endpoint**: `POST /api/v1/debug/rag-retrieval`
- **Description**: Inspects raw ChromaDB vector distance, cosine similarity, and chunk metadata returned for a given query text.
