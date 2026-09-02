"""Retrieval metrics for evidence-chain benchmarks.

Chain coverage is deliberately stricter than document recall: when an answer
depends on a historical chain, retrieving one relevant document is not success.
"""

from __future__ import annotations

import math


def rank(scores: dict[str, float], k: int) -> list[str]:
    """Top-k document ids, ties broken deterministically on the id."""
    return [d for d, _ in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))][:k]


def coverage(retrieved: list[str], required: list[str]) -> float:
    """Fraction of required evidence documents present in the retrieved set."""
    return len(set(retrieved) & set(required)) / len(required)


def complete(retrieved: list[str], required: list[str]) -> float:
    """1.0 only when every required document is present."""
    return float(set(required) <= set(retrieved))


def aggregate(per_task: dict[str, dict], ks, classes) -> tuple[dict, dict]:
    """Mean coverage/completeness overall and per task class."""
    n = len(per_task)
    agg = {}
    for k in ks:
        agg[f"cov{k}"] = sum(t[f"cov{k}"] for t in per_task.values()) / n
        agg[f"complete{k}"] = sum(t[f"complete{k}"] for t in per_task.values()) / n

    by_class = {}
    for cls in classes:
        rows = [t for t in per_task.values() if t["class"] == cls]
        if not rows:
            continue
        by_class[cls] = {f"cov{k}": sum(r[f"cov{k}"] for r in rows) / len(rows)
                         for k in ks}
    return agg, by_class


def percentile(sorted_vals: list[float], q: float) -> float:
    """Linear-interpolated percentile of an already-sorted list."""
    if not sorted_vals:
        return float("nan")
    pos = q * (len(sorted_vals) - 1)
    lo, hi = int(math.floor(pos)), int(math.ceil(pos))
    if lo == hi:
        return sorted_vals[lo]
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (pos - lo)
