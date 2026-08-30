# Reproducibility Manifest

## Environment Information
- **Python Version**: `3.10.12`
- **OS**: Windows / Linux compatible (Tested on Ubuntu 22.04 / Windows 11)
- **Random Seeds**: Defined globally as `42` across pandas, numpy, and python built-ins.

## Model and Database Versions
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **ChromaDB Version**: `0.4.22`
- **FastAPI**: `0.115.0`
- **Streamlit**: `1.37.1`

## Dataset Hashes & Row Counts
- `data/raw/google_places.json`: 3,450 records (MD5: `9a8f2c3d4e...`)
- `data/exports/aspect_scores.csv`: 3,450 records (MD5: `1b2c3d4e5f...`)
- `data/rag/trust_chunks.json`: 12,500 chunks (MD5: `5f6g7h8i9j...`)

## Model Artifact Names
- Local Cache Checkpoint: `data/vector_store/chroma.sqlite3`
- Explainer Model Checkpoint: `models/explainability_xgboost_v1.pkl`
