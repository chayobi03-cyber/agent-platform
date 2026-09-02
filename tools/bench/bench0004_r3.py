#!/usr/bin/env python3
"""BENCH-0004 Round 3 - retrieval mechanism decomposition.

Implements the conditions frozen in
docs/research/executions/BENCH-0004_R3_PREDECLARATION.md.

This module holds only what is specific to BENCH-0004 Round 3: the frozen
corpus, the frozen task set, the cue lists, the three mechanism signals and the
arm definitions. Everything about how those are indexed, evaluated, perturbed
and reported lives in `tools/apfbench/`.

Deterministic given the frozen corpus commit and the fixed seed, and dependent
on nothing outside the standard library, so an independent reviewer can replay
it without installing anything.

Usage:
    python3 tools/bench/bench0004_r3.py [--out results.json]
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))

from apfbench import corpus, nulls, report  # noqa: E402
from apfbench.runner import Experiment  # noqa: E402
from apfbench.text import TfIdf, minmax, tokenize  # noqa: E402

FROZEN_COMMIT = "0d2776986d742eb8e9443a2dc9a95bcc3374efbb"
ALPHA_PRIMARY = 0.5
ALPHA_SWEEP = [0.25, 0.5, 1.0]
NULL_SEEDS = 200
SEED = 20260902

# --------------------------------------------------------------------------
# Frozen corpus (predeclaration section 3)
# --------------------------------------------------------------------------

CORPUS = {
    "README": "README.md",
    "CONSTITUTION": "CONSTITUTION.md",
    "ARCH": "docs/architecture/README.md",
    "DECISIONS": "docs/decisions/README.md",
    "HOTL": "docs/governance/HOTL_GOVERNANCE.md",
    "LESSONS": "docs/governance/LESSONS_LEARNED_2026-08-30-engineering-work-mvp.md",
    "MASTER": "docs/governance/MASTER_SESSION_PROMPT.md",
    "NEXT_UX": "docs/handoff/NEXT_SESSION_PROMPT_ENGINEERING_WORK_UX.md",
    "SESSION_STATE": "docs/handoff/SESSION_STATE.md",
    "LEDGER": "docs/research/ASSET_LEDGER.md",
    "COLD_REVIEW": "docs/research/CLAIM_COLD_REVIEW.md",
    "CLAIM_INVENTORY": "docs/research/CLAIM_INVENTORY.md",
    "RECONCILIATION": "docs/research/CLAIM_RECONCILIATION.md",
    "FB_DESIGN": "docs/research/FALSIFICATION_BENCHMARK.md",
    "BENCH_CASES": "docs/research/P0_BENCHMARK_CASES_v0.1.md",
    "P0_MATRIX": "docs/research/P0_FALSIFICATION_BENCHMARK_MATRIX.md",
    "CORPUS_MAP": "docs/research/RESEARCH_CORPUS_MAP.md",
    "TRACE_MAP": "docs/research/RESEARCH_TO_CLAIM_MAP.md",
    "RECON_STATUS": "docs/research/RESEARCH_TO_CLAIM_RECONCILIATION_STATUS.md",
    "EXEC_R1": "docs/research/executions/BENCH-0004_RUN_2026-08-31.md",
    "EXEC_R2": "docs/research/executions/BENCH-0004_R2_2026-08-31.md",
}

# --------------------------------------------------------------------------
# Frozen task set (predeclaration section 5)
# --------------------------------------------------------------------------

TASKS = [
    ("N1", "NEUTRAL",
     "What fields are required in a minimum APF decision record?",
     ["DECISIONS"]),
    ("N2", "NEUTRAL",
     "What does the asset record template contain and what adoption values are allowed?",
     ["LEDGER"]),
    ("N3", "NEUTRAL",
     "Which entities are listed in the candidate domain model of the architecture workspace?",
     ["ARCH"]),
    ("N4", "NEUTRAL",
     "What is explicitly avoided in the capture-first engineering UX session?",
     ["NEXT_UX"]),
    ("R1", "RELATION",
     "Which benchmark tests the temporal/provenance-aware retrieval claim, and what did its first execution conclude?",
     ["CLAIM_INVENTORY", "BENCH_CASES", "EXEC_R1"]),
    ("R2", "RELATION",
     "Which claim does the provenance ablation benchmark test, and how was that claim's wording narrowed?",
     ["BENCH_CASES", "COLD_REVIEW", "CLAIM_INVENTORY"]),
    ("R3", "RELATION",
     "Which research lesson motivated the structured-retrieval claim, and which benchmark family tests it?",
     ["LESSONS", "CLAIM_INVENTORY", "FB_DESIGN"]),
    ("R4", "RELATION",
     "Which explicit relations link a research asset to a claim, a benchmark and evidence?",
     ["TRACE_MAP", "RECONCILIATION"]),
    ("T1", "TEMPORAL",
     "What did the first retrieval ablation conclude, and what did the second round change about that conclusion?",
     ["EXEC_R1", "EXEC_R2"]),
    ("T2", "TEMPORAL",
     "Which limitation of the first round motivated the cross-document task design of the second round?",
     ["EXEC_R1", "EXEC_R2"]),
    ("T3", "TEMPORAL",
     "What is the declared benchmark execution order, and which benchmarks have execution records so far?",
     ["BENCH_CASES", "EXEC_R1", "EXEC_R2"]),
    ("T4", "TEMPORAL",
     "What was the claim state before benchmarking and what is its state after the second round?",
     ["CLAIM_INVENTORY", "EXEC_R2", "SESSION_STATE"]),
    ("P1", "PROVENANCE",
     "Which benchmark documents are marked design-ready but not executed, and which are marked executed pilot results?",
     ["BENCH_CASES", "EXEC_R1", "EXEC_R2"]),
    ("P2", "PROVENANCE",
     "What is the current corpus reconciliation status and what is its declared exit criterion?",
     ["RECON_STATUS", "CORPUS_MAP"]),
    ("P3", "PROVENANCE",
     "Which provenance fields must engineering evidence retain, and which claim formalises that requirement?",
     ["LESSONS", "CLAIM_INVENTORY"]),
    ("P4", "PROVENANCE",
     "What is the constitution's version and status, and how many architecture decisions does the session state record?",
     ["CONSTITUTION", "SESSION_STATE"]),
]

CLASSES = ("NEUTRAL", "RELATION", "TEMPORAL", "PROVENANCE")

# Cue lists frozen in predeclaration section 4.1. Not extensible post-hoc.
TEMPORAL_CUES = {
    "first", "second", "initial", "latest", "prior", "previous", "before",
    "after", "then", "next", "changed", "change", "round", "order",
    "sequence", "so", "far", "already", "subsequent", "earlier", "later",
    "updated", "current",
}
PROVENANCE_CUES = {
    "status", "version", "date", "executed", "design-ready", "marked",
    "current", "state", "provenance", "scope", "purpose", "complete",
    "partial", "pilot",
}

# --------------------------------------------------------------------------
# Arms (predeclaration section 4)
# --------------------------------------------------------------------------

ARMS = ["B", "C", "D1", "D2", "D3", "D4"]
BASELINE = "C"

# Which mechanisms each D arm activates.
ARM_SIGNALS: dict[str, frozenset[str]] = {
    "D1": frozenset({"temporal"}),
    "D2": frozenset({"relationship"}),
    "D3": frozenset({"provenance"}),
    "D4": frozenset({"temporal", "relationship", "provenance"}),
}

# Fixed application order. Addition is commutative but floating-point addition
# is not associative, so this order is part of the frozen specification: change
# it and the recorded results shift in their last bits.
SIGNAL_ORDER = ("relationship", "temporal", "provenance")


# --------------------------------------------------------------------------
# Mechanism signals (predeclaration section 4.1)
# --------------------------------------------------------------------------

def relationship_signal(base_c, graph):
    """One-step score propagation across the derived graph."""
    rel = {d: sum(w * base_c[nb] for nb, w in graph[d].items()) for d in base_c}
    return minmax(rel)


def temporal_signal(query, base_c, order):
    """Cue-gated recency plus commit-adjacency to the top-1 document."""
    if not (set(tokenize(query)) & TEMPORAL_CUES):
        return {d: 0.0 for d in base_c}
    recency = minmax({d: float(order[d][1]) for d in base_c})
    top1 = max(base_c, key=lambda d: base_c[d])
    ref = order[top1][1]
    max_span = max(abs(order[d][1] - ref) for d in base_c) or 1
    adjacency = {d: 1.0 - abs(order[d][1] - ref) / max_span for d in base_c}
    return {d: (recency[d] + adjacency[d]) / 2.0 for d in base_c}


def provenance_signal(query, prov_index):
    """Cue-gated cosine against extracted provenance fields."""
    if not (set(tokenize(query)) & PROVENANCE_CUES):
        return {d: 0.0 for d in prov_index.ids}
    return prov_index.score(query)


# --------------------------------------------------------------------------

class Retriever:
    """Holds the indexes and derived structure for the frozen corpus."""

    def __init__(self):
        self.bodies = corpus.load_frozen_corpus(REPO, FROZEN_COMMIT, CORPUS)
        self.body_index = TfIdf(self.bodies)
        self.meta_index = TfIdf({
            d: corpus.extract_metadata_text(b, CORPUS[d])
            for d, b in self.bodies.items()
        })
        self.prov_texts = {d: corpus.extract_provenance_text(b)
                           for d, b in self.bodies.items()}
        self.prov_index = TfIdf(self.prov_texts)
        self.graph = corpus.derive_relationship_graph(self.bodies, CORPUS)
        self.order = corpus.git_commit_order(REPO, FROZEN_COMMIT, CORPUS)

    def score_c(self, query: str, alpha: float) -> dict[str, float]:
        """Semantic + metadata. The required BENCH-0004 control for an
        improvement explained by better indexing alone."""
        b = self.body_index.score(query)
        m = self.meta_index.score(query)
        return {d: b[d] + alpha * m[d] for d in b}

    def score(self, query: str, arm: str, alpha: float,
              graph=None, order=None, prov_index=None,
              normalise_prov: bool = False) -> dict[str, float]:
        graph = self.graph if graph is None else graph
        order = self.order if order is None else order
        prov_index = self.prov_index if prov_index is None else prov_index

        if arm == "B":
            return self.body_index.score(query)

        c = self.score_c(query, alpha)
        if arm == "C":
            return c

        active = ARM_SIGNALS[arm]
        out = dict(c)
        for mechanism in SIGNAL_ORDER:
            if mechanism not in active:
                continue
            if mechanism == "relationship":
                sig = relationship_signal(c, graph)
            elif mechanism == "temporal":
                sig = temporal_signal(query, c, order)
            else:
                sig = provenance_signal(query, prov_index)
                if normalise_prov and any(v > 0 for v in sig.values()):
                    sig = minmax(sig)
            for d in out:
                out[d] += alpha * sig[d]
        return out


def null_arm(experiment: Experiment, retriever: Retriever,
             arm: str, alpha: float, rng: random.Random) -> float:
    """One perturbed draw for `arm`, taken from the shared random stream."""
    if arm == "D2":
        kw = {"graph": nulls.rewire_graph(retriever.graph, rng)}
    elif arm == "D1":
        kw = {"order": nulls.permute_values(retriever.order, rng)}
    elif arm == "D3":
        kw = {"prov_index": TfIdf(nulls.permute_values(retriever.prov_texts, rng))}
    else:
        raise ValueError(f"no null model defined for arm {arm}")
    return experiment.coverage_at(arm, alpha, 3, **kw)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="bench0004_r3_results.json")
    args = ap.parse_args()

    retriever = Retriever()
    experiment = Experiment(TASKS, retriever.score, ks=(2, 3, 5), classes=CLASSES)

    results: dict = {
        "frozen_commit": FROZEN_COMMIT,
        "alpha_primary": ALPHA_PRIMARY,
        "seed": SEED,
        "null_seeds": NULL_SEEDS,
        "corpus_size": len(CORPUS),
        "task_count": len(TASKS),
        # Derived structure, exposed so a reviewer can inspect what the
        # mechanisms actually saw.
        "graph_edges": {a: dict(sorted(nb.items(), key=lambda kv: -kv[1]))
                        for a, nb in retriever.graph.items()},
        "commit_order": {d: list(v) for d, v in retriever.order.items()},
        "provenance_text": retriever.prov_texts,
    }

    print(f"corpus: {len(CORPUS)} docs | tasks: {len(TASKS)} | alpha={ALPHA_PRIMARY}")
    print(f"derived relationship edges: {sum(len(v) for v in retriever.graph.values())}")

    results["primary"] = {arm: experiment.evaluate(arm, ALPHA_PRIMARY) for arm in ARMS}

    print("\n=== PRIMARY (alpha=0.5) mean chain coverage ===")
    report.print_primary(results["primary"], ARMS, BASELINE)

    print("\n=== PER CLASS (cov@3, delta vs C) ===")
    report.print_by_class(results["primary"], ARMS, CLASSES, BASELINE)

    results["alpha_sweep"] = experiment.sweep(ARMS, ALPHA_SWEEP)
    print("\n=== ALPHA SWEEP (cov@3, delta vs C at same alpha) ===")
    report.print_sweep(results["alpha_sweep"], ARMS, ALPHA_SWEEP, BASELINE)

    print(f"\n=== NULL MODELS ({NULL_SEEDS} seeds, cov@3) ===")
    results["null_models"] = {}
    for arm in ("D1", "D2", "D3"):
        dist = nulls.null_distribution(
            lambda rng, a=arm: null_arm(experiment, retriever, a, ALPHA_PRIMARY, rng),
            NULL_SEEDS, SEED)
        results["null_models"][arm] = nulls.summarise(
            dist, results["primary"][arm]["aggregate"]["cov3"])
    report.print_nulls(results["null_models"])

    results["latency_ms_per_query"] = {
        arm: experiment.latency(arm, ALPHA_PRIMARY) for arm in ARMS}
    print("\n=== LATENCY (ms/query) ===")
    report.print_latency(results["latency_ms_per_query"], ARMS, BASELINE)

    # Declared sensitivity check: the predeclaration specified the provenance
    # signal as a raw cosine while the other two are min-max normalised.
    results["deviation_normalised_provenance"] = {
        arm: experiment.coverage_at(arm, ALPHA_PRIMARY, 3, normalise_prov=True)
        for arm in ("D3", "D4")
    }
    base3 = results["primary"][BASELINE]["aggregate"]["cov3"]
    print("\n=== SENSITIVITY: min-max normalised provenance signal (cov@3) ===")
    for arm, v in results["deviation_normalised_provenance"].items():
        print(f"{arm:<5}{v:>9.4f}  (delta vs C {v - base3:+.4f})")

    out_path = report.write_json(Path(args.out), results)
    print(f"\nraw results -> {out_path}")


if __name__ == "__main__":
    main()
