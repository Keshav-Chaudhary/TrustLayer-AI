from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.debug_service import DebugService, BatchDebugRequest
from app.services.recommendation_service import RecommendationService

debug_v1_router = APIRouter(tags=["Debug V1"])
debug_service = DebugService()
rec_service = RecommendationService()

@debug_v1_router.get("/debug/trace")
def get_debug_trace(query: str = Query("Hotels with excellent cleanliness ratings")):
    try:
        return rec_service.get_debug_trace(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@debug_v1_router.post("/debug/batch")
async def run_batch_debug(request: BatchDebugRequest):
    try:
        return await debug_service.run_batch_debug(request, trace_provider=rec_service)
    except RuntimeError as e:
        if "409 Conflict" in str(e):
            raise HTTPException(status_code=409, detail="A batch debug run is currently in progress. Please try again later.")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@debug_v1_router.get("/debug/batch")
def get_batch_debug(run_id: Optional[str] = None, limit: Optional[int] = None):
    try:
        runs = debug_service.get_batch_history(run_id=run_id, limit=limit)
        return {"runs": runs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
