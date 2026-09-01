# APF Claim ↔ Hypothesis Map

**Status:** Established 2026-09-01 / non-normative bridge document
**Purpose:** Keep the two falsification tracks parallel without letting either silently
adjudicate the other.

## 1. Two parallel tracks

APF now carries two falsification instruments on different axes. Neither replaces the other.

| | Track A | Track B |
|---|---|---|
| Document | `FALSIFICATION_BENCHMARK.md` (v0.1) | `FALSIFICATION_BENCHMARK_V2.md` (v0.2) |
| Unit | Claim (`CLM-0001`…`CLM-0010`) | Architecture hypothesis (`H01`…`H12`) |
| Asks | Is this product/semantic claim supported? | Does the architecture survive substitution/ablation? |
| Record | `FB-0001` benchmark record template | `T01`…`T12` test matrix |
| Executions | `BENCH-0004` R1, R2, E2 | none yet |

**Parallel decision:** v0.2 does not supersede v0.1. v0.1 retains benchmark continuity for
the CLM series and the executed BENCH-0004 lineage; v0.2 adds an architecture-level axis
with no executed evidence yet. There is no result that would justify retiring v0.1.

## 2. Correction to the handoff premise

The 2026-09-02 handoff stated that H07 and H11 were already defined as independent
falsification tests "in the claim inventory". They were not.

Verified 2026-09-01 against the repository:

- `docs/research/CLAIM_INVENTORY.md` contains `CLM-0001`…`CLM-0010` only.
- Repository-wide search for `H07`, `H11`, or any `H0*` hypothesis identifier returned
  **zero matches** before this commit.
- H07 and H11 existed solely inside the handoff copy of `FALSIFICATION_BENCHMARK_v0.2.md`,
  which was outside the repository evidence chain.

The H series enters the repository with this commit. Until then, any statement of the form
"assess CLM-0004 / H07 / H11" was not executable, because two of its three targets had no
repository definition.

## 3. Identifier collision warning

Two unrelated `T` namespaces are now in play. Do not conflate them.

| Symbol | Namespace | Meaning |
|---|---|---|
| `T`, `R`, `P` | BENCH-0004-E2 factor codes | temporal / relationship / provenance retrieval mechanisms |
| `T0R1P1`, `T1R1P1`, … | BENCH-0004-E2 cell IDs | one of 8 factorial cells |
| `T01`…`T12` | v0.2 test matrix IDs | architecture falsification tests |

`T07` is a v0.2 **test ID** (asset reuse). It is not a T/R/P factor level and has nothing to
do with the temporal mechanism in BENCH-0004.

## 4. Adjudication boundaries

The load-bearing rule:

```text
BENCH-0004-E2 adjudicates CLM-0004 ONLY.
E2 results are NOT evidence for or against H07 or H11.
```

E2 measures whether retrieval/context mechanism gains transfer to LLM answer quality.
H07 measures whether a *validated, promoted asset* changes downstream planning/execution
outcomes. H11 measures whether a promoted asset is correctly revised, deprecated, or
blocked once its basis goes stale. These are different experimental objects: E2 has no
asset promotion step, no second run, and no staleness injection, so it cannot produce
evidence about either.

| Target | Adjudicating benchmark | Status |
|---|---|---|
| CLM-0004 | BENCH-0004 R1, R2, **E2** | INCONCLUSIVE — E2 blocked at G1 |
| H07 | **T07** — `benchmarks/T07_ASSET_REUSE.md` | OPEN / not designed until now, not executed |
| H11 | **T11** — `benchmarks/T11_ASSET_INVALIDATION.md` | OPEN / not designed until now, not executed |

## 5. CLM ↔ H correspondence

Correspondence is thematic, not substitutive. A result on one side does not transfer to the
other without its own execution.

| H | v0.2 target | Thematically related CLM | Relation |
|---|---|---|---|
| H01 | portable execution overhead | CLM-0001, CLM-0008 | partial |
| H02 | executor substitution | CLM-0001, CLM-0008 | partial |
| H03 | evidence/provenance separation | CLM-0006 | partial |
| H04 | validation separation | CLM-0009 | partial |
| H05 | decision durability | CLM-0007 | partial |
| H06 | domain substitution | CLM-0001, CLM-0010 | partial |
| H07 | asset reuse | CLM-0002, CLM-0005 | partial |
| H08 | capability ablation | CLM-0008 | partial |
| H09 | identity substitution | — | **no CLM counterpart** |
| H10 | authorization substitution | — | **no CLM counterpart** |
| H11 | asset invalidation | CLM-0005, CLM-0006 | partial |
| H12 | living-spec integrity | CLM-0005 | partial |

Unmapped in the other direction:

- `CLM-0003` (progressive disclosure) — no H counterpart.
- `CLM-0004` (structured retrieval) — no H counterpart; tested only via BENCH-0004.

These gaps are recorded, not closed. Inventing an H for CLM-0004 to make the tables
symmetric would create the exact conflation this document exists to prevent.

## 6. Promotion rule

Unchanged from v0.1 §8 and v0.2 promotion logic, restated for the bridge:

- CLM-0004 may not be promoted on retrieval/context evidence alone.
- H07 and H11 require survival in at least two domains before strategic promotion.
- No claim or hypothesis is promoted by a benchmark that does not adjudicate it.
