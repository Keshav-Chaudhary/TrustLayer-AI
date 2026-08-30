import re
from typing import Dict, Any

def normalize_hotel_record(record: Dict[str, Any]) -> Dict[str, Any]:
    norm = dict(record)
    
    # 1. String trimming & canonicalization
    for key, val in norm.items():
        if isinstance(val, str):
            val_clean = val.strip()
            if val_clean.lower() in ("nan", "none", "null", ""):
                norm[key] = ""
            else:
                norm[key] = val_clean

    # 2. Hotel ID & Name
    norm["hotel_id"] = str(norm.get("hotel_id", "")).strip()
    hname = str(norm.get("name") or norm.get("hotel_name") or "").strip()
    norm["name"] = hname
    norm["hotel_name"] = hname

    # 3. Numeric Parsing
    try:
        norm["rating"] = round(float(norm.get("rating", 4.0)), 2) if norm.get("rating") != "" else 4.0
    except (ValueError, TypeError):
        norm["rating"] = 4.0

    try:
        norm["review_count"] = int(float(norm.get("review_count", 0))) if norm.get("review_count") != "" else 0
    except (ValueError, TypeError):
        norm["review_count"] = 0

    try:
        ts = float(norm.get("trust_score", 85.0)) if norm.get("trust_score") != "" else 85.0
        if ts <= 1.0 and ts > 0.0:
            ts *= 100.0
        norm["trust_score"] = round(ts, 2)
    except (ValueError, TypeError):
        norm["trust_score"] = 85.0

    try:
        norm["latitude"] = float(norm.get("latitude")) if norm.get("latitude") != "" else None
    except (ValueError, TypeError):
        norm["latitude"] = None

    try:
        norm["longitude"] = float(norm.get("longitude")) if norm.get("longitude") != "" else None
    except (ValueError, TypeError):
        norm["longitude"] = None

    # 4. Amenities list parsing
    amenities = norm.get("amenities", [])
    if isinstance(amenities, str):
        if amenities.startswith("[") and amenities.endswith("]"):
            amenities_clean = re.sub(r"[\[\]'\"]", "", amenities)
            norm["amenities"] = [a.strip() for a in amenities_clean.split(",") if a.strip()]
        else:
            norm["amenities"] = [a.strip() for a in amenities.split(",") if a.strip()]

    return norm
