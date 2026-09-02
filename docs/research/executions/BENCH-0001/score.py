"""BENCH-0001 — scoring. Preregistered; applies schemas.json mechanically.

Coverage = bound concepts / total concepts, per workflow.
Boundary violations = concepts that ESCAPE the core, per workflow.
Reported overall and per workflow class, since CLM-0001 claims generality
across BOTH agentic and non-agentic workloads.
"""

import json
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
concepts = json.load(open(os.path.join(HERE, "concepts.json")))
schemas = json.load(open(os.path.join(HERE, "schemas.json")))
BIND = schemas["bindings"]

rows, by_class = [], defaultdict(list)
for w in concepts["workflows"]:
    cs = w["concepts"]
    row = {"id": w["id"], "class": w["class"], "n": len(cs)}
    for cond in ("A", "B"):
        bound = [c for c in cs if BIND[c][cond] != "ESCAPE"]
        row[f"{cond}_coverage"] = len(bound) / len(cs) if cs else None
        row[f"{cond}_violations"] = len(cs) - len(bound)
        row[f"{cond}_escaped"] = sorted(c for c in cs if BIND[c][cond] == "ESCAPE")
    rows.append(row)
    by_class[w["class"]].append(row)


def agg(sel, key):
    vals = [r[key] for r in sel if r[key] is not None]
    return sum(vals) / len(vals) if vals else None


out = {
    "n_workflows": len(rows),
    "overall": {
        f"{c}_{m}": agg(rows, f"{c}_{m}")
        for c in ("A", "B") for m in ("coverage", "violations")
    },
    "by_class": {
        cls: {"n": len(sel), **{f"{c}_{m}": agg(sel, f"{c}_{m}")
                                for c in ("A", "B") for m in ("coverage", "violations")}}
        for cls, sel in sorted(by_class.items())
    },
    "per_workflow": rows,
}
out["overall"]["delta_coverage_B_minus_A"] = out["overall"]["B_coverage"] - out["overall"]["A_coverage"]

with open(os.path.join(HERE, "results_raw.json"), "w") as f:
    json.dump(out, f, indent=2, sort_keys=True)

print(f"{'workflow':6s} {'class':26s} {'n':>2s}  {'A cov':>6s} {'A viol':>6s}  {'B cov':>6s} {'B viol':>6s}")
for r in rows:
    print(f"{r['id']:6s} {r['class']:26s} {r['n']:2d}  "
          f"{r['A_coverage']:6.3f} {r['A_violations']:6d}  {r['B_coverage']:6.3f} {r['B_violations']:6d}")
print(f"\nOVERALL  A coverage {out['overall']['A_coverage']:.4f}  "
      f"B coverage {out['overall']['B_coverage']:.4f}  "
      f"delta {out['overall']['delta_coverage_B_minus_A']:+.4f}")
print(f"         A violations/wf {out['overall']['A_violations']:.2f}  "
      f"B violations/wf {out['overall']['B_violations']:.2f}\n")
for cls, e in out["by_class"].items():
    print(f"{cls:26s} n={e['n']}  A {e['A_coverage']:.3f} / B {e['B_coverage']:.3f}  "
          f"delta {e['B_coverage'] - e['A_coverage']:+.3f}")
