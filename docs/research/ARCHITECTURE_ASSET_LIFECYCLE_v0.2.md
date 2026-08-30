# APF Architecture Asset Lifecycle v0.2

**Status:** PROPOSED / RESEARCH GOVERNANCE

This document supersedes the assumption that A01~A13 must be globally adopted or rejected as a fixed set before APF can build new tools.

## 1. Core Principle

APF does not require a single frozen architecture for every tool.

APF maintains reusable architectural semantics as hypotheses/assets and allows each tool/project to select, compose, test, refine, split, merge, defer, or reject them according to context and evidence.

```text
Research Finding
→ Semantic Hypothesis
→ Architecture Asset Candidate
→ Applicability / Experiment Profile
→ Tool / PoC
→ Evidence + Counter-Evidence
→ Asset Refinement
→ Promotion / Split / Merge / Retire
→ Human Governance Gate when consequential
→ Contract Candidate
→ Human Approval
→ Implementation
→ Verification
```

## 2. Three Distinct Levels

### Tier 0 — APF Invariants

Stable principles that constrain the platform itself.

Examples:

- Work-centric orientation
- Human accountability for consequential decisions
- Research ≠ Decision
- Decision ≠ Contract Change
- Evidence before consequential architecture change
- Framework neutrality

Tier 0 changes require explicit governance and should be rare.

### Tier 1 — Architecture Semantics / Asset Knowledge

Reusable concepts discovered from multiple implementations or research sources.

Examples may include:

- Stateful/recoverable execution
- Human control
- Capability boundary
- Identity/delegation
- Authorization/policy
- Evidence/provenance
- Evaluation
- Outcome linkage

Tier 1 entries remain evolvable. They are not automatically mandatory for every tool.

### Tier 2 — Tool / Project Architecture Profile

A contextual selection and composition of Tier 1 semantics for one tool.

```yaml
architecture_profile:
  name: example-tool-v1
  assets:
    stateful_execution: context_dependent
    human_control: required
    capability_boundary: required
    identity_delegation: required
    authorization_policy: required
    evidence_provenance: required
    evaluation: optional
    business_outcome: required
```

The profile is an application decision, not a redefinition of the underlying asset.

## 3. Asset State and Applicability State Must Be Separate

### Asset State

```text
HYPOTHESIS
CANDIDATE
PROVISIONAL
ESTABLISHED
DEFERRED
RETIRED
```

### Applicability State

```text
REQUIRED
OPTIONAL
CONTEXT_DEPENDENT
NOT_APPLICABLE
EXPERIMENTAL
```

Example:

```text
Asset: Stateful Execution
Asset State: ESTABLISHED

Tool A: NOT_APPLICABLE
Tool B: OPTIONAL
Tool C: REQUIRED
Tool D: EXPERIMENTAL
```

An accepted/established asset therefore does not imply universal application.

## 4. Asset Promotion Must Be Evidence-Driven

Promotion is not triggered by a single human preference or a single successful implementation.

Evidence to consider:

- Cross-source convergence
- Repeated use across tools
- Measured engineering benefit
- Reliability/safety benefit
- Operational cost
- Counter-evidence
- Portability across runtimes
- Boundary stability
- Need for a stable contract

A candidate may be refined without being promoted.

## 5. Experimentation Is a First-Class Architecture Activity

For uncertain semantics, APF should permit multiple profiles or implementations to be tested.

```text
Hypothesis
 ├─ Profile A
 ├─ Profile B
 └─ Profile C
       ↓
   Comparative Evidence
       ↓
 Refine / Split / Merge / Retire
```

Example:

```text
Execution hypothesis:
"Recoverability is valuable for long-running or high-risk work."

Experiment:
- lightweight execution
- checkpointed execution
- durable workflow execution

Compare:
- recovery success
- latency
- cost
- operational complexity
- failure impact
```

## 6. Human Governance Is a Gate, Not the Architecture Generator

Human review is required when a change is consequential, including:

- APF invariant changes
- stable contract changes
- security/authority boundary changes
- production risk acceptance
- material vendor lock-in
- business acceptance

For ordinary applicability choices, the system may provide evidence and recommendations; the project workflow may determine whether explicit human approval is required.

The principle is:

```text
System generates options + evidence
Human governs consequential commitments
```

## 7. Contract Formation Should Be Delayed Until Semantics Stabilize

Do not convert a candidate directly into a permanent contract.

Preferred progression:

```text
Asset Hypothesis
→ Experiment
→ Observed Requirement
→ Contract Candidate
→ Contract Validation
→ Stable Contract
```

A contract should capture durable semantics, not the implementation details of a temporary experiment.

## 8. Runtime Neutrality

Runtime technologies are implementation choices unless a separate decision establishes otherwise.

```text
APF Semantics
      ↓
Runtime Adapter / Integration Boundary
      ↓
LangGraph / Temporal / OpenAI Agents SDK / Other Runtime
```

OpenHands, CrewAI, MCP, and similar technologies may serve as implementation or pattern evidence without defining APF architecture.

## 9. Asset Evolution Operations

The asset system must support:

```text
ADD
REFINE
SPLIT
MERGE
PROMOTE
DEMOTE
DEFER
RETIRE
REJECT
```

These operations operate on architecture knowledge, not on production contracts unless a separate governed change is approved.

## 10. Architecture Fitness Feedback

Each real tool can generate evidence about the usefulness and cost of an asset/profile.

Suggested dimensions:

- Reliability
- Recoverability
- Safety
- Human load
- Latency
- Cost
- Auditability
- Portability
- Engineering effort
- Business outcome relevance

```text
Tool Evidence
→ Architecture Fitness
→ Asset Knowledge Update
```

## 11. Required Separation

The following distinctions are mandatory in APF research/governance:

```text
Technology
≠ Primitive
≠ Pattern
≠ Asset Candidate
≠ Established Asset
≠ Applicability Decision
≠ Architecture Principle
≠ Contract
≠ Implementation
```

## 12. Consequence for A01~A13

A01~A13 remain a research snapshot only.

They are not the permanent APF architecture inventory.

Future research may:

- introduce new candidates;
- remove candidates;
- split one candidate into several semantics;
- merge overlapping candidates;
- downgrade a candidate to reference material;
- promote a repeated pattern into established asset knowledge.

No fixed candidate count is required.

## 13. Desired APF Operating Model

```text
                    APF
                     │
              Stable Invariants
                     │
              Asset Knowledge Base
                     │
          ┌──────────┴──────────┐
          │                     │
   Proven Semantics       Open Hypotheses
          │                     │
          └──────────┬──────────┘
                     ▼
             Tool Architecture
                     │
          Applicability / Profile
                     │
                 Experiment
                     │
                Evidence
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
       Refine               Counter-Evidence
          │                     │
          └──────────┬──────────┘
                     ▼
             Asset Evolution
                     │
             Contract Candidate
                     │
              Human Governance
```

**Status:** PROPOSED / NOT AN APPROVED ARCHITECTURE CONTRACT
