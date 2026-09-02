# APF Session State

**Session:** BENCH-0004 mechanism decomposition — first P0 claim falsified
**Status:** Active working state
**Last updated:** 2026-09-02 (Round 3 execution)

## Repository Evidence

- Repository: `chayobi03-cyber/agent-platform`
- Default branch: `main`
- Working branch: `claude/session-start-continue-03cik7`
- Foundation bootstrap committed
- Claim inventory, reconciliation protocol, corpus map, cold review, and benchmark cases are committed on `main`
- BENCH-0004 executed three times; execution records and raw results committed
- First falsification harness committed at `tools/bench/bench0004_r3.py`
  (standard library only, deterministic, independently replayable)

## Current State

- Constitution: v0.1 candidate/foundation
- Master Session Prompt: v0.3 operating protocol
- Research Asset Ledger: initialized; no accepted assets yet
- Claim Inventory: v0.1 established; initial claims CLM-0001 through CLM-0010
- Claim Reconciliation Protocol: v0.1 established
- Research Corpus Map: v0.1 established; corpus reconciliation is explicitly partial
- Claim Cold Review: v0.1 established; wording/causal-overreach issues identified
- P0 Falsification Benchmark Matrix: v0.1 established
- P0 Benchmark Cases: v0.1 design-ready; **BENCH-0004 executed (3 rounds), remainder not executed**
- Research-to-Claim traceability: established
- CLM-0004: **FALSIFIED at tested scope**; split into CLM-0004a/b/c, none surviving
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

- CLM-0001: work-centric abstraction generality — untested
- CLM-0002: zero-ceremony capture value — untested
- CLM-0004: structured retrieval value — **falsified at tested scope; split into a/b/c**
- CLM-0006: provenance value (evidence reuse) — untested, next
- CLM-0007: human-boundary value — untested
- CLM-0009: measured automation value — untested

## Cold Review Findings

- CLM-0006 wording was narrowed from necessity toward measurable trust/reproducibility value.
- CLM-0007 requires matched approval conditions; otherwise safety benefit is confounded with simply reducing autonomy.
- CLM-0009 must separate empirical net-value measurement from the human governance rule that may require such evidence.
- CLM-0001, CLM-0002, CLM-0003, CLM-0004, CLM-0005, CLM-0008, and CLM-0010 also require strict scope control during testing.

## Benchmark Execution Order

```text
BENCH-0004  retrieval ablation           DONE — 3 rounds, claim falsified
BENCH-0006  provenance ablation          NEXT
BENCH-0002  capture/context reconstruction
BENCH-0007  approval boundary
BENCH-0009  automation promotion
BENCH-0001  work abstraction coverage
```

## Executed Benchmarks

### BENCH-0004 — CLM-0004 structured retrieval

| Round | Design | Result |
|---|---|---|
| R1 (2026-08-31) | document-level recall, 4-doc corpus | no gain; weakened the broad claim |
| R2 (2026-08-31) | cross-document chains, 7-doc corpus, **hand-specified** graph | +0.208 coverage@2; provisionally supported a narrow subclaim |
| R3 (2026-09-02) | mechanism decomposition, 21-doc corpus, **derived** graph, null models, α sweep | **−0.135 coverage@3**; broad claim falsified |

Round 3 changed the graph from operator-drawn to mechanically derived and the
Round 2 advantage reversed. **R2's provisional SUPPORTED state is superseded.**

Key findings to carry forward:

1. The largest positive retrieval effect measured across all three rounds came
   from plain **metadata weighting** (+0.063), not from any structural mechanism.
   This is the alternative explanation BENCH-0004 named as its own falsifier.
2. **Hub amplification**: one-step relationship propagation adds score in
   proportion to connectivity, and in a governance corpus the best-connected
   documents are indexes rather than answers. It displaced correct single-document
   answers on the neutral control class (−0.25).
3. The derived relationship graph is nonetheless **real structure** — it beat its
   degree-preserving null at the 99.5th percentile. The failure is in how the
   structure is consumed, not in its existence.
4. **Ungated structural boosting is harmful; cue-gated boosting is at worst
   neutral.** The two gated arms never damaged the neutral class; the ungated one did.
5. Answer grounding, unsupported-claim rate and answer utility remain
   **unmeasured** after three rounds. Document-level coverage may be the wrong
   dependent variable for this claim.

## Immediate Next Tasks

1. Execute BENCH-0006 (provenance for evidence reuse/reproduction). This is a
   different claim from CLM-0004b, which concerned provenance for retrieval
   ranking only — Round 3 says nothing about it.
2. Complete durable reconciliation of prior APF research material.
3. Recover individual external-source findings into explicit `ASSET-*` records.
4. Attach every material asset to one or more claims or mark it
   reference-only/duplicate/out-of-scope/insufficient.
5. Record predeclared falsifiers and baseline controls before running experiments.
   The Round 3 predeclaration is the working template for this.
6. Execute, preserve raw results, and revise claim scope based on outcomes.
7. Only then consider architecture candidate promotion.

## Open Questions / Risks

- Every benchmark round so far has used APF's own governance corpus, whose hub
  topology is likely atypical. Both positive and negative results are bounded by
  this. An independent engineering corpus is required before generalising.
- The same operator writes the questions, implements the mechanisms and scores
  the results. Round 3 added null models and a neutral control class to limit
  this, and those controls are what caught the Round 2 bias — but they do not
  eliminate it.
- Three declared BENCH-0004 primary measures were never measured. A benchmark
  that never measures its own declared primary metrics cannot settle its claim.

## Non-Goals

- Do not freeze architecture from the current claim list.
- Do not select a graph DB or agent runtime as an APF contract merely because the research mentions it.
- Do not treat repeated source agreement as proof.
- Do not build a broad implementation before high-leverage claims have been tested.

## Repository Independence

This repository remains independent from `chayobi03-cyber/agent-factory`. No AgentFactory architecture, governance, or code is inherited automatically.
