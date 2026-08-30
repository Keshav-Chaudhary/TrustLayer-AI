# STAGE 27 — ORCHESTRATION GAP ANALYSIS

## Executive Summary
Stage 26 fully automated downstream ingestion from the canonical dataset (`final_hotel_dataset.csv`) to PostgreSQL 17 and `embedding_documents`.

However, **the upstream pipeline (Google Places API fetch -> Clean -> NLP sentiment/ABSA -> Feature Engineering -> Merge to `final_hotel_dataset.csv`) is currently executed via standalone scripts rather than a single unified CLI orchestrator.**

---

## Identified Orchestration Gaps

| Upstream Pipeline Stage | Current Implementation Status | Gap / Required Orchestration |
|---|---|---|
| **1. Source Acquisition** | Standalone API scripts | Needs unified error handling and environment API key check. |
| **2. Cleaning & Normalization** | Standalone Python scripts | Needs automatic intermediate directory staging (`data/sources/raw/`, `data/sources/normalized/`). |
| **3. NLP Sentiment & ABSA** | Standalone PyTorch/Transformers scripts | Needs model caching and stage-level execution flags (`--skip-nlp`). |
| **4. Feature Engineering** | Standalone pandas script | Needs validation checks before merge. |
| **5. Merge Engine** | Standalone script (`merge_dataset.py`) | Needs direct connection to Stage 26 `pipeline.py dry-run`. |
| **6. One-Command CLI Runner** | Not yet created | Requires `scripts/orchestrator.py` to trigger all 6 stages sequentially. |
