from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def token_overlap(a: str, b: str) -> float:
    left, right = _tokens(a), _tokens(b)
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def evaluate(records: Iterable[dict]) -> dict[str, float]:
    rows = list(records)
    if not rows:
        return {"answer_similarity": 0.0, "count": 0}

    scores = []
    for row in rows:
        scores.append(token_overlap(row["reference_answer"], row["prediction"]))
    return {"answer_similarity": sum(scores) / len(scores), "count": len(rows)}


def load_jsonl(path: str | Path):
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)
