from __future__ import annotations

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(min_length=3, max_length=4000)
    top_k: int = Field(default=5, ge=1, le=20)


class Citation(BaseModel):
    source: str
    score: float | None = None


class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation] = []
    cached: bool = False
    prompt_version: str
    provider: str
