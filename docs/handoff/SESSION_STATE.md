# APF Session State

**Session:** BENCH-0004 mechanism decomposition, then structure refactor
**Status:** Active working state
**Last updated:** 2026-09-03 (PCB/ODB++ shielding inspection methodology research)

## Repository Evidence

- Repository: `chayobi03-cyber/agent-platform`
- Default branch: `main`
- Working branch: `claude/pcb-odb-shielding-inspection-uzazqx`
- Foundation bootstrap committed
- Claim inventory, traceability protocol, corpus map, cold review and benchmark
  register are committed; four superseded documents remain as stubs so that
  paths cited by execution records stay resolvable
- BENCH-0004 executed three times; execution records and raw results committed
- First falsification harness committed at `tools/bench/bench0004_r3.py`
  (standard library only, deterministic, independently replayable)

## Current State

- Constitution: v0.1 candidate/foundation
- Master Session Prompt: v0.3 operating protocol
- Research Asset Ledger: three `ASSET_CANDIDATE` records (ASSET-0001..0003); no accepted assets yet
- Claim Inventory: v0.1 established; initial claims CLM-0001 through CLM-0010
- Research Corpus Map: corpus reconciliation is explicitly partial
- Claim Cold Review: v0.1 established; wording/causal-overreach issues identified
- Benchmark Register: v1.0 canonical; BENCH-0004 executed (3 rounds), remainder untested
- Research-to-Claim traceability and reconciliation protocol: consolidated into one document
- CLM-0004: **FALSIFIED at tested scope**; split into CLM-0004a/b/c, none surviving
- Domain Model: candidate only
- Architecture Contract: not established
- Architecture Decisions: **DEC-0001** recorded (identifier unification and document
  consolidation). It is a records-keeping decision and establishes no architecture contract
- HoTL Governance: initialized

### Structure refactor (DEC-0001, 2026-09-02)

The research layer previously carried three documents defining benchmarks and four
covering reconciliation, with three conflicting execution orders, three claim-state
vocabularies, two identifier schemes and two record templates in force at once.
Recording CLM-0004's state after Round 3 had required mixing two of those vocabularies.

Each subject is now declared in exactly one place. Emptied documents are retained as
superseded stubs because execution records cite their paths and are append-only evidence.

The BENCH-0004 harness was split into `tools/apfbench/` (reusable) and
`tools/bench/bench0004_r3.py` (this benchmark's frozen specification), so BENCH-0006
inherits the infrastructure rather than copying it.

Two guards were added and both pass:

- `tools/tests/test_reproducibility.py` — recorded R3 evidence reproduces bit-identically.
  Committed **before** the refactor so it is a real baseline rather than a test fitted
  to the outcome.
- `tools/tests/test_docs_integrity.py` — dangling references, citation artifacts,
  duplicate order declarations and retired identifiers now fail a test instead of
  surviving unnoticed.

### Domain research probe — PCB/ODB++ shielding inspection (2026-09-03)

First research in this repository against an **external engineering domain** rather
than APF's own governance corpus: how to inspect an ODB++ job for breaks and
overlaps in a signal's shielding, given a request to capture the board at real
viewer fidelity.

Recorded in `docs/research/PCB_ODB_SHIELDING_INSPECTION_METHODOLOGY.md`, with three
`ASSET_CANDIDATE` records added to `docs/research/ASSET_LEDGER.md` (the ledger's
first entries) and reproducible arithmetic in `tools/research/pcb_shield_budget.py`,
pinned by `tools/tests/test_pcb_shield_budget.py`.

Principal finding: the request's stated order — capture, then inspect — inverts the
dependency. A raster capture discards the net attribution that defines which copper
is the shield, cannot see an electrically floating shield at all, and is either
blind to the defect sizes in question or costs ~9 GB per copper stack to measure
them. Capture belongs downstream as evidence, and sideways as a cross-check that
falsifies the parse. Recommended method is vector-exact verdicts with rendered
evidence; six named checks replace the single ambiguous one, because "break" and
"overlap" each denote several physically distinct defects.

Nothing here is accepted, and no benchmark was registered — §12 of the document
lists the five points that require a human decision, including whether this domain
becomes an APF test case at all.

**Limitation on the record:** the normative ODB++ specification host is refused by
this session's egress policy, so the format details are inferred from two
independent open-source parsers that agree with each other. That is weaker than
the specification and is flagged in the document as a re-verification task.

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

## Benchmark Execution Position

The execution order is declared once, in `docs/research/BENCHMARK_REGISTER.md` §2.
This section records only where the project currently stands in it — it must not
restate the order, or the repository regains the multiple-declaration defect that
`DEC-0001` removed.

- **Completed:** BENCH-0004 (3 rounds; CLM-0004 falsified at tested scope)
- **Next:** BENCH-0006 provenance ablation
- **Remaining:** everything after BENCH-0006 in the register's order

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
- The DEC-0001 consolidation **changed the corpus topology** that R3 measured:
  merging overlapping documents removes cross-references that were themselves hub
  edges. Recorded R1–R3 results are unaffected because the harness reads the frozen
  commit `0d27769`, but a future round against the current corpus is measuring a
  different corpus. Pin the same frozen commit or declare a new one and treat the
  earlier rounds as historical baselines only. See `BENCHMARK_REGISTER.md` §6.

## Non-Goals

- Do not freeze architecture from the current claim list.
- Do not select a graph DB or agent runtime as an APF contract merely because the research mentions it.
- Do not treat repeated source agreement as proof.
- Do not build a broad implementation before high-leverage claims have been tested.

## Repository Independence

This repository remains independent from `chayobi03-cyber/agent-factory`. No AgentFactory architecture, governance, or code is inherited automatically.
