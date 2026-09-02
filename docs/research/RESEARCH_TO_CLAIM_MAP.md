# APF Research → Claim → Benchmark Traceability v0.1

**Status:** Canonical traceability and reconciliation protocol
**Purpose:** Prevent useful research from remaining as disconnected notes while also preventing unverified research from becoming architecture.

**Absorbed:** `CLAIM_RECONCILIATION.md` (dispositions, anti-drift rules, quality
gates, review questions) merged in on 2026-09-02 under
`docs/decisions/DEC-0001-benchmark-id-and-doc-consolidation.md`.

## 1. Traceability chain

APF research is now intended to be traceable through four distinct objects:

```text
RESEARCH ASSET
   │
   ├── supports ──→ CLAIM
   │                  │
   │                  ├── tested by ──→ BENCHMARK
   │                  │                   │
   │                  │                   └── produces ──→ EVIDENCE
   │                  │
   │                  └── informs ──→ DECISION
   │
   └── contradicts ──→ CLAIM
```

The direction matters: a source can support or contradict a claim without being adopted as an APF asset.

## 2. Object boundaries

### Research Asset

A reusable finding, primitive, pattern, mechanism, or observation extracted from research.

### Claim

A bounded proposition about APF, its users, its architecture, or a mechanism that can be tested and potentially falsified.

### Benchmark

A repeatable comparison or experiment intended to challenge a claim.

### Evidence

An observed artifact supporting, weakening, or contradicting a claim. Evidence should preserve its origin and relevant provenance.

### Decision

A human-owned determination to adopt, reject, defer, or otherwise constrain a claim or asset.

## 3. Required relationship types

Use explicit relations instead of free-form prose whenever possible:

```text
ASSET SUPPORTS CLAIM
ASSET CONTRADICTS CLAIM
CLAIM DEPENDS_ON CLAIM
CLAIM TESTED_BY BENCHMARK
BENCHMARK PRODUCES EVIDENCE
EVIDENCE SUPPORTS CLAIM
EVIDENCE WEAKENS CLAIM
EVIDENCE FALSIFIES CLAIM
DECISION ADDRESSES CLAIM
DECISION ADOPTS ASSET
DECISION REJECTS ASSET
```

## 4. Initial traceability register

| Research area / source family | Candidate asset | Claim refs | Benchmark refs | Current disposition |
|---|---|---|---|---|
| APF work-centric research | Work / Opportunity boundary | CLM-0001, CLM-0010 | BENCH-0001, BENCH-0010 | Candidate; test before contract |
| Engineering capture lesson | Zero-Ceremony Capture | CLM-0002 | BENCH-0002 | High-priority experiment |
| Progressive-disclosure lesson | Summary → Context → History → Evidence → Raw artifact | CLM-0003 | BENCH-0003 | Product/UX hypothesis |
| Engineering history lesson | Temporal/provenance/relation-aware history | CLM-0004, CLM-0005, CLM-0006 | BENCH-0004, BENCH-0005, BENCH-0006 | Mechanisms separated in BENCH-0004 R3; CLM-0004 falsified at tested scope and split into a/b/c. CLM-0005 and CLM-0006 untested |
| HoTL governance | Human decision boundaries | CLM-0007 | BENCH-0007 | Candidate control invariant |
| Framework research | Framework-neutral primitive extraction | CLM-0008 | BENCH-0008 | Cross-framework comparison required |
| Automation lesson | Measured work reduction | CLM-0009 | BENCH-0009 | Promotion criterion |
| Engineering augmentation thesis | Engineering Work Augmentation | CLM-0010 | BENCH-0010 | Product thesis, not architecture |

## 5. Current known gaps

The repository foundation currently has a Research Asset Ledger and governance/architecture workspaces, but no accepted assets or established architecture contracts (`docs/research/ASSET_LEDGER.md`: "no asset is accepted by default"; `docs/architecture/README.md`: "No Platform Contract or Architecture Decision is finalized yet").

The main gap is therefore **not more research volume**. The main gap is converting existing and future findings into reviewable claims with explicit falsifiers and benchmarks.

## 6. Research ingestion rule

For each new research source:

```text
1. Extract findings.
2. Identify reusable primitives.
3. Record candidate asset.
4. Derive one or more bounded claims.
5. Record supporting and contradictory evidence separately.
6. Define falsifier.
7. Attach a benchmark or explain why the claim is not yet testable.
8. Only then consider architecture impact.
```

Research source → architecture decision is an invalid shortcut.

## 7. Contradiction register

Contradictions must remain explicit. At minimum record:

```yaml
contradiction_id:
claim_ref:
asset_a:
asset_b:
conflict:
possible_scope_difference:
possible_context_difference:
resolution_status: OPEN | EXPLAINED | TESTED | UNRESOLVED
benchmark_ref:
notes:
```

A contradiction may resolve by scope separation rather than selecting one source as universally correct.

### Registered contradictions

```yaml
contradiction_id: CONTRA-0001
claim_ref: CLM-0004 / CLM-0004c
asset_a: docs/research/executions/BENCH-0004_R2_2026-08-31.md
asset_b: docs/research/executions/BENCH-0004_R3_2026-09-02.md
conflict: >
  R2 measured relationship/temporal-aware retrieval beating the semantic+metadata
  baseline by +0.208 chain coverage@2 and provisionally supported a narrow
  cross-document subclaim. R3 measured the same mechanism family losing to the
  same baseline by -0.135 chain coverage@3, and the relationship mechanism in
  isolation losing by -0.104 at every tested weight.
possible_scope_difference: >
  R2 used a 7-document corpus; R3 used 21. R2 scored coverage@2; R3 @2/@3/@5.
  Neither difference accounts for a sign reversal: R3's deficit holds at k=2
  (0.4688 vs 0.6771) as well.
possible_context_difference: >
  The decisive difference is graph construction. R2's relationship graph was
  hand-specified by the operator who also authored the questions. R3 derived
  edges mechanically from filename mentions and shared identifiers, with no
  operator discretion, and added a degree-preserving null model.
resolution_status: TESTED
benchmark_ref: BENCH-0004 R3
notes: >
  Resolved in favour of R3, not by recency but by control quality: R3 carries the
  null models, the neutral control class and the weight sweep that R2 lacked, and
  its null model directly implicates the variable R2 left uncontrolled. R2's
  provisional SUPPORTED state is superseded. R2 is retained as linked
  counter-evidence rather than deleted, per anti-drift rule 7.
  Residual finding preserved from R3: the derived graph beats its own null
  distribution at the 99.5th percentile, so the relationship structure is real
  even though propagating scores across it degrades retrieval.
```

## 8. Confidence rule

Confidence should not be a single subjective number detached from evidence. Prefer a structured description:

```text
source diversity
+ evidence class diversity
+ replication
+ adversarial resistance
+ baseline advantage
+ scope stability
```

A high-confidence claim can still be narrow. A broad claim with weak scope control should not be promoted merely because many sources mention similar ideas.

## 9. Architecture gate

No item should enter the architecture contract workspace as a stable primitive unless the trace is visible:

```text
candidate primitive
→ supporting asset(s)
→ bounded claim
→ counter-evidence review
→ falsification attempt
→ result
→ human decision
```

This keeps the current APF Constitution boundary intact: research, assets, decisions, implementation, and verification are distinct states and artifacts (`CONSTITUTION.md` §4 State Separation).

## 10. Reconciliation dispositions

Absorbed from `CLAIM_RECONCILIATION`. Every reviewed research item receives
exactly one disposition:

- `CLAIM_SUPPORT` — provides evidence supporting an existing claim
- `CLAIM_CONTRADICTION` — conflicts with an existing claim
- `NEW_CLAIM` — introduces a claim not represented in the inventory
- `REFERENCE_ONLY` — useful reference, no APF claim implied
- `DUPLICATE` — semantically redundant with an existing item
- `OUT_OF_SCOPE` — outside the current APF boundary
- `INSUFFICIENT` — interesting assertion, not yet specified enough to be falsifiable

Recommended reconciliation table:

| Asset | Claim | Relation | Evidence class | Contradiction | Falsifier | Benchmark | State |
|---|---|---|---|---|---|---|---|
| ASSET-* | CLM-* | support/contradict | external/repo/runtime/eval/human | linked claim | explicit condition | BENCH-* | state |

## 11. Anti-drift rules

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

Rule 7 is why §7 above retains BENCH-0004 Round 2 as linked counter-evidence
rather than deleting it once Round 3 reversed its result.

## 12. Claim quality gates

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

These gates sit downstream of the visible-trace requirement in §9. §9 asks
whether the trace exists; these ask whether it is strong enough to act on.

## 13. Review questions before accepting a claim

1. What observation would make this claim less plausible?
2. What is the strongest reasonable baseline?
3. Can the benchmark be run without depending on the proposed architecture?
4. Could the result be explained by a simpler mechanism?
5. What evidence would distinguish APF-specific value from generic tooling value?
6. What evidence would cause us to weaken, split, defer, or reject the claim?

Question 4 is the one BENCH-0004 Round 2 failed: a hand-specified relationship
graph was a simpler explanation of its result than relationship awareness, and
it was not controlled for until Round 3.

## 14. Immediate next work

The next research pass should populate the register with actual source-level records rather than adding more generic framework notes.

Priority order:

```text
P0-A  inventory all existing APF research assets / notes
P0-B  deduplicate and cluster into claim families
P0-C  identify contradictory evidence
P0-D  instantiate benchmark cases
P0-E  run the first falsification experiments
P0-F  promote only surviving, scoped claims toward architecture decisions
```

The goal is not to maximize the number of accepted claims. The goal is to maximize the number of **useful, bounded, falsifiable claims** while making failed claims and uncertainty visible.
