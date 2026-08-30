import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.schemas.response_models import RecommendationResponse
from app.services.recommendation_service import RecommendationService
from app.services.cache_service import cache_service

recommend_v1_router = APIRouter(tags=["Recommend V1"])
rec_service = RecommendationService()

class QueryRequest(BaseModel):
    query: str
    limit: int = 5
    max_results: int = 5

@recommend_v1_router.post("/recommend", response_model=RecommendationResponse)
def recommend(request: QueryRequest):
    trace_id = f"req-{uuid.uuid4().hex[:8]}"
    cache_key = cache_service.generate_key("rec", {"q": request.query, "k": request.max_results})

    cached_res = cache_service.get(cache_key)
    if cached_res:
        cached_res["metadata"]["cache_hit"] = True
        cached_res["trace_id"] = trace_id
        return cached_res

    try:
        recommendations, catalog_suggestions, metadata = rec_service.process_query(
            request.query, max(request.limit, request.max_results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    response = {
        "trace_id": trace_id,
        "query": request.query,
        "recommendations": recommendations,
        "catalog_suggestions": catalog_suggestions,
        "metadata": metadata
    }

    cache_service.set(cache_key, response)
    return response
