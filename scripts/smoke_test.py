import sys
import os

def run_smoke_test():
    print("Starting TrustLayer-AI Smoke Test...")
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    # 1. Test FastAPI import and instantiation
    try:
        from app.api.main import app
        print("[OK] FastAPI application instantiated.")
    except Exception as e:
        print(f"[FAIL] FastAPI failed to load: {e}")
        sys.exit(1)
        
    # 2. Test Vector Store loading (if exists)
    try:
        from scripts.rag.retriever import HybridRetriever
        vector_dir = "data/vector_store"
        if os.path.exists(vector_dir):
            retriever = HybridRetriever(vector_dir)
            print("[OK] Vector Store loaded successfully.")
        else:
            print("[SKIP] Vector store directory not found, skipping load test.")
    except Exception as e:
        print(f"[FAIL] Vector Store failed to load: {e}")
        sys.exit(1)
        
    # 3. Test API logic using TestClient
    from fastapi.testclient import TestClient
    client = TestClient(app)
    
    try:
        resp = client.get("/health")
        assert resp.status_code == 200
        print("[OK] /health returned 200.")
    except Exception as e:
        print(f"[FAIL] /health failed: {e}")
        sys.exit(1)
        
    try:
        resp = client.post("/recommend", json={"query": "A test query for luxury hotels"})
        assert resp.status_code == 200
        data = resp.json()
        assert len(data.get("recommendations", [])) > 0
        print("[OK] /recommend returned at least one recommendation.")
    except Exception as e:
        print(f"[FAIL] /recommend failed: {e}")
        sys.exit(1)
        
    # 4. Test Grounding Validator
    try:
        from app.services.grounding_validator import GroundingValidator
        validator = GroundingValidator()
        res = validator.validate_response("Some claim with a pool", [], "Hotel")
        assert res["is_valid"] is False
        print("[OK] Grounding Validator active and correctly rejecting ungrounded claims.")
    except Exception as e:
        print(f"[FAIL] Grounding Validator failed: {e}")
        sys.exit(1)

    print("\n--- ALL SMOKE TESTS PASSED ---")

if __name__ == "__main__":
    run_smoke_test()
