# EMBEDDING UPDATE POLICY

1. **Unchanged Hotels**: Vector documents in `embedding_documents` undergo zero recalculation.
2. **Updated Hotels**: Selective vector update (`sync_selective_vectors`) regenerates embeddings ONLY for modified chunk IDs using SentenceTransformer (`all-MiniLM-L6-v2`).
3. **New Hotels**: New vector chunks are encoded and appended to `embedding_documents`.
