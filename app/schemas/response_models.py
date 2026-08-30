from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional, Any

class ProvenanceChunk(BaseModel):
    chunk_id: str
    chunk_type: str
    snippet: str
    metadata: Optional[Dict[str, Any]] = None

class Recommendation(BaseModel):
    model_config = ConfigDict(extra="ignore")

    hotel_id: str
    name: str
    summary_text: str
    aspect_scores: Dict[str, float]
    trust_score: float
    explanation_badge: str
    ai_match_label: str
    match_reason: str
    query_alignment_score: float
    review_evidence: List[str]
    provenance: List[ProvenanceChunk]
    confidence_badge: str = "High"
    rating: float = 0.0
    reviews_count: Optional[int] = None
    price: Optional[str] = None
    area: str = ""
    city: str = ""
    destination: str = ""
    amenities: List[str] = []
    hero_image: Optional[str] = None
    verified_reviews_count: int = 0
    verified_review_count: int = 0
    evidence_confidence: str = "None"
    evidence_snippets: List[Dict[str, str]] = []
    cleanliness_score: Optional[float] = None
    service_score: Optional[float] = None
    location_score: Optional[float] = None
    value_score: Optional[float] = None
    semantic_score: Optional[float] = None
    raw_distance: Optional[float] = None
    retrieved_from: Optional[List[str]] = None
    fallback_distance: Optional[float] = None
    fallback_origin: Optional[str] = None

class RecommendationResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    trace_id: str
    query: str
    recommendations: List[Recommendation]
    catalog_suggestions: Optional[List[Recommendation]] = None
    metadata: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    message: str

class ReadinessResponse(BaseModel):
    status: str
    dependencies: Dict[str, str]

class MetricsResponse(BaseModel):
    total_hotels: int
    total_chunks: int
    cache_hit_rate: float
    avg_latency_ms: float

class HotelAnalysis(BaseModel):
    model_config = ConfigDict(extra="ignore")
    hotel_id: str
    name: str
    trust_score: float
    aspect_scores: Dict[str, float]
    positive_themes: List[str]
    common_complaints: List[str]
    professional_evidence: List[ProvenanceChunk]
    area: str = ""
    city: str = ""
    destination: str = ""
    rating: float = 0.0
    reviews_count: Optional[int] = None
    hero_image: Optional[str] = None

class AnalyzeRequest(BaseModel):
    hotel_id: str
    query: Optional[str] = None

class AnalyzeResponse(BaseModel):
    hotel_id: str
    grounded_analysis: str
    citations: List[ProvenanceChunk]
    is_hallucination_free: bool

class CompareRequest(BaseModel):
    hotel_ids: List[str]

class ComparisonInsight(BaseModel):
    aspect: str
    insight_text: str
    winner_hotel_id: Optional[str]
    citations: List[ProvenanceChunk]

class CompareResponse(BaseModel):
    grounded_summary: str
    insights: List[ComparisonInsight]

class EvidenceResponse(BaseModel):
    hotel_id: str
    evidence_chunks: List[ProvenanceChunk]

class ExplanationResponse(BaseModel):
    hotel_id: str
    feature_importance: Dict[str, float]
    score_breakdown: Dict[str, float]

class ChatRequest(BaseModel):
    query: str
    hotel_id: Optional[str] = None
    session_id: Optional[str] = None

class PaginationMetadata(BaseModel):
    page: int
    limit: int
    total_pages: int
    total_hotels: int
    has_next: bool
    has_previous: bool

class HotelCatalogResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    hotels: List[Recommendation]
    pagination: PaginationMetadata
    filter_counts: Dict[str, Dict[str, int]] = {}
