import os
import json
import asyncio
import requests
import aiohttp
from typing import Dict, Any, AsyncGenerator

class LLMService:
    def __init__(self):
        self.endpoint = os.environ.get("OLLAMA_ENDPOINT", "http://127.0.0.1:11434")
        self.model = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")
        
    def generate(self, prompt: str, injected_chunk_id: str = "", format: str = None, num_predict: int = 768) -> str:
        """
        Synchronous generation via Ollama REST API.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "keep_alive": "10m",
            "options": {
                "temperature": 0.1,
                "num_predict": num_predict
            }
        }
        if format:
            payload["format"] = format
            
        try:
            response = requests.post(f"{self.endpoint}/api/generate", json=payload, timeout=120)
            response.raise_for_status()
            res_json = response.json()
            return res_json.get("response", "").strip()
        except requests.exceptions.RequestException as e:
            raise Exception(f"503 Service Unavailable: Ollama API is down or unreachable. Error: {e}")
        
    async def stream_generate(self, prompt: str, injected_chunk_id: str = "") -> AsyncGenerator[str, None]:
        """
        Asynchronous chunked streaming generation via Ollama.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": 0.1
            }
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=120)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(f"{self.endpoint}/api/generate", json=payload) as response:
                    if response.status != 200:
                        raise Exception(f"503 Service Unavailable: Ollama streaming failed with status {response.status}")
                        
                    async for line in response.content:
                        if line:
                            decoded = json.loads(line.decode('utf-8'))
                            yield decoded.get("response", "")
        except asyncio.TimeoutError:
            raise Exception("503 Service Unavailable: Ollama streaming timed out.")
        except aiohttp.ClientError as e:
            raise Exception(f"503 Service Unavailable: Ollama streaming connection failed. Error: {e}")
