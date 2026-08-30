# Full Project Audit Report

## 1. Full Folder Inventory

| Folder | Purpose | Key Files | Used By | Dead Code Risk | Recommendation |
|---|---|---|---|---|---|
| `data/` | Root for all datasets and databases | N/A | All Stages | Low | Keep |
| `data/raw/` | Raw scraped data | Scraped JSON files | Data Cleaning | Low | Keep |
| `data/exports/` | Unified processed datasets | `final_hotel_dataset.csv` | Stage A, Stage C | Low | Keep |
| `data/rag/` | Segmented JSON chunks for embeddings | `ChIJ*.json` | Stage C | Low | Keep |
| `data/vector_store/` | ChromaDB vector database | ChromaDB files | Stage C.4, Stage D | Low | Keep |
| `data/models/` | Trained recommender models | `hybrid/model.pkl` | Stage B, Stage D | Medium | Keep Hybrid, Archive others |
| `scripts/synthetic/` | Synthetic interaction generators | `generate_interactions_v2.py` | Stage A | High | Archive Candidate (Historical) |
| `scripts/recommender/` | Recommendation modeling | `hybrid.py`, `baseline.py` | Stage A | Medium | Keep Hybrid logic, Archive rest |
| `scripts/explainability/` | Stage B explanation logic | `explainer.py` | Stage D | Low | Keep |
| `scripts/rag/` | RAG components and evaluation | `retriever.py`, `context_builder.py` | Stage C.4, Stage D | Low | Keep Core, Archive Audits |
| `research/reports/` | Markdown audit reports | `retrieval_evaluation.md` | Audit/Validation | Low | Keep (Historical) |
| `research/notebooks/` | Jupyter notebooks for EDA | `08_final_dataset_overview.ipynb`| Documentation | High | Keep (Historical) |
| `research/evaluation/` | Benchmark query datasets | `retrieval_queries.json` | Stage C.4 | Low | Keep |

## 2. Pipeline Dependency Graph

`data/raw/google_places/` + `data/raw/reviews/`
⬇
`scripts/recommender/merge_dataset.py` + `engineer_features.py`
⬇
`data/exports/final_hotel_dataset.csv`
⬇
`data/exports/final_hotel_dataset.csv` + `scripts/synthetic/generate_interactions_v2.py`
⬇
`interactions.csv`
⬇
`scripts/recommender/hybrid.py`
⬇
`data/models/hybrid/model.pkl`
⬇
`data/models/hybrid/model.pkl` + `data/exports/final_hotel_dataset.csv` + `scripts/explainability/explainer.py`
⬇
*Stage B Explanations*
⬇
`data/exports/final_hotel_dataset.csv` + `scripts/rag/build_hotel_documents.py`
⬇
`data/rag/` (Hotel Chunk JSONs)
⬇
`scripts/rag/build_vector_store.py`
⬇
`data/vector_store/` (ChromaDB)
⬇
`scripts/rag/query_parser.py` + `scripts/rag/retriever.py` + `scripts/rag/context_builder.py`
⬇
**Stage D (Answer Generation Pipeline)**

## 3. Stage-by-Stage Audit

### Stage A – Recommendation System
| Field | Description |
|---|---|
| Current Status | Complete |
| Core Deliverables | User interactions, CF/CB/Hybrid models, RRF |
| Files Consumed Later | `data/models/hybrid/model.pkl` |
| Audit Result | PASS |

### Stage B – Explainability
| Field | Description |
|---|---|
| Current Status | Complete |
| Core Deliverables | Explainer class, metadata structuring, fidelity audit |
| Files Consumed Later | `scripts/explainability/explainer.py` |
| Audit Result | PASS |

### Stage C – RAG Pipeline
| Field | Description |
|---|---|
| Current Status | Complete |
| Core Deliverables | Vector store, Hybrid Retriever, Context Builder, Evaluations |
| Files Consumed Later | `data/vector_store/`, `retriever.py`, `context_builder.py`, `query_parser.py` |
| Audit Result | PASS |
