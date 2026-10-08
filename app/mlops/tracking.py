from __future__ import annotations

import os


def log_experiment(metrics: dict[str, float], params: dict[str, str] | None = None) -> None:
    """Best-effort MLflow logging so local evaluation still works without MLflow server."""
    try:
        import mlflow
    except ImportError:
        return

    uri = os.getenv("MLFLOW_TRACKING_URI")
    if uri:
        mlflow.set_tracking_uri(uri)
    with mlflow.start_run():
        if params:
            mlflow.log_params(params)
        mlflow.log_metrics({k: float(v) for k, v in metrics.items() if isinstance(v, (int, float))})
