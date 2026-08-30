# Final Project Audit

## 1. Folder Inventory
Total files scanned: 1818
Python files: 56

## 2. File Purpose Mapping
- `app/api/`: FastAPI orchestration
- `scripts/rag/`: Retrieval and context assembly
- `scripts/evaluation/`: Metric generation

## 3. Dependency Graph
- `app/services/recommendation_service.py` -> `scripts/rag/retriever.py`, `scripts/rag/query_parser.py`

## 4. Dead-code Candidates
- scripts/synthetic/old_generator.py

## 5. Orphaned Scripts
None detected. All scripts in `scripts/rag/` and `app/` are reachable from `main.py` or `evaluate_stage_d.py`.

## 6. Unused Imports
- import requests in app/api/routes.py

## 7. Model Artifact Usage
- Embedding Model: `all-MiniLM-L6-v2` (Actively used in `retriever.py`)

## 8. Vector Store Usage
- `data/vector_store`: Actively queried by `HybridRetriever`.

## 9. API Route Usage
- `POST /recommend`: Active (Used by Streamlit)
- `POST /chat`: Active
- `GET /health`: Active
