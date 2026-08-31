# APF P0 Benchmark Cases v0.1

**Status:** Design-ready / not executed

These cases operationalize the P0 falsification matrix without requiring an APF implementation.

## BENCH-0001 — Work abstraction coverage

**Claim:** CLM-0001

**Question:** Can a work-centric representation preserve essential information and control boundaries across heterogeneous automation workloads without introducing materially greater modeling complexity?

**Task population:** At least 12 representative workflows spanning:
- deterministic automation
- agentic workflow
- human-in-the-loop workflow
- scheduled workflow
- external-system orchestration
- validation/checking workflow

**Conditions:**
- A: agent/tool-centric representation
- B: work-centric representation

**Primary measures:**
- essential-information coverage
- unresolved concepts
- boundary violations
- representation effort
- rework required after new workflow requirements

**Falsifier:** B shows no meaningful coverage/clarity advantage, or repeatedly requires agent/runtime concepts at the core boundary to represent target workflows.

**Critical control:** Neither representation may use undocumented target-platform-specific concepts.

## BENCH-0002 — Capture/context reconstruction

**Claim:** CLM-0002

**Question:** Does lower-friction capture create more retained, later-usable engineering context at acceptable noise/correction cost?

**Task population:** Historical engineering tasks where the operator must reconstruct prior context from available material.

**Conditions:**
- A: manual notes + conventional project search
- B: zero-ceremony capture + automatic structuring + retrieval

**Primary measures:**
- capture completion rate
- time-to-context
- omission rate
- correction actions
- irrelevant/noisy records
- successful reuse rate

**Guardrail:** correctness of the reconstructed context.

**Falsifier:** No meaningful reduction in reconstruction effort/repeated work, or increased noise/correction outweighs retention benefit.

## BENCH-0004 — Retrieval ablation

**Claim:** CLM-0004

**Question:** Is any retrieval improvement attributable specifically to temporal/relationship/provenance reasoning rather than simply better indexing or metadata?

**Conditions:**
- A: lexical/keyword retrieval
- B: semantic retrieval
- C: semantic + metadata filters
- D: relationship + temporal + provenance aware retrieval

**Primary measures:**
- evidence-grounded recall
- relevant-case precision
- false-positive rate
- unsupported-claim rate
- answer utility
- retrieval latency

**Required ablation:** Compare C vs D using the same corpus and metadata availability.

**Falsifier:** D does not outperform C on the declared engineering tasks, or improvement disappears after controlling for indexing/metadata quality.

## BENCH-0006 — Provenance ablation

**Claim:** CLM-0006 (narrowed)

**Question:** Does relevant provenance reduce reproduction/diagnosis time or error for engineering evidence reuse?

**Conditions:**
- A: evidence record without relevant provenance
- B: same evidence plus revision/configuration/tool/setup/time/actor metadata as applicable

**Primary measures:**
- successful reproduction rate
- diagnosis time
- wrong-reuse rate
- expert confidence calibration
- metadata capture/review burden

**Falsifier:** No material reduction in reproduction/diagnosis error or time, or burden dominates the benefit.

**Important:** Do not claim universal necessity from a positive result.

## BENCH-0007 — Approval boundary experiment

**Claim:** CLM-0007

**Question:** Does explicit placement of human approval at consequential boundaries improve safety/quality relative to no gate or poorly placed approval?

**Conditions:**
- A: no approval gate
- B: late/general approval
- C: boundary-specific approval at permission/policy/release/business acceptance events

**Primary measures:**
- harmful/unacceptable action rate
- prevented harmful action rate
- false approval rate
- correction/reversal rate
- approval latency
- escalation load

**Falsifier:** C provides no meaningful risk reduction over the best alternative, or approval cost dominates without compensating risk reduction.

**Critical control:** Keep underlying agent capability constant across conditions.

## BENCH-0009 — Automation promotion threshold

**Claim:** CLM-0009

**Question:** Can net value of an automation candidate be measured reliably enough to support a promotion decision?

**Conditions:**
- baseline/manual workflow
- augmented/automated workflow

**Primary measures:**
- engineer effort saved
- rework cost
- correctness delta
- evidence completeness
- failure/recovery cost
- escalation cost
- net value estimate

**Falsifier:** Net benefit is not reproducible, or positive time savings require unacceptable quality/trust degradation.

**Governance separation:** The experiment estimates evidence for promotion; the decision to require a threshold is a separate human policy decision.

## Cross-case execution rules

1. Declare falsifiers before observing results.
2. Freeze task populations before comparing conditions.
3. Record negative and null results.
4. Preserve raw evidence for every benchmark result.
5. Do not change claim scope to rescue a failed result without recording the original claim and the reason for splitting/weakening it.
6. Replicate successful findings on at least one independent task set before architectural promotion.

## First execution recommendation

Run in this order:

```text
BENCH-0004  retrieval ablation
BENCH-0006  provenance ablation
BENCH-0002  capture/context reconstruction
BENCH-0007  approval boundary
BENCH-0009  automation promotion
BENCH-0001  work abstraction coverage
```

Rationale: retrieval and provenance are narrower and cheaper to falsify; capture and control experiments depend more heavily on user/operator behavior; work abstraction is the broadest and should be tested after the more concrete evidence has matured.
