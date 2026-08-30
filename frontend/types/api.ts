export interface ProvenanceChunk {
  chunk_id: string;
  chunk_type: string;
  snippet: string;
}

export interface Recommendation {
  hotel_id: string;
  name: string;
  summary_text: string;
  aspect_scores: Record<string, number>;
  trust_score: number;
  explanation_badge: string;
  ai_match_label: string;
  match_reason: string;
  query_alignment_score: number;
  review_evidence: string[];
  provenance: ProvenanceChunk[];
  confidence_badge: string;
  rating: number;
  reviews_count?: number;
  price?: string;
  area: string;
  amenities: string[];
  hero_image?: string;
  verified_reviews_count: number;
  evidence_confidence: string;
}

export interface RecommendationResponse {
  trace_id: string;
  query: string;
  recommendations: Recommendation[];
  catalog_suggestions?: Recommendation[];
  metadata: Record<string, any>;
}

export interface PaginationMetadata {
  page: number;
  limit: number;
  total_pages: number;
  total_hotels: number;
  has_next: boolean;
  has_previous: boolean;
}

export interface HotelCatalogResponse {
  hotels: Recommendation[];
  pagination: PaginationMetadata;
  filter_counts: Record<string, Record<string, number>>;
}

export interface MetricsResponse {
  total_hotels: number;
  total_chunks: number;
  cache_hit_rate: number;
  avg_latency_ms: number;
}

export interface HotelAnalysis {
  hotel_id: string;
  name: string;
  trust_score: number;
  aspect_scores: Record<string, number>;
  positive_themes: string[];
  common_complaints: string[];
  professional_evidence: ProvenanceChunk[];
  area: string;
}

export interface AnalyzeResponse {
  hotel_id: string;
  grounded_analysis: string;
  citations: ProvenanceChunk[];
  is_hallucination_free: boolean;
}

export interface CompareResponse {
  grounded_summary: string;
  insights: {
    aspect: string;
    insight_text: string;
    winner_hotel_id: string | null;
    citations: ProvenanceChunk[];
  }[];
}

export interface EvidenceResponse {
  hotel_id: string;
  evidence_chunks: ProvenanceChunk[];
}

export interface ExplanationResponse {
  hotel_id: string;
  feature_importance: Record<string, number>;
  score_breakdown: Record<string, number>;
}

export interface SearchSuggestion {
  area: string;
  count: number;
  cluster: string;
  score: number;
}

export interface SearchSuggestResponse {
  suggestions: SearchSuggestion[];
}

export interface NearestAreaResponse {
  original_area: string;
  cluster: string | null;
  nearby_areas: string[];
  message: string;
}

export interface BatchRecommendedHotel {
  hotel_id: string;
  hotel_name: string;
  final_score: number;
  final_rank: number;
  trust_score: number;
  cleanliness: number;
  service: number;
  location: number;
  value: number;
  retrieved_from: string[];
}

export interface BatchQualityGateFailure {
  hotel_id: string;
  hotel_name: string;
  reason: string;
}

export interface BatchParsedIntent {
  intent: string;
  hard_constraints: Record<string, any>;
  soft_constraints: Record<string, any>;
}

export interface BatchQueryDetails {
  query: string;
  status: "success" | "failed" | "timeout";
  latency_ms: number;
  parsed_intent: BatchParsedIntent;
  final_recommendation_count: number;
  top_5_recommended_hotels: BatchRecommendedHotel[];
  quality_gate_failures: BatchQualityGateFailure[];
  error_message?: string;
  full_trace?: any;
}

export interface BatchRunResult {
  run_id: string;
  timestamp: string;
  total_queries: number;
  success_count: number;
  failure_count: number;
  avg_latency_ms: number;
  p95_latency_ms: number;
  queries: BatchQueryDetails[];
}

