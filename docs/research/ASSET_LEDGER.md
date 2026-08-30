# APF Research Asset Ledger

**Status:** Foundation / experimental; no research asset is accepted by default.

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
temporal_semantics:
provenance:
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
fitness_evidence:
```

## Evidence Classes

- EXTERNAL_EVIDENCE
- REPOSITORY_EVIDENCE
- RUNTIME_EVIDENCE
- EVALUATION_EVIDENCE
- HUMAN_DECISION_EVIDENCE

## Current High-Value Asset Candidates

### EHG-001 — Engineering History as a First-Class Model

**Status:** ASSET_CANDIDATE  
**Claim:** Engineering work benefits from preserving connected history rather than only isolated project documents.  
**Required validation:** Compare conventional relational/document history against explicit event/evidence/decision relationships.

### EHG-002 — Temporal / Provenance-Aware Engineering Event

**Status:** ASSET_CANDIDATE  
**Claim:** Consequential engineering results require revision, configuration, time, actor, and source context to remain interpretable.  
**Required validation:** Test reconstruction of historical state across design revisions and verification results.

### EHG-003 — Evidence-Linked Decision Pattern

**Status:** ASSET_CANDIDATE  
**Claim:** Decision records are more reusable when alternatives, rationale, consequences, and supporting/contradicting evidence are linked.  
**Required validation:** Measure decision-context reconstruction accuracy and engineer search effort.

### EHG-004 — Hypothesis / Experiment / Evidence Chain

**Status:** ASSET_CANDIDATE  
**Claim:** Failed and successful experiments should be retained as first-class history so future investigations can reuse prior reasoning and avoid repeated work.  
**Required validation:** Compare time-to-diagnosis with and without historical experiment chains.

### EHG-005 — Requirement-to-Verification Traceability

**Status:** ASSET_CANDIDATE  
**Claim:** Requirements, design checks, analysis, test evidence, and verification should be traversable as an engineering chain.  
**Required validation:** Test completeness and review effort against conventional document references.

### EHG-006 — Automatic Capture → AI Inference → Human Confirmation

**Status:** ASSET_CANDIDATE  
**Claim:** Relationship maintenance should minimize manual documentation by extracting candidate facts/relations from normal engineering work and requiring confirmation only where consequential.  
**Required validation:** Measure data-entry burden, false relation rate, and human correction rate.

### EHG-007 — Deterministic Validation + Agent Reasoning Separation

**Status:** ASSET_CANDIDATE  
**Claim:** Rules and analyzers should own deterministic checks; RAG should retrieve knowledge; agents should orchestrate and reason; humans should own consequential engineering judgement.  
**Required validation:** Compare correctness, explainability, and maintenance cost against end-to-end LLM judgement.

### EHG-008 — Engineering History → Agent Retrieval Context

**Status:** RESEARCH HYPOTHESIS  
**Claim:** Structured historical relationships may improve agent retrieval/reasoning over flat document RAG for engineering troubleshooting.  
**Required validation:** Direct H2 vs H3 experiment; this candidate must not be promoted on architecture aesthetics alone.

### EHG-009 — Simulation / Measurement Correlation

**Status:** RESEARCH HYPOTHESIS  
**Claim:** Explicit correlation between simulation predictions and physical measurement results can become reusable engineering knowledge.  
**Required validation:** Test whether historical correlation improves experiment selection and diagnosis.

### EHG-010 — Engineering Work Reduction as Primary Fitness

**Status:** ASSET_CANDIDATE  
**Claim:** Platform architecture should be judged first by engineering effort reduced without unacceptable quality, evidence, or accountability loss.  
**Required validation:** Time/cognitive-load/task-completion experiments on real engineering workflows.

## Initial Product Research Tracks

### P0 — Engineering Work Augmentation

- EMC / PCB validation
- ODB++ structure and topology analysis
- Schematic ↔ PCB consistency
- Requirement / design-rule traceability
- CST simulation automation
- Measurement / simulation correlation
- EMC expert retrieval
- Email / communication retrieval
- Engineering history model
- Engineering workflow orchestration
- Human approval boundaries

### P1 — Platform Composition

- LangGraph
- OpenHands / sandbox
- MCP
- Temporal
- Tool interoperability
- Agent evaluation
- Security / authorization
- Cost / resource controls

## Research Rule

For every external source, extract architectural primitives rather than copying framework-specific abstractions. Cross-source agreement increases confidence; contradictions must be recorded explicitly.

For every candidate asset, record both supporting evidence and counter-evidence. An implementation being technically possible is not evidence that the pattern reduces real engineering work.
