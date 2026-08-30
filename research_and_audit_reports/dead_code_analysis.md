# Dead Code & Orphan Detection Analysis

## Overview
This report identifies scripts, historical reports, and temporary validation files that are not strictly required for the final production pipeline (Stage D) but exist for reproducibility or documentation purposes.

**IMPORTANT:** No files have been deleted. This is purely an analytical classification.

## File Classification

### `scripts/synthetic/`
| File | Classification | Meaning |
|---|---|---|
| `generate_interactions_v2.py` | HISTORICAL | Used to bootstrap interaction data initially. Not needed during runtime. |

### `scripts/recommender/`
| File | Classification | Meaning |
|---|---|---|
| `hybrid.py` | ACTIVE | Required logic for `hybrid_model.pkl`. |
| `baseline.py` | ORPHANED | Replaced by `hybrid.py`. |
| `collaborative.py` | ORPHANED | Replaced by `hybrid.py`. |
| `content_based.py` | ORPHANED | Replaced by `hybrid.py`. |
| `engineer_features.py` | HISTORICAL | Used for EDA/training prep. |
| `generate_interactions.py`| ORPHANED | Superseded by v2 script in synthetic folder. |
| `generate_users.py` | HISTORICAL | Used for synthetic interaction generation. |
| `merge_dataset.py` | HISTORICAL | Data prep script. |

### `scripts/explainability/`
| File | Classification | Meaning |
|---|---|---|
| `explainer.py` | ACTIVE | Core logic for RRF decomposition. |
| `audit_explainability_b1.py`| VALIDATION ONLY | Audits the explainer fidelity. |
| `evaluate_explanations.py` | VALIDATION ONLY | Generates metrics on explanations. |

### `scripts/rag/`
| File | Classification | Meaning |
|---|---|---|
| `retriever.py` | ACTIVE | Core hybrid retrieval logic. |
| `context_builder.py` | ACTIVE | Context assembly and token management. |
| `query_parser.py` | ACTIVE | Parses natural language constraints. |
| `build_vector_store.py` | HISTORICAL | Executed once to build vector DB. |
| `build_hotel_documents.py`| HISTORICAL | Executed once to build chunks. |
| `evaluate_retrieval.py` | VALIDATION ONLY | Evaluates retriever metrics. |
| `validate_retriever_step1.py`| VALIDATION ONLY | Temporary step 1 validation. |
| `audit_hotel_documents.py` | VALIDATION ONLY | Auditing tool. |
| `audit_aspect_distribution.py`| VALIDATION ONLY | Auditing tool. |
| `audit_review_evidence.py` | VALIDATION ONLY | Auditing tool. |
| `generate_benchmark.py` | HISTORICAL | Generated `retrieval_queries.json`. |

### `research/reports/` and `research/notebooks/`
All markdown reports (e.g., `retrieval_evaluation.md`, `recommender_evaluation.md`) and `.ipynb` files are classified as **HISTORICAL** or **VALIDATION ONLY**. They exist for reference but are never executed during runtime.

## Summary
Most "orphaned" or "historical" code exists within `scripts/recommender/` where older baseline models were created and superseded by `hybrid.py`.
