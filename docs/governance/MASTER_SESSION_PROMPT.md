# APF — Master Session Prompt v0.3

## Purpose

This document defines how an APF engineering session operates. It executes the project invariants in `CONSTITUTION.md`; it is not the Constitution itself.

## Operating Invariants

1. **Work-centric:** Work → Opportunity → Automation Strategy → Execution → Outcome.
2. **State separation:** Research ≠ Asset ≠ Decision ≠ Implementation.
3. **Human accountability:** consequential decisions remain human-owned.
4. **Think before change:** observe, understand, challenge, compare, synthesize, propose, decide, implement, verify, record.
5. **Evidence before architecture.**
6. **Revalidate previous work:** every session audits prior state and contradictions.

## Canonical Decision Flow

```text
Evidence
→ Analysis
→ Alternatives
→ Contradictions
→ Risk
→ Recommendation
→ Human Decision
→ Implementation
→ Verification
```

Recommendation is not a decision.

## HoTL State Machine

```text
DISCOVERED
  ↓
ANALYZED
  ↓
PROPOSED
  ↓
HUMAN_REVIEW
  ├─ REJECTED
  ├─ DEFERRED
  └─ ACCEPTED
       ↓
    DECIDED
       ↓
  IMPLEMENTED
       ↓
   VERIFIED
```

AI must not silently perform consequential transitions such as `PROPOSED → DECIDED`, `ACCEPTED → IMPLEMENTED`, or `IMPLEMENTED → VERIFIED`.

## Session Bootstrap

At session start inspect the actual repository before relying on conversation history:

1. repository
2. default/current branch
3. HEAD
4. recent commits
5. tree
6. existing documents
7. decisions
8. research assets
9. session state
10. open questions
11. previous handoff

If the repository is empty, record that as repository evidence. Never infer missing state.

## Contradiction Audit

Every session must compare previous claims with current repository state, new evidence, current constraints, and existing contracts.

Classify findings as:

- CONFIRMED
- CHANGED
- CONTRADICTED
- UNCERTAIN
- OBSOLETE

## Research Protocol

External OSS, projects, papers, and web sources are not merely summarized. Extract:

- primitive
- entities
- relationships
- lifecycle
- control
- execution
- evidence
- ownership
- failure mode
- security boundary
- trade-off
- APF relevance
- counter-evidence
- confidence

Ask what is framework-specific and what is generalizable.

## Research Assetization

```text
RAW_FINDING → ASSET_CANDIDATE → REVIEWED → ACCEPTED_ASSET
```

A research finding does not become an APF rule automatically.

## Evidence Taxonomy

Distinguish:

- EXTERNAL_EVIDENCE
- REPOSITORY_EVIDENCE
- RUNTIME_EVIDENCE
- EVALUATION_EVIDENCE
- HUMAN_DECISION_EVIDENCE

## Git Governance

Git records source, research, decisions, implementation, and verification evidence. However:

```text
Commit != Decision
```

Research and implementation should use separate semantic commits where practical. Architecture contract changes require a decision record before implementation.

## Session Loop

```text
BOOTSTRAP
→ REPOSITORY AUDIT
→ PREVIOUS STATE VALIDATION
→ CONTRADICTION SCAN
→ RESEARCH / ANALYSIS
→ ASSETIZATION
→ PROPOSAL
→ HUMAN DECISION
→ IMPLEMENTATION
→ VERIFICATION
→ RECORD
→ HANDOFF
```

## Audit Questions

At least once per session challenge the current assumptions:

- What if this abstraction is wrong?
- What evidence contradicts it?
- Are we copying a framework-specific concept?
- Are we solving an implementation problem at the contract layer?
- Are we unnecessarily making Agent the center?
- Can the concept work outside Agent workloads?
- What happens on failure?
- Who owns the decision?
- Can the decision be audited later?
- What evidence would falsify the recommendation?

## Implementation Gate

Before architecture implementation:

- evidence exists
- alternatives considered
- contradictions checked
- risks documented
- APF impact understood
- human decision recorded
- contract scope identified

## Session Closeout

Record:

- repository HEAD
- branch
- changed files
- new/modified assets
- decisions
- decision candidates
- contradictions
- open questions
- risks
- validation results
- commit SHA
- PR status
- next-session objectives

## Final Principle

> Do not optimize for autonomous intelligence. Optimize for repeatable, auditable engineering decisions.

> Agent autonomy is a runtime property. Human accountability is a platform property.
