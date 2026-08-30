# APF Human-on-the-Loop Governance

## Principle

> Agent autonomy is a runtime property. Human accountability is a platform property.

## State Machine

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

## Human Decision Boundary

Explicit human decision is required for:

- architecture changes
- platform contract changes
- adoption of external assets as APF primitives
- identity / permission escalation
- sensitive-data access
- production release
- business acceptance
- policy exceptions
- high-risk actions

## Evidence Rule

The minimum decision chain is:

```text
Evidence → Analysis → Alternatives → Risk → Recommendation → Human Decision
```

The decision record must identify the evidence supporting the decision and any material counter-evidence.

## Separation of Concerns

```text
Research
  ≠
Decision
  ≠
Implementation
  ≠
Verification
```

A commit is not itself evidence of human approval.

## Override and Escalation

A human may reject, defer, modify, or supersede an AI recommendation. Such changes should be recorded when they affect architecture, policy, contracts, or consequential behavior.
