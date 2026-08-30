import hashlib
import time
from typing import Optional, Any

class CacheService:
    def __init__(self):
        self._cache = {}
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            item = self._cache[key]
            if time.time() < item['expires_at']:
                self.hits += 1
                return item['data']
            else:
                del self._cache[key]
        self.misses += 1
        return None

    def set(self, key: str, data: Any, ttl_seconds: int = 3600):
        self._cache[key] = {
            'data': data,
            'expires_at': time.time() + ttl_seconds
        }
        
    def generate_key(self, prefix: str, data_dict: dict) -> str:
        dict_str = str(sorted(data_dict.items()))
        hash_obj = hashlib.md5(dict_str.encode())
        return f"{prefix}_{hash_obj.hexdigest()}"
        
    def get_hit_rate(self) -> float:
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return self.hits / total

cache_service = CacheService()
