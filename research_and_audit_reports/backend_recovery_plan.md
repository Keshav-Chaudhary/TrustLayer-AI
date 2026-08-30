# Backend Recovery Plan

## Objective
Restore the FastAPI backend to full functionality without duplicating existing robust logic located in `scripts/rag/`.

## Files to Rebuild
1. **`app/api/main.py`**: Mount FastAPI, CORS middleware, and Routers.
2. **`app/api/routes.py`**: Re-implement `POST /recommend`, `GET /health`, and introduce `GET /hotel/{id}`, `GET /metrics`, `POST /save`, `POST /compare`.
3. **`app/schemas/response_models.py`**: Pydantic validation schemas matching the new frontend TypeScript interfaces.
4. **`app/services/recommendation_service.py`**: Re-wire `query_parser.py`, `retriever.py`, and `context_builder.py`.
5. **`app/services/grounding_validator.py`**: Restore hallucination interception logic.
6. **`app/services/cache_service.py`**: Restore simple MD5 dict caching.
7. **`app/services/llm_service.py`**: Re-wrap the mock LLM generation endpoint.

## Reused Dependencies (No Duplication allowed)
- `scripts.rag.query_parser.QueryParser`
- `scripts.rag.retriever.HybridRetriever`
- `scripts.rag.context_builder.ContextBuilder`

## Estimated Effort & Risk
- **Effort**: 1-2 hours.
- **Risk Assessment**: Medium. The highest risk is ensuring the Pydantic schemas exactly align with the strict TanStack query interfaces on the Next.js side, specifically around nested `provenance` arrays and `aspect_scores`.
