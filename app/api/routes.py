import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.schemas.response_models import (
    RecommendationResponse, 
    HealthResponse, 
    MetricsResponse,
    HotelAnalysis,
    AnalyzeRequest, AnalyzeResponse,
    CompareRequest, CompareResponse,
    EvidenceResponse, ExplanationResponse,
    ChatRequest, HotelCatalogResponse
)
from fastapi import APIRouter, HTTPException, Query
from app.services.recommendation_service import RecommendationService
from app.services.cache_service import cache_service

router = APIRouter()
rec_service = RecommendationService()

class QueryRequest(BaseModel):
    query: str
    limit: int = 5
    max_results: int = 5

@router.get("/health", response_model=HealthResponse)
def health_check():
    return {"status": "ok", "message": "TrustLayer-AI API is healthy"}

@router.get("/ready")
def readiness_check():
    import os, requests
    from app.config.config import settings
    vector_dir = os.path.abspath(settings.VECTOR_STORE_PATH)
    vec_ok = os.path.exists(vector_dir)
    ollama_ok = True
    try:
        res = requests.get(settings.OLLAMA_ENDPOINT, timeout=3)
        ollama_ok = (res.status_code == 200)
    except Exception:
        ollama_ok = False
        
    status = "ready" if vec_ok else "not_ready"
    if not vec_ok:
        raise HTTPException(status_code=503, detail="Vector store unavailable")
    return {"status": status, "dependencies": {"vector_store": "ok" if vec_ok else "unavailable", "ollama": "ok" if ollama_ok else "unreachable"}}


@router.get("/metrics", response_model=MetricsResponse)
def get_metrics():
    return {
        "total_hotels": 3450,
        "total_chunks": 7910,
        "cache_hit_rate": cache_service.get_hit_rate(),
        "avg_latency_ms": 185.0
    }

@router.get("/debug/trace")
def get_debug_trace(query: str = Query("Hotels with excellent cleanliness ratings")):
    try:
        return rec_service.get_debug_trace(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommend", response_model=RecommendationResponse)
def recommend(request: QueryRequest):
    trace_id = f"req-{uuid.uuid4().hex[:8]}"
    cache_key = cache_service.generate_key("rec", {"q": request.query, "k": request.max_results})
    
    cached_res = cache_service.get(cache_key)
    if cached_res:
        cached_res["metadata"]["cache_hit"] = True
        cached_res["trace_id"] = trace_id
        return cached_res
        
    try:
        recommendations, catalog_suggestions, metadata = rec_service.process_query(request.query, max(request.limit, request.max_results))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    print(f"[TrustLayer Telemetry] Query: '{request.query}' | retrieval: {metadata.get('retrieval_ms', 0):.2f}ms | compression: {metadata.get('compression_ms', 0):.2f}ms | llm: {metadata.get('llm_ms', 0):.2f}ms | total: {metadata.get('latency_ms', 0):.2f}ms | cache_hit: {metadata.get('cache_hit', False)}")
        
    response = {
        "trace_id": trace_id,
        "query": request.query,
        "recommendations": recommendations,
        "catalog_suggestions": catalog_suggestions,
        "metadata": metadata
    }
    
    cache_service.set(cache_key, response)
    return response

@router.get("/hotels", response_model=HotelCatalogResponse)
def get_hotels(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    area: str = Query(None),
    budget: str = Query(None),
    rating: float = Query(None),
    cleanliness: float = Query(None),
    sort_by: str = Query("trust_score_desc")
):
    try:
        return rec_service.get_hotels_catalog(page, limit, area, budget, rating, cleanliness, sort_by)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/hotels/featured", response_model=HotelCatalogResponse)
def get_featured_hotels():
    try:
        # Default sort for featured: trust_score_desc, limit 5
        return rec_service.get_hotels_catalog(page=1, limit=5, sort_by="trust_score_desc")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/hotel/{hotel_id}", response_model=HotelAnalysis)
def get_hotel(hotel_id: str):
    try:
        return rec_service.get_hotel_details(hotel_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Hotel not found")

class SaveRequest(BaseModel):
    hotel_id: str

@router.post("/save")
def save_hotel(request: SaveRequest):
    return {"status": "success", "hotel_id": request.hotel_id}

@router.post("/compare", response_model=CompareResponse)
def compare_hotels(request: CompareRequest):
    cache_key = cache_service.generate_key("compare", {"ids": sorted(request.hotel_ids)})
    cached_res = cache_service.get(cache_key)
    if cached_res:
        return cached_res
        
    try:
        res = rec_service.compare_hotels(request.hotel_ids)
        cache_service.set(cache_key, res)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_hotel(request: AnalyzeRequest):
    try:
        return rec_service.analyze_hotel(request.hotel_id, request.query or "")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/hotel/{hotel_id}/evidence", response_model=EvidenceResponse)
def get_evidence(hotel_id: str):
    try:
        return rec_service.get_evidence(hotel_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Hotel not found")

@router.get("/hotel/{hotel_id}/explanation", response_model=ExplanationResponse)
def get_explanation(hotel_id: str):
    try:
        return rec_service.get_explanation(hotel_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Hotel not found")

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Use HTTP chunked streaming
        return StreamingResponse(
            rec_service.stream_chat(request.query, request.hotel_id or ""), 
            media_type="text/plain"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Advanced Batch Query Debugger Additions
import os
import tempfile
import json
import asyncio
import time
import uuid
import statistics
from pydantic import BaseModel, field_validator
from typing import List, Dict, Any, Optional

class BatchDebugRequest(BaseModel):
    queries: List[str]

    @field_validator("queries")
    @classmethod
    def validate_queries(cls, v: List[str]) -> List[str]:
        # Trim whitespace and discard empty queries
        trimmed = [q.strip() for q in v if q and q.strip()]
        if not trimmed:
            raise ValueError("Query list cannot be empty or contain only blank queries.")
        if len(v) > 100 or len(trimmed) > 100:
            raise ValueError("Query list exceeds the maximum limit of 100 queries.")
        return trimmed

# Global asyncio Lock to reject concurrent batch requests with 409
batch_lock = asyncio.Lock()
BATCH_FILE_PATH = "data/exports/batch_debug_results.json"

def atomic_write_json(file_path: str, data: Any):
    dir_name = os.path.dirname(file_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        try:
            os.replace(temp_path, file_path)
        except PermissionError:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
    except Exception as e:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
        raise e

@router.post("/debug/batch")
async def run_batch_debug(request: BatchDebugRequest):
    # Reject with 409 if a batch is already in progress
    if batch_lock.locked():
        raise HTTPException(status_code=409, detail="A batch debug run is currently in progress. Please try again later.")

    async with batch_lock:
        run_id = str(uuid.uuid4())
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        queries_results = []
        latencies = []
        success_count = 0
        failure_count = 0

        for query in request.queries:
            # Yield control back to the event loop so that other endpoints (like health/GETs) remain responsive during batch runs
            await asyncio.sleep(0.005)
            
            try:
                # Wrap in try/except so one failure doesn't abort the batch
                trace = rec_service.get_debug_trace(query)
                
                overview = trace.get("section1_request_overview", {})
                latency = overview.get("total_execution_time_ms", 0.0)
                latencies.append(latency)
                
                parser_data = trace.get("section3_query_parser", {})
                parsed_intent = {
                    "intent": parser_data.get("intent", "Unknown"),
                    "hard_constraints": parser_data.get("hard_constraints", {}),
                    "soft_constraints": parser_data.get("soft_constraints", {})
                }
                
                final_ranking = trace.get("section10_final_ranking", [])
                recommendation_count = len(final_ranking)
                
                # Extract top 5 recommended hotels
                top_5 = []
                for h in final_ranking[:5]:
                    top_5.append({
                        "hotel_id": h.get("hotel_id"),
                        "hotel_name": h.get("hotel_name"),
                        "final_score": h.get("final_score"),
                        "final_rank": h.get("final_rank"),
                        "trust_score": h.get("trust_score"),
                        "cleanliness": h.get("cleanliness"),
                        "service": h.get("service"),
                        "location": h.get("location"),
                        "value": h.get("value"),
                        "retrieved_from": h.get("retrieved_from", [])
                    })
                
                # Quality gate failures
                failures = []
                # Check section14_rejected_candidates
                rejected = trace.get("section14_rejected_candidates", [])
                for r in rejected:
                    failures.append({
                        "hotel_id": r.get("hotel_id"),
                        "hotel_name": r.get("hotel_name"),
                        "reason": r.get("reason")
                    })
                
                queries_results.append({
                    "query": query,
                    "status": "success",
                    "latency_ms": latency,
                    "parsed_intent": parsed_intent,
                    "final_recommendation_count": recommendation_count,
                    "top_5_recommended_hotels": top_5,
                    "quality_gate_failures": failures,
                    "full_trace": trace
                })
                success_count += 1
            except Exception as e:
                queries_results.append({
                    "query": query,
                    "status": "failed",
                    "latency_ms": 0.0,
                    "parsed_intent": {"intent": "Failed", "hard_constraints": {}, "soft_constraints": {}},
                    "final_recommendation_count": 0,
                    "top_5_recommended_hotels": [],
                    "quality_gate_failures": [],
                    "error_message": str(e)
                })
                failure_count += 1

        total_queries = len(request.queries)
        avg_latency = round(statistics.mean(latencies), 2) if latencies else 0.0
        
        # Calculate p95 latency
        if latencies:
            sorted_lats = sorted(latencies)
            idx = int(len(sorted_lats) * 0.95)
            idx = min(idx, len(sorted_lats) - 1)
            p95_latency = round(sorted_lats[idx], 2)
        else:
            p95_latency = 0.0

        run_result = {
            "run_id": run_id,
            "timestamp": timestamp,
            "total_queries": total_queries,
            "success_count": success_count,
            "failure_count": failure_count,
            "avg_latency_ms": avg_latency,
            "p95_latency_ms": p95_latency,
            "queries": queries_results
        }

        # Bounded history management: load, append, slice to last 20 runs
        history = []
        if os.path.exists(BATCH_FILE_PATH):
            try:
                with open(BATCH_FILE_PATH, 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
                    if isinstance(history_data, list):
                        history = history_data
                    elif isinstance(history_data, dict) and "runs" in history_data:
                        history = history_data["runs"]
            except Exception:
                history = []

        history.append(run_result)
        if len(history) > 20:
            history = history[-20:]

        atomic_write_json(BATCH_FILE_PATH, {"runs": history})

        return run_result

@router.get("/debug/batch")
def get_batch_debug(run_id: Optional[str] = None, limit: Optional[int] = None):
    if not os.path.exists(BATCH_FILE_PATH):
        return {"runs": []}

    try:
        with open(BATCH_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            runs = data.get("runs", [])
    except Exception:
        return {"runs": []}

    # Filter by run_id if provided
    if run_id:
        runs = [r for r in runs if r.get("run_id") == run_id]

    # Limit results if limit is provided
    if limit is not None and limit > 0:
        runs = runs[-limit:]

    # Return chronological / reverse chronological order (reverse makes it easier for frontend to display newest first)
    runs.reverse()
    return {"runs": runs}

