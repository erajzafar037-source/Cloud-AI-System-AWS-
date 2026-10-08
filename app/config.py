from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_env: str = os.getenv("APP_ENV", "local")
    rag_provider: str = os.getenv("RAG_PROVIDER", "mock")
    bedrock_region: str = os.getenv("BEDROCK_REGION", "eu-central-1")
    bedrock_kb_id: str | None = os.getenv("BEDROCK_KB_ID") or None
    bedrock_model_arn: str | None = os.getenv("BEDROCK_MODEL_ARN") or None
    cache_enabled: bool = os.getenv("CACHE_ENABLED", "false").lower() == "true"
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    prompt_version: str = os.getenv("PROMPT_VERSION", "v1")
    mlflow_tracking_uri: str = os.getenv("MLFLOW_TRACKING_URI", "")


settings = Settings()
