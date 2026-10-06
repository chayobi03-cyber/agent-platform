# External Capability Landscape

APF should distinguish ownership from reuse.

| Capability | Representative prior art | APF stance |
|---|---|---|
| Agent runtime | OpenAI Agents SDK | BORROW |
| Stateful agent workflow | LangGraph | BORROW / ADAPT |
| Durable execution | Temporal | BORROW / ADAPT |
| Observability | OpenTelemetry | BORROW |
| Provenance | W3C PROV | ADAPT |
| Guardrails | Agent SDKs | ADAPT |
| Tool integration | MCP / APIs | BORROW |
| Domain semantics | Domain systems | EXTERNAL / PLUGGABLE |
| Execution contract | Fragmented across systems | OWN CANDIDATE |
| Validation/evidence/decision relationship | Fragmented | OWN CANDIDATE |
| Verification-driven asset lifecycle | Not identified as a common runtime contract | OWN CANDIDATE |

## Boundary rule
Do not claim novelty merely because APF combines known capabilities. Novelty/generalization must be demonstrated by a stable contract, heterogeneous workload coverage, portability, and a verified asset lifecycle.

## Important distinctions
- Telemetry is not audit.
- Provenance is not evidence.
- Evidence is not validation.
- HITL is not itself a differentiator.
- Checkpointing/durability is not itself a differentiator.
