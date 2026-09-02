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

## Governance

APF separates:

```text
Research ≠ Asset ≠ Decision ≠ Implementation
```

Human accountability is a platform invariant. Consequential architecture, contract, permission, release, and policy decisions require explicit human decision records.

## Repository Structure

- `CONSTITUTION.md` — project invariants and boundaries
- `docs/governance/MASTER_SESSION_PROMPT.md` — session operating protocol
- `docs/governance/` — governance and lifecycle rules
- `docs/architecture/README.md` — architecture workspace and contract boundary
- `docs/decisions/` — human-owned decision records
- `docs/handoff/` — session state and handoff records

Research layer, each subject declared in exactly one place:

- `docs/research/CLAIM_INVENTORY.md` — claims and the claim/result state vocabulary
- `docs/research/BENCHMARK_REGISTER.md` — which benchmarks exist, their cases, order and state
- `docs/research/FALSIFICATION_BENCHMARK.md` — how a falsification benchmark is designed and judged
- `docs/research/RESEARCH_TO_CLAIM_MAP.md` — traceability and reconciliation protocol
- `docs/research/RESEARCH_CORPUS_MAP.md` — corpus reconciliation status
- `docs/research/ASSET_LEDGER.md` — research and reusable design assets
- `docs/research/executions/` — benchmark predeclarations, results and raw evidence (append-only)

Tooling:

- `tools/apfbench/` — reusable benchmark infrastructure (standard library only)
- `tools/bench/` — per-benchmark definitions
- `tools/tests/` — reproducibility and document-integrity guards

## Current Status

Foundation bootstrap. Domain model and platform contracts remain candidate/proposal state until evidence and explicit human decision establish them.
