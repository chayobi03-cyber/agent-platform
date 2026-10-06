# APF Research Asset Registry vNext

## Asset lifecycle
DISCOVERED → CANDIDATE → VALIDATING → VALIDATED → ARCHITECTURE_ADOPTED

Alternative terminal/revision states: REVISED, DEPRECATED, INVALIDATED, REJECTED.

## Current assets

| ID | Asset | Type | Status | APF implication |
|---|---|---|---|---|
| RA-009 | Provenance Boundary | Research | CANDIDATE | Separate evidence from lineage |
| RA-010 | Execution Durability Boundary | Research | CANDIDATE | State needs checkpoint/resume semantics |
| RA-011 | Agent Observability Boundary | Research | CANDIDATE | Telemetry is not APF execution semantics |
| RA-012 | Validation vs Guardrail Boundary | Research | CANDIDATE | Validation is broader than runtime guardrails |
| RA-013 | Decision Durability | Research | CANDIDATE | Decisions should be durable execution records |
| RA-014 | Verification-driven Asset Lifecycle | Architecture candidate | CANDIDATE | Verified execution knowledge can be reused/revalidated |

## Required asset record
Each promoted asset should record: claim, evidence, provenance, applicability, limitations, counterexamples, validation method, confidence, version, dependencies, architecture impact, and adoption/rejection decision.

## Principle
An asset is not merely a useful idea. It is reusable knowledge with explicit evidence, scope, failure conditions, and validation status.
