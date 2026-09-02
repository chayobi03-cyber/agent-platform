# BENCH-0004-E2 tooling

Three scripts covering gates G2, G4 and G7 of
`docs/research/benchmarks/BENCH-0004-E2/PROTOCOL.md`.

**Standard library only.** No numpy, pandas, statsmodels, or provider SDK. This is
deliberate: the benchmark must be reproducible in a locked-down environment, and a
dependency that cannot be installed is a gate that cannot be cleared.

## G2 — verify_fixture.py

Recomputes the four locked SHA-256 values from source bytes and checks the structural
invariants. Emits `VERIFICATION.json`, which the runner requires.

```bash
python3 tools/bench0004_e2/verify_fixture.py --bundle <bundle-dir>
```

| Exit | Meaning |
|---|---|
| 0 | all checks passed |
| 1 | hash mismatch or structural violation |
| 2 | gate G1 not satisfied — fixture source bytes absent |

Checks are tiered. **Tier 1** hashes the four frozen files directly and is authoritative.
**Tier 2** rebuilds the canonical manifest and rechecks per-context hashes; when Tier 1
passes, a Tier 2 difference means this script's canonicalization differs from the original
builder, not that the fixture is corrupt.

The fixture is evidence. A mismatch is a finding to report — never edit the fixture to make
verification pass.

## G4 — run_generator.py

Atomic one-pass generation over the 96 frozen contexts.

```bash
# always dry-run first: every precondition is checked, no model call is made
python3 tools/bench0004_e2/run_generator.py \
  --bundle <bundle-dir> --out-dir <run-dir> \
  --config generator.json --system-prompt system.txt --user-template user.tmpl --dry-run
```

`generator.json`:

```json
{"provider": "openai", "model_version": "<pinned immutable version>",
 "temperature": 0.0, "top_p": 1.0, "max_tokens": 2048, "seed": 7}
```

Providers: `openai`, `anthropic` (called over plain HTTP; credential from
`OPENAI_API_KEY` / `ANTHROPIC_API_KEY`). The user template must contain `{context}`.

Refuses to run when: gate G2 is unsatisfied or failed, `answers_96.jsonl` already exists,
`model_version` is `UNSET`, `tools_enabled` is true, or `contexts_96.jsonl` changed since
verification.

A run is atomic. All 96 succeed → journal promoted to `answers_96.jsonl` plus
`ANSWER_MANIFEST.json`. Any context fails → run aborts, journal moves to
`runs/aborted/<utc>/` with `ABORT_REASON.json`, nothing is promoted. Resuming mid-run is
prohibited; a new run restarts from context 1. Retries cover transport failures only — a
completed answer is never discarded and re-requested.

`generated_at_utc` is written as true UTC with a `Z` suffix (PROTOCOL §4.1).

## G7 — analyze_e2.py

Fits `score ~ C(case) + T * R * P * evaluator` and reports whether the mechanism ranking
survives evaluator replacement.

```bash
python3 tools/bench0004_e2/analyze_e2.py \
  --answers <run-dir>/answers_96.jsonl --scores scores.jsonl --out results.json
```

`scores.jsonl`, one row per answer per evaluator:

```json
{"context_id": "...", "evaluator": "A", "factual_correctness": 0.8, "evidence_grounding": 0.6}
```

Response variables are auto-detected from the numeric fields, or named with `--metrics`.

Reports per-term coefficients with t and p; a partial-SS decomposition over case,
mechanism, evaluator and mechanism×evaluator; each evaluator's mechanism ranking; and
whether those rankings agree.

**Reading the result.** Material mechanism effects with a stable ranking support transfer to
answer quality. A dominant evaluator effect or a large mechanism×evaluator interaction means
the advantage is evaluator-sensitive and must not be promoted as an architecture invariant.

## Verification status of the tooling

Exercised against synthetic fixtures in a scratch directory — never against the real
fixture, which is unavailable.

| Check | Result |
|---|---|
| `verify_fixture` on a valid bundle | PASS (exit 0) |
| `verify_fixture` on a tampered fixture | MISMATCH caught at Tier 1 (exit 1) |
| `verify_fixture` on the docs-only handoff bundle | G1 blocker reported (exit 2) |
| runner preconditions (UNSET model, existing answer set, missing G2 stamp) | all refused with exit 2 |
| runner success path | 96/96 frozen, manifest emitted |
| runner abort at context 40 | 39 rows retained unpromoted, `answers_96.jsonl` never created |
| t and F p-values | agree with published critical values and with numerical integration to ~1e-14 |
| OLS coefficients, R², se | match hand-computed regression exactly; `F == t²` at 1 df |
| planted-effect recovery | recovered T/R/P and evaluator bias; correctly reported no interaction |
| planted evaluator-sensitivity | detected flipped ranking and interaction (F=86.3, p<0.0001) |
