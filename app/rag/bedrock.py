from __future__ import annotations

from typing import Any

import boto3


class BedrockKnowledgeBaseClient:
    """Thin adapter around Bedrock Agent Runtime retrieve-and-generate."""

    def __init__(self, region: str, knowledge_base_id: str, model_arn: str):
        self.client = boto3.client("bedrock-agent-runtime", region_name=region)
        self.knowledge_base_id = knowledge_base_id
        self.model_arn = model_arn

    def query(self, question: str, top_k: int = 5) -> dict[str, Any]:
        response = self.client.retrieve_and_generate(
            input={"text": question},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": self.knowledge_base_id,
                    "modelArn": self.model_arn,
                    "retrievalConfiguration": {
                        "vectorSearchConfiguration": {"numberOfResults": top_k}
                    },
                },
            },
        )
        citations = []
        for item in response.get("citations", []):
            for ref in item.get("retrievedReferences", []):
                location = ref.get("location", {})
                uri = (
                    location.get("s3Location", {}).get("uri")
                    or location.get("webLocation", {}).get("url")
                    or "unknown"
                )
                citations.append({"source": uri, "score": ref.get("score")})
        return {"answer": response.get("output", {}).get("text", ""), "citations": citations}
