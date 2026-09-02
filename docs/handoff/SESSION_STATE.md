# APF Session State

**Session:** Claim Inventory → Cold Review → P0 Benchmark Execution → Governance Decisions
**Status:** Active working state
**Last updated:** 2026-09-02

## Repository Evidence

- Repository: `chayobi03-cyber/agent-platform`
- Default branch: `main`
- Working branch: `claude/session-governance-decisions-6fi9vf`
- HEAD at last state update: `0d27769` (`research: execute BENCH-0004 round 2 cross-document temporal attack`)
- Foundation bootstrap committed
- Claim inventory, reconciliation protocol, corpus map, cold review, benchmark cases, and two BENCH-0004 execution records are committed

## Current State

- Constitution: v0.1 candidate/foundation
- Master Session Prompt: v0.3 operating protocol
- Research Asset Ledger: initialized; no accepted assets yet
- Claim Inventory: v0.1 established; CLM-0001 through CLM-0011; state index at `docs/research/claims/README.md`
- Claim Reconciliation Protocol: v0.1 established
- Research Corpus Map: v0.1 established; `CORPUS_RECONCILIATION = PARTIAL`
- Claim Cold Review: v0.1 established; wording/causal-overreach issues identified
- P0 Falsification Benchmark Matrix: v0.1 established
- P0 Benchmark Cases: v0.1 operationalized; BENCH-0004 executed, remaining cases design-ready
- Research-to-Claim traceability: established
- Domain Model: candidate only
- Architecture Contract: not established
- Architecture Decisions: DEC-0001 (evidence gate) and DEC-0002 (claim record completion timing) recorded and in force
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

## Governance Gate — DEC-0001 / DEC-0002

Records:

- `docs/decisions/DEC-0001-evidence-gate.md` — evidence gate on architecture promotion and implementation start
- `docs/decisions/DEC-0002-claim-record-completion-timing.md` — claim records completed per benchmark, option C

**DEC-0001 and DEC-0002 block nothing mechanically and everything in governance terms.**

There is no CI check, hook, or tooling that enforces them. Enforcement is normative: the absence of a mechanical block is not permission. A later session must not read "the repository let me do it" as evidence that the gate was cleared. This is the same rule the Constitution already states — a commit is not a decision.

Practical consequence for the next session:

- No architecture contract may be promoted from the current claim set.
- No implementation may be started on the strength of benchmark results alone.
- Benchmark execution, claim scoping, and corpus work remain open; consequential promotion does not.

DEC-0001 §4 states the four exit criteria a claim must meet to leave the gate: an independent corpus, a predeclared falsifier that was not met, a claim scope matching what the run tested, and a separate decision record authorizing the promotion. DEC-0001 §3 lists what the gate does and does not block — it blocks promotion, not investigation.

DEC-0002 selected **option C**: claim records are not completed as a batch up front. Each claim record is completed individually, at the point its benchmark is being prepared. Preparing a benchmark is therefore the trigger for finishing the corresponding claim record, not a separate later cleanup pass.

## Benchmark Execution Status

| Benchmark | Claim | State |
|---|---|---|
| BENCH-0004 | CLM-0004 | Executed — Rounds 1, 2, and 3. Round 3 is the first run on an independent corpus |
| BENCH-0004 R3 | CLM-0011 | Executed — `BENCH-0004_R3/EXECUTION.md`; all four predeclared falsifiers survived |
| BENCH-0001 | CLM-0001 | Executed — falsifier F4 fired; CLM-0001 `CONTRADICTED` as worded |
| BENCH-0002 | CLM-0002 | Not executed — queued |
| BENCH-0007 | CLM-0007 | Not executed — queued |
| BENCH-0009 | CLM-0009 | Not executed — queued |
| BENCH-0001 | CLM-0001 | Not executed — queued |
| BENCH-0006 | CLM-0006 | No execution record committed — see Unresolved References |

**Remaining queue (4 unverified P0 claims):**

```text
BENCH-0002  capture/context reconstruction
BENCH-0007  approval boundary
BENCH-0009  automation promotion
BENCH-0001  work abstraction coverage
```

### Corpora

| ID | Source | Role |
|---|---|---|
| CORPUS-0001 | `python/peps` @ `a4f4971` | First independent corpus; satisfies DEC-0001 exit criterion 1 |
| CORPUS-0002 | 16 workflows, 4 pinned third-party repos | BENCH-0001; six workload classes |

### BENCH-0004 outcome as recorded

- Round 1 falsified the weaker proposition: added structure did not improve document-level recall over a semantic baseline.
- Round 2 showed a cross-document chain-coverage advantage for the relationship/temporal condition (+0.21 at k=2, +0.15 at k=3) on n=8 frozen questions.
- Broad CLM-0004 remains **WEAKENED / INCONCLUSIVE — not promoted**.
- A narrow subclaim (structured retrieval helps recover multi-document evidence chains) is **provisionally supported within pilot scope only**.
- Round 2's own first-listed limitation: the corpus is not independent of APF development.
- Round 3 (independent corpus, 113 chain tasks, preregistered): relationship propagation +0.117 complete@5, CI [+0.053, +0.195]. Temporal did not separate from baseline; provenance marginal; combining added +0.009 while doubling the control cost. Effect vanishes at k=10.
- CLM-0011 is `SUPPORTED` on one corpus and does not clear DEC-0001 (criteria 3 and 4 unmet). Full detail in `BENCH-0004_R3/EXECUTION.md`.

## Standing Contradiction — CONSTITUTION.md section 2

BENCH-0001 fired falsifier F4 against CLM-0001, the claim the Constitution's work-centric boundary rests on. The work-centric core covers 0.664 of agentic-workload concepts against the agent-centric core's 0.900, escaping on in-flight state, inbound signals, and prompt content. It wins overall (+0.142) and on the other five classes.

What is contradicted is the generality — the word "both" — not the direction. The contradiction is recorded and unresolved: amending a Constitution invariant requires explicit review under section 9, and the decision belongs to a human under DEC-0001. Until decided, section 2 carries a known exception for agentic workloads.

Detail: `docs/research/executions/BENCH-0001/EXECUTION.md`.

## Cold Review — 2026-09-02

Recommendations from an end-of-session cold review. **None of these is decided.** They are recorded here because they change the queue order, and a recommendation is not an approval.

1. **The benchmark queue is ordered by testability, not by consequence.** All three executions went to BENCH-0004 because documents alone can run it. CLM-0002 — the actual product thesis, P0, testable in a week with three engineers and a shared notes file — has never been touched because it needs people. Falsification exists to kill bad ideas cheaply; testing the easiest claims first systematically tests the ones that matter least.
2. **Close the retrieval track.** Three rounds is past diminishing returns, and the decision it informs (whether to put a relation graph in the retrieval layer) is cheap to reverse, uncontroversial in the field, and not an architecture invariant. Round 3's value was mostly in what it ruled out.
3. **Round 3's headline finding is closer to arithmetic than discovery.** "+0.317 where an edge exists, 0.000 where it does not" is what score propagation does by definition. The genuine unknowns were narrower: body-reference recovery of declared relations (36%), baseline headroom (0.586 where edges exist), and the control cost. The queries are also synthetic — nobody types a title plus a relation cue — so the result may be an artifact of task construction.
4. **The corpus-independence framing was wrong.** It was the highest-value action inside the retrieval track, and the retrieval track was the wrong track. Acquiring CORPUS-0001 took about fifteen minutes.
5. **Governance mass exceeds what it governs.** Roughly twenty process documents, one tested claim of eleven, no product code, no contact with the EMC/PCB target domain. Suggested budget: a new process document must be one page or retire an existing one. `RESEARCH_CORPUS_MAP`, `RESEARCH_TO_CLAIM_MAP`, `RESEARCH_TO_CLAIM_RECONCILIATION_STATUS`, and `CLAIM_RECONCILIATION` overlap and are merge candidates.
6. **DEC-0001 may need tiering — open decision candidate.** Requiring all four exit criteria for cheap-to-reverse decisions makes the gate hardest to pass for exactly the claims that matter most, given current testing capacity. A gate that cannot be passed is a stall, not rigor. This is a candidate amendment to DEC-0001, not a change to it; DEC-0001 stands as written until a human decides otherwise.

## Next Session Entry Points

1. **DEC-0001 / DEC-0002 are in force.** Mechanically nothing is blocked; in governance terms everything downstream of benchmark execution is. Do not treat missing enforcement as approval.

2. **Secure an independent engineering corpus — highest-value action currently available.** L9 is never mitigated by doing more APF corpus work. Additional dogfood rounds against APF's own documents cannot remove the dependence between the corpus and the thing being tested; only an outside corpus with real revision, configuration, and evidence transitions can. Every further APF-internal retrieval round buys less than the first independent corpus would.

3. **E2b Stage 2** — the design is settled. It needs only immutable model pinning plus credentials to run. No further design work is the blocker.

4. **Continue the queue** — BENCH-0002 / BENCH-0007 / BENCH-0009 / BENCH-0001, the 4 unverified P0 claims.

5. **Claim records are completed individually at benchmark preparation time** (DEC-0002 option C). When picking up a queued benchmark, finish its claim record first as part of preparing it.

## Unresolved References

Recorded as gaps rather than filled by inference, per the Master Session Prompt ("never infer missing state"):

- **DEC-0002's rejected alternatives are a reconstruction.** Only the selection of option C was recoverable from the handoff. The option A / option B wording in the record is derived from repository evidence, not from a transcript of the original deliberation, and is marked as such in DEC-0002 §6.
- **"L9" is ambiguous against repository evidence.** `docs/governance/LESSONS_LEARNED_2026-08-30-engineering-work-mvp.md` §L9 is "Internal history and external knowledge must remain distinguishable." The corpus-independence problem referenced in entry point 2 matches BENCH-0004 Round 2 limitation #1 rather than that lesson text. DEC-0001 §6 sidesteps the label by citing the Round 2 limitation directly; confirm which label is intended before L9 is cited as authority elsewhere.
- **BENCH-0006 (CLM-0006, provenance ablation) has no execution record.** It sat second in the original execution order and is absent from the remaining queue. Either its execution record was never committed or it was deliberately dropped; establish which before treating CLM-0006 as anything other than untested.

## Immediate Next Tasks

1. Decide on the cold review above before picking up any benchmark — item 1 changes what comes next, and items 2 and 6 may retire work already queued.
2. If the queue is reordered: CLM-0002 first, which needs engineers and real engineering artifacts, not documents.
3. If the retrieval track continues instead: second independent corpus, different domain, messier structure — the test of whether 36% extraction coverage was corpus luck. Rule B6 is not satisfied by one corpus.
4. Run E2b Stage 2 once model pinning and credentials are in place.
5. Take the next queued benchmark, complete its claim record as part of preparation (DEC-0002), predeclare falsifiers and baseline controls, then execute and preserve raw results.
6. Continue recovering individual external-source findings into explicit `ASSET-*` records; mark reference-only / duplicate / out-of-scope / insufficient where applicable.
7. Keep `docs/research/claims/README.md` current — it is the single index of claim state and record status.
8. Rewrite CLM-0011 to the scope Round 3 actually tested (k ≤ 5, edge-coverage-bound, control cost), only if the retrieval track continues.
9. Only then consider architecture candidate promotion, via a separate decision record per DEC-0001 §4.

## Non-Goals

- Do not freeze architecture from the current claim list.
- Do not select a graph DB or agent runtime as an APF contract merely because the research mentions it.
- Do not treat repeated source agreement as proof.
- Do not build a broad implementation before high-leverage claims have been tested.
- Do not run further APF-internal retrieval rounds as a substitute for an independent corpus.

## Repository Independence

This repository remains independent from `chayobi03-cyber/agent-factory`. No AgentFactory architecture, governance, or code is inherited automatically.
