# APF Architecture Claims

Claims remain hypotheses until tested.

| ID | Claim | Status | Falsification focus |
|---|---|---|---|
| AC-001 | APF can represent heterogeneous work with a domain-independent execution contract. | UNVALIDATED | Compare EMC, document, general automation workloads |
| AC-002 | Agent is one execution actor among Agent/Tool/Script/Human. | CANDIDATE | Replace Agent without changing core trace/contract |
| AC-003 | Evidence should be explicit and separable from output. | CANDIDATE | Reconstruct decision support from recorded evidence |
| AC-004 | Provenance is distinct from evidence, telemetry, and audit. | CANDIDATE | Test lineage and decision reconstruction separately |
| AC-005 | Human decision can be represented as a durable state transition. | CANDIDATE | Pause, decide, resume without special-case workflow |
| AC-006 | Validation is broader than guardrail execution. | UNVALIDATED | Compare runtime safety checks with outcome validation |
| AC-007 | Validated execution knowledge can become a reusable asset. | UNVALIDATED | Asset reuse and revalidation experiment |
| AC-008 | APF should consume mature external capabilities rather than reimplement them. | CANDIDATE | Adapter portability across implementations |

## Status vocabulary
UNVALIDATED / CANDIDATE / SUPPORTED / CONTESTED / REJECTED.
