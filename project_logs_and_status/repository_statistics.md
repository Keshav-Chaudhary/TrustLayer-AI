# Repository Statistics

## Overview

* **Total Scripts**: 28
* **Total Datasets (CSV)**: 14
* **Total Reports (Markdown)**: 11
* **Total Notebooks (IPYNB)**: 10
* **Total Figures (PNG)**: 23
* **Total Images**: 3
* **Total Models (PKL)**: 4
* **Total Documentation Files**: 11
* **Total Lines of Code (estimate)**: ~5,500

## Directory Size Breakdown (Estimate)
* `data/raw/`: ~45% (Heavy text data from reviews)
* `data/processed/`: ~25% (Engineered features)
* `data/models/`: ~15% (Serialized model objects)
* `research/`: ~10% (Notebooks and figures)
* `scripts/`: ~5% (Python source code)

## File Type Breakdown
* **.csv**: 24.1%
* **.py**: 48.2%
* **.md**: 20.6%
* **.ipynb**: 17.2%
* **.png**: 44.8%
* **.pkl**: 6.8%
*(Note: Percentages map to relative counts, not sizes)*

## Largest Files
1. `data/raw/reviews/reviews_raw.csv`
2. `data/processed/cleaned/reviews_cleaned.csv`
3. `data/processed/features/review_features.csv`
4. `data/raw/synthetic_users/interactions_v2.csv`
5. `data/models/collaborative/model.pkl`

## Most Critical Files
* **Master Dataset**: `data/exports/final_hotel_dataset.csv`
* **Hybrid Engine**: `scripts/recommender/hybrid.py`
* **Explainer Logic**: `scripts/explainability/explainer.py`

## Repository Growth Summary
The repository has grown linearly through Stages 1-4 as data was acquired and transformed. Stage 5 and 6 saw rapid expansion in model artifacts and scripts. Stage 7 stabilized the codebase, focusing heavily on documentation, validation scripts, and generated analytical reports. Future stages (RAG, Dashboard) are expected to introduce new structural directories (e.g., `frontend/`, `api/`).
