from __future__ import annotations

import json
import os

import boto3


client = boto3.client("bedrock-agent-runtime", region_name=os.getenv("BEDROCK_REGION", "eu-central-1"))


def _query_bedrock(question: str, top_k: int = 5) -> dict:
    kb_id = os.getenv("BEDROCK_KB_ID")
    model_arn = os.getenv("BEDROCK_MODEL_ARN")
    if not kb_id or not model_arn:
        raise ValueError("BEDROCK_KB_ID and BEDROCK_MODEL_ARN must be configured")

    response = client.retrieve_and_generate(
        input={"text": question},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": kb_id,
                "modelArn": model_arn,
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

    return {
        "answer": response.get("output", {}).get("text", ""),
        "citations": citations,
        "cached": False,
        "provider": "amazon_bedrock_knowledge_base",
    }


def _response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body),
    }


def handler(event, context):
    try:
        raw_body = event.get("body") or "{}"
        payload = json.loads(raw_body) if isinstance(raw_body, str) else raw_body
        question = str(payload.get("query", "")).strip()
        if len(question) < 3:
            return _response(400, {"error": "query must be at least 3 characters"})
        top_k = min(max(int(payload.get("top_k", 5)), 1), 20)
        return _response(200, _query_bedrock(question, top_k))
    except Exception as exc:
        return _response(502, {"error": str(exc)})
