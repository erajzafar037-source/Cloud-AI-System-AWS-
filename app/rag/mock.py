from __future__ import annotations


def query(question: str, top_k: int = 5) -> dict:
    return {
        "answer": (
            "Mock mode: configure RAG_PROVIDER=bedrock_kb for live retrieval. "
            f"Received question: {question}"
        ),
        "citations": [],
    }
