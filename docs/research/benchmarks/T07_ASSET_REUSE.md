# T07 — Asset Reuse (H07)

**Status:** Design / not executed
**Hypothesis:** H07 — a validated finding promoted to an asset measurably improves subsequent execution.
**Falsifier (v0.2):** the asset is just retrieved text with no operational effect.
**Adjudicates:** H07 only. **Not** adjudicated by BENCH-0004-E2 — see `../CLAIM_HYPOTHESIS_MAP.md` §4.

## 1. Why this cannot ride on E2

E2 has no asset promotion step, no second run, and no execution outcome — it scores answer
quality over a frozen fixture. H07 asks whether promoting a *validated* finding changes what
happens on the **next** run. Different object, different design.

## 2. Design

```text
Run #1  →  finding  →  validation  →  asset promotion  →  Run #2      (treatment)
Run #1  →  finding  →  validation  →  (no promotion)   →  Run #2'     (control)
```

Run #2 and Run #2' are matched on task, executor, and starting state. The only manipulated
variable is asset availability.

## 3. The load-bearing confound

An asset that contains the answer will improve outcomes trivially. That result would be
uninformative about H07 and must be designed out.

Required controls:

- **C1 — Leakage split.** Tasks are partitioned into *answer-adjacent* (the asset contains
  content that directly resolves the task) and *process-bearing* (the asset changes planning,
  ordering, tool choice, or failure avoidance without containing the answer). H07 is
  adjudicated on the process-bearing partition. The answer-adjacent partition is reported
  separately as a leakage ceiling, never pooled into the headline effect.
- **C2 — Inert-asset arm.** A third arm supplies a length- and format-matched asset with the
  operative content removed. If Run #2 beats Run #2' but does not beat the inert arm, the
  effect is presentation, not asset content.
- **C3 — Executor blinding where feasible.** The executor is not told which arm it is in.

Without C1 and C2, a positive result does not support H07.

## 4. Metrics

Primary (per v0.2 scorecard, "asset reuse lift"):

| Metric | Direction |
|---|---|
| task success rate | higher |
| error rate | lower |
| execution latency | lower |
| decision quality (rubric) | higher |

Secondary: rework count, escalation count, steps to completion, unsupported-claim rate.

Effect size must be **predeclared** before the first run. Per v0.2 promotion logic, H07 is
`SURVIVED` only with a predefined non-trivial effect on at least one outcome metric in **two
domains**.

## 5. Domains

Two minimum, drawn from the v0.2 dataset axes, materially different:

1. EMC / engineering analysis
2. document / review automation

A third (general business operation) is optional and does not substitute for either.

## 6. Anti-bias requirements

- Hidden cases reserved before any scoring (v0.2 anti-bias rule 2).
- Thresholds fixed before the first run; changing them after seeing results requires a
  decision record (v0.2 scorecard note).
- Implementation convenience is not architectural validity (rule 4).

## 7. Prerequisites

- An asset promotion path must exist and be recorded (`ASSET_LEDGER.md` state model:
  `RAW_FINDING → ASSET_CANDIDATE → REVIEWED → ACCEPTED_ASSET`).
- The ledger currently holds **no accepted assets**, so T07 has no promotable input yet.
  This is the T07 blocking gate.

## 8. Result states

`SURVIVED` · `PARTIALLY_SURVIVED` (effect only in one domain or only answer-adjacent) ·
`FALSIFIED` (no operational effect beyond the inert arm) · `INCONCLUSIVE`.
