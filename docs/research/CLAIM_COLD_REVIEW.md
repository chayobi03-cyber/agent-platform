# APF Claim Cold Review v0.1

**Status:** Pre-benchmark quality review

The purpose of this review is to identify claims that appear falsifiable but contain hidden assumptions, causal overreach, ambiguous scope, or an unfair baseline.

## Review findings

| Claim | Main issue | Cold-review action |
|---|---|---|
| CLM-0001 | "more general" can become a vague superiority claim | Narrow to coverage / essential-information preservation / control complexity over a declared workload matrix |
| CLM-0002 | "increases usable engineering memory" combines capture behavior and downstream retrieval value | Split measurement into capture retention and later successful reuse; avoid assuming causality from one metric |
| CLM-0003 | Usability claim risks conflating speed, evidence access, and decision quality | Treat as a multi-metric interaction-cost hypothesis; correctness remains a guardrail, not a secondary metric |
| CLM-0004 | "improves engineering retrieval" may be explained by better indexing or metadata alone | Require matched retrieval baselines and ablation of relationship, temporal, and provenance features |
| CLM-0005 | "improves future decisions" is broad and causally expensive | First test repeated-work reduction and dead-end avoidance; decision-quality effects are secondary |
| CLM-0006 | "necessary" is stronger than the evidence currently warrants | Reword as a measurable trust/reproducibility hypothesis; reserve "necessary" for a demonstrated boundary condition |
| CLM-0007 | Explicit approval may reduce risk simply by reducing autonomy, not because the boundary model is superior | Compare matched autonomy levels and measure both prevented harmful actions and approval burden |
| CLM-0008 | Portability is not the only possible benefit and may be hard to isolate | Test migration/extension cost, semantic leakage, and dependency lock-in across at least two implementations |
| CLM-0009 | "should be promoted only" is partly a governance rule rather than an empirical claim | Separate empirical net-value threshold from the subsequent human governance decision |
| CLM-0010 | Product thesis comparison mixes market scope, validation risk, and user value | First test within declared target users/workloads; do not infer universal superiority from initial engineering-domain results |

## Strongest immediate narrowing candidates

### CLM-0006

Current wording is too strong. A better testable form is:

> For target engineering evidence-reuse tasks, relevant provenance and configuration metadata reduce reproduction/diagnosis error or time relative to an otherwise equivalent evidence record without that metadata.

### CLM-0007

The benchmark should not compare "human approval" with unrestricted automation only. It should distinguish:

```text
no gate
vs
late approval
vs
boundary-specific approval
```

Otherwise the experiment cannot determine whether the location and specificity of the decision boundary matter.

### CLM-0009

Separate:

```text
empirical claim: measured net value can be estimated
```

from:

```text
governance rule: APF will require such evidence before promotion
```

The second is a human policy decision, not a benchmark result.

## General rejection criteria

Reject or split a claim when:

1. The dependent variable is a vague aggregate such as "better" or "more useful" without operationalization.
2. The baseline is materially weaker than the proposed system for reasons unrelated to the claim.
3. The benchmark requires the architecture under test in order to run.
4. A positive result has an obvious simpler explanation that is not controlled.
5. The falsifier only describes failure of the implementation, not failure of the underlying claim.
6. The claim scope exceeds the population actually tested.
7. Human policy preference is disguised as an empirical statement.

## Outcome

No claim in this review is promoted merely because it survives wording review. The next state is benchmark design/execution.
