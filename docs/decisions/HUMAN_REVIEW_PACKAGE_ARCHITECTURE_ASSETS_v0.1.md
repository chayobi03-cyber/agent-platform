# APF Human Review Decision Package — Architecture Assets v0.1

**Status:** PROPOSED / HUMAN DECISION REQUIRED  
**Source candidate set:** `docs/research/ARCHITECTURE_ASSET_CANDIDATES_v0.1.md`  
**No decision is recorded by this package.** This package prepares decisions for human review.

## 1. Decision Objective

Decide which research-derived abstractions should become APF-owned Architecture Assets, which should remain supporting/reference patterns, and which require further research.

The decision is explicitly **not**:

- which OSS to adopt;
- which runtime to deploy;
- which framework becomes the APF architecture;
- whether any contract should be changed immediately.

The decision is:

> Which durable semantics should APF own independently of implementation technology?

## 2. Current Evidence Baseline

Repository evidence confirms that APF already defines a work-centric platform purpose, separates research/asset/decision/implementation states, requires human ownership of consequential decisions, and treats frameworks as references until contracts are established. `CONSTITUTION.md`, the architecture workspace, and the research ledger are therefore the governance baseline for this review.

External evidence reviewed for this package includes:

- Temporal: durable/resumable workflow execution and recovery semantics.
- LangGraph: checkpoint persistence, interrupts, human approval and resume.
- OpenFGA: relationship-based authorization checks.
- OPA: policy decision point separated from policy enforcement, with decision logging.
- MCP: authorization, consent, and tool safety boundaries.
- OpenTelemetry: common telemetry semantics and events for operations, state changes, and outcomes.
- A2A: stateful Task, context, history, and artifact semantics across agent boundaries.
- Backstage: entity, relation, ownership, and lifecycle modeling.
- NIST: agent identity, authorization, auditing, and non-repudiation as distinct concerns.

## 3. Review Classification

### Recommended for Human Review as Core

| ID | Candidate | Why it deserves core review | Main risk |
|---|---|---|---|
| A01 | Work / Opportunity Model | APF business anchor | Over-modeling |
| A02 | Automation Decision Model | APF-specific choice/rationale boundary | Process overhead |
| A03 | Stateful Durable Execution Model | Strong cross-source convergence | Excess durability |
| A04 | Human Control / Intervention | Human accountability + execution control | Throughput impact |
| A05 | Capability Boundary | Defines executable surface | Catalog complexity |
| A06 | Identity / Delegation | Principal and acting-for semantics | IAM complexity |
| A07 | Authorization / Policy Decision | Separates relation, policy, enforcement | Policy complexity |
| A08 | Evidence / Provenance | Auditable execution semantics | Cost/privacy |
| A10 | Business Outcome Linkage | Differentiates APF from agent runtime | Attribution difficulty |

### Recommended as Important / Supporting

| ID | Candidate | Review stance |
|---|---|---|
| A09 | Evaluation / Learning Loop | Strong candidate; keep evaluation distinct from outcome |
| A11 | Work–Execution Identity / Correlation | Supporting cross-cutting asset |
| A13 | Agent–Workflow Composition | Keep as composition semantics, not a runtime choice |

### Recommended to Defer

| ID | Candidate | Reason |
|---|---|---|
| A12 | Context / Lineage Model | Boundary versus state versus provenance remains insufficiently settled |

## 4. Decision Questions

### Gate D1 — APF Ownership

For each candidate:

> Would APF still need this semantic if Temporal, LangGraph, OpenFGA, OPA, MCP, or another technology were replaced tomorrow?

YES → strong APF ownership signal.  
NO → likely implementation/reference concern.

### Gate D2 — Reuse

> Does the semantic apply to Work, Workflow, Agent, Human-assisted, and non-agent automation where relevant?

Broad applicability increases asset value.

### Gate D3 — Boundary

> Can the candidate be described without importing a framework's object model or execution API?

If not, it should remain a reference/implementation pattern.

### Gate D4 — Failure

> Does the candidate define what happens when the normal path fails?

Candidates without explicit failure/recovery semantics should not be elevated to a contract prematurely.

### Gate D5 — Security

> Is the trust/authority/data/side-effect boundary explicit?

This is mandatory for capability, identity, authorization, and evidence-related assets.

### Gate D6 — Evidence

> Is there enough cross-source evidence to justify abstraction, and what evidence would falsify it?

## 5. High-Priority Human Decisions

### Decision H1 — Make Work the canonical platform anchor?

Candidate: A01  
Question: Should all automation initiatives be traceable to a Work/Opportunity semantic, including event-driven or highly ephemeral cases?

**Arguments for:** APF identity is business/work-centric; it avoids Agent-centric architecture.  
**Arguments against:** Some automations may be too ephemeral or infrastructure-level to justify a persistent Work object.

### Decision H2 — Establish Automation Decision as an APF semantic boundary?

Candidate: A02  
Question: Should APF explicitly represent why a chosen automation mechanism and autonomy level were selected?

**Arguments for:** Makes strategy choice auditable and prevents technology from becoming the decision.  
**Arguments against:** Low-risk automations may not justify decision records.

### Decision H3 — Define runtime-independent Execution semantics?

Candidate: A03  
Question: What is the minimum APF guarantee: state, checkpoint, retry, resume, idempotency, interrupt, history?

**Arguments for:** Strong Temporal/LangGraph convergence.  
**Arguments against:** Not every execution needs maximum durability.

### Decision H4 — Define Human Control as a first-class platform boundary?

Candidate: A04  
Question: Should approve/edit/reject/escalate/resume/abort become semantic control actions rather than UI features?

**Arguments for:** Directly aligns with HoTL governance and execution safety.  
**Arguments against:** Fine-grained intervention can create operational bottlenecks.

### Decision H5 — Separate Capability from Authorization?

Candidates: A05 + A07  
Question: Should APF explicitly model "what can be done" separately from "who may do it" and "whether this action is allowed now"?

**Recommendation rationale:** Strong architectural separation; MCP, OpenFGA, and OPA provide complementary evidence.

### Decision H6 — Separate Identity, Authorization, and Approval?

Candidates: A06 + A07 + A04  
Question: Should the platform prohibit a single `Actor`/`Auth`/`Approval` object from representing all three semantics?

**Recommendation rationale:** Prevents identity spoofing, permission confusion, and governance ambiguity.

### Decision H7 — Treat Evidence as more than telemetry?

Candidate: A08  
Question: Should APF define explicit execution/decision/approval/outcome evidence semantics above OTel traces/logs/metrics?

**Recommendation rationale:** OTel standardizes telemetry; OPA provides decision logs; A2A exposes task history/artifacts. These are evidence inputs, not one universal evidence object.

### Decision H8 — Keep Evaluation distinct from Business Outcome?

Candidates: A09 + A10  
Question: Should APF prohibit treating evaluator score as business success?

**Recommendation rationale:** Evaluation tests quality; Outcome represents actual business effect and acceptance.

## 6. Proposed Core Semantic Stack

This is a synthesis hypothesis, not an approved architecture:

```text
WORK
  ↓
AUTOMATION DECISION
  ↓
CONTROLLED EXECUTION
  ├── CAPABILITY
  ├── IDENTITY / DELEGATION
  ├── AUTHORIZATION / POLICY
  └── HUMAN CONTROL
  ↓
EXECUTION EVIDENCE / PROVENANCE
  ↓
EVALUATION ───────────────┐
  ↓                       │
BUSINESS OUTCOME           │
  ↓                       │
LEARNING / IMPROVEMENT ───┘

Cross-cutting:
  CORRELATION / IDENTITY
  CONTEXT / LINEAGE
```

**PROPOSED / NOT APPROVED**

## 7. Explicit Non-Decisions

This package does not decide:

- Temporal vs LangGraph vs another runtime;
- OpenFGA vs OPA vs another authorization implementation;
- MCP vs another capability protocol;
- OpenTelemetry vs another observability implementation;
- database schema;
- API schema;
- deployment topology;
- production security policy;
- final APF Architecture Contract.

## 8. Candidate-to-Contract Impact Map

| Candidate | Potential contract | Nature of impact |
|---|---|---|
| A01 | Domain Contract | Work/Opportunity entities and relationships |
| A02 | Domain + Decision Contract | Strategy/rationale/lifecycle |
| A03 | Execution Contract | State, recovery, idempotency, lifecycle |
| A04 | Execution + Control Contract | Intervention semantics |
| A05 | Capability Contract | Action/resource/side-effect model |
| A06 | Identity Contract | Principal/delegation semantics |
| A07 | Authorization Contract | Relation/policy/decision/enforcement |
| A08 | Evidence Contract | Evidence/provenance semantics |
| A09 | Evaluation Contract | Dataset/evaluator/experiment semantics |
| A10 | Domain/Outcome Contract | Outcome/measurement/acceptance |
| A11 | Cross-cutting Identity/Correlation | Identifier and linkage semantics |
| A12 | Context Contract | Context/snapshot/version semantics |
| A13 | Execution Contract | Agent/workflow composition semantics |

**No contract is modified by this document.**

## 9. Human Review Worksheet

For each candidate, record:

```text
asset_id:
reviewer:
decision: ACCEPT | REJECT | DEFER | SPLIT | MERGE
reason:
required_changes:
conditions_of_acceptance:
contract_impact_confirmed: YES | NO
technology_decision_required: YES | NO
security_review_required: YES | NO
business_owner_required: YES | NO
followup_research:
```

## 10. Recommended Decision Sequence

1. Decide the semantic boundaries before selecting technologies.
2. Approve/reject the Core candidates A01–A08 and A10 as abstractions, not implementations.
3. Decide whether A09/A11/A13 are standalone assets or supporting primitives.
4. Keep A12 in research until Context vs State vs Provenance boundaries are clarified.
5. Only after asset decisions, create Contract Proposals.
6. Only after contract approval, make technology and implementation decisions.

## 11. Exit Criteria

Human Review is complete only when:

- each candidate has an explicit decision;
- any split/merge action is recorded;
- architecture principles are distinguished from implementation preferences;
- contract impacts are identified;
- technology choices remain separate decisions;
- unresolved questions are classified as research-level or decision-level uncertainty.

## 12. Suggested Outcome States

```text
RESEARCH_ASSET
   ↓
ARCHITECTURE_ASSET_CANDIDATE
   ↓
HUMAN_REVIEW
   ├── REJECTED
   ├── DEFERRED
   ├── SPLIT / REFINED
   └── ACCEPTED_ASSET
             ↓
      DECISION RECORD
             ↓
      CONTRACT PROPOSAL
             ↓
      HUMAN APPROVAL
```

**Current package status:** `HUMAN_REVIEW_REQUIRED`
