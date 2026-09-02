# APF Session State

**Session:** Claim Inventory + Research Reconciliation + Falsification Benchmark foundation
**Status:** Active working state
**Last update:** 2026-09-02 — full project audit
**Latest audit:** `docs/research/APF_PROJECT_AUDIT_2026-09-02.md` — governance holding;
coverage thin. F1 closed (CLM-0004a/b/c entered with the factorial attached); F3 and F8 raised
as decision records awaiting human approval; F2/F4/F5 open.
**Open decisions:** `docs/decisions/DEC-0001` (parallel benchmark tracks),
`DEC-0002` (claim record completeness). Neither may be self-approved.

## BENCH-0004-E2b (2026-09-02)

E2 is blocked at G1 and its fixture bytes were verified to have never existed in this
repository, so git rollback cannot recover them. E2b was built instead: a new 96-context
factorial over the repository's own committed history, pinned at `a0bc5a6`, deterministic, and
**committed to the repository** — which is what E2 lacked. G2 byte-level verification passes and
the G4 dry run is clean; only G3 (pinned model + credential) blocks Stage 2.

Stage 1 executed. **P and R replicate the original factorial; T does not** (+0.0191, p=0.438
against the original +0.1683, p=0.023). Temporal filtering changed the retrieved set in 92% of
comparisons, so the null is a failure to improve sufficiency rather than inaction. `CLM-0004a`
moves to `WEAKENED`; `CLM-0004b` and `CLM-0004c` record the replication and stay `UNDER_TEST`.
Nothing promoted.

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

## BENCH-0004-E2 Integration (2026-09-01)

The E2 stage arrived as an out-of-repository handoff bundle and has been brought into the
evidence chain. Its execution record is `docs/research/executions/BENCH-0004_E2_2026-09-01.md`.

- E2 status: `NOT EXECUTED — blocked at G1`. The handoff contained protocol documents only;
  `contexts_96.jsonl`, both manifests, the generator contract, and the two original scripts
  were absent, so the four locked hashes cannot be recomputed and there is no request payload.
- Verified: cross-document hash consistency (PASS), factorial arithmetic recheck (PASS, all
  7 effects reproduce from the published cell means). Byte-level verification remains PENDING.
- Fixture lock v2 corrects a `locked_at_utc` field that carried a `+09:00` offset.
- Falsification benchmark now runs on two parallel tracks: v0.1 (claim level, `CLM-*`) and
  v0.2 (architecture hypothesis level, `H01`–`H12`). v0.2 does not supersede v0.1.
  `docs/research/CLAIM_HYPOTHESIS_MAP.md` holds the bridge and the adjudication boundaries.
- H07 and H11 had no repository definition before this commit and are **not** adjudicated by
  E2. They now have their own designs: `benchmarks/T07_ASSET_REUSE.md`,
  `benchmarks/T11_ASSET_INVALIDATION.md`. Both are blocked on the asset ledger, which holds
  no accepted assets.
- Tooling for gates G2/G4/G7 is in `tools/bench0004_e2/`, standard library only.

**CLM-0004 remains INCONCLUSIVE and must not be promoted.**

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
