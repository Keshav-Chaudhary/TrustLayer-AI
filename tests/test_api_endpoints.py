from unittest.mock import patch
from fastapi.testclient import TestClient
from app.api.main import app
from app.services.llm_service import LLMService

def mock_generate(self, prompt: str, injected_chunk_id: str = "", format: str = None, num_predict: int = 768) -> str:
    if format == "json":
        return "{}"
    return "Mocked response"

async def mock_stream_generate(self, prompt: str, injected_chunk_id: str = ""):
    yield "Mocked "
    yield "chat "
    yield "response"

LLMService.generate = mock_generate
LLMService.stream_generate = mock_stream_generate

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_recommend():
    response = client.post("/recommend", json={"query": "test"})
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert "trace_id" in data

def test_chat():
    response = client.post("/chat", json={"query": "hello"})
    assert response.status_code == 200
    assert len(response.text) > 0
