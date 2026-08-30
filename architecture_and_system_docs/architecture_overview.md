# TrustLayer-AI Architecture Overview

## Introduction
TrustLayer-AI is an end-to-end framework that integrates large language models (LLMs) with grounded retrieval-augmented generation (RAG) to provide trustworthy, explainable hotel recommendations.

## Core Components
1. **API Layer (`app/api/`)**: FastAPI routing handling queries and chats.
2. **Services Layer (`app/services/`)**: Orchestration of prompts, LLMs, caching, and validation.
3. **RAG Pipeline (`scripts/rag/`)**: 
   - **Query Parser**: Extracts hard constraints (e.g. area, budget) and soft constraints.
   - **Hybrid Retriever**: Retrieves relevant hotel profiles, aspect scores, and review evidence chunks using semantic and metadata search via ChromaDB.
   - **Context Builder**: Assembles structured context for the LLM.
4. **Validation Layer (`app/services/grounding_validator.py`)**: Intercepts LLM hallucinations and enforces strict adherence to retrieved provenance chunks.

## Interaction
The `RecommendationService` coordinates all modules, ensuring high modularity and testability. Streamlit serves as the frontend client.
