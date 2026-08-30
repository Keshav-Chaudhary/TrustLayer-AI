def test_query_parser():
    # Simple mock test to represent regression testing for parser
    from scripts.rag.query_parser import QueryParser
    parser = QueryParser()
    result = parser.parse("Luxury hotel in Delhi")
    assert "hard" in result
    assert "soft" in result
    assert isinstance(result["hard"], dict)
