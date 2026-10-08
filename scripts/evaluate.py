from __future__ import annotations

import argparse

from app.config import settings
from app.mlops.evaluator import evaluate, load_jsonl
from app.mlops.tracking import log_experiment
from app.rag.service import RAGService


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--log-mlflow", action="store_true")
    args = parser.parse_args()

    service = RAGService(settings)
    rows = []
    for item in load_jsonl(args.dataset):
        result = service.query(item["question"], top_k=5)
        rows.append({**item, "prediction": result["answer"]})

    metrics = evaluate(rows)
    print(metrics)
    if args.log_mlflow:
        log_experiment(metrics, {"prompt_version": settings.prompt_version, "provider": settings.rag_provider})


if __name__ == "__main__":
    main()
