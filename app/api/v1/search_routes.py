from fastapi import APIRouter, Query
from app.services.search_service import SearchService

search_v1_router = APIRouter(prefix="/search", tags=["Search V1"])
search_service = SearchService()

@search_v1_router.get("/suggest")
def suggest_area(q: str = Query(..., min_length=1, description="Prefix or fuzzy query for area suggestions")):
    suggestions = search_service.suggest(q)
    return {"suggestions": suggestions}

@search_v1_router.get("/nearest")
def nearest_area(area: str = Query(..., description="The area that returned too few results")):
    result = search_service.get_nearest(area)
    return result
