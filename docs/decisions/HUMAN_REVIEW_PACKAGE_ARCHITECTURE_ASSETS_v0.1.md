# APF Human Review / Architecture Experiment Package v0.2

**Status:** PROPOSED / HUMAN GOVERNANCE REQUIRED

This package is a decision aid, not a permanent architecture decision. It explicitly supports experimentation and project-specific architecture profiles.

## 1. Decision Objective

Do not ask Human Review to pre-classify A01~A13 as the permanent APF architecture.

Instead review:

1. Which semantic hypotheses are useful enough to keep in APF architecture knowledge.
2. Which hypotheses need experiments before promotion.
3. Which semantics are globally stable invariants versus reusable assets.
4. Which semantics should remain contextual/project-specific.
5. What evidence threshold is required before creating a stable contract.
6. Which changes are consequential enough to require explicit human governance.

## 2. Current Research Position

A01~A13 are a research snapshot, not a fixed inventory.

New candidates may be added. Existing candidates may be refined, split, merged, demoted, deferred, or retired.

The preferred lifecycle is:

```text
Research Finding
→ Semantic Hypothesis
→ Architecture Asset Candidate
→ Applicability / Experiment Profile
→ Tool / PoC
→ Evidence + Counter-Evidence
→ Asset Refinement
→ Promotion Candidate
→ Human Governance when consequential
→ Contract Candidate
→ Human Approval
→ Implementation
→ Verification
```

## 3. Review Gates

### G1 — Semantic Stability

Can the idea be expressed independently of a specific framework/vendor?

### G2 — Reusability

Does the semantic recur across multiple tools or workload classes?

### G3 — Boundary Stability

Can its responsibility be separated cleanly from neighboring semantics?

### G4 — Empirical Fitness

Does actual tool evidence show meaningful benefit relative to cost/complexity?

### G5 — Counter-Evidence

What observations would make the abstraction unnecessary, harmful, or too broad?

### G6 — Contract Necessity

Is a stable cross-project contract actually needed, or is a project profile sufficient?

### G7 — Consequence

Does promotion/change affect security, authority, platform invariants, interoperability, data integrity, or material operating risk?

Only consequential changes require the strongest human gate.

## 4. Human Role

Human governance is a gate for consequential commitment, not a requirement to manually design every project architecture.

Preferred division:

```text
System
→ generates hypotheses, options, experiments, evidence, and recommendations

Project
→ selects applicable semantics/profile for its workload

Human
→ governs consequential commitments and contract/invariant changes
```

## 5. Applicability Model

Asset state and project applicability are separate.

### Asset State

```text
HYPOTHESIS
CANDIDATE
PROVISIONAL
ESTABLISHED
DEFERRED
RETIRED
```

### Applicability

```text
REQUIRED
OPTIONAL
CONTEXT_DEPENDENT
NOT_APPLICABLE
EXPERIMENTAL
```

Example:

```yaml
architecture_profile:
  name: engineering-agent-v1
  assets:
    stateful_execution: experimental
    human_control: required
    capability_boundary: required
    identity_delegation: required
    authorization_policy: required
    evidence_provenance: required
    evaluation: optional
    business_outcome: required
```

A project profile does not redefine the asset and does not imply that every other project must use it.

## 6. Experimentation Model

When applicability or semantic scope is uncertain, compare alternatives rather than forcing a binary decision.

Example:

```text
Execution Hypothesis
  ├─ lightweight execution
  ├─ checkpointed execution
  └─ durable workflow execution
          ↓
  Architecture Fitness Evidence
          ↓
   refine / split / merge / retire
```

Candidate dimensions include:

- reliability
- recovery success
- safety
- human load
- latency
- cost
- auditability
- portability
- engineering effort
- business outcome relevance

## 7. Proposed Architecture Knowledge Stack

```text
Tier 0 — APF Invariants
  ↓
Tier 1 — Semantic Asset Knowledge
  ↓
Tier 2 — Project Architecture Profiles
  ↓
Tool / PoC / Implementation
  ↓
Evidence + Counter-Evidence
  ↓
Asset Evolution
```

This is a governance model, not an approved implementation architecture.

## 8. Human Decision Worksheet

```text
item:
type: INVARIANT | ASSET | PROFILE | CONTRACT | TECHNOLOGY
question:
evidence:
counter_evidence:
alternatives:
consequence_level: LOW | MEDIUM | HIGH
human_gate_required: YES | NO
proposed_action: TEST | REFINE | SPLIT | MERGE | PROMOTE | DEFER | RETIRE | REJECT
reason:
followup_research:
```

## 9. Contract Formation Gate

A project profile does not automatically produce a platform contract.

Preferred path:

```text
Observed Requirement
→ Repeated Requirement
→ Stable Semantic Boundary
→ Contract Candidate
→ Validation
→ Human Approval
→ Stable Contract
```

A temporary implementation convenience must not become a platform contract merely because it worked once.

## 10. Runtime and OSS Boundary

The experiment may use LangGraph, OpenHands, CrewAI, Temporal, MCP, OpenFGA, OPA, OpenTelemetry, Phoenix, A2A, or other technologies.

Their presence in an experiment does not by itself establish an APF architecture decision.

The evaluation target is the semantic behavior and fitness of the architecture, not vendor loyalty.

## 11. Current Candidate Set

A01~A13 remain available as hypotheses from the current research snapshot. No fixed count is required.

The next tool project may:

- use none of the current candidates;
- use a subset;
- combine several candidates;
- test competing interpretations;
- introduce a new candidate;
- identify an overlap requiring a merge;
- split an overly broad candidate.

## 12. Explicit Non-Decisions

This package does not decide:

- universal adoption of A01~A13;
- mandatory use of any asset in every tool;
- Temporal vs LangGraph vs another runtime;
- OpenFGA vs OPA vs another authorization implementation;
- MCP vs another capability protocol;
- production deployment topology;
- final API/database schemas;
- final APF Architecture Contract.

## 13. Recommended Operating Principle

> APF should standardize durable semantics only when evidence demonstrates that the semantics are reusable, boundary-stable, and valuable across contexts.

> Project architecture should remain free to choose, combine, test, or omit those semantics according to workload context.

> Human governance should concentrate on consequential commitments, not routine architectural experimentation.

## 14. Exit Condition

A research phase may conclude with:

```text
RESEARCH_COMPLETE
→ EXPERIMENTATION_READY
→ HUMAN_GOVERNANCE_REQUIRED only for consequential commitments
```

It does not need to conclude with a globally frozen asset catalog.
