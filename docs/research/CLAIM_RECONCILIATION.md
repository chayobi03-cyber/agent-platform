# APF Claim Reconciliation Protocol v0.1

**Status:** Experimental / verification infrastructure

## Purpose

Prevent research accumulation from silently becoming architecture. Every reusable research asset must be reconciled against a claim state before it can influence an APF architectural contract.

## Reconciliation Unit

For each `ASSET-*` or research finding:

```text
SOURCE → FINDING → ASSET → CLAIM → EVIDENCE → FALSIFIER → BENCHMARK → DECISION
```

A source may produce multiple findings; a finding may support multiple claims; a claim may be supported and contradicted by multiple assets.

## Mandatory Outcomes

Every reviewed research item receives exactly one disposition:

- `CLAIM_SUPPORT` — provides evidence supporting an existing claim
- `CLAIM_CONTRADICTION` — conflicts with an existing claim
- `NEW_CLAIM` — introduces a claim not represented in the inventory
- `REFERENCE_ONLY` — useful reference, no APF claim implied
- `DUPLICATE` — semantically redundant with an existing item
- `OUT_OF_SCOPE` — outside the current APF boundary
- `INSUFFICIENT` — interesting assertion but not yet sufficiently specified to become a falsifiable claim

## Anti-Drift Rules

1. Framework popularity is not evidence for an APF claim.
2. Repeated sources do not count as independent evidence unless their evidence-generating conditions are meaningfully independent.
3. A successful prototype is runtime evidence, not architectural proof.
4. An accepted asset does not authorize implementation.
5. A claim without an explicit plausible falsifier is incomplete.
6. A benchmark that cannot distinguish the claim from a baseline is invalid.
7. Contradictory evidence must remain linked; do not average it away.
8. Claim wording must be narrower than or equal to its evidence scope.
9. Architecture candidates cannot be promoted solely from qualitative agreement.
10. Human decisions remain separate from measured results.

## Claim Quality Gate

A claim is `BENCHMARK_READY` only when all are present:

```text
statement
scope
observable_prediction
falsifier
baseline
metric
benchmark_case
known_counter_evidence
```

A claim becomes `ARCHITECTURE_CANDIDATE` only after:

```text
benchmark execution
+ result recorded
+ counter-evidence reviewed
+ scope updated
+ explicit decision record
```

## Recommended Reconciliation Table

| Asset | Claim | Relation | Evidence class | Contradiction | Falsifier | Benchmark | State |
|---|---|---|---|---|---|---|---|
| ASSET-* | CLM-* | support/contradict | external/repo/runtime/eval/human | linked claim | explicit condition | BENCH-* | state |

## Review Questions

Before accepting a claim:

1. What observation would make this claim less plausible?
2. What is the strongest reasonable baseline?
3. Can the benchmark be run without depending on the proposed architecture?
4. Could the result be explained by a simpler mechanism?
5. What evidence would distinguish APF-specific value from generic tooling value?
6. What evidence would cause us to weaken, split, defer, or reject the claim?

## Exit Condition for This Phase

Do not declare the architecture validated. Exit only when the current research corpus has a traceable disposition and every P0 claim has a benchmark or an explicit `INSUFFICIENT` reason.
