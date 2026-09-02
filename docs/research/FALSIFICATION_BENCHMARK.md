# APF Falsification Benchmark v0.1

**Status:** Canonical benchmark method
**Purpose:** Provide a repeatable method for attempting to disprove APF claims before promoting them into architecture contracts or implementation dependencies.

**Scope boundary.** This document defines *how* a falsification benchmark is
designed and judged. Which benchmarks exist, what each tests and what state each
is in are declared in `BENCHMARK_REGISTER.md`. Claim wording and claim state are
declared in `CLAIM_INVENTORY.md`. See
`docs/decisions/DEC-0001-benchmark-id-and-doc-consolidation.md`.

## 1. Benchmark principle

APF validation must not ask only:

> Does the proposed mechanism work?

It must also ask:

> Under what conditions does the claim fail, and does the proposed abstraction still outperform a simpler or competing alternative?

The benchmark therefore compares claims against explicit baselines and adversarial conditions.

```text
CLAIM
  ↓
PREDICTION
  ↓
BASELINE / ALTERNATIVE
  ↓
TEST SCENARIO
  ↓
FALSIFIER
  ↓
MEASUREMENT
  ↓
RESULT
  ↓
CLAIM STATE UPDATE
```

## 2. Benchmark record

This is the single benchmark record template. It merges the fields formerly
split between this document and `P0_FALSIFICATION_BENCHMARK_MATRIX`.

```yaml
benchmark_id: BENCH-0001
title:
claim_refs: []
objective:
workload_class:
task_population:
minimum_sample:
sample_size:
baseline:
candidate:
controls: []
variables: []
operator_profile:
scenarios: []
adversarial_cases: []
inputs:
primary_metrics: []
secondary_metrics: []
acceptance_rule:
predeclared_falsifier:
evidence_type: RUNTIME_EVIDENCE | EVALUATION_EVIDENCE | HUMAN_DECISION_EVIDENCE
artifacts: []
result:
counter_observations:
limitations:
reproducibility:
conclusion:
claim_update:
next_action:
reviewer:
review_date:
```

## 3. Required comparison discipline

Every benchmark should define, where applicable:

### A. Baseline

The simplest credible existing method. Examples include manual workflow, flat document retrieval, conventional semantic search, or current commercial automation.

### B. Candidate

The APF mechanism being tested.

### C. Alternative explanation

A plausible reason the candidate may appear better that is unrelated to the claimed mechanism, such as better prompt wording, more data, more compute, or higher operator attention.

### D. Failure boundary

An explicit condition under which the claim should be considered weakened or falsified.

### E. Cost

Engineering and operational cost must be measured alongside benefit. A technically superior result can still fail the platform fitness test if its maintenance, latency, data burden, or operator burden is disproportionate.

## 4. Core metric families

Use task-specific metrics rather than a single aggregate score.

### Work reduction

- engineer active time
- elapsed time
- context reconstruction time
- repeated work
- number of manual handoffs

### Quality

- task correctness
- defect/error rate
- missed issue rate
- false-positive rate
- rework rate

### Evidence / trust

- evidence completeness
- provenance completeness
- grounding accuracy
- unsupported-claim rate
- verification success

### Retrieval

- relevant-case recall
- precision of retrieved context
- time-to-relevant-evidence
- relation/temporal recovery rate

### Human interaction

- correction burden
- approval burden
- escalation rate
- time-to-decision
- override rate

### Operations

- latency
- failure rate
- recovery effort
- maintenance effort
- cost per completed task

## 5. APF benchmark matrix

The register of which benchmarks exist, what each tests, and what state each is
in now lives in `BENCHMARK_REGISTER.md`. It is maintained there so that a
benchmark's identity, its concrete case and its current result state cannot
drift apart across documents.

This document defines *how* to build and judge a falsification benchmark. It
does not enumerate them.

## 6. Adversarial test categories

A benchmark is incomplete unless it attempts at least one adversarial condition relevant to the claim.

### Data adversaries

- incomplete source data
- stale information
- contradictory records
- missing provenance
- duplicate artifacts

### Context adversaries

- cross-project ambiguity
- revision changes
- superseded decisions
- long time gaps
- terminology drift

### Model adversaries

- plausible but unsupported inference
- incorrect relation extraction
- overconfident summarization
- retrieval of semantically similar but operationally wrong cases

### Workflow adversaries

- high correction volume
- approval bottlenecks
- partial tool failure
- permission denial
- human override

### Scale adversaries

- large project history
- many concurrent work items
- high capture volume
- long-running execution history

## 7. Falsification rules

The benchmark should distinguish three outcomes:

### FALSIFIED

A defined failure condition is reproduced with sufficient evidence and the claim no longer holds at its stated scope.

### WEAKENED

The claim remains directionally useful but only within a narrower scope or under stronger preconditions.

### SUPPORTED

The benchmark did not defeat the claim and the candidate outperformed the baseline on the defined criteria.

`SUPPORTED` must never be interpreted as proof of universal validity.

## 8. Ablation requirement

When a claim depends on multiple mechanisms, remove one mechanism where practical.

Example:

```text
Full system
vs
Full system - relationship awareness
vs
Full system - provenance awareness
vs
Semantic retrieval baseline
```

This prevents the benchmark from attributing a gain to the wrong component.

## 9. Stop / split rules

Stop testing a broad claim and split it when:

- the claim contains multiple independent mechanisms;
- different workloads produce opposite results;
- evidence supports only a subset of the stated scope;
- the falsifier is too vague to reproduce;
- a benchmark result reveals a previously unmodeled variable.

Example:

```text
CLM-0004 broad claim
      ↓
CLM-0004a temporal awareness
CLM-0004b provenance awareness
CLM-0004c relationship awareness
```

## 10. Evidence packaging

Each benchmark run should retain enough information for independent review:

```text
benchmark definition
+ workload snapshot
+ baseline configuration
+ candidate configuration
+ tool/model versions
+ input set
+ output set
+ metric calculation
+ failure examples
+ operator notes
+ conclusion
```

The benchmark result is evidence. It is not itself an architecture decision.

## 11. Promotion gate

A claim can be considered for architecture discussion only after:

```text
TESTABLE
→ at least one falsification attempt
→ baseline comparison
→ adversarial test
→ evidence review
→ scope adjustment if needed
→ explicit human decision
```

For high-risk claims, require multiple independent evidence classes where practical.

## 12. Execution order

Declared once, in `BENCHMARK_REGISTER.md` §2.

This document previously carried a third, conflicting order. Three documents
each declaring a different execution order is exactly the contradiction the
contradiction audit in `MASTER_SESSION_PROMPT` exists to catch, and it went
uncaught. The register is now the only place an order may be declared.

## 13. Benchmark design rules

Absorbed from `P0_FALSIFICATION_BENCHMARK_MATRIX`.

### B1 — Architecture independence

The benchmark must be executable with a simple baseline. It must not require the
APF architecture being tested.

### B2 — Matched tasks

Compare systems on the same underlying tasks, evidence corpus, user role, and
information availability.

### B3 — Predeclared falsifiers

The failure condition must be written before looking at the result.

### B4 — Human cost counts

Capture, correction, approval, verification, and recovery effort are part of the
outcome, not overhead to be ignored.

### B5 — Quality and speed are joint outcomes

A faster workflow that increases wrong or ungrounded decisions is not a positive
result.

### B6 — Independent replication

Where practical, repeat tests with different projects, task types, users, or
evidence sets to avoid overfitting to APF dogfood data.
