from fastapi import APIRouter, Query
from app.utils.search_utils import SearchUtility
from app.api.routes import rec_service

search_router = APIRouter(prefix="/search", tags=["Search"])

# Initialize SearchUtility lazily or directly using the existing hotels_db
search_utility = None

def get_search_utility():
    global search_utility
    if search_utility is None:
        search_utility = SearchUtility(rec_service.hotels_db)
    return search_utility

@search_router.get("/suggest")
def suggest_area(q: str = Query(..., min_length=1, description="Prefix or fuzzy query for area suggestions")):
    """
    Returns ranked area suggestions dynamically computed from the loaded catalog.
    """
    util = get_search_utility()
    suggestions = util.suggest(q)
    return {"suggestions": suggestions}

@search_router.get("/nearest")
def nearest_area(area: str = Query(..., description="The area that returned too few results")):
    """
    Returns nearby areas ordered by similarity / geographic cluster for fallback routing.
    """
    util = get_search_utility()
    result = util.get_nearest(area)
    return result
