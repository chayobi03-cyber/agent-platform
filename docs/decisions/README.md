# APF Decision Records

This directory contains human-owned decision records.

## Decision Principle

```text
Evidence
→ Analysis
→ Alternatives
→ Risk
→ Recommendation
→ Human Decision
→ Implementation
→ Verification
```

A recommendation is not an approval.

## Decision States

- PROPOSED
- ACCEPTED
- DECIDED
- SUPERSEDED
- REJECTED
- DEFERRED

## Minimum Decision Record

```yaml
id:
title:
status:
date:
context:
problem:
evidence:
contradictions:
alternatives:
risks:
recommendation:
human_decision:
impact:
implementation_scope:
verification_plan:
related_assets:
related_commits:
```

## Records

| ID | Title | Status | Date |
|---|---|---|---|
| DEC-0001 | [Evidence gate on architecture promotion and implementation start](DEC-0001-evidence-gate.md) | DECIDED | 2026-09-02 |
| DEC-0002 | [Claim records completed individually at benchmark preparation time](DEC-0002-claim-record-completion-timing.md) | DECIDED | 2026-09-02 |

## Governance Rule

An Architecture Contract must not be treated as approved solely because code or documentation has been committed. The corresponding decision must be explicitly recorded.
