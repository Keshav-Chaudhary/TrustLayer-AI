from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class HotelDomainModel(BaseModel):
    hotel_id: str
    google_place_id: Optional[str] = None
    name: str
    address: str = ""
    area: str = ""
    city: str = ""
    destination: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    rating: float = 0.0
    review_count: int = 0
    price: Optional[str] = None
    budget_category: str = "Mid-Range"
    trust_score: float = 0.0
    cleanliness_score: Optional[float] = None
    service_score: Optional[float] = None
    location_score: Optional[float] = None
    value_score: Optional[float] = None
    staff_behavior_score: Optional[float] = None
    aspect_scores: Dict[str, float] = Field(default_factory=dict)
    amenities: List[str] = Field(default_factory=list)
    hero_image: Optional[str] = None
    
    # Metadata, Freshness & Provenance Fields
    source: str = "final_hotel_dataset.csv"
    source_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    ingested_at: Optional[str] = None
    content_hash: Optional[str] = None
    version: int = 1

class ReviewDomainModel(BaseModel):
    review_id: str
    hotel_id: str
    review_text: str
    rating: Optional[float] = None
    sentiment_score: Optional[float] = None
    aspect_mentions: Dict[str, Any] = Field(default_factory=dict)
    source: str = "google_reviews"
    ingested_at: Optional[str] = None

class CandidateDomainModel(BaseModel):
    hotel_id: str
    document: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)
    retrieval_channels: List[str] = Field(default_factory=list)
    raw_distance: float = 0.0
    semantic_score: float = 0.0
    metadata_score: float = 0.0
    recommendation_score: float = 0.0
    area_boost: float = 0.0
    amenities_penalty: float = 0.0
    final_score: float = 0.0
    rerank_position: Optional[int] = None

class SearchQueryDomainModel(BaseModel):
    raw_query: str
    parsed_area: Optional[str] = None
    travel_intent: Optional[str] = None
    aspects: List[str] = Field(default_factory=list)
    budget_constraint: Optional[str] = None
    other_constraints: Dict[str, Any] = Field(default_factory=dict)
    hard_constraints: Dict[str, Any] = Field(default_factory=dict)
    soft_constraints: Dict[str, Any] = Field(default_factory=dict)

class ProvenanceChunk(BaseModel):
    chunk_id: str
    chunk_type: str
    snippet: str
    metadata: Optional[Dict[str, Any]] = None

class DebugTraceDomainModel(BaseModel):
    trace_id: str
    query: str
    parser_output: Dict[str, Any] = Field(default_factory=dict)
    retrieval_channels: List[str] = Field(default_factory=list)
    candidate_pool: List[Dict[str, Any]] = Field(default_factory=list)
    quality_gate_results: Dict[str, Any] = Field(default_factory=dict)
    pareto_results: Dict[str, Any] = Field(default_factory=dict)
    ranking_results: List[Dict[str, Any]] = Field(default_factory=list)
    timings: Dict[str, float] = Field(default_factory=dict)
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    final_recommendations: List[Dict[str, Any]] = Field(default_factory=list)
