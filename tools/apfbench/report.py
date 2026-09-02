"""Console tables and result serialisation.

Kept separate from the runner so that changing how a result is presented can
never change what the result is.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence


def print_primary(primary: dict, arms: Sequence[str], baseline: str,
                  ks: Sequence[int] = (2, 3, 5), k_delta: int = 3) -> None:
    base = primary[baseline]["aggregate"][f"cov{k_delta}"]
    head = f"{'arm':<5}" + "".join(f"{'cov@' + str(k):>8}" for k in ks)
    print(head + f"{'cmpl@' + str(k_delta):>9}{'d_cov@' + str(k_delta):>9}")
    for arm in arms:
        a = primary[arm]["aggregate"]
        row = f"{arm:<5}" + "".join(f"{a['cov' + str(k)]:>8.4f}" for k in ks)
        print(row + f"{a['complete' + str(k_delta)]:>9.4f}"
                    f"{a['cov' + str(k_delta)] - base:>+9.4f}")


def print_by_class(primary: dict, arms: Sequence[str], classes: Sequence[str],
                   baseline: str, k: int = 3) -> None:
    print(f"{'arm':<5}" + "".join(f"{c:>13}" for c in classes))
    for arm in arms:
        row = f"{arm:<5}"
        for cls in classes:
            v = primary[arm]["by_class"][cls][f"cov{k}"]
            d = v - primary[baseline]["by_class"][cls][f"cov{k}"]
            row += f"{v:>7.3f}({d:+.2f})"
        print(row)


def print_sweep(sweep: dict, arms: Sequence[str], alphas: Sequence[float],
                baseline: str) -> None:
    print(f"{'arm':<5}" + "".join(f"{'a=' + str(a):>18}" for a in alphas))
    for arm in arms:
        row = f"{arm:<5}"
        for alpha in alphas:
            v = sweep[str(alpha)][arm]
            row += f"{v:>11.4f}({v - sweep[str(alpha)][baseline]:+.2f})"
        print(row)


def print_nulls(nulls: dict) -> None:
    print(f"{'arm':<5}{'true':>9}{'null_mean':>11}{'null_p95':>10}"
          f"{'pctile':>9}{'F3':>7}")
    for arm, n in nulls.items():
        verdict = "PASS" if n["passes_f3"] else "FAIL"
        print(f"{arm:<5}{n['true']:>9.4f}{n['null_mean']:>11.4f}"
              f"{n['null_p95']:>10.4f}{n['true_percentile']:>9.3f}{verdict:>7}")


def print_latency(latency: dict, arms: Sequence[str], baseline: str) -> None:
    for arm in arms:
        print(f"{arm:<5}{latency[arm]:>9.3f}  "
              f"({latency[arm] / latency[baseline]:.2f}x {baseline})")


def write_json(path: Path, results: dict) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    return path
