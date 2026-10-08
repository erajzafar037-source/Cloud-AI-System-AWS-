from __future__ import annotations

import hashlib
import json

try:
    from redis import Redis
except ImportError:  # pragma: no cover
    Redis = None


class ResponseCache:
    def __init__(self, url: str, enabled: bool = False, ttl_seconds: int = 300):
        self.enabled = enabled and Redis is not None
        self.ttl_seconds = ttl_seconds
        self.client = Redis.from_url(url, decode_responses=True) if self.enabled else None

    @staticmethod
    def key(query: str, top_k: int, prompt_version: str) -> str:
        raw = f"{prompt_version}:{top_k}:{query}".encode()
        return "rag:" + hashlib.sha256(raw).hexdigest()

    def get(self, query: str, top_k: int, prompt_version: str):
        if not self.enabled:
            return None
        value = self.client.get(self.key(query, top_k, prompt_version))
        return json.loads(value) if value else None

    def set(self, query: str, top_k: int, prompt_version: str, value: dict):
        if self.enabled:
            self.client.setex(self.key(query, top_k, prompt_version), self.ttl_seconds, json.dumps(value))
