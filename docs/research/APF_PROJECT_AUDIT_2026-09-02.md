# APF Project Audit — 2026-09-02

**Scope:** Full repository state, claim and hypothesis coverage, evidence-chain integrity,
governance compliance, and progress against the stated goals in `docs/handoff/SESSION_STATE.md`.
**Method:** Executed checks against repository content, not assertion. Every result below was
produced by a check that ran; where a check could not run, that is stated. Counts include this
audit document itself. The first cross-reference pass under-resolved by searching too few
candidate directories and was re-run with basename resolution; the corrected figures are used.

## 1. Verdict

**Governance discipline: strong. Evidence production: thin. One structural gap: material.**

The project consistently refuses to overclaim. Across every document, CLM-0004 is recorded as
`INCONCLUSIVE` with an explicit non-promotion guard, blocked states are labelled blocked rather
than approximated, and a prior session declined to fabricate an answer set when generation was
unavailable. That is the behaviour the Constitution asks for and it is holding.

What is thin is throughput. One of ten claims has any execution against it, and that one is
inconclusive. Zero of twelve v0.2 hypotheses have been executed. The binding constraints are
inputs — corpus independence, an asset population, fixture bytes, model credentials — not
analytical rigour.

The material gap is **F1**: the project's strongest quantitative result has no claim record to
attach to.

## 2. Repository state

| | |
|---|---|
| Working tree | clean |
| Branch | `claude/handover-eu02yk`, 1 commit ahead of `main` |
| Files | 34 (excluding `.git`) |
| Documentation | 3,422 lines across 26 markdown files under `docs/` |
| Tooling | 3 Python scripts, standard library only |
| Cross-references | 60 resolvable; 8 unresolved — 7 are runtime artifacts not yet created (`contexts_96.jsonl`, `answers_96.jsonl`, `VERIFICATION.json`, `ANSWER_MANIFEST.json`, `ABORT_REASON.json`, `generator.json`, `scores.jsonl`) and 1 names the handoff bundle's own file. No broken repository reference. |
| Decision records | **0** |
| Architecture contracts | 0 (foundation stage, as declared) |

Tooling regression re-run at audit time: `verify_fixture` returns 0 on a valid bundle and 2 on
a docs-only bundle; `analyze_e2` returns 0. No regressions.

## 3. Coverage

### 3.1 Claims (Track A, v0.1)

| Claim | P0 | Executions | State |
|---|:--:|---|---|
| CLM-0001 work-centric generality | P0 | — | NOT TESTED |
| CLM-0002 capture value | P0 | — | NOT TESTED |
| CLM-0003 progressive disclosure | | — | NOT TESTED |
| CLM-0004 structured retrieval | P0 | R1, R2, E2 | **INCONCLUSIVE** |
| CLM-0005 failure evidence | | — | NOT TESTED |
| CLM-0006 provenance trust | P0 | — | NOT TESTED |
| CLM-0007 human boundary | P0 | — | NOT TESTED |
| CLM-0008 primitive extraction | | — | NOT TESTED |
| CLM-0009 measured automation | P0 | — | NOT TESTED |
| CLM-0010 engineering augmentation | | — | NOT TESTED |

**1/10 claims executed. 5 of 6 P0 claims untested.**

### 3.2 Hypotheses (Track B, v0.2)

12 hypotheses, `H01`–`H12`. **2 designed** (`T07`, `T11`, both this session), **0 executed**.

## 4. Goal check — `SESSION_STATE.md` immediate next tasks

| # | Task | Status |
|---|---|---|
| 1 | Complete durable reconciliation of prior research material | PARTIAL |
| 2 | Recover external-source findings into explicit `ASSET-*` records | **NOT STARTED** |
| 3 | Attach every material asset to claims or mark out-of-scope | **NOT STARTED** (blocked by 2) |
| 4 | Create benchmark datasets/fixtures for BENCH-0004 and BENCH-0006 | 0004 PARTIAL (fixture exists but outside the repository); 0006 NOT STARTED |
| 5 | Record predeclared falsifiers and baseline controls before running | DONE for BENCH-0004 |
| 6 | Execute, preserve raw results, revise claim scope | Executed; **claim scope not revised** — see F1 |
| 7 | Only then consider architecture candidate promotion | Correctly not done |

Benchmark execution order: `BENCH-0004` has 3 executions. `BENCH-0006`, `BENCH-0002`,
`BENCH-0007`, `BENCH-0009`, `BENCH-0001` have **zero**. The queue has not advanced past its
first entry.

## 5. Findings

### F1 — HIGH — The factorial evidence has no claim to attach to

`FALSIFICATION_BENCHMARK.md` §9 gives the canonical split of CLM-0004 as:

```text
CLM-0004a temporal · CLM-0004b provenance · CLM-0004c relationship
```

`BENCH-0004_R2` §10 required exactly that decomposition as the next attack. The E2 factorial
then **executed** it, producing per-mechanism effects with p-values (T p=0.023, R p=0.024,
P p=0.001, case block p<1e-13, R²=0.733).

`CLM-0004a`, `CLM-0004b` and `CLM-0004c` do not exist in `CLAIM_INVENTORY.md`. Repository
search returns zero matches.

So the strongest quantitative result the project holds cannot update any claim record. It sits
in an execution record with nothing downstream. v0.2's own required metric — *claim→evidence
linkage completeness* — fails at exactly this point, and v0.1 §8 promotion requires a claim
record that here does not exist.

This is also a slow-drift risk: each further execution widens the gap between what has been
measured and what the inventory says is known.

**Action:** enter `CLM-0004a/b/c` into the inventory with the factorial result attached as
scoped, retrieval-level evidence. This does not promote anything — the mechanism claims stay
bounded to context sufficiency in a controlled reconstruction until E2 executes.

### F2 — HIGH — The asset ledger is empty, and two benchmark tracks start there

`ASSET_LEDGER.md` contains its state model and record template and **zero `ASSET-*` records**.

Consequences:

- `SESSION_STATE` next task #2 is not started, and #3 is blocked behind it.
- `T07` (asset reuse) and `T11` (asset invalidation) both require a promoted asset population.
  Both are blocked at step 0, not by design difficulty.
- The governance model routes `Research → Asset → Claim`, but no claim carries populated
  `source_assets`. The provenance leg of that chain is unpopulated.

### F3 — MEDIUM — No claim satisfies the inventory's own quality gate

`CLAIM_INVENTORY.md` §5 states a claim is `TESTABLE` only with six elements present. Measured
across all ten claims:

| Element | Claims having it |
|---|---:|
| bounded statement | 10/10 |
| falsifier | 10/10 |
| explicit scope | 0/10 |
| explicit non-scope | 0/10 |
| observable prediction | 0/10 |
| minimum evidence | 0/10 |

The §4 record template defines 23 fields; **zero claims are populated with it**. BENCH-0004 was
nonetheless executed against CLM-0004.

This is not an argument that the executions were invalid — statement plus falsifier is a
workable operating minimum, and the R1/R2 runs did predeclare falsifiers. It is that the
document's stated gate and its actual practice disagree. Resolve in one direction: either
complete the records for the P0 claims, or amend §5 to describe the minimum actually in use and
record why.

### F4 — MEDIUM — Coverage is 1/10 claims and 0/12 hypotheses

Restated from §3 as a standing risk rather than a new observation. Five of six P0 claims —
the ones whose failure would invalidate broad portions of the platform thesis — have no
evidence at all. The project's confidence in its own thesis currently rests on one inconclusive
retrieval experiment over an APF-dogfood corpus.

### F5 — MEDIUM — BENCH-0004-E2 remains blocked at G1

Fixture source bytes absent; no LLM credential in the environment. Detailed in
`executions/BENCH-0004_E2_2026-09-01.md` §4. Unchanged by this audit.

### F6 — LOW — Same-name scripts are not the same scripts (fixed)

`tools/bench0004_e2/` contains `run_generator.py` and `analyze_e2.py`, the same filenames the
handoff lists as missing. These are new implementations written against `PROTOCOL.md`, not
recovered originals; prompt construction in particular is unknown for the original. Fixed this
session by stating the distinction in the E2 record §4. Flagged because assuming
interchangeability would contaminate the run.

### F7 — LOW — Date skew between handoff and record

`BENCH-0004_E2_2026-09-01.md` is dated one day before the `2026-09-02` handoff it describes.
Explicable as KST/UTC skew (the handoff is stamped KST). Harmless, but the E2 protocol depends
on timestamp discipline, so it is noted rather than ignored.

### F8 — LOW — No decision records exist, including for a structural change made this session

`docs/decisions/` holds zero records. For a foundation-stage project with no accepted assets or
contracts that is largely correct.

However, the decision to run v0.1 and v0.2 as **parallel tracks** rather than superseding v0.1
is a structural governance change: it determines which instrument adjudicates what, and
`CLAIM_HYPOTHESIS_MAP.md` now depends on it. Constitution §3 places architecture and contract
changes under human ownership, and §7 requires the sequence to terminate in a human decision.
The change was directed by the project owner in session, but no decision record exists.

**Action:** record it. A draft can be prepared for approval; it should not be self-approved.

## 6. Evidence-chain integrity

| Check | Result |
|---|---|
| CLM-0004 status consistent across all documents | **PASS** — `INCONCLUSIVE` everywhere, no document asserts promotion |
| Any document claiming E2 executed or answers frozen | **NONE** |
| Non-promotion guards present in execution and protocol documents | 5 documents |
| Handoff hash cross-document consistency | **PASS** — exactly 4 distinct SHA-256 literals, no conflicting value |
| Factorial arithmetic reproducible from published cell means | **PASS** — all 7 effects, deviation < 5e-5 |
| Byte-level fixture verification | **PENDING** — source bytes unavailable |
| Claim→evidence linkage | **FAIL** — see F1 |

## 7. Governance compliance

| Constitution | Status |
|---|---|
| §3 human accountability | Holding, with the F8 exception |
| §4 state separation | Holding — no state is asserted as another; blocked states stay blocked |
| §5 evidence before architecture | Holding — no architecture derived from the inconclusive result |
| §6 framework neutrality | Not yet exercised |
| §7 change governance | Sequence followed up to Human Decision, which is unrecorded (F8) |
| §8 repository independence | Holding — no AgentFactory inheritance observed |

## 8. Recommended order

1. **F1** — enter `CLM-0004a/b/c` and attach the factorial result as scoped retrieval-level
   evidence. Cheapest high-value fix; closes the linkage failure.
2. **F8** — record the parallel-track decision for human approval.
3. **F2** — populate `ASSET-*` records. Unblocks next tasks #2 and #3 and both T07 and T11.
4. **F3** — resolve the gate/practice disagreement for the six P0 claims.
5. **F5** — deliver the fixture bundle; G2 is then one command.
6. **F4** — advance the benchmark queue past BENCH-0004; BENCH-0006 is next and its
   provenance ablation shares mechanism structure with the P factor already measured.

Nothing in this audit changes any claim state. **CLM-0004 remains INCONCLUSIVE and unpromoted.**
