# APF Falsification Benchmark

## FB-001 Agent-less execution
Remove the Agent and execute through a tool/script/human path. Failure: core execution contract becomes unusable.

## FB-002 Actor replacement
Run the same work with different Agents, a script, and a human. Failure: core semantics depend on a specific actor implementation.

## FB-003 Domain replacement
Model EMC/PCB analysis, document review, and general automation. Failure: domain-specific exceptions dominate the common model.

## FB-004 Human/autonomous mode replacement
Run the same execution with human approval enabled/disabled. Failure: HITL requires a separate incompatible workflow model.

## FB-005 Asset reuse
Create a validated asset in Run 1 and use it in Run 2. Failure: asset cannot influence planning/execution or applicability cannot be checked.

## FB-006 Asset invalidation
Introduce counter-evidence against an asset. Failure: system cannot revise/deprecate/invalidate the asset with traceability.

## FB-007 Interruption/recovery
Interrupt execution and resume from a durable checkpoint. Failure: execution semantics depend on ephemeral process state.

## FB-008 Evidence/provenance reconstruction
Reconstruct what happened, why, based on what, and how an output was derived. Failure: evidence, provenance, and decision lineage cannot be distinguished.

## Verdict rule
A failed core claim is not patched silently. The claim is marked CONTESTED or REJECTED, the affected asset/specification is identified, and the architecture hypothesis is reconsidered.
