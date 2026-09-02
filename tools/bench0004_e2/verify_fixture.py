#!/usr/bin/env python3
"""BENCH-0004-E2 gate G2 — byte-level fixture verification.

Recomputes the four locked SHA-256 values from source bytes and checks the
structural invariants of the 96-context fixture. Emits VERIFICATION.json, which
run_generator.py requires before it will call a model.

The fixture is evidence. If a hash mismatches, that is a finding to report --
never edit the fixture to make this pass.

Exit codes
  0  all checks passed
  1  verification failed (hash mismatch or structural violation)
  2  usage / missing input
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

CELLS = [f"T{t}R{r}P{p}" for t in (0, 1) for r in (0, 1) for p in (0, 1)]
EXPECTED_TOTAL = 96
EXPECTED_PER_CELL = 12

# bundle artifact -> candidate filenames, in preference order
ARTIFACTS = {
    "contexts_jsonl": ["contexts_96.jsonl", "contexts.jsonl"],
    "canonical_context_manifest": [
        "canonical_context_manifest.json",
        "context_manifest.json",
        "canonical_manifest.json",
    ],
    "declared_bundle_manifest": ["bundle_manifest.json", "manifest.json"],
    "generator_contract": [
        "generator_contract.json",
        "generator_contract.md",
        "generator_contract.yaml",
    ],
}

ID_FIELDS = ("context_id", "id")
SHA_FIELDS = ("context_sha256", "sha256", "context_hash")
TEXT_FIELDS = ("context", "context_text", "text")
CELL_FIELDS = ("cell", "cell_id", "condition")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pick(record: dict, names: tuple[str, ...]) -> tuple[str | None, object]:
    for n in names:
        if n in record:
            return n, record[n]
    return None, None


def resolve(bundle: Path, overrides: dict[str, str]) -> dict[str, Path | None]:
    found: dict[str, Path | None] = {}
    for key, candidates in ARTIFACTS.items():
        if key in overrides:
            found[key] = Path(overrides[key])
            continue
        hit = None
        for name in candidates:
            p = bundle / name
            if p.is_file():
                hit = p
                break
        if hit is None:  # fall back to a recursive search
            for name in candidates:
                matches = sorted(bundle.rglob(name))
                if matches:
                    hit = matches[0]
                    break
        found[key] = hit
    return found


def build_canonical_manifest(records: list[dict], id_f: str, sha_f: str, cell_f: str | None) -> bytes:
    """Reference canonicalization, used only as a cross-check against the
    manifest file that ships in the bundle. A mismatch here when every Tier 1
    file hash passes means the original builder used different canonicalization
    rules -- not that the fixture is corrupt."""
    rows = []
    for r in records:
        row = {"context_id": r[id_f], "context_sha256": r[sha_f]}
        if cell_f:
            row["cell"] = r[cell_f]
        rows.append(row)
    rows.sort(key=lambda x: x["context_id"])
    text = json.dumps(rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return (text + "\n").encode("utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="BENCH-0004-E2 fixture verification (gate G2)")
    ap.add_argument("--bundle", required=True, type=Path, help="directory holding the fixture bundle")
    ap.add_argument("--lock", type=Path,
                    default=Path("docs/research/benchmarks/BENCH-0004-E2/FIXTURE_LOCK.json"))
    ap.add_argument("--out", type=Path, default=None,
                    help="path for VERIFICATION.json (default: <bundle>/VERIFICATION.json)")
    for key in ARTIFACTS:
        ap.add_argument(f"--{key.replace('_', '-')}", dest=key, help=f"explicit path to {key}")
    args = ap.parse_args()

    if not args.bundle.is_dir():
        print(f"ERROR: bundle directory not found: {args.bundle}", file=sys.stderr)
        return 2
    if not args.lock.is_file():
        print(f"ERROR: lock file not found: {args.lock}", file=sys.stderr)
        return 2

    lock = json.loads(args.lock.read_text())
    expected = lock["expected_sha256"]
    overrides = {k: getattr(args, k) for k in ARTIFACTS if getattr(args, k)}
    paths = resolve(args.bundle, overrides)

    missing = [k for k, v in paths.items() if v is None or not Path(v).is_file()]
    if missing:
        print("ERROR: gate G1 not satisfied -- fixture source bytes absent.\n", file=sys.stderr)
        for k in missing:
            print(f"  missing: {k}  (looked for {', '.join(ARTIFACTS[k])})", file=sys.stderr)
        print("\nThe handoff bundle must contain the fixture itself, not only protocol documents.",
              file=sys.stderr)
        return 2

    results: list[tuple[str, str, str]] = []
    failures: list[str] = []

    # ---- Tier 1: byte hashes of the frozen files -------------------------
    print("Tier 1 -- byte hashes")
    tier1 = {}
    for key in ARTIFACTS:
        actual = sha256_file(Path(paths[key]))
        want = expected[key]
        ok = actual == want
        tier1[key] = {"path": str(paths[key]), "expected": want, "actual": actual, "pass": ok}
        status = "PASS" if ok else "MISMATCH"
        if not ok:
            failures.append(f"tier1:{key}")
        results.append((key, status, actual))
        print(f"  {key:32} {status}")
        if not ok:
            print(f"    expected {want}")
            print(f"    actual   {actual}")

    # ---- structural invariants -------------------------------------------
    print("\nStructural invariants")
    raw = Path(paths["contexts_jsonl"]).read_text(encoding="utf-8")
    records = [json.loads(line) for line in raw.splitlines() if line.strip()]

    id_f, _ = pick(records[0], ID_FIELDS) if records else (None, None)
    sha_f, _ = pick(records[0], SHA_FIELDS) if records else (None, None)
    text_f, _ = pick(records[0], TEXT_FIELDS) if records else (None, None)
    cell_f, _ = pick(records[0], CELL_FIELDS) if records else (None, None)
    print(f"  field mapping: id={id_f} sha={sha_f} text={text_f} cell={cell_f}")

    if not (id_f and sha_f):
        print("  ERROR: could not locate id/sha fields in the fixture records", file=sys.stderr)
        return 2

    ids = [r[id_f] for r in records]
    shas = [r[sha_f] for r in records]
    checks = [
        ("record count == 96", len(records) == EXPECTED_TOTAL, f"{len(records)}"),
        ("unique context ids == 96", len(set(ids)) == EXPECTED_TOTAL, f"{len(set(ids))}"),
        ("unique context sha256 == 96", len(set(shas)) == EXPECTED_TOTAL, f"{len(set(shas))}"),
    ]
    cell_counts: Counter = Counter()
    if cell_f:
        cell_counts = Counter(r[cell_f] for r in records)
        checks.append(("8 cells present", set(cell_counts) == set(CELLS), f"{len(cell_counts)}"))
        checks.append(("12 contexts per cell",
                       all(cell_counts.get(c) == EXPECTED_PER_CELL for c in CELLS),
                       ", ".join(f"{c}={cell_counts.get(c, 0)}" for c in CELLS)))
    for label, ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        if not ok:
            failures.append(f"structural:{label}")
        print(f"  {label:32} {status}  ({detail})")

    # ---- Tier 2: derived cross-checks ------------------------------------
    print("\nTier 2 -- derived cross-checks (informational when Tier 1 passes)")
    tier2: dict[str, object] = {}

    if text_f:
        mismatched = [r[id_f] for r in records
                      if hashlib.sha256(str(r[text_f]).encode("utf-8")).hexdigest() != r[sha_f]]
        tier2["per_context_sha256_recheck_mismatches"] = mismatched
        print(f"  per-context sha256 recheck        "
              f"{'PASS' if not mismatched else f'{len(mismatched)} MISMATCH'}")
        if mismatched:
            print(f"    first: {mismatched[:5]}")
            print("    note: hashed field was "
                  f"'{text_f}' as raw UTF-8; the original may have hashed a different payload.")
    else:
        tier2["per_context_sha256_recheck_mismatches"] = None
        print("  per-context sha256 recheck        SKIPPED (no context text field)")

    rebuilt = build_canonical_manifest(records, id_f, sha_f, cell_f)
    rebuilt_sha = hashlib.sha256(rebuilt).hexdigest()
    manifest_matches = rebuilt_sha == expected["canonical_context_manifest"]
    tier2["rebuilt_canonical_manifest_sha256"] = rebuilt_sha
    tier2["rebuilt_matches_lock"] = manifest_matches
    print(f"  canonical manifest rebuild        {'PASS' if manifest_matches else 'DIFFERENT'}")
    if not manifest_matches:
        print("    note: the manifest FILE hash in Tier 1 is authoritative. A difference here")
        print("    means this script's canonicalization rules differ from the original builder,")
        print("    not that the fixture is corrupt.")

    # ---- verdict ----------------------------------------------------------
    all_pass = not failures
    stamp = {
        "benchmark": "BENCH-0004-E2",
        "gate": "G2",
        "verified_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "lock_file": str(args.lock),
        "bundle": str(args.bundle),
        "all_pass": all_pass,
        "failures": failures,
        "tier1": tier1,
        "tier2": tier2,
        "field_mapping": {"id": id_f, "sha": sha_f, "text": text_f, "cell": cell_f},
        "cell_counts": dict(cell_counts),
        "contexts_jsonl_sha256": tier1["contexts_jsonl"]["actual"],
    }
    out = args.out or (args.bundle / "VERIFICATION.json")
    out.write_text(json.dumps(stamp, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"\n{'=' * 60}")
    print(f"G2 VERIFICATION: {'PASS' if all_pass else 'FAIL'}")
    print(f"stamp written to {out}")
    if not all_pass:
        print("\nDo NOT modify the fixture to make this pass. Report the mismatch.")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
