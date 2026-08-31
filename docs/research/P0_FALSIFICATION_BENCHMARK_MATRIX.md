# APF P0 Falsification Benchmark Matrix v0.1

**Status:** Experimental / not yet executed

This matrix turns the highest-leverage APF claims into independently testable benchmark families. No architecture implementation is assumed by the benchmark.

| Claim | Core question | Baseline | Proposed comparison | Primary metric | Falsifier | Priority |
|---|---|---|---|---|---|---|
| CLM-0001 | Is Work the more stable organizing abstraction than Agent/Framework? | Agent/tool-centric task record | Work-centric record linking opportunity, strategy, execution and outcome | task-model coverage; boundary violations; rework | Work-centric model provides no measurable coverage/clarity advantage across representative workloads | P0 |
| CLM-0002 | Does zero-ceremony capture reduce context reconstruction effort? | Manual notes + conventional project search | capture + automatic structuring + retrieval | time-to-context; omissions; user actions | no meaningful reduction or quality regresses | P0 |
| CLM-0004 | Does relationship/time-aware retrieval improve engineering recall? | keyword + semantic retrieval | relationship + temporal + provenance retrieval | evidence-grounded recall; answer utility; false-positive rate | improvement is absent or explained by better indexing alone | P0 |
| CLM-0006 | Does provenance/configuration retention improve trust and diagnosability? | evidence without full provenance | evidence with revision/config/tool/time/actor metadata | reproduction success; diagnosis time; trust calibration | provenance does not improve reproducibility/diagnosis or creates unacceptable burden | P0 |
| CLM-0007 | Do explicit human decision boundaries improve consequential workflow quality? | unrestricted automation / implicit approval | explicit approval gates at consequential boundaries | unsafe action rate; correction rate; latency | no safety benefit or approval burden dominates without material risk reduction | P0 |
| CLM-0009 | Should automation be promoted only with measurable work reduction? | automation selected by intuition/convenience | thresholded evidence-based promotion | engineer effort saved; quality delta; failure cost | qualitative benefit exists but measured net value is non-positive, or threshold cannot be operationalized | P0 |

## Benchmark Design Rules

### B1 — Architecture independence

The benchmark must be executable with a simple baseline. It must not require the APF architecture being tested.

### B2 — Matched tasks

Compare systems on the same underlying tasks, evidence corpus, user role, and information availability.

### B3 — Predeclared falsifiers

The failure condition must be written before looking at the result.

### B4 — Human cost counts

Capture, correction, approval, verification, and recovery effort are part of the outcome, not overhead to be ignored.

### B5 — Quality and speed are joint outcomes

A faster workflow that increases wrong or ungrounded decisions is not a positive result.

### B6 — Independent replication

Where practical, repeat tests with different projects, task types, users, or evidence sets to avoid overfitting to APF dogfood data.

## Initial Test Sequence

```text
BENCH-0001  CLM-0001 Work abstraction coverage
BENCH-0002  CLM-0002 Capture/context reconstruction
BENCH-0004  CLM-0004 Retrieval comparison
BENCH-0006  CLM-0006 Provenance/reproducibility
BENCH-0007  CLM-0007 Human decision boundary
BENCH-0009  CLM-0009 Automation promotion rule
```

## Result States

```text
UNTESTED
→ RUNNING
→ SUPPORTED
→ WEAKENED
→ SPLIT
→ CONTRADICTED
→ REJECTED
```

`SUPPORTED` never means universally true. It means the claim survived the declared benchmark within its tested scope.

## Benchmark Record Minimum

Each execution should record:

```yaml
benchmark_id:
claim_id:
task_population:
sample_size:
baseline:
variant:
operator_profile:
inputs:
metrics:
predeclared_falsifier:
result:
counter_observations:
limitations:
reproducibility:
conclusion:
next_action:
```
