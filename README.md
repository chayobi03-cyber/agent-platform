# APF — Internal Agent Platform

APF (Internal Agent Platform) is a work-centric platform for discovering automation opportunities and repeatedly engineering, controlling, executing, evaluating, and improving automation outcomes.

## Core Loop

```text
WORK
  ↓
OPPORTUNITY
  ↓
AUTOMATION DECISION
  ↓
ENGINEERING
  ↓
CONTROL
  ↓
EXECUTION
  ↓
EVIDENCE
  ↓
EVALUATION
  ↓
BUSINESS OUTCOME
  ↓
LEARNING
```

Agentic automation is one automation strategy, not the center of the platform.

## First Experimental Workload

APF's first concrete workload is an **Engineering Work Augmentation Platform**, initially focused on EMC / PCB engineering.

Candidate capability loop:

```text
Requirement
  ↓
Design / Revision
  ↓
Validation
  ↓
Problem
  ↓
Historical + Domain Context
  ↓
Hypothesis
  ↓
Experiment / Simulation / Measurement
  ↓
Decision
  ↓
Design Change
  ↓
Verification
  ↓
Learning
```

Candidate integrated capabilities include HyperLynx DRC baseline evidence, Python validation, ODB++ / schematic analysis, CST automation, EMC expert retrieval, email/communication retrieval, and Engineering History modeling.

Canonical product specification:

- `docs/product/ENGINEERING_WORK_AUGMENTATION_SPEC.md`

## Governance

APF separates:

```text
Research ≠ Asset ≠ Decision ≠ Implementation
```

Human accountability is a platform invariant. Consequential architecture, contract, permission, release, and policy decisions require explicit human decision records.

## Repository Structure

- `CONSTITUTION.md` — project invariants and boundaries
- `docs/product/ENGINEERING_WORK_AUGMENTATION_SPEC.md` — first product/workload specification
- `docs/governance/MASTER_SESSION_PROMPT.md` — session operating protocol
- `docs/research/ASSET_LEDGER.md` — research and reusable design assets
- `docs/architecture/README.md` — architecture workspace and candidate contracts
- `docs/decisions/README.md` — decision-record rules
- `docs/decisions/ADR-001-ENGINEERING-WORK-AUGMENTATION-SCOPE.md` — approved experimental product scope
- `docs/governance/` — governance and lifecycle rules
- `docs/handoff/` — session state and handoff records

## Current Status

Foundation / experimental workload selected. Product architecture remains hypothesis-driven. No specific graph database, agent runtime, or framework is frozen as an APF platform contract.
