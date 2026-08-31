# APF Claim Inventory v0.1

**Status:** Working inventory / non-normative
**Purpose:** Convert APF research and design assertions into explicit, falsifiable claims before architecture adoption.

## 1. Why a Claim Inventory exists

The Research Asset Ledger records reusable findings and candidate assets. It is insufficient by itself for evaluating whether an APF assertion is actually supported.

A Claim is the smallest reviewable statement that can be:

```text
supported / weakened / contradicted / falsified / left unresolved
```

The Claim Inventory therefore sits between research assets and architecture decisions:

```text
Research Finding
      ↓
Research Asset Candidate
      ↓
CLAIM INVENTORY
      ↓
Evidence + Counter-evidence
      ↓
Falsification Benchmark
      ↓
Human Decision
      ↓
Architecture / Implementation
```

A claim does **not** become an APF invariant merely because it is repeated across sources.

## 2. Claim state model

```text
DISCOVERED
  ↓
FORMULATED
  ↓
TESTABLE
  ↓
UNDER_TEST
  ├── SUPPORTED
  ├── WEAKENED
  ├── CONTRADICTED
  ├── FALSIFIED
  └── INCONCLUSIVE
```

A state transition requires an evidence reference. `SUPPORTED` does not mean `PROVEN`; it means the current evidence has not defeated the claim and supports the stated scope.

## 3. Claim taxonomy

Use the smallest useful class:

- PRODUCT — user/workflow value claim
- SEMANTIC — claim about a reusable domain concept or relation
- ARCHITECTURAL — claim about system structure or boundaries
- OPERATIONAL — claim about runtime behavior, reliability, or maintainability
- CONTROL — claim about permission, policy, governance, or human accountability
- EVALUATION — claim about measurement, benchmark validity, or fitness
- SECURITY — claim about threat resistance or isolation

## 4. Required claim record

```yaml
claim_id: CLM-0001
title:
statement:
claim_type: PRODUCT | SEMANTIC | ARCHITECTURAL | OPERATIONAL | CONTROL | EVALUATION | SECURITY
scope:
non_scope:
source_assets: []
origin:
mechanism:
preconditions: []
observable_prediction:
falsifier:
minimum_evidence:
preferred_evidence:
counter_evidence: []
benchmark_refs: []
related_claims: []
related_decisions: []
current_state: DISCOVERED | FORMULATED | TESTABLE | UNDER_TEST | SUPPORTED | WEAKENED | CONTRADICTED | FALSIFIED | INCONCLUSIVE
confidence:
owner:
last_reviewed:
notes:
```

## 5. Quality gate for a usable claim

A claim is `TESTABLE` only when all of the following are present:

1. A bounded statement rather than a slogan.
2. A defined scope and explicit non-scope.
3. An observable prediction or expected behavior.
4. At least one plausible falsifier.
5. A minimum evidence requirement.
6. A way to distinguish the claim from a nearby competing explanation.

Claims that cannot satisfy these conditions remain research observations, not architecture inputs.

## 6. Initial APF claim candidates

These are intentionally hypotheses, not accepted APF invariants.

### CLM-0001 — Work-centric abstraction is more general than agent-centric abstraction

**Statement:** A platform organized around work, automation opportunity, execution, evidence, and outcome can support both agentic and non-agentic automation without making an agent runtime the core abstraction.

**Falsifier:** Important target workloads require agent-specific concepts at the core boundary such that the work-centric model consistently loses essential information or creates materially worse implementation/control complexity.

**Benchmark direction:** Compare a representative workload matrix modeled with a work-centric core versus an agent-centric core.

### CLM-0002 — Zero-ceremony capture increases usable engineering memory

**Statement:** Reducing capture friction while automatically structuring content increases the amount of project history that is actually retained and later reusable.

**Falsifier:** Lower-friction capture does not increase retained/retrievable engineering context, or the resulting semantic noise offsets the benefit.

**Benchmark direction:** Capture rate, reconstruction time, retrieval usefulness, correction burden, and noise rate versus a manual-note baseline.

### CLM-0003 — Progressive disclosure improves engineering usability without reducing evidence access

**Statement:** Showing summary/context first and allowing drill-down to history, evidence, and raw artifacts reduces interaction burden while preserving access to verification detail.

**Falsifier:** Users make materially more incorrect judgments, cannot reach evidence efficiently, or interaction cost remains equal/worse than an evidence-dense interface.

**Benchmark direction:** Task completion time, error rate, evidence lookup time, and drill-down frequency.

### CLM-0004 — Temporal/provenance-aware history improves engineering retrieval

**Statement:** Retrieval that understands chronology, provenance, configuration, and relationships recovers useful engineering reasoning better than flat semantic retrieval alone for target engineering questions.

**Falsifier:** A conventional semantic baseline matches or exceeds useful-case recall/precision and grounding on representative tasks, or the added structure creates unacceptable maintenance cost.

**Benchmark direction:** Same corpus and questions; compare flat semantic retrieval with relationship/provenance-aware retrieval.

### CLM-0005 — Failed attempts are first-class engineering evidence

**Statement:** Preserving rejected hypotheses, failed experiments, and superseded decisions improves future engineering decisions by preventing repeated dead ends and clarifying decision history.

**Falsifier:** Failure-history access produces no measurable reduction in repeated work/errors, or false-history contamination creates larger costs than its benefit.

**Benchmark direction:** Repeated-issue rate, time-to-resolution, decision confidence, and false-recall rate.

### CLM-0006 — Provenance/configuration is necessary for trusted engineering evidence

**Statement:** Engineering evidence lacking relevant revision/configuration/tool/setup provenance is materially less trustworthy for reuse and audit than evidence carrying that context.

**Falsifier:** Target decisions remain equally reliable without provenance, or provenance collection imposes disproportionate burden without measurable benefit.

**Benchmark direction:** Blind provenance ablation versus full-provenance condition; assess expert agreement and reuse error.

### CLM-0007 — Human approval belongs at consequential boundaries

**Statement:** Explicit human ownership/approval at architecture, permission, policy exception, release, and business-acceptance boundaries reduces unacceptable autonomous outcomes relative to unrestricted execution.

**Falsifier:** Approval gates do not reduce material risk/error, or their latency/operational cost overwhelms the benefit for the intended workload class.

**Benchmark direction:** Controlled scenarios measuring prevented harmful actions, false approvals, latency, and escalation load.

### CLM-0008 — External frameworks should be extracted into primitives rather than copied into APF contracts

**Statement:** Framework-neutral primitives preserve more portability and reduce accidental coupling while retaining the reusable value of external systems.

**Falsifier:** Direct adoption of a framework abstraction consistently provides superior portability, clarity, operability, and lifecycle fitness for target workloads.

**Benchmark direction:** Cross-framework capability matrix plus implementation migration/extension exercise.

### CLM-0009 — Automation should be promoted only when measured work reduction exists

**Statement:** Candidate automation should be promoted when it reduces engineer effort while maintaining required correctness, evidence quality, and trust.

**Falsifier:** Work reduction is not reproducible, or gains require unacceptable quality/trust degradation.

**Benchmark direction:** Baseline/manual versus augmented workflow with time, rework, correctness, evidence completeness, and escalation metrics.

### CLM-0010 — Engineering Work Augmentation is a more testable initial product thesis than a generic Agent Platform

**Statement:** Framing APF around concrete engineering-work augmentation produces more measurable user value and lower validation risk than starting from a generic agent-building surface.

**Falsifier:** Generic agent-builder framing attracts more validated high-value workflows with equal/lower effort and stronger evidence, or engineering augmentation does not generalize beyond the initial domain.

**Benchmark direction:** Compare opportunity discovery and validation outcomes across representative non-agentic, agentic, and engineering-augmentation workflows.

## 7. Claim-to-Asset relation

A research asset may support multiple claims; a claim may depend on multiple assets. Do not collapse either relation.

```text
Asset A ─┬─→ Claim 1
Asset B ─┼─→ Claim 1
Asset C ─└─→ Claim 2

Claim 1 ─→ Benchmark B1
Claim 1 ─→ Decision D1
```

Contradictory assets must remain linked to the claim rather than being silently discarded.

## 8. Promotion rule

No claim should be promoted to:

```text
APF invariant / architecture contract / implementation dependency
```

without:

```text
claim record
+ supporting evidence
+ explicit counter-evidence review
+ falsification attempt
+ scope statement
+ human decision where consequential
```

## 9. Initial review priority

P0 claims should be tested first where failure would invalidate broad portions of the platform thesis:

```text
CLM-0001  Work-centric generality
CLM-0002  Capture value
CLM-0004  Structured retrieval value
CLM-0006  Provenance trust
CLM-0007  Human boundary value
CLM-0009  Measured automation value
```

The inventory should remain editable. New evidence may split one claim into narrower claims rather than forcing a single broad claim to survive.
