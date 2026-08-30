import asyncio
import time
import uuid
import statistics
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, field_validator
from app.repositories.trace_repository import JsonTraceRepository
from app.config.config import settings

class BatchDebugRequest(BaseModel):
    queries: List[str]

    @field_validator("queries")
    @classmethod
    def validate_queries(cls, v: List[str]) -> List[str]:
        trimmed = [q.strip() for q in v if q and q.strip()]
        if not trimmed:
            raise ValueError("Query list cannot be empty or contain only blank queries.")
        if len(v) > settings.MAX_BATCH_QUERIES or len(trimmed) > settings.MAX_BATCH_QUERIES:
            raise ValueError(f"Query list exceeds maximum limit of {settings.MAX_BATCH_QUERIES} queries.")
        return trimmed


class DebugService:
    """
    Application Service responsible for trace generation and concurrent batch debug execution.
    """
    def __init__(self, trace_repo: Optional[JsonTraceRepository] = None):
        self.trace_repo = trace_repo or JsonTraceRepository()
        self.batch_lock = asyncio.Lock()

    def get_batch_history(self, run_id: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        return self.trace_repo.get_history(run_id=run_id, limit=limit)

    async def run_batch_debug(self, request: BatchDebugRequest, trace_provider: Any) -> Dict[str, Any]:
        if self.batch_lock.locked():
            raise RuntimeError("409 Conflict: A batch debug run is currently in progress.")

        async with self.batch_lock:
            run_id = str(uuid.uuid4())
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            queries_results = []
            latencies = []
            success_count = 0
            failure_count = 0

            for query in request.queries:
                await asyncio.sleep(0.005)
                try:
                    trace = trace_provider.get_debug_trace(query)
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

                    failures = []
                    for r in trace.get("section14_rejected_candidates", []):
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
                        "final_recommendation_count": len(final_ranking),
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

            avg_latency = round(statistics.mean(latencies), 2) if latencies else 0.0
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
                "total_queries": len(request.queries),
                "success_count": success_count,
                "failure_count": failure_count,
                "avg_latency_ms": avg_latency,
                "p95_latency_ms": p95_latency,
                "queries": queries_results
            }

            self.trace_repo.save_run(run_result)
            return run_result
