"""Null models — the control that separates encoded structure from perturbation.

A mechanism arm that cannot beat its own null distribution is reordering
documents, not reasoning over structure. Each perturbation destroys the encoded
structure while preserving its statistical shape.

Determinism note: `null_distribution` seeds one generator and advances it
sequentially across all draws. Reseeding per draw, or changing the order of
random calls inside a perturbation, changes the resulting distribution — so
these functions preserve their call sequence exactly.
"""

from __future__ import annotations

import random
from typing import Callable


def permute_values(mapping: dict, rng: random.Random) -> dict:
    """Keep keys, shuffle values between them.

    Used for commit order (destroys chronology) and provenance text (destroys
    the document/provenance association).
    """
    ids = list(mapping)
    vals = [mapping[d] for d in ids]
    rng.shuffle(vals)
    return dict(zip(ids, vals))


def rewire_graph(graph: dict[str, dict[str, float]],
                 rng: random.Random) -> dict[str, dict[str, float]]:
    """Degree-preserving rewire: keep each row's out-degree and weight multiset,
    reassign the targets at random. Topology is destroyed, shape is not."""
    ids = list(graph)
    out = {}
    for a in ids:
        weights = list(graph[a].values())
        candidates = [x for x in ids if x != a]
        targets = rng.sample(candidates, len(weights))
        out[a] = dict(zip(targets, weights))
    return out


def null_distribution(evaluate: Callable[[random.Random], float],
                      seeds: int, seed: int) -> list[float]:
    """Sorted distribution of `seeds` perturbed evaluations.

    `evaluate` receives the shared generator and must perform its perturbation
    from it, so every draw advances one continuous random stream.
    """
    rng = random.Random(seed)
    out = [evaluate(rng) for _ in range(seeds)]
    return sorted(out)


def summarise(distribution: list[float], true_value: float,
              q: float = 0.95) -> dict:
    """Compare an arm's true score against its null distribution."""
    from .metrics import percentile

    threshold = percentile(distribution, q)
    below = sum(1 for v in distribution if v < true_value)
    return {
        "true": true_value,
        "null_mean": sum(distribution) / len(distribution),
        "null_p95": threshold,
        "null_min": distribution[0],
        "null_max": distribution[-1],
        "true_percentile": below / len(distribution),
        "passes_f3": bool(true_value > threshold),
        "distribution": distribution,
    }
