#!/usr/bin/env python3
"""BENCH-0006 -- provenance ablation for CLM-0006.

CLM-0006 holds that engineering evidence lacking revision/configuration provenance
is materially less trustworthy for reuse and audit. Ablating the provenance header
and then asking provenance questions would be tautological, so that is not what
this measures.

The non-trivial question is how much provenance survives ablation because the
content carries it itself -- documents that state their own date, version or
status. Where content-embedded provenance holds, external carriage adds little;
where it fails, external carriage is what stands between a reader and a stale
citation. This measures that boundary against git ground truth.

Conditions
  P+   evidence with a provenance header (commit, date, author, path)
  P-   the same evidence, header ablated -- content only

Audit questions, per evidence item, with ground truth from git
  Q1 attribution   who produced this
  Q2 dating        when was it produced
  Q3 currency      is this the current version, or superseded

Primary metric: audit-completeness rate.
Secondary and sharper: stale-evidence escape rate -- of the items that are NOT
current, how many present no in-content signal that they are superseded.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

DATE = re.compile(r"20\d{2}-\d{2}-\d{2}")
# A document merely HAVING a status field says nothing about whether the copy in
# hand has been superseded. "Status: Active working state" is not a staleness
# signal. Only an explicit supersession marker is.
SUPERSEDED = re.compile(r"\bsuperseded\b|\bdeprecated\b|\breplaced by\b|\bobsolete\b", re.I)


def git(*a: str) -> str:
    return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout


def main() -> int:
    ap = argparse.ArgumentParser(description="BENCH-0006 provenance ablation")
    ap.add_argument("--at-commit", default="HEAD")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    at = git("rev-parse", args.at_commit).strip()

    paths = [p for p in git("ls-tree", "-r", "--name-only", at).split()
             if p.endswith((".md", ".json")) and not p.startswith("tools/")]

    items = []
    for path in sorted(paths):
        log = [l for l in git("log", "--reverse", "--format=%H|%aI|%an", at, "--", path)
               .strip().splitlines() if l]
        for n, line in enumerate(log, 1):
            sha, iso, author = line.split("|", 2)
            try:
                text = git("show", f"{sha}:{path}")
            except subprocess.CalledProcessError:
                continue
            items.append({"path": path, "version": n, "of": len(log), "commit": sha[:12],
                          "date": iso[:10], "author": author, "text": text,
                          "is_current": n == len(log)})

    rows = []
    for it in items:
        body = it["text"]
        # what the content alone reveals -- the only thing ablation can leave behind
        content_date = it["date"] in DATE.findall(body)
        content_author = it["author"].lower() in body.lower()
        content_supersession = bool(SUPERSEDED.search(body))
        for cond in ("P+", "P-"):
            has = (cond == "P+")
            rows.append({
                "path": it["path"], "version": it["version"], "condition": cond,
                "is_current": it["is_current"],
                "q1_attribution": 1 if (has or content_author) else 0,
                "q2_dating": 1 if (has or content_date) else 0,
                "q3_currency": 1 if (has or content_supersession) else 0,
                "weak_date_cue": 1 if content_date else 0,
            })
    for r in rows:
        r["audit_complete"] = int(r["q1_attribution"] and r["q2_dating"] and r["q3_currency"])

    def rate(cond, key, filt=lambda r: True):
        sel = [r for r in rows if r["condition"] == cond and filt(r)]
        return sum(r[key] for r in sel) / len(sel) if sel else float("nan")

    print(f"BENCH-0006 provenance ablation   corpus pinned at {at[:12]}")
    print(f"  evidence items: {len(items)}  ({sum(1 for i in items if not i['is_current'])} "
          f"non-current)   observations: {len(rows)}\n")
    print(f"  {'question':16} {'P+':>7} {'P-':>7} {'delta':>8}")
    for k, label in [("q1_attribution", "attribution"), ("q2_dating", "dating"),
                     ("q3_currency", "currency"), ("audit_complete", "AUDIT COMPLETE")]:
        a, b = rate("P+", k), rate("P-", k)
        print(f"  {label:16} {a:7.3f} {b:7.3f} {a-b:8.3f}")

    stale = lambda r: not r["is_current"]
    esc = 1.0 - rate("P-", "q3_currency", stale)
    print(f"\n  stale-evidence escape rate (P-): {esc:.3f}"
          f"   ({int(round(esc*sum(1 for i in items if not i['is_current'])))} of "
          f"{sum(1 for i in items if not i['is_current'])} superseded items carry no "
          f"in-content supersession signal)")
    print(f"  stale-evidence escape rate (P+): {1.0-rate('P+','q3_currency',stale):.3f}")

    weak = rate("P-", "weak_date_cue", stale)
    print(f"  weak cue only -- superseded items that at least self-date: {weak:.3f}")
    print("     a self-dated stale document lets an attentive reader suspect age, but not")
    print("     confirm supersession; it is not equivalent to carried provenance.")

    recovery = rate("P-", "audit_complete")
    print(f"\n  content-only provenance recovery: {recovery:.3f}")
    print("  -> the fraction of evidence that remains fully auditable after ablation "
          "because\n     the document carries its own provenance in its text.")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(
        {"pinned_at_commit": at, "items": len(items), "rows": rows}, indent=2) + "\n")
    print(f"\nraw results -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
