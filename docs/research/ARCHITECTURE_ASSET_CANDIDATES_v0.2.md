# APF Architecture Asset Candidates v0.2

**Status:** CANDIDATE / EXPERIMENTATION READY

This document is the flexible successor to the fixed A01~A13 review model. The current candidates remain useful research handles, but neither their count nor their boundaries are permanent.

## 1. Operating Model

```text
Research Finding
→ Semantic Hypothesis
→ Asset Candidate
→ Applicability / Experiment Profile
→ Tool / PoC
→ Evidence + Counter-Evidence
→ Asset Refinement
→ Promotion / Split / Merge / Retire
→ Human Governance when consequential
→ Contract Candidate
→ Human Approval
→ Implementation
→ Verification
```

## 2. Core Separation

```text
Technology
≠ Primitive
≠ Pattern
≠ Asset Candidate
≠ Established Asset
≠ Applicability
≠ Principle
≠ Contract
≠ Implementation
```

## 3. Current Candidate Map

| ID | Candidate | Current semantic hypothesis | Confidence | Primary test |
|---|---|---|---|---|
| A01 | Work / Opportunity | Business anchor for automation | High | Cross-workload applicability |
| A02 | Automation Decision | Why this automation mechanism was selected | Medium | Benefit vs decision overhead |
| A03 | Stateful / Recoverable Execution | State, checkpoint, recovery, resume | High | Durability tier fitness |
| A04 | Human Control | Approval/intervention as execution control | High | Risk reduction vs human load |
| A05 | Capability Boundary | What actions/resources can be invoked | High | Side-effect control |
| A06 | Identity / Delegation | Who acts and on whose authority | High | Attribution/delegation clarity |
| A07 | Authorization / Policy | Whether action is permitted | High | Relationship/policy separation |
| A08 | Evidence / Provenance | Reconstruction and proof of meaningful actions | High | Evidence completeness/cost |
| A09 | Evaluation / Learning | Evidence-driven quality improvement | High | Improvement signal |
| A10 | Business Outcome | Execution connected to actual business effect | Medium | Attribution validity |
| A11 | Work–Execution Correlation | Continuity across lifecycle objects | Medium-High | Traceability without duplication |
| A12 | Context / Lineage | Versioned context/derivation semantics | Medium | Separation from state/evidence |
| A13 | Agent–Workflow Composition | Agentic mechanism inside controlled execution | Medium-High | Benefit vs complexity |

These are research handles, not approved architecture elements.

## 4. Asset Evolution

Any candidate may be:

- ADDED
- REFINED
- SPLIT
- MERGED
- PROMOTED
- DEMOTED
- DEFERRED
- RETIRED
- REJECTED

A future synthesis may create A14+ or replace the present identifiers.

## 5. Applicability Is Contextual

Asset status and project use are independent.

```yaml
architecture_profile:
  name: example-tool-v1
  assets:
    stateful_execution: experimental
    human_control: required
    capability_boundary: required
    identity_delegation: context_dependent
    authorization_policy: required
    evidence_provenance: required
    evaluation: optional
    business_outcome: required
```

The profile is a project-level hypothesis/selection. It does not change the meaning of the asset.

## 6. Architecture Experiment

When a semantic boundary is uncertain, APF should test alternatives rather than force a permanent classification.

Example:

```text
Execution Hypothesis
 ├─ ephemeral
 ├─ checkpointed
 └─ durable
       ↓
Architecture Fitness Evidence
       ↓
refine / split / merge / retire
```

Compare at minimum where applicable:

- reliability
- recovery
- safety
- human load
- latency
- cost
- auditability
- portability
- engineering effort
- business relevance

## 7. Promotion Heuristic

Promotion toward stable APF-owned semantics should normally require a combination of:

1. recurrence across meaningful workloads or sources;
2. stable semantic boundary;
3. measurable benefit relative to complexity;
4. credible counter-evidence review;
5. independence from one implementation;
6. evidence that reuse justifies a common abstraction.

No fixed numeric threshold is established here. Thresholds may themselves be experimentally refined.

## 8. Human Governance

Human review is focused on consequential commitments rather than routine classification.

Human governance is expected when changes affect:

- APF invariants;
- stable platform contracts;
- security/authority boundaries;
- material production risk;
- irreversible business commitments;
- material vendor lock-in.

Routine project-level experimentation may proceed under the applicable project governance without turning every experiment into a platform-wide architecture decision.

## 9. Contract Formation

```text
Candidate
→ Experiment
→ Observed Requirement
→ Repeated Requirement
→ Stable Semantic Boundary
→ Contract Candidate
→ Validation
→ Human Approval
→ Stable Contract
```

A one-off implementation detail must not become a platform contract merely because it worked once.

## 10. Runtime Neutrality

LangGraph, Temporal, OpenHands, CrewAI, MCP, OpenFGA, OPA, OpenTelemetry, Phoenix, A2A, and other systems are evidence or implementation candidates.

The experiment evaluates semantic behavior, architecture fitness, and portability rather than selecting a vendor by default.

## 11. Research Status

`RESEARCH_COMPLETE → EXPERIMENTATION_READY`

The next Tool project is expected to act as an architecture experiment and may produce new evidence that changes this catalog.
