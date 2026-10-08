from __future__ import annotations

from fastapi import FastAPI, HTTPException

from app.config import settings
from app.rag.service import RAGService
from app.schemas import QueryRequest, QueryResponse

app = FastAPI(title="Cloud AI Serverless AWS", version="1.0.0")
service = RAGService(settings)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "env": settings.app_env, "provider": settings.rag_provider}


@app.post("/query", response_model=QueryResponse)
def query(payload: QueryRequest) -> QueryResponse:
    try:
        result = service.query(payload.query, payload.top_k)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return QueryResponse(
        answer=result["answer"],
        citations=result.get("citations", []),
        cached=result.get("cached", False),
        prompt_version=settings.prompt_version,
        provider=result["provider"],
    )
