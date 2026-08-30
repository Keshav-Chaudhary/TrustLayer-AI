from typing import Dict, List, Any
import difflib

class SearchUtility:
    # Configurable geographic clusters (can be loaded from a config file/DB later)
    CLUSTERS = {
        "East Delhi": ["Preet Vihar", "Patparganj", "Laxmi Nagar", "Anand Vihar", "Krishna Nagar", "Shahdara"],
        "Central Delhi": ["Paharganj", "Karol Bagh", "Connaught Place", "Daryaganj"],
        "Airport Corridor": ["Mahipalpur", "Aerocity", "Rangpuri", "Kapas Hera"],
        "Gurugram": ["Sector 39", "Sector 43", "Sector 53", "Sector 57", "DLF Phase IV", "Gurgaon", "Golf Course Ext Rd", "Gurugram"]
    }

    def __init__(self, hotels_db: Dict[str, Any]):
        """
        Initializes the SearchUtility with dynamic area counts derived directly from the hotels database.
        """
        self.area_counts = self._build_area_counts(hotels_db)
        # Create a reverse mapping for O(1) cluster lookups
        self.area_to_cluster = {}
        for cluster_name, areas in self.CLUSTERS.items():
            for area in areas:
                self.area_to_cluster[area.lower()] = cluster_name

    def _build_area_counts(self, hotels_db: Dict[str, Any]) -> Dict[str, int]:
        counts = {}
        for hotel in hotels_db.values():
            area = hotel.get("area")
            if area:
                # Keep original casing for display, but sum accurately
                normalized_area = area.strip()
                if normalized_area not in counts:
                    counts[normalized_area] = 0
                counts[normalized_area] += 1
        return counts

    def suggest(self, query: str) -> List[Dict[str, Any]]:
        """
        Returns ranked area suggestions using exact, prefix, substring, and fuzzy matching.
        """
        if not query:
            return []

        query_lower = query.lower()
        suggestions = []

        for area, count in self.area_counts.items():
            area_lower = area.lower()
            
            # Determine match score
            score = 0
            if area_lower == query_lower:
                score = 100 # Exact match
            elif area_lower.startswith(query_lower):
                score = 80 # Prefix match
            elif query_lower in area_lower:
                score = 60 # Substring match
            else:
                # Fuzzy match (e.g. "gurgaon" vs "gurugram" might not match well here, 
                # but "mhipalpur" vs "mahipalpur" will)
                similarity = difflib.SequenceMatcher(None, query_lower, area_lower).ratio()
                if similarity > 0.6:
                    score = int(similarity * 100)
            
            if score > 0:
                cluster = self.area_to_cluster.get(area_lower, "Other")
                suggestions.append({
                    "area": area,
                    "count": count,
                    "cluster": cluster,
                    "score": score
                })

        # Rank by score (descending) then by popularity (hotel count)
        suggestions.sort(key=lambda x: (x["score"], x["count"]), reverse=True)
        return suggestions[:10] # Return top 10 suggestions

    def get_nearest(self, area: str) -> Dict[str, Any]:
        """
        Returns nearby areas ordered by geographic cluster for fallback routing.
        """
        area_lower = area.lower()
        cluster_name = self.area_to_cluster.get(area_lower)
        
        if not cluster_name:
            return {
                "original_area": area,
                "cluster": None,
                "nearby_areas": [],
                "message": f"Could not find nearby alternatives for {area}."
            }

        # Get all areas in this cluster (excluding the original area) that actually have hotels
        cluster_areas = self.CLUSTERS[cluster_name]
        nearby_areas = [
            a for a in cluster_areas 
            if a.lower() != area_lower and self.area_counts.get(a, 0) > 0
        ]
        
        # Sort nearby areas by popularity
        nearby_areas.sort(key=lambda x: self.area_counts.get(x, 0), reverse=True)

        return {
            "original_area": area,
            "cluster": cluster_name,
            "nearby_areas": nearby_areas,
            "message": f"Showing nearby hotels in {cluster_name} because few properties were found in {area}."
        }
