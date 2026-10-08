# Architecture notes

The design separates the synchronous **question-answering path** from the asynchronous **document/MLOps path**.

## Synchronous path

Client -> API Gateway -> Lambda orchestrator -> optional Redis cache -> Amazon Bedrock Knowledge Base -> answer + citations.

## Asynchronous path

S3 document upload -> EventBridge object event -> SQS -> ingestion worker. This keeps document processing out of the user request path and provides a queue boundary for retries/DLQ.

## MLOps path

Golden evaluation dataset -> evaluator -> MLflow run -> versioned prompt/model configuration. Promotion should be governed by evaluation thresholds instead of changing production prompts/models blindly.
