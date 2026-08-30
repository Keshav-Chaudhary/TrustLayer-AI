from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from app.schemas.response_models import (
    HotelAnalysis, AnalyzeRequest, AnalyzeResponse,
    CompareRequest, CompareResponse, EvidenceResponse,
    ExplanationResponse, ChatRequest, HotelCatalogResponse
)
from app.services.hotel_service import HotelService
from app.services.recommendation_service import RecommendationService
from app.services.cache_service import cache_service

hotel_v1_router = APIRouter(tags=["Hotels V1"])
hotel_service = HotelService()
rec_service = RecommendationService()

class SaveRequest(BaseModel):
    hotel_id: str

@hotel_v1_router.get("/hotels", response_model=HotelCatalogResponse)
def get_hotels(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    area: str = Query(None),
    budget: str = Query(None),
    rating: float = Query(None),
    cleanliness: float = Query(None),
    sort_by: str = Query("trust_score_desc")
):
    try:
        return hotel_service.get_hotels_catalog(page, limit, area, budget, rating, cleanliness, sort_by)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@hotel_v1_router.get("/hotels/featured", response_model=HotelCatalogResponse)
def get_featured_hotels():
    try:
        return hotel_service.get_hotels_catalog(page=1, limit=5, sort_by="trust_score_desc")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@hotel_v1_router.get("/hotel/{hotel_id}", response_model=HotelAnalysis)
def get_hotel(hotel_id: str):
    try:
        return hotel_service.get_hotel_details(hotel_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Hotel not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@hotel_v1_router.post("/save")
def save_hotel(request: SaveRequest):
    return {"status": "success", "hotel_id": request.hotel_id}

@hotel_v1_router.post("/compare", response_model=CompareResponse)
def compare_hotels(request: CompareRequest):
    cache_key = cache_service.generate_key("compare", {"ids": sorted(request.hotel_ids)})
    cached_res = cache_service.get(cache_key)
    if cached_res:
        return cached_res

    try:
        res = rec_service.compare_hotels(request.hotel_ids)
        cache_service.set(cache_key, res)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@hotel_v1_router.post("/analyze", response_model=AnalyzeResponse)
def analyze_hotel(request: AnalyzeRequest):
    try:
        return rec_service.analyze_hotel(request.hotel_id, request.query or "")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@hotel_v1_router.get("/hotel/{hotel_id}/evidence", response_model=EvidenceResponse)
def get_evidence(hotel_id: str):
    try:
        return hotel_service.get_evidence(hotel_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Hotel not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@hotel_v1_router.get("/hotel/{hotel_id}/explanation", response_model=ExplanationResponse)
def get_explanation(hotel_id: str):
    try:
        return hotel_service.get_explanation(hotel_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Hotel not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@hotel_v1_router.post("/chat")
async def chat(request: ChatRequest):
    try:
        return StreamingResponse(
            rec_service.stream_chat(request.query, request.hotel_id or ""),
            media_type="text/plain"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
