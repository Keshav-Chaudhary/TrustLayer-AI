# Stage F: Repository State Audit

## 1. Folder Inventory
- **Complete directory tree:**
  - `data/`: Contains `vector_store`, `raw`, `exports`, `rag`.
  - `docs/`: Architecture documentation and reproducibility manifest.
  - `scripts/`: Contains `rag`, `evaluation`, `synthetic`, `explainability`, `recommender`, `smoke_test.py`, etc.
  - `tests/`: Automated tests.
  - `research/`: Reports and notebooks.
  - `log/`: System logs.
- **Total files:** Approx 45 (excluding vector store artifacts).
- **Python files:** Approx 30.
- **TypeScript files:** 0 (Frontend not yet initialized).
- **Configuration files:** `.env`, `.env.example`, `docker-compose.yml`, `Dockerfile`, `requirements.txt`.

## 2. Existing Assets Still Available
- **`scripts/rag/*`**: Fully intact (`query_parser.py`, `retriever.py`, `context_builder.py`, `index_store.py`).
- **`scripts/evaluation/*`**: Intact (`evaluate_stage_d.py`, etc.).
- **`data/vector_store/*`**: Intact (ChromaDB artifacts).
- **`models/*`**: Intact (Pickle files, etc. if any).
- **`research/reports/*`**: Intact (`stage_d_evaluation.md`, `ui_verification.md`, `final_project_audit.md`, etc.).
- **`tests/*`**: Intact (`test_api_endpoints.py`, `test_grounding_validator.py`, etc. - some are orphaned).
- **`docs/*`**: Intact (`architecture_overview.md`, `data_flow.md`, `api_contract.md`, `reproducibility_manifest.md`).
- **`frontend/*`**: NOT PRESENT.

## 3. Dependency Traceability
- **`scripts/rag/query_parser.py`**:
  - *Purpose*: Parses natural language into constraint dicts.
  - *Status*: **ACTIVE**
- **`scripts/rag/retriever.py`**:
  - *Purpose*: Queries ChromaDB vector store.
  - *Status*: **ACTIVE**
- **`scripts/rag/context_builder.py`**:
  - *Purpose*: Assembles retrieved chunks into context window.
  - *Status*: **ACTIVE**
- **`scripts/evaluation/evaluate_stage_d.py`**:
  - *Purpose*: Evaluates end-to-end performance.
  - *Status*: **ACTIVE**

## 4. Backend Recovery Assessment
| File | Missing | Can Be Recovered | Existing Dependency |
|---|---|---|---|
| `main.py` | Yes | Yes (Rewrite) | `FastAPI` |
| `routes.py` | Yes | Yes (Rewrite) | `RecommendationService` |
| `response_models.py` | Yes | Yes (Rewrite) | `Pydantic` |
| `recommendation_service.py` | Yes | Yes (Rewrite) | `query_parser`, `retriever`, `context_builder` |
| `grounding_validator.py` | Yes | Yes (Rewrite) | None |
| `cache_service.py` | Yes | Yes (Rewrite) | None |

## 5. Dead Code Verification
- **Unused scripts**: `scripts/smoke_test.py` (Broken imports due to missing `app/`). Status: **CANDIDATE FOR ARCHIVE/REWRITE**.
- **Unused tests**: `tests/test_api_endpoints.py`, `tests/test_grounding_validator.py` (Broken imports). Status: **CANDIDATE FOR ARCHIVE/REWRITE**.
- **Unused reports**: None. Status: **SAFE TO KEEP**.
- **Unused assets**: Old Streamlit configurations inside `docker-compose.yml`. Status: **CANDIDATE FOR ARCHIVE/REWRITE**.

## 6. Frontend Recovery Assessment
- **Existing frontend code**: None (`streamlit_app.py` and `app/ui/` were deleted).
- **Classification**: **Must Rebuild** completely using Next.js 14.
