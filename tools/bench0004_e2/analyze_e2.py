#!/usr/bin/env python3
"""BENCH-0004-E2 gate G7 -- evaluator-swap variance decomposition.

Fits  score ~ C(case) + T * R * P * evaluator  over the frozen answer set scored
by evaluators A, B and C, and answers the primary question: does the mechanism
ranking survive evaluator replacement?

Pure standard library -- no numpy, pandas or statsmodels. OLS is solved from the
normal equations with partial pivoting; t and F p-values come from a regularized
incomplete beta.

Exit codes
  0  analysis completed
  2  usage / missing or malformed input
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

MECHANISMS = ("T", "R", "P")
CELL_RE = re.compile(r"T([01])R([01])P([01])")


# --------------------------------------------------------------------------
# statistics
# --------------------------------------------------------------------------
def betacf(a: float, b: float, x: float) -> float:
    tiny, eps, itmax = 1e-30, 3e-16, 300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, itmax + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        c = 1.0 + aa / c
        if abs(d) < tiny:
            d = tiny
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        c = 1.0 + aa / c
        if abs(d) < tiny:
            d = tiny
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def betai(a: float, b: float, x: float) -> float:
    """Regularized incomplete beta I_x(a, b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(lbeta + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * betacf(a, b, x) / a
    return 1.0 - front * betacf(b, a, 1.0 - x) / b


def t_pvalue(t: float, df: int) -> float:
    if df <= 0:
        return float("nan")
    return betai(df / 2.0, 0.5, df / (df + t * t))


def f_pvalue(f: float, df1: int, df2: int) -> float:
    if df1 <= 0 or df2 <= 0 or f <= 0:
        return float("nan")
    return betai(df2 / 2.0, df1 / 2.0, df2 / (df2 + df1 * f))


def solve(a: list[list[float]], b: list[float]) -> list[float] | None:
    """Gaussian elimination with partial pivoting."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[piv][col]) < 1e-12:
            return None
        m[col], m[piv] = m[piv], m[col]
        inv = 1.0 / m[col][col]
        for r in range(n):
            if r == col:
                continue
            f = m[r][col] * inv
            if f:
                for c in range(col, n + 1):
                    m[r][c] -= f * m[col][c]
    return [m[i][n] / m[i][i] for i in range(n)]


def invert(a: list[list[float]]) -> list[list[float]] | None:
    n = len(a)
    m = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[piv][col]) < 1e-12:
            return None
        m[col], m[piv] = m[piv], m[col]
        inv = 1.0 / m[col][col]
        for c in range(2 * n):
            m[col][c] *= inv
        for r in range(n):
            if r == col:
                continue
            f = m[r][col]
            if f:
                for c in range(2 * n):
                    m[r][c] -= f * m[col][c]
    return [row[n:] for row in m]


class OLS:
    def __init__(self, X: list[list[float]], y: list[float], names: list[str]):
        n, k = len(y), len(names)
        xtx = [[sum(X[i][a] * X[i][b] for i in range(n)) for b in range(k)] for a in range(k)]
        xty = [sum(X[i][a] * y[i] for i in range(n)) for a in range(k)]
        beta = solve(xtx, xty)
        if beta is None:
            raise ValueError("design matrix is singular -- check for collinear or empty terms")
        self.names, self.beta, self.n, self.k = names, beta, n, k
        fitted = [sum(X[i][j] * beta[j] for j in range(k)) for i in range(n)]
        self.resid = [y[i] - fitted[i] for i in range(n)]
        self.rss = sum(r * r for r in self.resid)
        ybar = sum(y) / n
        self.tss = sum((v - ybar) ** 2 for v in y)
        self.df_resid = n - k
        self.r2 = 1.0 - self.rss / self.tss if self.tss else float("nan")
        self.mse = self.rss / self.df_resid if self.df_resid > 0 else float("nan")
        xtxi = invert(xtx)
        self.se = ([math.sqrt(max(self.mse * xtxi[j][j], 0.0)) for j in range(k)]
                   if xtxi else [float("nan")] * k)

    def t(self, j: int) -> float:
        return self.beta[j] / self.se[j] if self.se[j] else float("nan")

    def p(self, j: int) -> float:
        return t_pvalue(self.t(j), self.df_resid)


# --------------------------------------------------------------------------
def load(answers: Path, scores: Path, case_field: str | None):
    ctx = {}
    for line in answers.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        cid = r["context_id"]
        m = CELL_RE.search(r.get("cell", "") or cid)
        if not m:
            raise SystemExit(f"cannot parse T/R/P cell from context {cid!r}")
        case = r.get(case_field) if case_field else None
        if case is None:
            tail = CELL_RE.sub("", cid).strip("-_ ")
            case = tail or cid
        ctx[cid] = {"T": int(m.group(1)), "R": int(m.group(2)), "P": int(m.group(3)), "case": case}

    rows = []
    for line in scores.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        s = json.loads(line)
        cid = s["context_id"]
        if cid not in ctx:
            raise SystemExit(f"score references unknown context_id {cid!r}")
        rows.append({**ctx[cid], "context_id": cid,
                     "evaluator": str(s["evaluator"]), "scores": s})
    if not rows:
        raise SystemExit("no score rows found")
    return ctx, rows


def build_design(rows, metric):
    cases = sorted({r["case"] for r in rows})
    evals = sorted({r["evaluator"] for r in rows})
    names, cols, groups = ["intercept"], [lambda r: 1.0], {}

    for c in cases[1:]:
        names.append(f"case[{c}]")
        cols.append(lambda r, c=c: 1.0 if r["case"] == c else 0.0)
    groups["case"] = list(range(1, len(names)))

    mech_terms = []
    for size in (1, 2, 3):
        for combo in combinations(MECHANISMS, size):
            mech_terms.append(combo)
    start = len(names)
    for combo in mech_terms:
        names.append("x".join(combo))
        cols.append(lambda r, combo=combo: math.prod(1.0 if r[f] else -1.0 for f in combo))
    groups["mechanism"] = list(range(start, len(names)))

    start = len(names)
    for e in evals[1:]:
        names.append(f"eval[{e}]")
        cols.append(lambda r, e=e: 1.0 if r["evaluator"] == e else 0.0)
    groups["evaluator"] = list(range(start, len(names)))

    start = len(names)
    for combo in mech_terms:
        for e in evals[1:]:
            names.append(f"{'x'.join(combo)}:eval[{e}]")
            cols.append(lambda r, combo=combo, e=e:
                        (math.prod(1.0 if r[f] else -1.0 for f in combo))
                        * (1.0 if r["evaluator"] == e else 0.0))
    groups["mechanism x evaluator"] = list(range(start, len(names)))

    X, y = [], []
    for r in rows:
        v = r["scores"].get(metric)
        if v is None:
            continue
        X.append([f(r) for f in cols])
        y.append(float(v))
    return X, y, names, groups, cases, evals


def analyze_metric(rows, metric):
    X, y, names, groups, cases, evals = build_design(rows, metric)
    if len(y) < len(names) + 2:
        print(f"  SKIPPED -- {len(y)} observations for {len(names)} parameters")
        return None
    full = OLS(X, y, names)

    print(f"  n={full.n}  params={full.k}  df_resid={full.df_resid}  "
          f"R2={full.r2:.4f}  RSS={full.rss:.5f}")

    print(f"\n  {'term':28} {'coef':>10} {'se':>9} {'t':>8} {'p':>10}")
    for j, nm in enumerate(names):
        if nm.startswith("case[") or nm == "intercept":
            continue
        print(f"  {nm:28} {full.beta[j]:10.4f} {full.se[j]:9.4f} "
              f"{full.t(j):8.3f} {full.p(j):10.4f}")

    print(f"\n  {'group':24} {'df':>4} {'partial SS':>12} {'F':>9} {'p':>10} {'var share':>10}")
    decomp = {}
    for gname, idx in groups.items():
        keep = [j for j in range(full.k) if j not in idx]
        Xr = [[row[j] for j in keep] for row in X]
        try:
            red = OLS(Xr, y, [names[j] for j in keep])
        except ValueError:
            print(f"  {gname:24} singular after removal -- skipped")
            continue
        ss = red.rss - full.rss
        df1 = len(idx)
        f = (ss / df1) / full.mse if full.mse > 0 else float("nan")
        p = f_pvalue(f, df1, full.df_resid)
        share = ss / full.tss if full.tss else float("nan")
        decomp[gname] = {"df": df1, "ss": ss, "F": f, "p": p, "share": share}
        print(f"  {gname:24} {df1:4d} {ss:12.5f} {f:9.3f} {p:10.4f} {share:9.1%}")
    print(f"  {'residual':24} {full.df_resid:4d} {full.rss:12.5f} "
          f"{'':>9} {'':>10} {full.rss / full.tss:9.1%}")

    # ---- the primary question -------------------------------------------
    print("\n  Mechanism effect by evaluator (2 x mean difference, raw):")
    per_eval = {}
    for e in evals:
        sub = [r for r in rows if r["evaluator"] == e and r["scores"].get(metric) is not None]
        eff = {}
        for mech in MECHANISMS:
            hi = [float(r["scores"][metric]) for r in sub if r[mech]]
            lo = [float(r["scores"][metric]) for r in sub if not r[mech]]
            eff[mech] = (sum(hi) / len(hi) - sum(lo) / len(lo)) if hi and lo else float("nan")
        per_eval[e] = eff
        order = sorted(MECHANISMS, key=lambda m: -eff[m])
        print(f"    {e}:  " + "  ".join(f"{m}={eff[m]:+.4f}" for m in MECHANISMS)
              + f"   ranking: {' > '.join(order)}")

    orders = {e: tuple(sorted(MECHANISMS, key=lambda m: -per_eval[e][m])) for e in evals}
    stable = len(set(orders.values())) == 1
    inter = decomp.get("mechanism x evaluator", {})
    print(f"\n  ranking identical across evaluators: {'YES' if stable else 'NO'}")
    if inter:
        print(f"  mechanism x evaluator interaction:   F={inter['F']:.3f} p={inter['p']:.4f} "
              f"({inter['share']:.1%} of total variance)")
    return {"metric": metric, "r2": full.r2, "decomposition": decomp,
            "per_evaluator_effect": per_eval,
            "rankings": {e: list(o) for e, o in orders.items()},
            "ranking_stable": stable}


def main() -> int:
    ap = argparse.ArgumentParser(description="BENCH-0004-E2 evaluator-swap analysis (gate G7)")
    ap.add_argument("--answers", required=True, type=Path, help="frozen answers_96.jsonl")
    ap.add_argument("--scores", required=True, type=Path,
                    help="JSONL: context_id, evaluator, and one field per response variable")
    ap.add_argument("--metrics", nargs="*", default=None,
                    help="response variables to model (default: every numeric field found)")
    ap.add_argument("--case-field", default=None, help="explicit case field in the answers file")
    ap.add_argument("--out", type=Path, default=None, help="write results as JSON")
    args = ap.parse_args()

    for p in (args.answers, args.scores):
        if not p.is_file():
            print(f"ERROR: not found: {p}", file=sys.stderr)
            return 2

    ctx, rows = load(args.answers, args.scores, args.case_field)
    evals = sorted({r["evaluator"] for r in rows})
    by_eval = defaultdict(int)
    for r in rows:
        by_eval[r["evaluator"]] += 1

    print(f"BENCH-0004-E2 evaluator-swap analysis")
    print(f"  contexts: {len(ctx)}   score rows: {len(rows)}")
    print(f"  evaluators: {', '.join(f'{e} (n={by_eval[e]})' for e in evals)}")
    if len(evals) < 2:
        print("\nWARNING: fewer than two evaluators -- the evaluator-swap question cannot be "
              "answered. Mechanism effects below are single-evaluator only.")

    metrics = args.metrics
    if not metrics:
        metrics = sorted({k for r in rows for k, v in r["scores"].items()
                          if k not in ("context_id", "evaluator") and isinstance(v, (int, float))})
    if not metrics:
        print("ERROR: no numeric response variables found in the scores file", file=sys.stderr)
        return 2

    out = []
    for m in metrics:
        print(f"\n{'=' * 70}\nRESPONSE VARIABLE: {m}\n{'=' * 70}")
        res = analyze_metric(rows, m)
        if res:
            out.append(res)

    print(f"\n{'=' * 70}\nSUMMARY")
    for r in out:
        print(f"  {r['metric']:28} ranking stable: {'YES' if r['ranking_stable'] else 'NO':3}  "
              f"R2={r['r2']:.3f}")
    print("\nReading: mechanism effects material and ranking stable across evaluators supports")
    print("transfer to answer quality. A dominant evaluator effect or a large mechanism x")
    print("evaluator interaction means the advantage is evaluator-sensitive and must NOT be")
    print("promoted as an architecture invariant.")

    if args.out:
        args.out.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"\nresults written to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
