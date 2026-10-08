from __future__ import annotations

from app.cache.redis_cache import ResponseCache
from app.config import Settings
from app.rag.bedrock import BedrockKnowledgeBaseClient
from app.rag.mock import query as mock_query


class RAGService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.cache = ResponseCache(settings.redis_url, settings.cache_enabled)
        self.bedrock = None
        if settings.rag_provider == "bedrock_kb":
            if not settings.bedrock_kb_id or not settings.bedrock_model_arn:
                raise ValueError("BEDROCK_KB_ID and BEDROCK_MODEL_ARN are required for bedrock_kb mode")
            self.bedrock = BedrockKnowledgeBaseClient(
                settings.bedrock_region,
                settings.bedrock_kb_id,
                settings.bedrock_model_arn,
            )

    def query(self, question: str, top_k: int = 5) -> dict:
        cached = self.cache.get(question, top_k, self.settings.prompt_version)
        if cached:
            return {**cached, "cached": True}

        if self.settings.rag_provider == "bedrock_kb":
            result = self.bedrock.query(question, top_k)
            provider = "amazon_bedrock_knowledge_base"
        else:
            result = mock_query(question, top_k)
            provider = "mock"

        result = {**result, "cached": False, "provider": provider}
        self.cache.set(question, top_k, self.settings.prompt_version, result)
        return result
