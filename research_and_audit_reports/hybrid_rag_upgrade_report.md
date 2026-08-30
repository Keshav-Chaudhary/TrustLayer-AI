# Stage G: Hybrid RAG Architecture Upgrade

## Overview
The TrustLayer-AI backend has been successfully upgraded to a professional-grade Hybrid RAG architecture. This upgrade introduces robust LLM orchestration, precise context compression, strict provenance citation injection, and conversational streaming memory capabilities, satisfying the original vision of the project.

## Architectural Additions

### 1. `PromptOrchestrator`
- **Location**: `app/services/prompt_orchestrator.py`
- **Purpose**: Routes context through task-specific prompts. It maintains a centralized repository of grounding instructions to guarantee the LLM adheres to the provided context and injects required citations natively, separating prompt logic from the core retrieval loop.

### 2. `ContextCompressor`
- **Location**: `app/services/context_compressor.py`
- **Purpose**: A token-budget aware service that deduplicates redundant review chunks and enforces maximum context lengths (e.g., 1500 tokens). It strictly formats chunks with `[Chunk ID: XYZ]` markers so the PromptOrchestrator can instruct the LLM to output accurate citations.

### 3. `CitationInjector`
- **Location**: `app/services/citation_injector.py`
- **Purpose**: A post-processing utility that parses the raw LLM output, extracting and validating inline citations. It acts as the bridge to convert textual LLM responses into structured JSON arrays of `ProvenanceChunk` objects, ensuring the frontend can lazily load or render evidence without hallucinatory source mappings.

### 4. Conversational Streaming & `LLMService` Upgrades
- **Location**: `app/services/llm_service.py`
- **Purpose**: Added `async stream_generate` utilizing Python async generators (`yield`). This enables HTTP chunked streaming (which can later be adapted to Server-Sent Events) via FastAPI's `StreamingResponse`, eliminating long polling wait times for end users.

## New API Endpoints
- `POST /analyze`: Returns grounded AI analysis for a specific hotel ID.
- `POST /compare` (Upgraded): Now returns AI-generated objective comparisons based on vector retrieved chunks instead of raw data dumps.
- `GET /hotel/{id}/evidence`: Exposes raw provenance chunks to allow the frontend to lazy-load the "Provenance Drawer" independently.
- `GET /hotel/{id}/explanation`: Exposes the core analytical feature importance and exact score breakdowns from the Stage B metrics engine.
- `POST /chat`: RAG conversation interface utilizing the new `StreamingResponse`.

## Integration Flow
The pipeline now follows a strict pipeline:
1. `HybridRetriever` -> fetches chunks
2. `ContextCompressor` -> deduplicates and formats
3. `PromptOrchestrator` -> wraps in task grounding instructions
4. `LLMService` -> generates grounded response (sync or streaming)
5. `CitationInjector` -> maps outputs to valid provenance metadata
6. `GroundingValidator` -> final security layer stripping hallucinations.

The system is now fully aligned with a professional production Hybrid RAG environment.
