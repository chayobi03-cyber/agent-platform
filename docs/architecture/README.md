# APF Architecture Workspace

## Status

Foundation / experimental. No final Platform Contract has been established.

The first concrete workload is an **Engineering Work Augmentation Platform** experiment, initially focused on EMC / PCB engineering.

Canonical product specification:

- `docs/product/ENGINEERING_WORK_AUGMENTATION_SPEC.md`

## Candidate Domain Model

```text
Work
Opportunity
Requirement
Specification
Constraint
Project
Milestone
Design
DesignRevision
Artifact
EngineeringEvent
Issue
Observation
Hypothesis
Experiment
Simulation
Measurement
Decision
Action
Change
Result
Verification
Violation
Recommendation
Lesson
Communication
Actor
ToolRun
Release
Automation
Agent
Capability
Context
Policy
Workflow
Worker
Resource
Execution
Evidence
Evaluation
Outcome
Approval
```

This remains a **candidate semantic model**, not a frozen schema.

## Candidate Engineering Work Flow

```text
Requirement
 ↓
Design / Revision
 ↓
Validation
 ↓
Problem / Observation
 ↓
Historical + Domain Context
 ↓
Hypothesis
 ↓
Experiment / Simulation / Measurement
 ↓
Decision
 ↓
Action / Design Change
 ↓
Verification
 ↓
Release / Learning
```

## Candidate Engineering History Model

The Engineering History Graph is currently a hypothesis for preserving relationships that are difficult to recover from isolated project records.

```text
Problem
 ├─ observed_in → Evidence
 ├─ investigated_by → Experiment
 ├─ supported_by → Evidence
 ├─ contradicted_by → Evidence
 ├─ leads_to → Decision
 ├─ resolved_by → Action
 └─ verified_by → Verification
```

The graph is a semantic/history layer, not necessarily a graph-database requirement and not primarily a visualization feature.

## Architecture Rules

1. Work is the primary business-domain anchor.
2. Engineering history is modeled around events, evidence, relationships, time, and provenance.
3. Agent is one automation strategy, not the platform root.
4. Deterministic validation should be used where deterministic judgement is sufficient.
5. Definition and execution remain separate concerns.
6. Evidence must remain distinguishable from AI inference.
7. Requirement / revision / configuration context must be preserved for consequential results.
8. Human accountability remains the authority for consequential engineering decisions.
9. Automatic capture is preferred over mandatory manual graph construction.
10. Failed experiments and rejected hypotheses are retained as useful engineering history.
11. Internal engineering history and external knowledge remain source-distinguishable.
12. Runtime choices must not prematurely become platform contracts.
13. Architecture contracts require evidence and explicit decision records before final adoption.

## Candidate Capability Layers

```text
Validation
  └─ HyperLynx baseline / Python custom checks / ODB++ / schematic

Analysis
  └─ CST / numerical processing / measurement analysis

Knowledge
  └─ EMC knowledge / historical cases / email / external references

History
  └─ Engineering events / evidence / decisions / provenance

Workflow
  └─ deterministic workflows / stateful orchestration / human checkpoints

Agent
  └─ planning / retrieval / reasoning / tool orchestration
```

These are capability boundaries, not implementation commitments.

## Runtime Research

LangGraph, OpenHands, MCP, Temporal, and other execution technologies are treated as implementation candidates and research inputs. Their suitability must be demonstrated against workload-specific fitness criteria.

## Open Architecture Questions

- Canonical EngineeringEvent boundary
- Minimal History Graph schema
- Temporal and provenance representation
- Relationship confidence semantics
- Requirement-to-verification traceability
- Revision/configuration identity
- Measurement-to-simulation correlation
- Evidence storage boundary
- Internal vs external knowledge boundary
- Rule Engine vs Analyzer vs RAG vs Agent boundary
- Human decision checkpoint semantics
- Cross-runtime portability
- Data-ingestion and graph-maintenance cost
- Security / permission model for engineering artifacts and email
- Fitness thresholds for adopting graph/agent architecture
