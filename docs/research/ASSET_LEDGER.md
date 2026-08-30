# APF Research Asset Ledger

**Status:** Initial foundation; no asset is accepted by default.

## State Model

```text
RAW_FINDING → ASSET_CANDIDATE → REVIEWED → ACCEPTED_ASSET
```

A research finding is not an APF rule. Adoption requires evidence, analysis, and an explicit human decision where consequential.

## Asset Record Template

```yaml
asset_id:
title:
status:
source:
source_type:
primitive:
entities:
relationships:
lifecycle:
control:
execution:
evidence:
ownership:
failure_mode:
security_boundary:
finding:
counter_evidence:
apf_relevance:
architectural_impact:
recommendation:
adoption: ADOPT | REFERENCE | DEFER | REJECT
confidence:
related_assets:
related_decisions:
evidence_links:
```

## Evidence Classes

- EXTERNAL_EVIDENCE
- REPOSITORY_EVIDENCE
- RUNTIME_EVIDENCE
- EVALUATION_EVIDENCE
- HUMAN_DECISION_EVIDENCE

## Initial Research Tracks

### P0

- Work / Opportunity
- Backstage
- Temporal
- LangGraph
- OpenFGA
- OPA
- MCP
- OpenTelemetry
- Phoenix / Evaluation
- Identity / Authorization

### P1

- A2A
- OpenHands / Sandbox
- Agent Security
- FinOps
- Agent Governance
- Operational Knowledge

## Research Rule

For every external source, extract architectural primitives rather than copying its framework-specific model. Cross-source agreement increases confidence; contradictions must be recorded explicitly.
