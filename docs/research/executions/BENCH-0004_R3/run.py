"""BENCH-0004 Round 3 — mechanism decomposition on an independent corpus.

Preregistered instrumentation. This is benchmark instrumentation, not APF
implementation (DEC-0001 section 3).

Corpus: CORPUS-0001 (python/peps @ a4f4971816e2edf74ce90672df91f01e87df0ce5).
Claim under test: CLM-0011 (narrow cross-document chain recovery), split from
CLM-0004 by BENCH-0004 Round 2.

Design invariants that must not be changed after first execution:
  * Ground truth comes ONLY from header-declared relations
    (Superseded-By / Replaces / Requires), authored by PEP authors.
  * The D2 relation graph comes ONLY from PEP references in document BODIES.
    Ground-truth edges are never handed to any condition.
  * Queries are generated mechanically from the SOURCE document title plus a
    fixed relation cue. A query never contains the target's number or title.
  * Parameters ALPHA/BETA/GAMMA are fixed below and were not tuned.
"""

import json
import math
import os
import random
import re
import sys
from collections import defaultdict

PEP_DIR = "/home/user/python/peps/peps"
CORPUS_SHA = "a4f4971816e2edf74ce90672df91f01e87df0ce5"

# Preregistered, untuned parameters.
ALPHA = 0.30   # D1 temporal boost
BETA = 0.50    # D2 one-hop relation propagation
GAMMA = 0.30   # D3 provenance boost
K_VALUES = (3, 5, 10)
PRIMARY_K = 5
BOOTSTRAP_N = 2000
SEED = 20260902

TOKEN_RE = re.compile(r"[a-z0-9]+")
PEP_REF_RE = re.compile(r"\bPEP\s*[#-]?\s*(\d{1,4})\b")
MONTHS = {m: i + 1 for i, m in enumerate(
    "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}


def parse_date(s):
    """'12-Sep-2020' -> ordinal int; unparsable -> None."""
    m = re.match(r"(\d{1,2})-([A-Za-z]{3})-(\d{4})", (s or "").strip())
    if not m:
        return None
    d, mon, y = int(m.group(1)), MONTHS.get(m.group(2).title()), int(m.group(3))
    if not mon:
        return None
    return y * 372 + mon * 31 + d


def parse_pep(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    lines = raw.split("\n")
    headers, key, i = {}, None, 0
    for i, line in enumerate(lines):
        if not line.strip():
            break
        m = re.match(r"^([A-Za-z][A-Za-z-]*):\s*(.*)$", line)
        if m:
            key = m.group(1).lower()
            headers[key] = m.group(2).strip()
        elif key and line[:1] in (" ", "\t"):
            headers[key] += " " + line.strip()
    body = "\n".join(lines[i:])
    if "pep" not in headers or not headers["pep"].strip().isdigit():
        return None
    return {
        "pep": int(headers["pep"]),
        "title": headers.get("title", ""),
        "status": headers.get("status", ""),
        "type": headers.get("type", ""),
        "author": headers.get("author", ""),
        "created": parse_date(headers.get("created", "")),
        "resolution": headers.get("resolution", ""),
        "python_version": headers.get("python-version", ""),
        "superseded_by": headers.get("superseded-by", ""),
        "replaces": headers.get("replaces", ""),
        "requires": headers.get("requires", ""),
        "body": body,
        "text": raw,
    }


def nums(s):
    return [int(x) for x in re.findall(r"\d+", s or "")]


def tokenize(s):
    return TOKEN_RE.findall(s.lower())


def build_index(docs):
    tf, df = [], defaultdict(int)
    for d in docs:
        counts = defaultdict(int)
        for t in tokenize(d["text"]):
            counts[t] += 1
        tf.append(counts)
        for t in counts:
            df[t] += 1
    n = len(docs)
    idf = {t: math.log(n / c) for t, c in df.items()}
    vecs = []
    for counts in tf:
        v = {t: (1 + math.log(c)) * idf.get(t, 0.0) for t, c in counts.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vecs.append({t: x / norm for t, x in v.items()})
    return vecs, idf


def score_query(query, vecs, idf):
    counts = defaultdict(int)
    for t in tokenize(query):
        counts[t] += 1
    q = {t: (1 + math.log(c)) * idf.get(t, 0.0) for t, c in counts.items()}
    norm = math.sqrt(sum(x * x for x in q.values())) or 1.0
    q = {t: x / norm for t, x in q.items()}
    out = []
    for i, v in enumerate(vecs):
        s = 0.0
        for t, x in q.items():
            y = v.get(t)
            if y:
                s += x * y
        out.append(s)
    return out


def rank(scores, k):
    return [i for i, _ in sorted(enumerate(scores), key=lambda p: -p[1])[:k]]


def main():
    files = sorted(f for f in os.listdir(PEP_DIR) if re.match(r"pep-\d+\.rst$", f))
    docs = [d for d in (parse_pep(os.path.join(PEP_DIR, f)) for f in files) if d]
    idx_of = {d["pep"]: i for i, d in enumerate(docs)}
    print(f"corpus: {len(docs)} documents")

    # --- D2 relation graph: body-text PEP references ONLY (no header relations)
    body_edges = defaultdict(set)
    for i, d in enumerate(docs):
        for ref in set(int(x) for x in PEP_REF_RE.findall(d["body"])):
            j = idx_of.get(ref)
            if j is not None and j != i:
                body_edges[i].add(j)
                body_edges[j].add(i)

    # --- Ground truth: header-declared relations ONLY
    tasks = []
    for i, d in enumerate(docs):
        for field, cue, fam in (
            ("superseded_by", "superseded replaced by successor proposal status", "T1"),
            ("replaces", "replaces predecessor earlier superseded proposal", "T1"),
            ("requires", "requires depends on prerequisite proposal", "T2"),
        ):
            for target in nums(d[field]):
                j = idx_of.get(target)
                if j is None or j == i:
                    continue
                tasks.append({
                    "family": fam,
                    "query": f"{d['title']} {cue}",
                    "source": i,
                    "required": sorted({i, j}),
                })
    # dedupe symmetric duplicates by (query, required)
    seen, uniq = set(), []
    for t in tasks:
        key = (t["query"], tuple(t["required"]))
        if key not in seen:
            seen.add(key)
            uniq.append(t)
    tasks = uniq

    # --- T0 control: single-document retrieval, no chain required
    rng = random.Random(SEED)
    for i in rng.sample(range(len(docs)), 100):
        tasks.append({
            "family": "T0",
            "query": docs[i]["title"],
            "source": i,
            "required": [i],
        })
    fam_counts = defaultdict(int)
    for t in tasks:
        fam_counts[t["family"]] += 1
    print("tasks:", dict(fam_counts), "total", len(tasks))

    vecs, idf = build_index(docs)
    graph_recall_hits = graph_recall_total = 0

    for t in tasks:
        base = score_query(t["query"], vecs, idf)
        top1 = max(range(len(base)), key=lambda i: base[i])

        # D1 temporal-only: boost documents created after the top-1 anchor,
        # decaying with distance. Uses no ground truth.
        anchor = docs[top1]["created"]
        d1 = list(base)
        if anchor:
            for i, d in enumerate(docs):
                c = d["created"]
                if c and c > anchor:
                    d1[i] = base[i] * (1 + ALPHA * math.exp(-(c - anchor) / (372 * 5)))

        # D2 relationship-only: one-hop propagation over body-reference edges.
        d2 = list(base)
        for i in range(len(docs)):
            nb = body_edges.get(i)
            if nb:
                d2[i] = base[i] + BETA * max(base[j] for j in nb)

        # D3 provenance-only: boost documents sharing the anchor's author or
        # carrying an explicit resolution record.
        a_authors = {x.strip().lower() for x in re.split(r"[,;]", docs[top1]["author"]) if x.strip()}
        d3 = list(base)
        for i, d in enumerate(docs):
            authors = {x.strip().lower() for x in re.split(r"[,;]", d["author"]) if x.strip()}
            mult = 1.0
            if a_authors & authors:
                mult += GAMMA
            if d["resolution"]:
                mult += GAMMA / 3
            d3[i] = base[i] * mult

        # D4 combined.
        d4 = list(base)
        if anchor:
            for i, d in enumerate(docs):
                c = d["created"]
                if c and c > anchor:
                    d4[i] = d4[i] * (1 + ALPHA * math.exp(-(c - anchor) / (372 * 5)))
        for i, d in enumerate(docs):
            authors = {x.strip().lower() for x in re.split(r"[,;]", d["author"]) if x.strip()}
            mult = 1.0
            if a_authors & authors:
                mult += GAMMA
            if d["resolution"]:
                mult += GAMMA / 3
            d4[i] = d4[i] * mult
        prop = list(d4)
        for i in range(len(docs)):
            nb = body_edges.get(i)
            if nb:
                prop[i] = d4[i] + BETA * max(d4[j] for j in nb)
        d4 = prop

        t["scores"] = {}
        for name, sc in (("C", base), ("D1", d1), ("D2", d2), ("D3", d3), ("D4", d4)):
            per_k = {}
            for k in K_VALUES:
                top = set(rank(sc, k))
                req = set(t["required"])
                per_k[k] = {
                    "coverage": len(top & req) / len(req),
                    "complete": float(req <= top),
                }
            t["scores"][name] = per_k

        if len(t["required"]) == 2:
            a, b = t["required"]
            graph_recall_total += 1
            if b in body_edges.get(a, ()):
                graph_recall_hits += 1
            # topical similarity of the two required documents, for the
            # preregistered prediction that the margin is largest where the
            # pair is topically dissimilar.
            va, vb = vecs[a], vecs[b]
            small, large = (va, vb) if len(va) < len(vb) else (vb, va)
            t["pair_similarity"] = sum(x * large.get(tk, 0.0) for tk, x in small.items())

    # --- aggregate
    conds = ("C", "D1", "D2", "D3", "D4")
    results = {
        "corpus_sha": CORPUS_SHA,
        "n_docs": len(docs),
        "params": {"ALPHA": ALPHA, "BETA": BETA, "GAMMA": GAMMA, "SEED": SEED},
        "task_counts": dict(fam_counts),
        "graph_ground_truth_edge_overlap": (
            graph_recall_hits / graph_recall_total if graph_recall_total else None),
        "by_family": {},
    }
    for fam in ("T1", "T2", "T0", "ALL_CHAIN"):
        sel = [t for t in tasks if (t["family"] in ("T1", "T2")
                                    if fam == "ALL_CHAIN" else t["family"] == fam)]
        if not sel:
            continue
        entry = {"n": len(sel)}
        for c in conds:
            entry[c] = {}
            for k in K_VALUES:
                cov = [t["scores"][c][k]["coverage"] for t in sel]
                comp = [t["scores"][c][k]["complete"] for t in sel]
                entry[c][f"coverage@{k}"] = sum(cov) / len(cov)
                entry[c][f"complete@{k}"] = sum(comp) / len(comp)
        results["by_family"][fam] = entry

    # --- paired bootstrap on the primary metric (complete@PRIMARY_K, chain tasks)
    chain = [t for t in tasks if t["family"] in ("T1", "T2")]
    rng = random.Random(SEED)
    boot = {}
    for c in ("D1", "D2", "D3", "D4"):
        diffs = []
        for _ in range(BOOTSTRAP_N):
            sample = [chain[rng.randrange(len(chain))] for _ in chain]
            dc = sum(t["scores"][c][PRIMARY_K]["complete"] for t in sample) / len(sample)
            cc = sum(t["scores"]["C"][PRIMARY_K]["complete"] for t in sample) / len(sample)
            diffs.append(dc - cc)
        diffs.sort()
        boot[c] = {
            "mean_diff": sum(diffs) / len(diffs),
            "ci95_low": diffs[int(0.025 * BOOTSTRAP_N)],
            "ci95_high": diffs[int(0.975 * BOOTSTRAP_N)],
            "p_gt_0": sum(1 for d in diffs if d > 0) / len(diffs),
        }
    results["bootstrap_primary"] = {
        "metric": f"complete@{PRIMARY_K} on chain tasks (T1+T2)", "vs": "C", **boot}

    # Preregistered prediction check: margin by topical similarity of the pair.
    sims = sorted(t["pair_similarity"] for t in chain)
    median = sims[len(sims) // 2]
    results["by_pair_similarity"] = {"median": median}
    for half, sel in (("dissimilar_below_median",
                       [t for t in chain if t["pair_similarity"] <= median]),
                      ("similar_above_median",
                       [t for t in chain if t["pair_similarity"] > median])):
        entry = {"n": len(sel)}
        for c in conds:
            entry[c] = sum(
                t["scores"][c][PRIMARY_K]["complete"] for t in sel) / len(sel)
        results["by_pair_similarity"][half] = entry

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_raw.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=2, sort_keys=True)
    json.dump(results, sys.stdout, indent=2, sort_keys=True)
    print(f"\n\nwrote {out}")


if __name__ == "__main__":
    main()
