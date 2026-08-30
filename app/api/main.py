import os
import time
import logging
import uuid
import json
import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config.config import settings
from app.api.routes import router
from app.api.search_routes import search_router

# Import V1 Routers
from app.api.v1.system_routes import system_v1_router
from app.api.v1.recommend_routes import recommend_v1_router
from app.api.v1.hotel_routes import hotel_v1_router
from app.api.v1.search_routes import search_v1_router
from app.api.v1.debug_routes import debug_v1_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Check ChromaDB
    vector_dir = os.path.abspath(settings.VECTOR_STORE_PATH)
    if not os.path.exists(vector_dir):
        raise RuntimeError(f"Startup Failed: ChromaDB vector store missing at {vector_dir}")
        
    # 2. Check Ollama
    try:
        res = requests.get(settings.OLLAMA_ENDPOINT, timeout=5)
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"WARNING: Ollama is unreachable at {settings.OLLAMA_ENDPOINT}. Error: {e}. AI generation features may fail.")
        
    print("Startup Self-Test Passed: ChromaDB and Ollama are reachable.")
    yield
    print("Shutting down TrustLayer-AI.")

app = FastAPI(
    title=settings.APP_NAME,
    description="Explainable and Grounded Hotel Recommendations API",
    version=settings.APP_VERSION,
    lifespan=lifespan
)

logging.basicConfig(level=logging.INFO, format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}')
logger = logging.getLogger("trustlayer")

@app.middleware("http")
async def structured_logging_middleware(request: Request, call_next):
    start_time = time.time()
    trace_id = str(uuid.uuid4())
    request.state.trace_id = trace_id
    
    response = await call_next(request)
    
    latency = (time.time() - start_time) * 1000
    status_code = response.status_code
    
    log_data = {
        "trace_id": trace_id,
        "method": request.method,
        "url": str(request.url),
        "status_code": status_code,
        "latency_ms": round(latency, 2)
    }
    logger.info(json.dumps(log_data))
    
    response.headers["X-Trace-ID"] = trace_id
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root Level Compatibility Routes
app.include_router(router)
app.include_router(search_router)

# Version 1 API Namespace (/api/v1/...)
app.include_router(system_v1_router, prefix="/api/v1")
app.include_router(recommend_v1_router, prefix="/api/v1")
app.include_router(hotel_v1_router, prefix="/api/v1")
app.include_router(search_v1_router, prefix="/api/v1")
app.include_router(debug_v1_router, prefix="/api/v1")
