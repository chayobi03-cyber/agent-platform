"""Experiment driver: arms x tasks x weights, plus latency.

A benchmark supplies its task set and a scoring function; everything about how
those are evaluated and aggregated lives here so the next benchmark does not
reimplement it.
"""

from __future__ import annotations

import time
from typing import Callable, Iterable, Sequence

from .metrics import aggregate, complete, coverage, rank

# (task_id, class, query, required_evidence)
Task = tuple[str, str, str, list[str]]

# (query, arm, alpha, **overrides) -> {doc_id: score}
ScoreFn = Callable[..., dict[str, float]]


class Experiment:
    def __init__(self, tasks: Sequence[Task], score_fn: ScoreFn,
                 ks: Iterable[int] = (2, 3, 5), classes: Sequence[str] | None = None):
        self.tasks = list(tasks)
        self.score_fn = score_fn
        self.ks = tuple(ks)
        if classes is None:
            seen: list[str] = []
            for _, cls, _, _ in self.tasks:
                if cls not in seen:
                    seen.append(cls)
            classes = seen
        self.classes = tuple(classes)

    def evaluate(self, arm: str, alpha: float, **overrides) -> dict:
        per_task = {}
        for tid, cls, query, required in self.tasks:
            scores = self.score_fn(query, arm, alpha, **overrides)
            entry: dict = {"class": cls, "required": required}
            for k in self.ks:
                top = rank(scores, k)
                entry[f"top{k}"] = top
                entry[f"cov{k}"] = coverage(top, required)
                entry[f"complete{k}"] = complete(top, required)
            per_task[tid] = entry

        agg, by_class = aggregate(per_task, self.ks, self.classes)
        return {"aggregate": agg, "by_class": by_class, "per_task": per_task}

    def coverage_at(self, arm: str, alpha: float, k: int = 3, **overrides) -> float:
        """Single aggregate number — the form the null models compare."""
        return self.evaluate(arm, alpha, **overrides)["aggregate"][f"cov{k}"]

    def sweep(self, arms: Sequence[str], alphas: Sequence[float],
              k: int = 3) -> dict[str, dict[str, float]]:
        """Weight sensitivity: an effect that changes sign across weights is an
        artefact of the weight, not of the mechanism."""
        return {str(a): {arm: self.coverage_at(arm, a, k) for arm in arms}
                for a in alphas}

    def latency(self, arm: str, alpha: float, repeats: int = 20) -> float:
        """Mean wall-clock ms per query, including signal computation.

        Cost is part of the outcome, not overhead to be ignored: a mechanism
        that wins on quality but loses badly on latency has still failed the
        platform fitness test.
        """
        start = time.perf_counter()
        for _ in range(repeats):
            for _, _, query, _ in self.tasks:
                self.score_fn(query, arm, alpha)
        elapsed = time.perf_counter() - start
        return elapsed * 1000.0 / (repeats * len(self.tasks))
