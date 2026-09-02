"""apfbench — reusable falsification-benchmark infrastructure for APF.

Extracted from the BENCH-0004 Round 3 harness so that later benchmarks
(BENCH-0006 onward) reuse the evaluation machinery instead of copying it.

The split is deliberate:

    apfbench/          how a benchmark is measured   (generic, reusable)
    tools/bench/*.py   what a benchmark measures     (per-benchmark definition)

A benchmark module supplies its corpus, task set, arms and scoring function.
Everything else — indexing, ranking, coverage metrics, null models, weight
sweeps, latency, reporting — lives here.

Standard library only, by design: a falsification harness that needs an
install step is one an independent reviewer will not rerun.
"""

from __future__ import annotations

__all__ = ["corpus", "metrics", "nulls", "report", "runner", "text"]
