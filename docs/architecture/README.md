# APF Architecture Workspace

## Status

Foundation stage. No Platform Contract or Architecture Decision is finalized yet.

## Candidate Domain Model

```text
Work
Opportunity
Automation
Actor
Identity
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
Decision
Approval
```

This is a **candidate model**, not a frozen schema.

## Candidate Platform Flow

```text
Work
 ↓
Opportunity
 ↓
Automation Strategy
 ↓
Engineering Proposal
 ↓
Human Approval
 ↓
Implementation
 ↓
Verification
 ↓
Execution
 ↓
Evidence
 ↓
Evaluation
 ↓
Outcome
 ↓
Learning
```

## Architecture Rules

1. Work is the primary business-domain anchor.
2. Agent is one automation strategy, not the platform root.
3. Definition and Execution are separate concerns.
4. Policy and Identity are platform control primitives.
5. Evidence connects execution to evaluation and outcome.
6. Runtime choices must not prematurely become platform contracts.
7. Architecture contracts require evidence and explicit decision records before implementation.

## Runtime Research

LangGraph, Temporal, and other execution technologies are treated as reference implementations and research inputs until APF contracts are established.

## Open Architecture Questions

- Canonical Work / Opportunity boundary
- Automation Strategy representation
- Actor / Identity / Delegation model
- Capability contract
- Context contract
- Policy decision boundary
- Execution contract
- Evidence semantic model
- Evaluation contract
- Outcome model
- Cross-runtime portability requirements
