from __future__ import annotations

import argparse
import statistics
import time

import httpx


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--n", type=int, default=20)
    parser.add_argument("--query", default="What is the incident response policy?")
    args = parser.parse_args()

    latencies = []
    with httpx.Client(timeout=30) as client:
        for _ in range(args.n):
            start = time.perf_counter()
            response = client.post(
                args.url.rstrip("/") + "/query",
                json={"query": args.query},
            )
            response.raise_for_status()
            latencies.append((time.perf_counter() - start) * 1000)

    latencies.sort()
    p50 = statistics.median(latencies)
    p95 = latencies[min(len(latencies) - 1, int(len(latencies) * 0.95))]
    print(f"p50_ms={p50:.2f}")
    print(f"p95_ms={p95:.2f}")


if __name__ == "__main__":
    main()
