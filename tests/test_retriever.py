def test_retriever():
    import os
    from scripts.rag.retriever import HybridRetriever
    
    vector_dir = "data/vector_store"
    # only test if dir exists
    if os.path.exists(vector_dir):
        retriever = HybridRetriever(vector_dir)
        results, fallback_level = retriever.retrieve("Delhi", {}, {})
        assert isinstance(results, list)
        assert isinstance(fallback_level, int)
