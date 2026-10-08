# LinkedIn showcase post

🚀 I upgraded my AWS Cloud AI project into a flagship **LLM/RAG + MLOps + Cloud AI** platform.

Instead of treating AI as a notebook or a single API call, I designed the system around an enterprise production flow:

- Amazon Bedrock Knowledge Base for managed RAG
- Lambda + API Gateway for serverless inference
- Redis for response caching
- S3 → EventBridge → SQS for event-driven document workflows
- MLflow-based evaluation for answer quality and experiment tracking
- Versioned prompts/model configuration
- Terraform Infrastructure as Code
- CloudWatch logging and GitHub Actions CI
- Automated benchmark for measured p50/p95 latency

The strongest part is the connection between AI and engineering: **retrieval quality, prompt/model versioning, reproducibility, cloud infrastructure, observability and CI all live in one repository.**

I am deliberately not claiming a latency number before measuring the deployed AWS endpoint. The repo includes the benchmark needed to produce a defensible metric.

GitHub: https://github.com/erajzafar037-source/cloud-ai-serverless-aws

#AI #LLM #RAG #MLOps #AWS #AmazonBedrock #CloudEngineering #Python #Terraform #Serverless #DevOps #MachineLearning
