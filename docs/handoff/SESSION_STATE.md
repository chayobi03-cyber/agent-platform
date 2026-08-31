# APF Session State

**Session:** Claim Inventory + Research Reconciliation + Falsification Benchmark foundation
**Status:** Active working state

## Repository Evidence

- Repository: `chayobi03-cyber/agent-platform`
- Default branch: `main`
- Foundation bootstrap committed
- Claim inventory, reconciliation protocol, corpus map, cold review, and benchmark cases are committed on `main`

## Current State

- Constitution: v0.1 candidate/foundation
- Master Session Prompt: v0.3 operating protocol
- Research Asset Ledger: initialized; no accepted assets yet
- Claim Inventory: v0.1 established; initial claims CLM-0001 through CLM-0010
- Claim Reconciliation Protocol: v0.1 established
- Research Corpus Map: v0.1 established; corpus reconciliation is explicitly partial
- Claim Cold Review: v0.1 established; wording/causal-overreach issues identified
- P0 Falsification Benchmark Matrix: v0.1 established
- P0 Benchmark Cases: v0.1 design-ready, not executed
- Research-to-Claim traceability: established
- Domain Model: candidate only
- Architecture Contract: not established
- Architecture Decisions: none yet
- HoTL Governance: initialized

## Current Working Model

```text
Research Finding
    ↓
Research Asset Candidate
    ↓
Claim Inventory
    ↓
Evidence + Counter-evidence
    ↓
Falsification Benchmark
    ↓
Scoped Claim State
    ↓
Human Decision
    ↓
Architecture / Implementation
    ↓
Verification
```

## Key Boundary

```text
Research ≠ Asset ≠ Claim ≠ Evidence ≠ Decision ≠ Implementation
```

A claim that survives one benchmark remains a supported claim within tested scope; it is not automatically a universal rule or architecture invariant.

## Initial Priority Claims

- CLM-0001: work-centric abstraction generality
- CLM-0002: zero-ceremony capture value
- CLM-0004: structured retrieval value
- CLM-0006: provenance value
- CLM-0007: human-boundary value
- CLM-0009: measured automation value

## Cold Review Findings

- CLM-0006 wording was narrowed from necessity toward measurable trust/reproducibility value.
- CLM-0007 requires matched approval conditions; otherwise safety benefit is confounded with simply reducing autonomy.
- CLM-0009 must separate empirical net-value measurement from the human governance rule that may require such evidence.
- CLM-0001, CLM-0002, CLM-0003, CLM-0004, CLM-0005, CLM-0008, and CLM-0010 also require strict scope control during testing.

## Benchmark Execution Order

```text
BENCH-0004  retrieval ablation
BENCH-0006  provenance ablation
BENCH-0002  capture/context reconstruction
BENCH-0007  approval boundary
BENCH-0009  automation promotion
BENCH-0001  work abstraction coverage
```

## Immediate Next Tasks

1. Complete durable reconciliation of prior APF research material.
2. Recover individual external-source findings into explicit `ASSET-*` records.
3. Attach every material asset to one or more claims or mark it reference-only/duplicate/out-of-scope/insufficient.
4. Create benchmark datasets and execution fixtures for BENCH-0004 and BENCH-0006 first.
5. Record predeclared falsifiers and baseline controls before running experiments.
6. Execute, preserve raw results, and revise claim scope based on outcomes.
7. Only then consider architecture candidate promotion.

## Non-Goals

- Do not freeze architecture from the current claim list.
- Do not select a graph DB or agent runtime as an APF contract merely because the research mentions it.
- Do not treat repeated source agreement as proof.
- Do not build a broad implementation before high-leverage claims have been tested.

## Repository Independence

This repository remains independent from `chayobi03-cyber/agent-factory`. No AgentFactory architecture, governance, or code is inherited automatically.
