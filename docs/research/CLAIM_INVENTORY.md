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

This is the **single canonical state vocabulary** for claims and benchmark
results. It is declared here and nowhere else.

```text
DISCOVERED
  ↓
FORMULATED
  ↓
TESTABLE
  ↓
UNTESTED          ← testable, no falsification attempt run yet
  ↓
UNDER_TEST
  ├── SUPPORTED
  ├── WEAKENED
  ├── CONTRADICTED
  ├── FALSIFIED
  ├── INCONCLUSIVE
  └── SPLIT        ← claim contained multiple mechanisms; replaced by narrower claims
```

A state transition requires an evidence reference. `SUPPORTED` does not mean `PROVEN`; it means the current evidence has not defeated the claim and supports the stated scope.

Distinctions that matter and are easy to blur:

- `UNTESTED` means no attempt has been made. It is not doubt about the claim.
- `INCONCLUSIVE` means an attempt was made and settled nothing.
- `WEAKENED` means the claim survives only in a narrower scope.
- `CONTRADICTED` means evidence runs *against* the claim, which is stronger than
  merely failing to support it.
- `FALSIFIED` means a declared failure condition was reproduced and the claim
  does not hold at its stated scope.
- `SPLIT` is a structural outcome, not a result: the claim is replaced by
  narrower mechanism claims, each of which then carries its own state.

Every state is scoped. `FALSIFIED at tested scope` is the honest form; a bare
`FALSIFIED` overclaims exactly as much as a bare `SUPPORTED` would.

### Superseded vocabularies

Two other state lists previously existed in the repository. They are retired,
and mapped here so older references remain readable:

| Retired term | Source | Canonical equivalent |
|---|---|---|
| `RUNNING` | `P0_FALSIFICATION_BENCHMARK_MATRIX` | `UNDER_TEST` |
| `REJECTED` | `P0_FALSIFICATION_BENCHMARK_MATRIX` | `CONTRADICTED` or `FALSIFIED`, depending on whether evidence ran against the claim or reproduced its declared failure condition |
| `UNTESTED` | `P0_FALSIFICATION_BENCHMARK_MATRIX` | adopted into the model above |
| `SPLIT` | `P0_FALSIFICATION_BENCHMARK_MATRIX` | adopted into the model above |

Benchmark result states in `BENCHMARK_REGISTER.md` use this vocabulary.

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

**Current state:** `FALSIFIED at tested scope` — see BENCH-0004 Round 3
(`docs/research/executions/BENCH-0004_R3_2026-09-02.md`).

The statement above is preserved verbatim as the original wording, per
`P0_BENCHMARK_CASES` cross-case execution rule 5. It has been **split** into
CLM-0004a/b/c below, as required by `FALSIFICATION_BENCHMARK` §9 for a claim
containing multiple independent mechanisms. The split was predeclared before
execution and does not depend on the outcome.

**Evidence trail:**

| Round | Design | Result |
|---|---|---|
| BENCH-0004 R1 | document-level recall, 4 docs | no gain over baseline |
| BENCH-0004 R2 | cross-document chains, 7 docs, **hand-specified** graph | +0.208 coverage@2 |
| BENCH-0004 R3 | mechanism decomposition, 21 docs, **derived** graph, null models | **−0.135** coverage@3 |

Round 3 changed the graph from operator-drawn to mechanically derived and the
Round 2 advantage reversed. Round 2's provisional `SUPPORTED` state is therefore
superseded; its result is best explained by operator construction of the graph.
Contradictory evidence remains linked here rather than averaged away, per
`CLAIM_RECONCILIATION` anti-drift rule 7.

#### CLM-0004a — Temporal awareness improves engineering retrieval

**Statement:** Retrieval that weights chronology and commit/revision order
recovers engineering evidence better than an equivalent retriever without
temporal weighting.

**State:** `UNSUPPORTED at tested scope`. Zero change in mean chain coverage at
k=2 and k=3 despite the temporal gate firing on 6/16 queries and reordering 5/16
top-3 sets; below the 95th percentile of a random-commit-order null model.
Temporal weighting moved documents without recovering evidence.

#### CLM-0004b — Provenance awareness improves engineering retrieval

**Statement:** Retrieval that matches on provenance and configuration metadata
recovers engineering evidence better than an equivalent retriever without it.

**State:** `UNSUPPORTED at tested scope`. +0.021, below the predeclared +0.05
threshold; not distinguishable from randomly reassigned provenance text; its only
measured gain fell on temporal questions rather than provenance questions.

**Scope note:** This concerns provenance for *retrieval ranking*. It is a
different claim from CLM-0006, which concerns provenance for *evidence reuse and
reproduction*. Round 3 says nothing about CLM-0006.

#### CLM-0004c — Relationship awareness improves engineering retrieval

**Statement:** Retrieval that propagates relevance across declared relationships
between engineering records recovers evidence better than an equivalent retriever
without relationship propagation.

**State:** `CONTRADICTED at tested scope`. −0.104 mean chain coverage@3,
consistent across every tested weight and degrading monotonically as the weight
increases. It also damaged the neutral control class by −0.25 — questions
answerable from a single obvious document, which no structural mechanism should
affect.

**Retained positive observation:** the mechanically derived graph is *not* noise.
It beat its own degree-preserving shuffle at the 99.5th percentile, and it helped
exactly the claim→benchmark→execution chain questions it was predicted to help.
The failure is in consumption, not in the structure: one-step score propagation
amplifies hubs, and in a governance corpus the best-connected documents are
indexes rather than answers. A hub-penalised or set-expansion consumption
strategy is a separate, narrower hypothesis requiring its own predeclaration.

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
CLM-0001  Work-centric generality          UNTESTED
CLM-0002  Capture value                    UNTESTED
CLM-0004  Structured retrieval value       FALSIFIED at tested scope (R3)
          CLM-0004a temporal               UNSUPPORTED at tested scope
          CLM-0004b provenance (ranking)   UNSUPPORTED at tested scope
          CLM-0004c relationship           CONTRADICTED at tested scope
CLM-0006  Provenance trust (reuse)         UNTESTED — next in execution order
CLM-0007  Human boundary value             UNTESTED
CLM-0009  Measured automation value        UNTESTED
```

The inventory should remain editable. New evidence may split one claim into narrower claims rather than forcing a single broad claim to survive.

CLM-0004 is the first claim to complete that path. It was split into three
mechanism claims and none survived at the tested scope. A falsified P0 claim is a
successful use of this inventory, not a failure of it: the alternative was
adopting relationship-aware retrieval as an architecture contract on the strength
of a result that a null model has now shown to be operator-constructed.

State labels above are scoped to the executed benchmarks. `UNTESTED` means no
falsification attempt has been run, not that the claim is doubted.
