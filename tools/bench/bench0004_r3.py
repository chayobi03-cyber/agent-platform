#!/usr/bin/env python3
"""BENCH-0004 Round 3 - retrieval mechanism decomposition harness.

Implements the conditions frozen in
docs/research/executions/BENCH-0004_R3_PREDECLARATION.md.

Dependency-free (Python standard library only) and deterministic given the
frozen corpus commit and the fixed seed, so an independent reviewer can
reproduce the numbers without installing anything.

Usage:
    python3 tools/bench/bench0004_r3.py [--out results.json]
"""

from __future__ import annotations

import argparse
import json
import math
import random
import re
import subprocess
import time
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

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

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "does", "do", "for",
    "from", "has", "have", "how", "in", "is", "it", "its", "of", "on", "or",
    "that", "the", "this", "to", "was", "were", "what", "when", "where",
    "which", "who", "why", "with", "many", "much", "not", "but", "if",
}

TOKEN_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
IDENT_RE = re.compile(r"\b(?:CLM-\d+[a-c]?|BENCH-\d+|FB-\d+|ASSET-[A-Z0-9*]+|HP-\d+)\b")
META_FIELD_RE = re.compile(r"^\*\*(?:Status|Date|Scope|Purpose|Target claim|Session):\*\*.*$",
                           re.MULTILINE)
VERSION_RE = re.compile(r"v\d+\.\d+")
H1_RE = re.compile(r"^#\s+(.*)$", re.MULTILINE)


def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOPWORDS]


# --------------------------------------------------------------------------
# TF-IDF (predeclaration section 4)
# --------------------------------------------------------------------------

class TfIdf:
    """tf = 1 + log(count), idf = log(N/df) + 1, L2-normalised cosine."""

    def __init__(self, docs: dict[str, str]):
        self.ids = list(docs)
        self.tokens = {d: tokenize(docs[d]) for d in self.ids}
        n = len(self.ids)
        df: dict[str, int] = defaultdict(int)
        for d in self.ids:
            for term in set(self.tokens[d]):
                df[term] += 1
        self.idf = {t: math.log(n / df[t]) + 1.0 for t in df}
        self.vectors = {d: self._vec(self.tokens[d]) for d in self.ids}

    def _vec(self, tokens: list[str]) -> dict[str, float]:
        counts: dict[str, int] = defaultdict(int)
        for t in tokens:
            counts[t] += 1
        vec = {}
        for t, c in counts.items():
            if t in self.idf:
                vec[t] = (1.0 + math.log(c)) * self.idf[t]
        norm = math.sqrt(sum(v * v for v in vec.values()))
        if norm > 0:
            for t in vec:
                vec[t] /= norm
        return vec

    def score(self, query: str) -> dict[str, float]:
        q = self._vec(tokenize(query))
        out = {}
        for d in self.ids:
            dv = self.vectors[d]
            if len(q) < len(dv):
                out[d] = sum(w * dv.get(t, 0.0) for t, w in q.items())
            else:
                out[d] = sum(w * q.get(t, 0.0) for t, w in dv.items())
        return out


def minmax(scores: dict[str, float]) -> dict[str, float]:
    vals = list(scores.values())
    lo, hi = min(vals), max(vals)
    if hi - lo < 1e-12:
        return {k: 0.0 for k in scores}
    return {k: (v - lo) / (hi - lo) for k, v in scores.items()}


# --------------------------------------------------------------------------
# Corpus features
# --------------------------------------------------------------------------

def load_corpus() -> dict[str, str]:
    """Read each document at FROZEN_COMMIT rather than from the working tree.

    Corpus documents are ordinary repository files and keep changing after the
    benchmark runs. Reading them from the frozen commit is what makes the
    recorded numbers reproducible at any later HEAD.
    """
    out = {}
    for doc_id, path in CORPUS.items():
        out[doc_id] = subprocess.run(
            ["git", "show", f"{FROZEN_COMMIT}:{path}"],
            cwd=REPO, capture_output=True, text=True, check=True,
        ).stdout
    return out


def metadata_text(doc_id: str, body: str) -> str:
    parts = []
    h1 = H1_RE.search(body)
    if h1:
        parts.append(h1.group(1))
    parts.extend(META_FIELD_RE.findall(body))
    path = CORPUS[doc_id]
    parts.append(" ".join(re.split(r"[/_\-.]", path.replace(".md", ""))))
    return "\n".join(parts)


def provenance_text(doc_id: str, body: str) -> str:
    parts = list(META_FIELD_RE.findall(body))
    parts.extend(VERSION_RE.findall(body))
    return "\n".join(parts)


def build_relationship_graph(bodies: dict[str, str]) -> dict[str, dict[str, float]]:
    """Mechanically derived edges: filename mentions + shared identifiers.

    No operator discretion; this is the Round 3 repair of Round 2's
    hand-specified graph.
    """
    ids = list(bodies)

    # Mention strings. A bare basename is only usable when it is unambiguous
    # across the corpus (README.md appears three times, so those documents can
    # only be matched on their full path).
    basename_counts: dict[str, int] = defaultdict(int)
    for d in ids:
        basename_counts[Path(CORPUS[d]).stem] += 1

    mention_keys: dict[str, list[str]] = {}
    for d in ids:
        path = CORPUS[d]
        keys = [path, Path(path).name]
        stem = Path(path).stem
        if basename_counts[stem] == 1:
            keys.append(stem)
        mention_keys[d] = keys

    idents = {d: set(IDENT_RE.findall(bodies[d])) for d in ids}

    graph: dict[str, dict[str, float]] = {d: {} for d in ids}
    for a in ids:
        for b in ids:
            if a == b:
                continue
            w = 0.0
            if any(k in bodies[a] for k in mention_keys[b]):
                w += 1.0
            union = idents[a] | idents[b]
            if union:
                w += len(idents[a] & idents[b]) / len(union)
            if w > 0:
                graph[a][b] = w

    # Row normalisation.
    for a in ids:
        total = sum(graph[a].values())
        if total > 0:
            for b in graph[a]:
                graph[a][b] /= total
    return graph


def git_commit_order() -> dict[str, tuple[int, int]]:
    """(first_commit_index, last_commit_index) per document, oldest commit = 0."""
    out = subprocess.run(
        ["git", "log", "--reverse", "--format=@%H", "--name-only", FROZEN_COMMIT],
        cwd=REPO, capture_output=True, text=True, check=True,
    ).stdout
    path_to_id = {p: d for d, p in CORPUS.items()}
    first: dict[str, int] = {}
    last: dict[str, int] = {}
    idx = -1
    for line in out.splitlines():
        if line.startswith("@"):
            idx += 1
        elif line.strip() in path_to_id:
            doc = path_to_id[line.strip()]
            first.setdefault(doc, idx)
            last[doc] = idx
    return {d: (first.get(d, 0), last.get(d, 0)) for d in CORPUS}


# --------------------------------------------------------------------------
# Mechanism signals (predeclaration section 4.1)
# --------------------------------------------------------------------------

def relationship_signal(base_c: dict[str, float],
                        graph: dict[str, dict[str, float]]) -> dict[str, float]:
    rel = {d: sum(w * base_c[nb] for nb, w in graph[d].items()) for d in base_c}
    return minmax(rel)


def temporal_signal(query: str, base_c: dict[str, float],
                    order: dict[str, tuple[int, int]]) -> dict[str, float]:
    if not (set(tokenize(query)) & TEMPORAL_CUES):
        return {d: 0.0 for d in base_c}
    recency = minmax({d: float(order[d][1]) for d in base_c})
    top1 = max(base_c, key=lambda d: base_c[d])
    ref = order[top1][1]
    spans = [abs(order[d][1] - ref) for d in base_c]
    max_span = max(spans) or 1
    adjacency = {d: 1.0 - abs(order[d][1] - ref) / max_span for d in base_c}
    return {d: (recency[d] + adjacency[d]) / 2.0 for d in base_c}


def provenance_signal(query: str, prov_index: TfIdf) -> dict[str, float]:
    if not (set(tokenize(query)) & PROVENANCE_CUES):
        return {d: 0.0 for d in prov_index.ids}
    return prov_index.score(query)


# --------------------------------------------------------------------------
# Scoring / metrics
# --------------------------------------------------------------------------

def rank(scores: dict[str, float], k: int) -> list[str]:
    # Deterministic tie-break on document id.
    return [d for d, _ in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))][:k]


def coverage(retrieved: list[str], required: list[str]) -> float:
    return len(set(retrieved) & set(required)) / len(required)


class Engine:
    def __init__(self):
        self.bodies = load_corpus()
        self.body_index = TfIdf(self.bodies)
        self.meta_index = TfIdf({d: metadata_text(d, b) for d, b in self.bodies.items()})
        self.prov_texts = {d: provenance_text(d, b) for d, b in self.bodies.items()}
        self.prov_index = TfIdf(self.prov_texts)
        self.graph = build_relationship_graph(self.bodies)
        self.order = git_commit_order()

    def score_c(self, query: str, alpha: float) -> dict[str, float]:
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

        use_t = arm in ("D1", "D4")
        use_r = arm in ("D2", "D4")
        use_p = arm in ("D3", "D4")

        out = dict(c)
        if use_r:
            sig = relationship_signal(c, graph)
            for d in out:
                out[d] += alpha * sig[d]
        if use_t:
            sig = temporal_signal(query, c, order)
            for d in out:
                out[d] += alpha * sig[d]
        if use_p:
            sig = provenance_signal(query, prov_index)
            if normalise_prov and any(v > 0 for v in sig.values()):
                sig = minmax(sig)
            for d in out:
                out[d] += alpha * sig[d]
        return out

    def evaluate(self, arm: str, alpha: float, ks=(2, 3, 5), **kw) -> dict:
        per_task = {}
        for tid, cls, q, required in TASKS:
            scores = self.score(q, arm, alpha, **kw)
            entry = {"class": cls, "required": required}
            for k in ks:
                top = rank(scores, k)
                entry[f"top{k}"] = top
                entry[f"cov{k}"] = coverage(top, required)
                entry[f"complete{k}"] = float(set(required) <= set(top))
            per_task[tid] = entry

        agg = {}
        for k in ks:
            agg[f"cov{k}"] = sum(t[f"cov{k}"] for t in per_task.values()) / len(per_task)
            agg[f"complete{k}"] = sum(t[f"complete{k}"] for t in per_task.values()) / len(per_task)
        by_class = {}
        for cls in ("NEUTRAL", "RELATION", "TEMPORAL", "PROVENANCE"):
            rows = [t for t in per_task.values() if t["class"] == cls]
            by_class[cls] = {f"cov{k}": sum(r[f"cov{k}"] for r in rows) / len(rows) for k in ks}
        return {"aggregate": agg, "by_class": by_class, "per_task": per_task}


# --------------------------------------------------------------------------
# Null models (predeclaration section 4.2)
# --------------------------------------------------------------------------

def shuffled_graph(graph: dict[str, dict[str, float]], rng: random.Random):
    """Degree-preserving rewire: keep out-degree and weight multiset per row,
    reassign targets at random."""
    ids = list(graph)
    out = {}
    for a in ids:
        weights = list(graph[a].values())
        candidates = [x for x in ids if x != a]
        targets = rng.sample(candidates, len(weights))
        out[a] = dict(zip(targets, weights))
    return out


def shuffled_order(order: dict[str, tuple[int, int]], rng: random.Random):
    ids = list(order)
    vals = [order[d] for d in ids]
    rng.shuffle(vals)
    return dict(zip(ids, vals))


def shuffled_prov(prov_texts: dict[str, str], rng: random.Random) -> TfIdf:
    ids = list(prov_texts)
    vals = [prov_texts[d] for d in ids]
    rng.shuffle(vals)
    return TfIdf(dict(zip(ids, vals)))


def null_distribution(engine: Engine, arm: str, alpha: float, seeds: int) -> list[float]:
    rng = random.Random(SEED)
    out = []
    for _ in range(seeds):
        if arm == "D2":
            kw = {"graph": shuffled_graph(engine.graph, rng)}
        elif arm == "D1":
            kw = {"order": shuffled_order(engine.order, rng)}
        elif arm == "D3":
            kw = {"prov_index": shuffled_prov(engine.prov_texts, rng)}
        else:
            raise ValueError(arm)
        out.append(engine.evaluate(arm, alpha, **kw)["aggregate"]["cov3"])
    return sorted(out)


def percentile(sorted_vals: list[float], q: float) -> float:
    if not sorted_vals:
        return float("nan")
    pos = q * (len(sorted_vals) - 1)
    lo, hi = int(math.floor(pos)), int(math.ceil(pos))
    if lo == hi:
        return sorted_vals[lo]
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (pos - lo)


def measure_latency(engine: Engine, arm: str, alpha: float, repeats: int = 20) -> float:
    """Mean wall-clock ms per query, including signal computation."""
    start = time.perf_counter()
    for _ in range(repeats):
        for _, _, q, _ in TASKS:
            engine.score(q, arm, alpha)
    total = time.perf_counter() - start
    return total * 1000.0 / (repeats * len(TASKS))


# --------------------------------------------------------------------------

ARMS = ["B", "C", "D1", "D2", "D3", "D4"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="bench0004_r3_results.json")
    args = ap.parse_args()

    engine = Engine()
    results: dict = {
        "frozen_commit": FROZEN_COMMIT,
        "alpha_primary": ALPHA_PRIMARY,
        "seed": SEED,
        "null_seeds": NULL_SEEDS,
        "corpus_size": len(CORPUS),
        "task_count": len(TASKS),
    }

    # Corpus feature summary, so a reviewer can inspect the derived structure.
    results["graph_edges"] = {a: dict(sorted(nb.items(), key=lambda kv: -kv[1]))
                              for a, nb in engine.graph.items()}
    results["commit_order"] = {d: list(v) for d, v in engine.order.items()}
    results["provenance_text"] = engine.prov_texts

    print(f"corpus: {len(CORPUS)} docs | tasks: {len(TASKS)} | alpha={ALPHA_PRIMARY}")
    edge_count = sum(len(v) for v in engine.graph.values())
    print(f"derived relationship edges: {edge_count}")

    # Primary evaluation.
    primary = {arm: engine.evaluate(arm, ALPHA_PRIMARY) for arm in ARMS}
    results["primary"] = primary

    print("\n=== PRIMARY (alpha=0.5) mean chain coverage ===")
    print(f"{'arm':<5}{'cov@2':>8}{'cov@3':>8}{'cov@5':>8}{'cmpl@3':>9}{'d_cov@3':>9}")
    base3 = primary["C"]["aggregate"]["cov3"]
    for arm in ARMS:
        a = primary[arm]["aggregate"]
        delta = a["cov3"] - base3
        print(f"{arm:<5}{a['cov2']:>8.4f}{a['cov3']:>8.4f}{a['cov5']:>8.4f}"
              f"{a['complete3']:>9.4f}{delta:>+9.4f}")

    print("\n=== PER CLASS (cov@3, delta vs C) ===")
    print(f"{'arm':<5}" + "".join(f"{c:>13}" for c in
                                  ("NEUTRAL", "RELATION", "TEMPORAL", "PROVENANCE")))
    for arm in ARMS:
        row = f"{arm:<5}"
        for cls in ("NEUTRAL", "RELATION", "TEMPORAL", "PROVENANCE"):
            v = primary[arm]["by_class"][cls]["cov3"]
            d = v - primary["C"]["by_class"][cls]["cov3"]
            row += f"{v:>7.3f}({d:+.2f})"
        print(row)

    # Alpha sweep (falsifier F5).
    sweep = {}
    for alpha in ALPHA_SWEEP:
        sweep[str(alpha)] = {arm: engine.evaluate(arm, alpha)["aggregate"]["cov3"]
                             for arm in ARMS}
    results["alpha_sweep"] = sweep
    print("\n=== ALPHA SWEEP (cov@3, delta vs C at same alpha) ===")
    print(f"{'arm':<5}" + "".join(f"{'a=' + str(a):>18}" for a in ALPHA_SWEEP))
    for arm in ARMS:
        row = f"{arm:<5}"
        for alpha in ALPHA_SWEEP:
            v = sweep[str(alpha)][arm]
            d = v - sweep[str(alpha)]["C"]
            row += f"{v:>11.4f}({d:+.2f})"
        print(row)

    # Null models (falsifier F3).
    print(f"\n=== NULL MODELS ({NULL_SEEDS} seeds, cov@3) ===")
    print(f"{'arm':<5}{'true':>9}{'null_mean':>11}{'null_p95':>10}{'pctile':>9}{'F3':>7}")
    nulls = {}
    for arm in ("D1", "D2", "D3"):
        dist = null_distribution(engine, arm, ALPHA_PRIMARY, NULL_SEEDS)
        true = primary[arm]["aggregate"]["cov3"]
        p95 = percentile(dist, 0.95)
        below = sum(1 for v in dist if v < true)
        pct = below / len(dist)
        nulls[arm] = {
            "true": true,
            "null_mean": sum(dist) / len(dist),
            "null_p95": p95,
            "null_min": dist[0],
            "null_max": dist[-1],
            "true_percentile": pct,
            "passes_f3": bool(true > p95),
            "distribution": dist,
        }
        print(f"{arm:<5}{true:>9.4f}{nulls[arm]['null_mean']:>11.4f}{p95:>10.4f}"
              f"{pct:>9.3f}{'PASS' if true > p95 else 'FAIL':>7}")
    results["null_models"] = nulls

    # Latency (declared BENCH-0004 primary measure, unmeasured in R1/R2).
    lat = {arm: measure_latency(engine, arm, ALPHA_PRIMARY) for arm in ARMS}
    results["latency_ms_per_query"] = lat
    print("\n=== LATENCY (ms/query) ===")
    for arm in ARMS:
        print(f"{arm:<5}{lat[arm]:>9.3f}  ({lat[arm] / lat['C']:.2f}x C)")

    # Declared deviation check: provenance min-max normalised (see report).
    dev = {arm: engine.evaluate(arm, ALPHA_PRIMARY, normalise_prov=True)["aggregate"]["cov3"]
           for arm in ("D3", "D4")}
    results["deviation_normalised_provenance"] = dev
    print("\n=== SENSITIVITY: min-max normalised provenance signal (cov@3) ===")
    for arm in ("D3", "D4"):
        print(f"{arm:<5}{dev[arm]:>9.4f}  (delta vs C {dev[arm] - base3:+.4f})")

    out_path = Path(args.out)
    out_path.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    print(f"\nraw results -> {out_path}")


if __name__ == "__main__":
    main()
