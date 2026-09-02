"""BENCH-0004 Round 3 — EXPLORATORY post-hoc analysis.

Not part of the preregistered verdict. Per CLM-0011 preregistered analysis
constraint 1, nothing here can change the F1-F4 outcome. Run after run.py.

Two questions:
  A. Is D2's gain concentrated on the tasks where a body-reference edge to the
     target actually exists? (mechanism attribution)
  B. Does the D2 result depend on the untuned BETA=0.50? (sensitivity)
"""

import importlib.util
import json
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("r3", os.path.join(HERE, "run.py"))
r3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r3)


def load():
    files = sorted(f for f in os.listdir(r3.PEP_DIR) if re.match(r"pep-\d+\.rst$", f))
    docs = [d for d in (r3.parse_pep(os.path.join(r3.PEP_DIR, f)) for f in files) if d]
    idx = {d["pep"]: i for i, d in enumerate(docs)}
    edges = {}
    for i, d in enumerate(docs):
        for ref in set(int(x) for x in r3.PEP_REF_RE.findall(d["body"])):
            j = idx.get(ref)
            if j is not None and j != i:
                edges.setdefault(i, set()).add(j)
                edges.setdefault(j, set()).add(i)
    tasks = []
    for i, d in enumerate(docs):
        for field, cue in (
            ("superseded_by", "superseded replaced by successor proposal status"),
            ("replaces", "replaces predecessor earlier superseded proposal"),
            ("requires", "requires depends on prerequisite proposal"),
        ):
            for target in r3.nums(d[field]):
                j = idx.get(target)
                if j is not None and j != i:
                    tasks.append({"query": f"{d['title']} {cue}",
                                  "required": sorted({i, j})})
    seen, uniq = set(), []
    for t in tasks:
        key = (t["query"], tuple(t["required"]))
        if key not in seen:
            seen.add(key)
            uniq.append(t)
    return docs, edges, uniq


def main():
    docs, edges, tasks = load()
    vecs, idf = r3.build_index(docs)
    K = r3.PRIMARY_K
    betas = [0.0, 0.25, 0.50, 1.00, 2.00]

    rows = []
    for t in tasks:
        base = r3.score_query(t["query"], vecs, idf)
        req = set(t["required"])
        a, b = t["required"]
        row = {"has_edge": b in edges.get(a, ()),
               "C": float(req <= set(r3.rank(base, K)))}
        for beta in betas:
            sc = list(base)
            for i in range(len(docs)):
                nb = edges.get(i)
                if nb:
                    sc[i] = base[i] + beta * max(base[j] for j in nb)
            row[f"D2_beta_{beta}"] = float(req <= set(r3.rank(sc, K)))
        rows.append(row)

    def mean(xs):
        return sum(xs) / len(xs) if xs else None

    out = {"metric": f"complete@{K} on chain tasks", "n": len(rows),
           "note": "EXPLORATORY. Cannot change the F1-F4 verdict."}

    out["A_by_direct_edge"] = {}
    for label, sel in (("edge_present", [r for r in rows if r["has_edge"]]),
                       ("edge_absent", [r for r in rows if not r["has_edge"]])):
        out["A_by_direct_edge"][label] = {
            "n": len(sel),
            "C": mean([r["C"] for r in sel]),
            "D2": mean([r["D2_beta_0.5"] for r in sel]),
            "delta": (mean([r["D2_beta_0.5"] for r in sel]) - mean([r["C"] for r in sel]))
            if sel else None,
        }

    out["B_beta_sensitivity"] = {
        "C": mean([r["C"] for r in rows]),
        **{f"beta={beta}": mean([r[f"D2_beta_{beta}"] for r in rows]) for beta in betas},
    }

    path = os.path.join(HERE, "results_posthoc.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2, sort_keys=True)
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
