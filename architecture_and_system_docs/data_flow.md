# TrustLayer-AI Data Flow

## 1. Data Ingestion & Indexing
1. **Raw Google Places JSON** -> `data/raw/`
2. **Explainer Pipeline** -> Generates aspect scores, synthetic reviews, and structured profiles.
3. **Vector Store Ingestion** -> `scripts/rag/index_store.py` chunks data and embeds via `all-MiniLM-L6-v2`. Stored in ChromaDB (`data/vector_store`).

## 2. Recommendation Flow
1. **User Query** -> `Streamlit` -> `FastAPI /recommend`
2. **Parser** -> Extracts `{area: 'Delhi', budget: 'Luxury'}`.
3. **Retriever** -> Queries ChromaDB using hard/soft constraints with defined fallback levels (0-3). Returns `top_k` chunks.
4. **Context Builder** -> Formats chunks into an injected string payload.
5. **LLM Generation** -> The prompt strictly limits the LLM to context facts.
6. **Grounding Validation** -> Checks LLM response against raw chunks. If unsupported claims exist, strips them.
7. **Response Delivery** -> JSON with `recommendations`, `metadata`, and `trace_id` sent to UI.
