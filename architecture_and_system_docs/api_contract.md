# TrustLayer-AI API Contract

## `POST /recommend`
**Request Body**:
```json
{
  "query": "A nice hotel in Mahipalpur with good breakfast",
  "max_results": 3
}
```

**Response Body** (200 OK):
```json
{
  "trace_id": "req-1234abcd",
  "query": "A nice hotel in Mahipalpur with good breakfast",
  "recommendations": [
    {
      "hotel_id": "<example_id>",
      "name": "<Example Value>",
      "summary_text": "Highly rated budget option.",
      "aspect_scores": {"cleanliness": 4.5},
      "trust_score": 85.0,
      "explanation_badge": "Top Choice",
      "review_evidence": ["Great service"],
      "provenance": [
        {
          "chunk_id": "chunk_01",
          "chunk_type": "Profile",
          "snippet": "Hotel Luxury Stay..."
        }
      ],
      "confidence_badge": "High"
    }
  ],
  "metadata": {
    "latency_ms": 150.0,
    "fallback_level": 0,
    "cache_hit": false
  }
}
```

## `POST /analyze`
**Request Body**:
```json
{
  "hotel_id": "<example_id>",
  "query": "Is it good for families?"
}
```

**Response Body**:
```json
{
  "hotel_id": "<example_id>",
  "grounded_analysis": "The hotel is great for families as they have a large pool [chunk_02].",
  "citations": [
    {
      "chunk_id": "chunk_02",
      "chunk_type": "Review",
      "snippet": "We loved the large pool with our kids."
    }
  ],
  "is_hallucination_free": true
}
```

## `POST /compare`
**Request Body**:
```json
{
  "hotel_ids": ["<example_id>", "<example_id>"]
}
```

**Response Body**:
```json
{
  "grounded_summary": "Both hotels offer great service, but Hotel 1 is better for budget.",
  "insights": [
    {
      "aspect": "Value",
      "insight_text": "Hotel 1 provides free breakfast [chunk_01].",
      "winner_hotel_id": "<example_id>",
      "citations": [
         {"chunk_id": "chunk_01", "chunk_type": "Review", "snippet": "Free breakfast was a huge plus."}
      ]
    }
  ]
}
```

## `GET /hotel/{id}/evidence`
**Response Body**:
```json
{
  "hotel_id": "<example_id>",
  "evidence_chunks": [
     {"chunk_id": "chunk_01", "chunk_type": "Review", "snippet": "Clean rooms."}
  ]
}
```

## `GET /hotel/{id}/explanation`
**Response Body**:
```json
{
  "hotel_id": "<example_id>",
  "feature_importance": {"cleanliness_score": 0.4, "location_score": 0.2},
  "score_breakdown": {"cleanliness": 4.5, "location": 4.2}
}
```

## `POST /chat`
**Request Body**:
```json
{
  "query": "Tell me more about it",
  "hotel_id": "<example_id>",
  "session_id": "req-1234abcd"
}
```
**Response Stream (Chunked HTTP Text Stream)**:
```text
Based on the reviews...
... it seems very clean [chunk_03].
```

## `GET /health`
**Response Body**:
```json
{
  "status": "ok",
  "message": "TrustLayer-AI API is healthy"
}
```
