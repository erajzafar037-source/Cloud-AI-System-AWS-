from app.config import Settings
from app.mlops.evaluator import token_overlap
from app.rag.service import RAGService
from app.schemas import QueryRequest


def test_mock_query():
    service = RAGService(Settings(rag_provider="mock"))
    result = service.query("hello world")
    assert result["provider"] == "mock"
    assert "hello world" in result["answer"]


def test_token_overlap():
    assert token_overlap("incident response plan", "incident response plan") == 1.0
    assert token_overlap("abc", "xyz") == 0.0


def test_schema_validation():
    request = QueryRequest(query="What is RAG?", top_k=3)
    assert request.top_k == 3
