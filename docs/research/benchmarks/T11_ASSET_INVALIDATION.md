# T11 — Asset Invalidation (H11)

**Status:** Design / not executed
**Hypothesis:** H11 — once a promoted asset's basis goes stale, reuse is correctly revised, deprecated, blocked, or qualified.
**Falsifier (v0.2):** a stale asset remains indistinguishable from a valid asset.
**Adjudicates:** H11 only. **Not** adjudicated by BENCH-0004-E2 — see `../CLAIM_HYPOTHESIS_MAP.md` §4.

## 1. Design

```text
validated asset  →  inject counterexample / context change  →  reuse attempt  →  observe disposition
```

Required disposition — exactly one must occur, and it must be attributable:

- `REVISED` — asset updated to reflect the new basis
- `DEPRECATED` — asset retired
- `BLOCKED` — reuse refused
- `QUALIFIED` — reuse permitted with an explicit scope caveat
- `ESCALATED` — routed to a human boundary

Silent reuse of a stale asset is the falsifying observation.

## 2. Staleness injection classes

Each class is exercised independently; a system may handle one and fail another.

| Class | Injection |
|---|---|
| S1 direct counterexample | evidence contradicting the asset's finding |
| S2 configuration drift | the configuration the asset was validated under is superseded |
| S3 temporal expiry | the asset's basis passes a declared validity horizon |
| S4 upstream retraction | a source the asset depends on is withdrawn or corrected |
| S5 partial invalidation | only part of the asset's scope goes stale |

S5 is the discriminating case: a system that can only do all-or-nothing invalidation will
either over-block (retiring still-valid scope) or under-block (reusing invalid scope). Both
are reportable failures.

## 3. Metrics

Primary: **stale-asset escape rate** — fraction of stale-reuse attempts that proceed with no
disposition. v0.2 gate: 100% of stale cases blocked, downgraded, or escalated per policy.

Secondary:

| Metric | Direction |
|---|---|
| over-blocking rate (valid asset wrongly retired) | lower |
| detection latency (injection → disposition) | lower |
| disposition attribution completeness | 100% |
| partial-scope precision (S5) | higher |

Over-blocking must be reported alongside escape rate. A system that blocks everything scores
a perfect escape rate and is useless; the pair must be read together.

## 4. Hidden cases

Per v0.2 anti-bias rule 2, stale cases are **hidden**: the staleness injection set is sealed
before execution and is not visible to the system under test or to whoever tunes it. A T11 run
scored against a known injection set does not count.

## 5. Prerequisites

- A promoted asset population (shares T07's blocking gate: `ASSET_LEDGER.md` holds no accepted
  assets yet).
- A declared invalidation policy stating which disposition is required per staleness class.
  Without a predeclared policy, "blocked, downgraded, or escalated according to policy" has no
  referent and the run is unscoreable.

## 6. Relationship to T07

T07 and T11 share an asset population but are scored independently. A system may pass T07
(assets help) and fail T11 (assets keep helping after they stop being true) — that combination
is the specific risk H11 exists to detect, and it is why H07 must not be promoted on T07
evidence alone.

## 7. Result states

`SURVIVED` · `PARTIALLY_SURVIVED` (holds for some staleness classes) · `FALSIFIED`
(stale asset indistinguishable from valid) · `INCONCLUSIVE`.
