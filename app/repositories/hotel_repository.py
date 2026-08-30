import os
import re
import hashlib
import logging
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from app.repositories.base import BaseHotelRepository
from app.config.config import settings

logger = logging.getLogger("trustlayer")

def _safe_int(val: Any, default: int = 0) -> int:
    try:
        if pd.isna(val):
            return default
        return int(float(str(val).strip()))
    except (ValueError, TypeError):
        return default

def _safe_float(val: Any, default: float = 0.0, min_val: float = None, max_val: float = None) -> float:
    try:
        if pd.isna(val):
            return default
        v = float(str(val).strip())
        if min_val is not None and v < min_val:
            return min_val
        if max_val is not None and v > max_val:
            return max_val
        return v
    except (ValueError, TypeError):
        return default

def _safe_str(val: Any, default: str = "") -> str:
    if pd.isna(val) or val is None:
        return default
    s = str(val).strip()
    return s if s else default


class CsvHotelRepository(BaseHotelRepository):
    """
    CSV storage adapter for hotel data. Reads final_hotel_dataset.csv as the 
    authoritative bootstrap store and caches records in memory.
    """
    def __init__(self, csv_path: Optional[str] = None):
        self.csv_path = csv_path or settings.CSV_DATASET_PATH
        self._hotels_db: Dict[str, Dict[str, Any]] = {}
        self._area_counts: Dict[str, int] = {}
        self._load_csv()

    def _load_csv(self):
        resolved_path = os.path.abspath(self.csv_path)
        if not os.path.exists(resolved_path):
            logger.warning(f"CSV dataset path missing at {resolved_path}")
            return

        image_urls = [
            "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1551882547-ff40eb0d1e73?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=600&q=80"
        ]

        try:
            df = pd.read_csv(resolved_path)
            for idx, row in df.iterrows():
                hid = _safe_str(row.get('hotel_id'))
                if not hid:
                    continue

                hotel_name = _safe_str(row.get('hotel_name')) or f"Hotel {hid[:6]}"
                raw_area = _safe_str(row.get('area'))
                area = raw_area if raw_area else "Delhi NCR"
                
                # Derive city/destination dynamically from dataset fields
                raw_city = _safe_str(row.get('city') or row.get('destination') or row.get('area_cluster'))
                city = raw_city if raw_city else (area if area != "Delhi NCR" else "Delhi")
                destination = city

                raw_budget = _safe_str(row.get('budget_category'), default="Mid-Range")
                name_lower = hotel_name.lower()
                if any(k in name_lower for k in ["pullman", "radisson", "hilton", "taj", "hyatt", "marriott", "crowne", "le meridien", "itc"]):
                    budget_cat = "Luxury"
                elif any(k in name_lower for k in ["holiday inn", "novotel", "lemon tree", "doubletree", "country inn", "ibis", "residency", "suites"]):
                    budget_cat = "Mid-Range"
                elif any(k in name_lower for k in ["treebo", "oyo", "fabhotel", "hostel", "pg", "homestay", "stay", "inn"]):
                    budget_cat = "Budget"
                else:
                    budget_cat = raw_budget if raw_budget in ["Luxury", "Mid-Range", "Budget"] else "Mid-Range"

                img_idx = int(hashlib.md5(hid.encode()).hexdigest(), 16) % len(image_urls)
                hero_image = image_urls[img_idx]

                raw_trust = _safe_float(row.get('trust_score'), default=0.85)
                trust_score = round(raw_trust * 100 if raw_trust <= 1.0 else raw_trust, 1)

                raw_clean = _safe_float(row.get('cleanliness_score'), default=0.8)
                clean_score = round(raw_clean * 5.0 if raw_clean <= 1.0 else raw_clean, 1)

                raw_serv = _safe_float(row.get('service_score'), default=0.8)
                serv_score = round(raw_serv * 5.0 if raw_serv <= 1.0 else raw_serv, 1)

                raw_loc = _safe_float(row.get('location_score'), default=0.8)
                loc_score = round(raw_loc * 5.0 if raw_loc <= 1.0 else raw_loc, 1)

                raw_val = _safe_float(row.get('value_for_money_score'), default=0.8)
                val_score = round(raw_val * 5.0 if raw_val <= 1.0 else raw_val, 1)

                rating = round(_safe_float(row.get('rating') or row.get('rating_score'), default=4.0, min_val=1.0, max_val=5.0), 1)
                reviews_count = _safe_int(row.get('review_count'), default=0)

                hotel_obj = {
                    "hotel_id": hid,
                    "name": hotel_name,
                    "area": area,
                    "city": city,
                    "destination": destination,
                    "address": _safe_str(row.get('address')),
                    "latitude": _safe_float(row.get('latitude')) if not pd.isna(row.get('latitude')) else None,
                    "longitude": _safe_float(row.get('longitude')) if not pd.isna(row.get('longitude')) else None,
                    "rating": rating,
                    "reviews_count": reviews_count,
                    "review_count": reviews_count,
                    "price": _safe_str(row.get('price'), default="₹2,500 - ₹5,000 / night"),
                    "trust_score": trust_score,
                    "budget_category": budget_cat,
                    "aspect_scores": {
                        "cleanliness": clean_score,
                        "service": serv_score,
                        "location": loc_score,
                        "value": val_score,
                        "staff": round(_safe_float(row.get('staff_behavior_score'), default=0.8) * 5.0 if _safe_float(row.get('staff_behavior_score')) <= 1.0 else _safe_float(row.get('staff_behavior_score')), 1)
                    },
                    "cleanliness_score": clean_score,
                    "service_score": serv_score,
                    "location_score": loc_score,
                    "value_score": val_score,
                    "amenities": ["Free Wi-Fi", "Air Conditioning", "Housekeeping", "Room Service", "24-hour Desk"],
                    "hero_image": hero_image,
                    "review_evidence": [],
                    # Metadata provenance
                    "source": "final_hotel_dataset.csv",
                    "version": 1
                }
                
                self._hotels_db[hid] = hotel_obj
                
                # Dynamic area counts
                norm_area = area.strip()
                if norm_area:
                    self._area_counts[norm_area] = self._area_counts.get(norm_area, 0) + 1

            logger.info(f"Loaded {len(self._hotels_db)} hotels from CSV dataset {resolved_path}")
        except Exception as e:
            logger.error(f"Error loading CSV dataset: {e}")

    def get_by_id(self, hotel_id: str) -> Optional[Dict[str, Any]]:
        return self._hotels_db.get(hotel_id)

    def get_all_hotels(self) -> Dict[str, Dict[str, Any]]:
        return self._hotels_db

    def get_area_counts(self) -> Dict[str, int]:
        return self._area_counts

    def count(self) -> int:
        return len(self._hotels_db)

    def exists(self, hotel_id: str) -> bool:
        return hotel_id in self._hotels_db

    def list_hotels(
        self,
        page: int = 1,
        limit: int = 20,
        area: Optional[str] = None,
        budget: Optional[str] = None,
        rating: Optional[float] = None,
        cleanliness: Optional[float] = None,
        sort_by: str = "trust_score_desc"
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        hotels = list(self._hotels_db.values())

        if area:
            area_lower = area.strip().lower()
            hotels = [h for h in hotels if area_lower in h.get("area", "").lower()]
        if budget:
            budget_lower = budget.strip().lower()
            hotels = [h for h in hotels if budget_lower == h.get("budget_category", "").lower()]
        if rating is not None:
            hotels = [h for h in hotels if h.get("rating", 0.0) >= rating]
        if cleanliness is not None:
            hotels = [h for h in hotels if h.get("cleanliness_score", 0.0) >= cleanliness]

        if sort_by == "trust_score_desc":
            hotels.sort(key=lambda x: x.get("trust_score", 0.0), reverse=True)
        elif sort_by == "trust_score_asc":
            hotels.sort(key=lambda x: x.get("trust_score", 0.0))
        elif sort_by == "rating_desc":
            hotels.sort(key=lambda x: x.get("rating", 0.0), reverse=True)
        elif sort_by == "cleanliness_desc":
            hotels.sort(key=lambda x: x.get("cleanliness_score", 0.0), reverse=True)

        total_hotels = len(hotels)
        total_pages = max(1, (total_hotels + limit - 1) // limit)
        page = min(page, total_pages)
        start_idx = (page - 1) * limit
        paginated_hotels = hotels[start_idx:start_idx + limit]

        pagination = {
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "total_hotels": total_hotels,
            "has_next": page < total_pages,
            "has_previous": page > 1
        }
        return paginated_hotels, pagination

    def upsert(self, hotel_data: Dict[str, Any]) -> bool:
        hid = hotel_data.get("hotel_id")
        if not hid:
            return False
        self._hotels_db[hid] = hotel_data
        return True

    def bulk_upsert(self, hotels: List[Dict[str, Any]]) -> int:
        count = 0
        for h in hotels:
            if self.upsert(h):
                count += 1
        return count
