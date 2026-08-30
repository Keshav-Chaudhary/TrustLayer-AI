import json
import math
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, Session
from app.config.config import settings
from app.repositories.base import BaseHotelRepository
from app.repositories.db_schema import (
    Base, HotelModel, HotelLocationModel, HotelScoreModel, HotelSourceModel,
    HotelAmenityModel, HotelProvenanceModel, IngestionRecordModel, DomainEventModel,
    calculate_canonical_content_hash
)

class PostgresHotelRepository(BaseHotelRepository):
    def __init__(self, db_url: Optional[str] = None, session: Optional[Session] = None):
        self.db_url = db_url or settings.DATABASE_URL or "sqlite:///:memory:"
        if session:
            self.session_factory = None
            self._external_session = session
        else:
            self._external_session = None
            self.engine = create_engine(self.db_url, connect_args={"check_same_thread": False} if "sqlite" in self.db_url else {})
            Base.metadata.create_all(self.engine)
            self.session_factory = sessionmaker(bind=self.engine)

    def _get_session(self) -> Session:
        if self._external_session:
            return self._external_session
        return self.session_factory()

    def _hotel_to_dict(self, hotel: HotelModel) -> Dict[str, Any]:
        loc = hotel.location
        score = hotel.score
        amenities = json.loads(hotel.amenities.amenities_json) if (hotel.amenities and hotel.amenities.amenities_json) else ["Free Wi-Fi", "Air Conditioning"]

        clean_score = round(score.cleanliness_score, 1) if (score and score.cleanliness_score is not None) else 4.5
        serv_score = round(score.service_score, 1) if (score and score.service_score is not None) else 4.5
        loc_score = round(score.location_score, 1) if (score and score.location_score is not None) else 4.5
        val_score = round(score.value_score, 1) if (score and score.value_score is not None) else 4.5
        staff_score = round(score.staff_behavior_score, 1) if (score and score.staff_behavior_score is not None) else 4.5

        area = loc.area if loc else "Delhi"
        city = loc.city if loc else "Delhi"
        dest = loc.destination if loc else city

        return {
            "hotel_id": hotel.hotel_id,
            "name": hotel.name,
            "address": hotel.address or f"{area}, {city}",
            "area": area,
            "city": city,
            "destination": dest,
            "area_cluster": city,
            "latitude": loc.latitude if loc else 28.6139,
            "longitude": loc.longitude if loc else 77.2090,
            "rating": round(hotel.rating, 1),
            "reviews_count": hotel.review_count,
            "review_count": hotel.review_count,
            "price": hotel.price or "₹2,500 - ₹5,000 / night",
            "trust_score": round(score.trust_score, 1) if score else 85.0,
            "budget_category": hotel.budget_category or "Mid-Range",
            "aspect_scores": {
                "cleanliness": clean_score,
                "service": serv_score,
                "location": loc_score,
                "value": val_score,
                "staff": staff_score
            },
            "cleanliness_score": clean_score,
            "service_score": serv_score,
            "location_score": loc_score,
            "value_score": val_score,
            "amenities": amenities,
            "hero_image": hotel.hero_image,
            "review_evidence": [],
            "source": "postgresql",
            "version": hotel.version
        }

    def get_by_id(self, hotel_id: str) -> Optional[Dict[str, Any]]:
        session = self._get_session()
        try:
            hotel = session.query(HotelModel).filter(HotelModel.hotel_id == str(hotel_id).strip()).first()
            if not hotel:
                return None
            return self._hotel_to_dict(hotel)
        finally:
            if not self._external_session:
                session.close()

    def get_all_hotels(self) -> Dict[str, Dict[str, Any]]:
        session = self._get_session()
        try:
            hotels = session.query(HotelModel).all()
            return {h.hotel_id: self._hotel_to_dict(h) for h in hotels}
        finally:
            if not self._external_session:
                session.close()

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
        session = self._get_session()
        try:
            query = session.query(HotelModel).join(HotelLocationModel).join(HotelScoreModel)

            if area:
                areas = [a.strip().lower() for a in area.split(",") if a.strip()]
                query = query.filter(func.lower(HotelLocationModel.area).in_(areas))
            if budget:
                query = query.filter(func.lower(HotelModel.budget_category).contains(budget.lower()))
            if rating:
                query = query.filter(HotelModel.rating >= float(rating))
            if cleanliness:
                query = query.filter(HotelScoreModel.cleanliness_score >= float(cleanliness))

            if sort_by == "rating_desc":
                query = query.order_by(HotelModel.rating.desc(), HotelModel.hotel_id.asc())
            elif sort_by == "rating_asc":
                query = query.order_by(HotelModel.rating.asc(), HotelModel.hotel_id.asc())
            elif sort_by == "reviews_count_desc":
                query = query.order_by(HotelModel.review_count.desc(), HotelModel.hotel_id.asc())
            else:
                query = query.order_by(HotelScoreModel.trust_score.desc(), HotelModel.hotel_id.asc())

            total_hotels = query.count()
            total_pages = max(1, math.ceil(total_hotels / limit)) if limit > 0 else 1

            start_idx = (page - 1) * limit
            hotels = query.offset(start_idx).limit(limit).all()

            results = [self._hotel_to_dict(h) for h in hotels]
            pagination = {
                "current_page": page,
                "total_pages": total_pages,
                "total_hotels": total_hotels,
                "limit": limit
            }
            return results, pagination
        finally:
            if not self._external_session:
                session.close()

    def get_area_counts(self) -> Dict[str, int]:
        session = self._get_session()
        try:
            results = session.query(HotelLocationModel.area, func.count(HotelLocationModel.id))\
                .group_by(HotelLocationModel.area).all()
            return {r[0]: r[1] for r in results if r[0]}
        finally:
            if not self._external_session:
                session.close()

    def count(self) -> int:
        session = self._get_session()
        try:
            return session.query(HotelModel).count()
        finally:
            if not self._external_session:
                session.close()

    def exists(self, hotel_id: str) -> bool:
        session = self._get_session()
        try:
            return session.query(HotelModel.id).filter(HotelModel.hotel_id == str(hotel_id).strip()).first() is not None
        finally:
            if not self._external_session:
                session.close()

    def upsert(self, hotel_data: Dict[str, Any]) -> bool:
        return self.bulk_upsert([hotel_data]) > 0

    def bulk_upsert(self, hotels: List[Dict[str, Any]]) -> int:
        session = self._get_session()
        upserted_count = 0
        try:
            for hdata in hotels:
                hid = str(hdata["hotel_id"]).strip()
                existing = session.query(HotelModel).filter(HotelModel.hotel_id == hid).first()
                if not existing:
                    existing = HotelModel(hotel_id=hid)
                    session.add(existing)

                existing.name = hdata.get("name", "Unknown Hotel")
                existing.address = hdata.get("address", "")
                existing.rating = float(hdata.get("rating", 0.0))
                existing.review_count = int(hdata.get("review_count", hdata.get("reviews_count", 0)))
                existing.price = hdata.get("price")
                existing.budget_category = hdata.get("budget_category", "Mid-Range")
                existing.hero_image = hdata.get("hero_image")

                # Upsert Location
                if not existing.location:
                    existing.location = HotelLocationModel(hotel_id=hid)
                existing.location.area = hdata.get("area", "")
                existing.location.city = hdata.get("city", "")
                existing.location.destination = hdata.get("destination", hdata.get("city", ""))
                existing.location.latitude = hdata.get("latitude")
                existing.location.longitude = hdata.get("longitude")

                # Upsert Scores
                if not existing.score:
                    existing.score = HotelScoreModel(hotel_id=hid)
                aspects = hdata.get("aspect_scores", {})
                existing.score.trust_score = float(hdata.get("trust_score", 85.0))
                existing.score.cleanliness_score = float(aspects.get("cleanliness", hdata.get("cleanliness_score", 4.5)))
                existing.score.service_score = float(aspects.get("service", hdata.get("service_score", 4.5)))
                existing.score.location_score = float(aspects.get("location", hdata.get("location_score", 4.5)))
                existing.score.value_score = float(aspects.get("value", hdata.get("value_score", 4.5)))
                existing.score.staff_behavior_score = float(aspects.get("staff", hdata.get("staff_behavior_score", 4.5)))

                # Upsert Amenities
                if not existing.amenities:
                    existing.amenities = HotelAmenityModel(hotel_id=hid)
                existing.amenities.amenities_json = json.dumps(hdata.get("amenities", ["Free Wi-Fi", "Air Conditioning"]))

                # Transactional Outbox Event
                import uuid
                evt_type = "HOTEL_CREATED" if not existing.id else "HOTEL_UPDATED"
                domain_evt = DomainEventModel(
                    event_id=str(uuid.uuid4()),
                    event_type=evt_type,
                    aggregate_type="Hotel",
                    aggregate_id=hid,
                    payload=json.dumps(hdata)
                )
                session.add(domain_evt)

                upserted_count += 1

            if not self._external_session:
                session.commit()
            return upserted_count
        except Exception:
            if not self._external_session:
                session.rollback()
            raise
        finally:
            if not self._external_session:
                session.close()
