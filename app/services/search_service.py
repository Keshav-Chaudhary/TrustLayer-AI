import difflib
from typing import Dict, List, Any, Optional
from app.repositories.base import BaseHotelRepository
from app.repositories.hotel_repository import CsvHotelRepository

class SearchService:
    """
    Service responsible for area auto-suggestions and nearest area fallback routing,
    dynamically derived from dataset metadata in HotelRepository.
    """
    def __init__(self, hotel_repo: Optional[BaseHotelRepository] = None):
        self.hotel_repo = hotel_repo or CsvHotelRepository()

    def suggest(self, query: str) -> List[Dict[str, Any]]:
        if not query:
            return []

        query_lower = query.lower()
        suggestions = []
        area_counts = self.hotel_repo.get_area_counts()

        for area, count in area_counts.items():
            area_lower = area.lower()
            score = 0
            if area_lower == query_lower:
                score = 100
            elif area_lower.startswith(query_lower):
                score = 80
            elif query_lower in area_lower:
                score = 60
            else:
                similarity = difflib.SequenceMatcher(None, query_lower, area_lower).ratio()
                if similarity > 0.6:
                    score = int(similarity * 100)

            if score > 0:
                suggestions.append({
                    "area": area,
                    "count": count,
                    "cluster": "Dataset Region",
                    "score": score
                })

        suggestions.sort(key=lambda x: (x["score"], x["count"]), reverse=True)
        return suggestions[:10]

    def get_nearest(self, area: str) -> Dict[str, Any]:
        area_counts = self.hotel_repo.get_area_counts()
        area_lower = area.lower()

        # Find nearby areas in dataset sorted by popularity
        nearby_areas = [
            a for a in area_counts.keys()
            if a.lower() != area_lower and area_counts.get(a, 0) > 0
        ]
        nearby_areas.sort(key=lambda x: area_counts.get(x, 0), reverse=True)
        nearby_top = nearby_areas[:5]

        if not nearby_top:
            return {
                "original_area": area,
                "cluster": None,
                "nearby_areas": [],
                "message": f"No nearby alternative properties found for {area} in the current dataset."
            }

        return {
            "original_area": area,
            "cluster": "Catalog Region",
            "nearby_areas": nearby_top,
            "message": f"Showing alternative properties near {area}."
        }
