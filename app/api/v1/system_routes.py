import os
import requests
from fastapi import APIRouter, HTTPException
from app.schemas.response_models import HealthResponse, ReadinessResponse, MetricsResponse
from app.services.cache_service import cache_service
from app.config.config import settings

system_v1_router = APIRouter(tags=["System V1"])

@system_v1_router.get("/health", response_model=HealthResponse)
def health_check():
    return {"status": "ok", "message": "TrustLayer-AI API is healthy"}

@system_v1_router.get("/ready", response_model=ReadinessResponse)
def readiness_check():
    dependencies = {}
    
    # 1. Vector Store check
    vector_dir = os.path.abspath(settings.VECTOR_STORE_PATH)
    if os.path.exists(vector_dir):
        dependencies["vector_store"] = "ok"
    else:
        dependencies["vector_store"] = "unavailable"

    # 2. Ollama Reachability check
    try:
        res = requests.get(settings.OLLAMA_ENDPOINT, timeout=3)
        if res.status_code == 200:
            dependencies["ollama"] = "ok"
        else:
            dependencies["ollama"] = f"unreachable_status_{res.status_code}"
    except Exception as e:
        dependencies["ollama"] = f"unreachable: {str(e)}"

    is_ready = dependencies.get("vector_store") == "ok"
    if not is_ready:
        raise HTTPException(status_code=503, detail={"status": "not_ready", "dependencies": dependencies})

    return {"status": "ready", "dependencies": dependencies}

@system_v1_router.get("/metrics", response_model=MetricsResponse)
def get_metrics():
    return {
        "total_hotels": 1661,
        "total_chunks": 7910,
        "cache_hit_rate": cache_service.get_hit_rate(),
        "avg_latency_ms": 185.0
    }
