def test_context_builder():
    from scripts.rag.context_builder import ContextBuilder
    builder = ContextBuilder(max_tokens=2000)
    mock_results = [{"id": "1", "document": "A nice hotel.", "metadata": {"chunk_type": "Chunk B", "hotel_id": "h1"}}]
    context_str, audit = builder.build_context(mock_results)
    assert "A nice hotel" in context_str
    assert "compression_ratio" in audit
