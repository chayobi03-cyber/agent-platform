# DEC-0001 — Run falsification benchmark v0.1 and v0.2 as parallel tracks

**Status:** `PROPOSED — awaiting human decision`
**Raised:** 2026-09-02
**Raised by:** Session work on the BENCH-0004-E2 handoff, at the project owner's direction
**Decision owner:** Project owner (human). **This record must not be self-approved.**
**Constitution basis:** §3 human accountability, §7 change governance, §9 evolution

## 1. Why this needs a decision record

The 2026-09-02 handoff introduced `FALSIFICATION_BENCHMARK_v0.2`, a falsification instrument
built on a different axis from the v0.1 already in the repository. v0.1 tests **claims**
(`CLM-0001`…`CLM-0010`); v0.2 tests **architecture hypotheses** (`H01`…`H12`) through a
substitution/ablation matrix (`T01`…`T12`).

Choosing whether v0.2 supersedes v0.1 or runs beside it determines which instrument adjudicates
what. `CLAIM_HYPOTHESIS_MAP.md` and the adjudication boundary "BENCH-0004-E2 adjudicates
CLM-0004 only" both depend on the answer. Constitution §3 places architecture and contract
changes under human ownership, and §7 requires the sequence to terminate in a human decision.

The change was made in session at the owner's direction and is already committed
(`60f131d`). This record exists because the direction was given conversationally and the
governance model does not treat a commit as a decision (Constitution §4: `Commit != human
decision`). Approving or rejecting this record is what makes the state legitimate.

## 2. Decision proposed

**v0.2 runs parallel to v0.1. It does not supersede it.**

| | Track A | Track B |
|---|---|---|
| Document | `FALSIFICATION_BENCHMARK.md` (v0.1) | `FALSIFICATION_BENCHMARK_V2.md` (v0.2) |
| Unit | claim (`CLM-*`) | architecture hypothesis (`H01`–`H12`) |
| Executions | BENCH-0004 R1, R2, E2 | none |

With the consequence that **no benchmark promotes a claim or hypothesis it does not
adjudicate** — specifically, BENCH-0004-E2 produces no evidence for or against H07 or H11.

## 3. Evidence

- v0.1 carries the entire executed BENCH-0004 lineage. Retiring it would orphan three
  execution records and the only evidence the project holds.
- v0.2 has zero executions and two of twelve designs. There is no result that would justify
  retiring the instrument that has evidence in favour of one that has none.
- The two are not substitutes. v0.2's `T07` (asset reuse) and `T11` (asset invalidation) have
  no CLM counterpart; v0.1's `CLM-0003` and `CLM-0004` have no H counterpart. Merging would
  either drop those or force invented counterparts.

## 4. Alternatives considered

| Alternative | Why not |
|---|---|
| v0.2 supersedes v0.1 | Orphans the executed BENCH-0004 lineage; retires the instrument with evidence for one without. |
| Merge into one document | Requires inventing counterparts across four unmapped items; produces exactly the conflation the map exists to prevent. |
| Defer, leave v0.2 out of the repository | Leaves H07/H11 undefined in-repo while the handoff instructs assessing them — the condition that made "assess CLM-0004 / H07 / H11" unexecutable. |

## 5. Risk if approved

Two instruments means two vocabularies. The `T01`–`T12` test IDs collide visually with the
`T`/`R`/`P` factor codes and the `T0R1P1` cell IDs used in BENCH-0004-E2. Mitigated by the
warning in `CLAIM_HYPOTHESIS_MAP.md` §3, but the collision is real and will need care in every
future document that spans both tracks.

## 6. Risk if rejected

`CLAIM_HYPOTHESIS_MAP.md` and the adjudication boundaries must be withdrawn or rewritten, and
the H07/H11 designs (`benchmarks/T07_ASSET_REUSE.md`, `benchmarks/T11_ASSET_INVALIDATION.md`)
lose their parent instrument.

## 7. Scope of this decision

Approving this record decides **only** the parallel-track structure and the adjudication
boundary. It does not accept any v0.2 hypothesis, does not promote any claim, and does not make
either document normative. Both remain candidate instruments.

## 8. Human decision

```text
Decision:        [ ] APPROVED   [ ] REJECTED   [ ] REVISE
Decided by:
Date:
Notes:
```
