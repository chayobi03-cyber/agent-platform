# APF Falsification Benchmark v0.1

**Status:** Benchmark design / candidate
**Purpose:** Provide a repeatable method for attempting to disprove APF claims before promoting them into architecture contracts or implementation dependencies.

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

```yaml
benchmark_id: FB-0001
title:
claim_refs: []
objective:
workload_class:
baseline:
candidate:
controls: []
variables: []
scenarios: []
adversarial_cases: []
primary_metrics: []
secondary_metrics: []
acceptance_rule:
falsification_rule:
minimum_sample:
evidence_type: RUNTIME_EVIDENCE | EVALUATION_EVIDENCE | HUMAN_DECISION_EVIDENCE
artifacts: []
result:
claim_update:
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

| Benchmark | Claim | Baseline | Candidate | Primary falsification question |
|---|---|---|---|---|
| FB-0001 | CLM-0001 | Agent-centric core | Work-centric core | Does work-centric modeling lose essential information or materially increase complexity? |
| FB-0002 | CLM-0002 | Manual notes / no structured capture | Capture + auto-structuring | Does lower capture friction increase reusable project memory without intolerable noise? |
| FB-0003 | CLM-0003 | Evidence-dense UI | Progressive disclosure | Does progressive disclosure reduce usability cost without increasing judgment/evidence errors? |
| FB-0004 | CLM-0004 | Flat semantic retrieval | Provenance/temporal/relation-aware retrieval | Is structure genuinely useful beyond semantic similarity? |
| FB-0005 | CLM-0005 | Current-record-only workflow | Failure-aware history | Does retaining failed attempts measurably reduce repeated work or error? |
| FB-0006 | CLM-0006 | Evidence without full provenance | Provenance-rich evidence | Does provenance improve expert trust/reuse accuracy enough to justify collection cost? |
| FB-0007 | CLM-0007 | Unrestricted automation | Explicit human boundary | Do human gates reduce consequential errors without making the workflow unusable? |
| FB-0008 | CLM-0008 | Framework-specific adoption | Primitive extraction | Does framework neutrality preserve required capabilities with lower coupling? |
| FB-0009 | CLM-0009 | Manual/baseline automation | Augmented automation | Is measured engineer effort reduction real and durable at required quality? |
| FB-0010 | CLM-0010 | Generic agent-builder thesis | Engineering-work augmentation | Which framing produces stronger validated work reduction across representative workloads? |

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

## 12. Initial execution order

The first benchmark wave should prioritize claims that can invalidate the broader product thesis:

```text
FB-0002  Capture value
FB-0004  Structured retrieval value
FB-0006  Provenance value
FB-0009  Measured automation value
FB-0007  Human boundary value
```

Only after those have credible evidence should deeper implementation choices become binding.
