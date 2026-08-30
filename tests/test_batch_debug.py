from unittest.mock import patch
from fastapi.testclient import TestClient
from app.api.main import app
from app.api.routes import rec_service

client = TestClient(app)

@patch("app.api.routes.atomic_write_json", return_value=None)
def test_valid_small_batch(mock_write):
    # Test valid small batch of 2 queries
    payload = {"queries": ["luxury hotel in CP", "clean rooms in Delhi"]}
    response = client.post("/debug/batch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "run_id" in data
    assert data["total_queries"] == 2
    assert len(data["queries"]) == 2
    assert data["queries"][0]["status"] == "success"
    assert "top_5_recommended_hotels" in data["queries"][0]

@patch("app.api.routes.atomic_write_json", return_value=None)
def test_exactly_100_queries(mock_write):
    # Test exactly 100 queries
    queries = [f"query {i}" for i in range(100)]
    payload = {"queries": queries}
    # Mock get_debug_trace to run quickly
    mock_trace = {
        "section1_request_overview": {"total_execution_time_ms": 10.0},
        "section3_query_parser": {"intent": "Mocked", "hard_constraints": {}, "soft_constraints": {}},
        "section10_final_ranking": []
    }
    with patch.object(rec_service, "get_debug_trace", return_value=mock_trace):
        response = client.post("/debug/batch", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["total_queries"] == 100
        assert len(data["queries"]) == 100

def test_101_queries_rejection():
    # Test 101 queries (exceeds 100 limit)
    queries = [f"query {i}" for i in range(101)]
    payload = {"queries": queries}
    response = client.post("/debug/batch", json=payload)
    assert response.status_code == 422  # Unprocessable Entity for validation error

def test_empty_list_rejection():
    # Test empty list rejection
    response = client.post("/debug/batch", json={"queries": []})
    assert response.status_code == 422

    # Test only blank queries
    response = client.post("/debug/batch", json={"queries": ["  ", ""]})
    assert response.status_code == 422

@patch("app.api.routes.atomic_write_json", return_value=None)
def test_partial_failure_handling(mock_write):
    # Test batch with one failing query
    payload = {"queries": ["good hotel", "FAIL_QUERY", "cheap hotel"]}
    
    original_get_debug_trace = rec_service.get_debug_trace
    
    def side_effect(query):
        if query == "FAIL_QUERY":
            raise ValueError("Intentional debug trace failure")
        return {
            "section1_request_overview": {"total_execution_time_ms": 15.0},
            "section3_query_parser": {"intent": "Mocked", "hard_constraints": {}, "soft_constraints": {}},
            "section10_final_ranking": []
        }

    with patch.object(rec_service, "get_debug_trace", side_effect=side_effect):
        response = client.post("/debug/batch", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["total_queries"] == 3
        assert data["success_count"] == 2
        assert data["failure_count"] == 1
        
        results = data["queries"]
        assert results[0]["status"] == "success"
        assert results[1]["status"] == "failed"
        assert "Intentional debug trace failure" in results[1]["error_message"]
        assert results[2]["status"] == "success"

def test_get_batch_history():
    response = client.get("/debug/batch")
    assert response.status_code == 200
    data = response.json()
    assert "runs" in data
    assert isinstance(data["runs"], list)
