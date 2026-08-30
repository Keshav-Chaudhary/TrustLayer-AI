import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy import (
    Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey, Index, create_engine
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from app.config.config import settings

Base = declarative_base()

class HotelModel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, default="")
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    price = Column(String(100), nullable=True)
    budget_category = Column(String(50), default="Mid-Range")
    hero_image = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)

    location = relationship("HotelLocationModel", back_populates="hotel", uselist=False, cascade="all, delete-orphan")
    score = relationship("HotelScoreModel", back_populates="hotel", uselist=False, cascade="all, delete-orphan")
    sources = relationship("HotelSourceModel", back_populates="hotel", cascade="all, delete-orphan")
    amenities = relationship("HotelAmenityModel", back_populates="hotel", uselist=False, cascade="all, delete-orphan")
    provenance = relationship("HotelProvenanceModel", back_populates="hotel", cascade="all, delete-orphan")


class HotelLocationModel(Base):
    __tablename__ = "hotel_locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(String(255), ForeignKey("hotels.hotel_id"), nullable=False, index=True)
    area = Column(String(255), default="")
    city = Column(String(255), default="")
    destination = Column(String(255), default="")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    hotel = relationship("HotelModel", back_populates="location")


class HotelScoreModel(Base):
    __tablename__ = "hotel_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(String(255), ForeignKey("hotels.hotel_id"), nullable=False, index=True)
    trust_score = Column(Float, default=0.0)
    cleanliness_score = Column(Float, nullable=True)
    service_score = Column(Float, nullable=True)
    location_score = Column(Float, nullable=True)
    value_score = Column(Float, nullable=True)
    staff_behavior_score = Column(Float, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

    hotel = relationship("HotelModel", back_populates="score")


class HotelSourceModel(Base):
    __tablename__ = "hotel_sources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(String(255), ForeignKey("hotels.hotel_id"), nullable=False, index=True)
    source = Column(String(255), default="final_hotel_dataset.csv")
    source_id = Column(String(255), nullable=True)
    source_url = Column(Text, nullable=True)
    content_hash = Column(String(64), nullable=False, index=True)
    ingested_at = Column(DateTime, default=datetime.utcnow)
    last_seen_at = Column(DateTime, default=datetime.utcnow)

    hotel = relationship("HotelModel", back_populates="sources")


class HotelAmenityModel(Base):
    __tablename__ = "hotel_amenities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(String(255), ForeignKey("hotels.hotel_id"), nullable=False, index=True)
    amenities_json = Column(Text, default="[]")

    hotel = relationship("HotelModel", back_populates="amenities")


class HotelProvenanceModel(Base):
    __tablename__ = "hotel_provenance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(String(255), ForeignKey("hotels.hotel_id"), nullable=False, index=True)
    field_name = Column(String(100), nullable=False)
    source = Column(String(255), default="final_hotel_dataset.csv")
    source_id = Column(String(255), nullable=True)
    content_hash = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    hotel = relationship("HotelModel", back_populates="provenance")


class EmbeddingDocumentModel(Base):
    __tablename__ = "embedding_documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(String(255), nullable=False, index=True)
    chunk_id = Column(String(255), unique=True, nullable=False, index=True)
    chunk_type = Column(String(100), default="Chunk A (Profile)")
    snippet = Column(Text, default="")
    content_hash = Column(String(64), nullable=False, index=True)
    embedding_model = Column(String(100), default="all-MiniLM-L6-v2")
    embedding_version = Column(Integer, default=1)
    embedding_dimension = Column(Integer, default=384)
    embedding_vector = Column(Text, nullable=False)  # Serialized vector representation
    created_at = Column(DateTime, default=datetime.utcnow)


class IngestionRunModel(Base):
    __tablename__ = "ingestion_runs"

    run_id = Column(String(100), primary_key=True)
    source = Column(String(255), default="final_hotel_dataset.csv")
    source_checksum = Column(String(64), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    records_seen = Column(Integer, default=0)
    records_inserted = Column(Integer, default=0)
    records_updated = Column(Integer, default=0)
    records_unchanged = Column(Integer, default=0)
    records_rejected = Column(Integer, default=0)
    validation_errors = Column(Text, default="[]")
    status = Column(String(50), default="IN_PROGRESS")


class IngestionRecordModel(Base):
    __tablename__ = "ingestion_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ingestion_run_id = Column(String(100), ForeignKey("ingestion_runs.run_id"), nullable=False, index=True)
    hotel_id = Column(String(255), nullable=False, index=True)
    operation = Column(String(50), nullable=False)  # CREATED, UPDATED, UNCHANGED, REJECTED
    previous_hash = Column(String(64), nullable=True)
    new_hash = Column(String(64), nullable=False)
    changed_fields = Column(Text, default="[]")
    error = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


class DomainEventModel(Base):
    __tablename__ = "domain_events"

    event_id = Column(String(100), primary_key=True)
    event_type = Column(String(100), nullable=False, index=True)  # HOTEL_CREATED, HOTEL_UPDATED, EMBEDDING_REQUIRED
    aggregate_type = Column(String(100), default="Hotel")
    aggregate_id = Column(String(255), nullable=False, index=True)
    version = Column(Integer, default=1)
    payload = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    attempt_count = Column(Integer, default=0)
    last_error = Column(Text, nullable=True)


# --- CANONICAL CONTENT HASH CALCULATION ---

def calculate_canonical_content_hash(record: Dict[str, Any]) -> str:
    """
    Computes a deterministic SHA-256 hash across all source-controlled canonical fields
    for robust change detection during ingestion.
    """
    keys = [
        "hotel_id", "name", "address", "area", "city", "destination",
        "latitude", "longitude", "rating", "review_count", "price", "budget_category",
        "trust_score", "cleanliness_score", "service_score", "location_score", "value_score",
        "amenities"
    ]
    
    canonical_parts = []
    for k in keys:
        val = record.get(k)
        if isinstance(val, list):
            val_str = json.dumps(sorted([str(item).strip().lower() for item in val if item]))
        elif isinstance(val, float):
            val_str = f"{val:.4f}"
        elif val is None:
            val_str = "null"
        else:
            val_str = str(val).strip().lower()
        canonical_parts.append(f"{k}:{val_str}")
        
    canonical_str = "|".join(canonical_parts)
    return hashlib.sha256(canonical_str.encode('utf-8')).hexdigest()
