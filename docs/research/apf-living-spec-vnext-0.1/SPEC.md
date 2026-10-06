# APF Specification — Scope & Candidate Core

## Status
Hypothesis-driven; not a frozen architecture.

## Scope
APF investigates a general work-execution layer for Agentic Engineering and business work. It must remain independent of any single LLM, Agent SDK, workflow engine, UI, database, or domain ontology.

## Candidate execution semantics
A work item may expose: intent, context, plan, action, observation/evidence, validation, decision, outcome, and state transition.

## Candidate core boundaries
1. Execution Contract — common representation of work execution.
2. Evidence/Validation/Decision relationships — explicit, inspectable relationships rather than implicit chat history.
3. Semantic Boundary — execution semantics separated from domain/task semantics.
4. Asset Lifecycle — verified execution knowledge can become reusable engineering assets.

## Non-core / replaceable capabilities
Agent runtime, LLM, tool protocol, durable execution engine, telemetry, provenance implementation, UI, memory/vector store, and domain ontology are replaceable capabilities.

## Open architectural question
Execution-, Case-, Workflow-, and Event-centric object models remain competing hypotheses until tested across heterogeneous workloads.
