import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(name: str, method: str, path: str, payload: dict = None, is_stream: bool = False):
    print(f"\n--- Testing {name} ---")
    url = f"{BASE_URL}{path}"
    try:
        if method == "GET":
            res = requests.get(url)
        else:
            res = requests.post(url, json=payload, stream=is_stream)
            
        print(f"Status Code: {res.status_code}")
        if res.status_code != 200:
            print("Error Details:", res.text)
            return None
            
        if is_stream:
            content = ""
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    content += chunk.decode('utf-8')
            print("Stream Output:", content)
            return content
        else:
            data = res.json()
            print("JSON Output:", str(data)[:500] + "..." if len(str(data)) > 500 else data)
            return data
    except requests.exceptions.RequestException as e:
        print(f"Connection Error: {e}")
        return None

def verify_api():
    print("Starting API Verification Suite...")
    
    test_endpoint("Health", "GET", "/health")
    test_endpoint("Metrics", "GET", "/metrics")
    
    rec_data = test_endpoint("Recommend", "POST", "/recommend", {"query": "clean hotels in Delhi"})
    
    hotel_id = None
    if rec_data and rec_data.get("recommendations"):
        hotel_id = rec_data["recommendations"][0]["hotel_id"]
        
    if not hotel_id:
        print("\n[!] No hotel_id retrieved from /recommend, skipping specific endpoints.")
        return
        
    test_endpoint("Analyze", "POST", "/analyze", {"hotel_id": hotel_id, "query": "Is it good?"})
    test_endpoint("Compare", "POST", "/compare", {"hotel_ids": [hotel_id, hotel_id]})
    test_endpoint("Evidence", "GET", f"/hotel/{hotel_id}/evidence")
    test_endpoint("Explanation", "GET", f"/hotel/{hotel_id}/explanation")
    test_endpoint("Chat Stream", "POST", "/chat", {"query": "tell me more", "hotel_id": hotel_id}, is_stream=True)
    
if __name__ == "__main__":
    verify_api()
