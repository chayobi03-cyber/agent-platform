# DEC-0001 — Benchmark identifier unification and research document consolidation

```yaml
id: DEC-0001
title: Unify benchmark identifiers on BENCH-* and consolidate the research document set
status: DECIDED
date: 2026-09-02
```

## Context

APF's research layer grew document-by-document across sessions. By the time
BENCH-0004 completed three rounds, seven documents covered two subjects:
benchmark definition (3 documents) and reconciliation/traceability
(4 documents).

This is the first decision record in the repository. `docs/decisions/` held zero
records while the research layer had accumulated ten claims, ten benchmarks and
three execution rounds — the governance surface the Constitution requires had
not yet been used.

## Problem

The overlap was not merely redundancy. Three substantive contradictions were in
force simultaneously, and the repository's own contradiction audit
(`MASTER_SESSION_PROMPT`, "Contradiction Audit") had never been applied to its
own documents.

## Evidence

| Finding | Location |
|---|---|
| Two identifier systems for the same benchmarks | `FALSIFICATION_BENCHMARK` §5 used `FB-0004`; `P0_FALSIFICATION_BENCHMARK_MATRIX` and `P0_BENCHMARK_CASES_v0.1` used `BENCH-0004`; `RESEARCH_TO_CLAIM_MAP` §4 used **both in the same table row** |
| Three conflicting execution orders | `FALSIFICATION_BENCHMARK` §12: 0002→0004→0006→0009→0007 · `P0_MATRIX`: 0001→0002→0004→0006→0007→0009 · `P0_BENCHMARK_CASES`: 0004→0006→0002→0007→0009→0001 |
| Three claim/result state models | `CLAIM_INVENTORY` §2 (DISCOVERED→…→FALSIFIED/INCONCLUSIVE) · `P0_MATRIX` (UNTESTED→RUNNING→…→SPLIT→REJECTED) · `FALSIFICATION_BENCHMARK` §7 (SUPPORTED/WEAKENED/FALSIFIED) |
| Two benchmark record templates | `FALSIFICATION_BENCHMARK` §2 and `P0_MATRIX` "Benchmark Record Minimum" |
| Three exit criteria for the same phase | `CLAIM_RECONCILIATION`, `RESEARCH_CORPUS_MAP`, `RESEARCH_TO_CLAIM_RECONCILIATION_STATUS` |
| Monolithic harness blocking reuse | `tools/bench/bench0004_r3.py` at 605 lines mixed reusable infrastructure with the BENCH-0004 specification; BENCH-0006 is next and would have copied ~400 lines |

Concrete consequence, not hypothetical: recording CLM-0004's state after
BENCH-0004 Round 3 required using `FALSIFIED` from one state model and `SPLIT`
from another, because no single vocabulary contained both.

## Contradictions

All three contradictions above were live in `main` and none had been recorded.
Anti-drift rule 7 requires contradictory evidence to remain linked rather than
averaged away; that rule had been applied to research evidence but never to the
governance documents themselves.

## Alternatives

**A — Unify on `FB-*`.** Rejected. Every execution record on disk is named
`BENCH-0004_*` and filenames of evidence records cannot be rewritten. Unifying
on `FB-*` would put the identifier scheme permanently at odds with the evidence
it indexes.

**B — Keep both schemes, add a mapping table.** Rejected. It preserves the
defect and adds a lookup step. The two schemes carried no distinct meaning; they
were an accident of documents written in different sessions.

**C — Delete the emptied documents outright.** Rejected. Execution records cite
those paths and are append-only evidence. Deleting them would create dangling
references inside evidence documents — the same class of provenance defect that
the `fileciteturnNfileM` markers represented and that commit `184139b`
removed.

**D — Unify on `BENCH-*`, consolidate into canonical documents, retain emptied
paths as superseded stubs.** Adopted.

## Risks

| Risk | Mitigation |
|---|---|
| Consolidation silently alters recorded BENCH-0004 R3 evidence | The harness reads its corpus from frozen commit `0d27769`, and `tools/tests/test_reproducibility.py` (committed at `c825c76`, **before** any refactoring) asserts every deterministic output is bit-identical to the recorded results |
| Refactoring the harness changes results through floating-point reordering | Signal application order fixed and documented as part of the specification; null-model RNG stream preserved; verified by the same test |
| Stub files become clutter | Four stubs, each five lines, each naming its replacement |
| Document consolidation changes the benchmark corpus | Recorded in `BENCHMARK_REGISTER` §6: recorded results are unaffected, but a future round against the current corpus measures a different corpus and is not comparable to R1–R3 |

## Recommendation

Adopt alternative D.

## Human decision

Approved by the repository owner (chayobi03@gmail.com) in the working session of
2026-09-02, which selected: full scope covering both documents and code,
unification on `BENCH-*`, and creation of this decision record.

Per `CONSTITUTION.md` §3 and `HOTL_GOVERNANCE`, this transition is
`PROPOSED → ACCEPTED → DECIDED` with the decision owned by a human. The
recommendation was produced by an agent; the decision was not.

## Impact

- Benchmark identity, cases and state are declared once, in `BENCHMARK_REGISTER.md`
- Benchmark method is declared once, in `FALSIFICATION_BENCHMARK.md`
- Claim wording and the single claim/result state vocabulary live in `CLAIM_INVENTORY.md`
- Traceability and reconciliation protocol live in `RESEARCH_TO_CLAIM_MAP.md`
- Corpus status and the single exit criterion live in `RESEARCH_CORPUS_MAP.md`
- Reusable benchmark infrastructure lives in `tools/apfbench/`; per-benchmark
  definitions live in `tools/bench/`

This decision does **not** change any claim state, does not promote any claim,
and does not establish an architecture contract. It changes how the repository
records things, not what it asserts.

## Implementation scope

```text
tools/apfbench/                                    new framework package
tools/bench/bench0004_r3.py                        reduced to benchmark definition
tools/tests/                                       reproducibility + integrity guards
docs/research/BENCHMARK_REGISTER.md                new canonical register
docs/research/FALSIFICATION_BENCHMARK.md           method only
docs/research/CLAIM_INVENTORY.md                   single state vocabulary
docs/research/RESEARCH_TO_CLAIM_MAP.md             absorbed CLAIM_RECONCILIATION
docs/research/RESEARCH_CORPUS_MAP.md               absorbed RECONCILIATION_STATUS
docs/research/P0_FALSIFICATION_BENCHMARK_MATRIX.md superseded stub
docs/research/P0_BENCHMARK_CASES_v0.1.md           superseded stub
docs/research/CLAIM_RECONCILIATION.md              superseded stub
docs/research/RESEARCH_TO_CLAIM_RECONCILIATION_STATUS.md  superseded stub
```

Out of scope: `docs/research/executions/**` (append-only evidence),
`CONSTITUTION.md` invariants, and any claim state.

## Verification plan

```bash
python3 -m unittest discover -s tools/tests -v
```

- `test_reproducibility.py` — recorded BENCH-0004 R3 evidence reproduces
  bit-identically after the refactor
- `test_docs_integrity.py` — no dangling document references, no unresolved
  citation artifacts, exactly one declared execution order, no `FB-*` outside
  the mapping table

## Related assets

- `docs/research/executions/BENCH-0004_R3_2026-09-02.md`
- `docs/research/executions/BENCH-0004_R3_PREDECLARATION.md`
- `RESEARCH_TO_CLAIM_MAP.md` §7 `CONTRA-0001`

## Related commits

```text
c825c76  test: guard BENCH-0004 R3 reproducibility before refactoring
12299b0  refactor: extract apfbench framework from the BENCH-0004 harness
2297385  docs: consolidate benchmark documents into a single register
38d59e7  docs: consolidate traceability and corpus status documents
```

Preceded by `184139b`, which removed the dangling citation artifacts that
motivated the retain-paths-as-stubs choice in alternative D.
