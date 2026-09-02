# BENCH-0004 Round 3 — Mechanism Decomposition Predeclaration

**Status:** PREDECLARED / not executed at time of writing
**Target claim:** CLM-0004 — Temporal/provenance-aware history improves engineering retrieval
**Frozen corpus commit:** `0d2776986d742eb8e9443a2dc9a95bcc3374efbb` (2026-08-31)

> This document is committed **before** the harness is implemented and **before** any
> result is observed, to satisfy `P0_BENCHMARK_CASES` cross-case execution rule 1
> ("declare falsifiers before observing results"), rule 2 ("freeze task populations
> before comparing conditions") and `P0_FALSIFICATION_BENCHMARK_MATRIX` rule B3.
>
> Nothing in this document may be edited after results are observed. Deviations
> discovered during execution must be recorded in the execution report as
> deviations, not silently corrected here.

## 1. Why Round 3 exists

Round 3 is not a discretionary extension. It is required by three independent
repository sources:

| Source | Requirement |
|---|---|
| `CLAIM_COLD_REVIEW` (CLM-0004 row) | "Require matched retrieval baselines and **ablation of relationship, temporal, and provenance features**" |
| `FALSIFICATION_BENCHMARK` §8 Ablation requirement | "When a claim depends on multiple mechanisms, remove one mechanism where practical" |
| `BENCH-0004_R2` §10 Required next attack | Compare C vs D1 temporal-only / D2 relationship-only / D3 provenance-only / D4 combined |

Round 2 limitation #6 states the defect Round 3 must repair:

> "Provenance, temporal, and relationship effects are not fully separated from one another in this round."

Round 2 reported D beating C by +0.208 chain coverage@2. That result is
**uninterpretable as evidence for CLM-0004** until the contributing mechanism is
identified, because CLM-0004 asserts value for chronology, provenance,
configuration *and* relationships jointly. A gain produced entirely by one
mechanism would not support the claim as worded.

`FALSIFICATION_BENCHMARK` §9 already predeclares the split target:

```text
CLM-0004 broad claim
      ↓
CLM-0004a temporal awareness
CLM-0004b provenance awareness
CLM-0004c relationship awareness
```

## 2. Changes from Round 2 (declared in advance)

| Dimension | Round 2 | Round 3 |
|---|---|---|
| Corpus size | 7 documents | 21 documents (all repository Markdown at frozen commit) |
| Mechanisms | fused into one arm `D` | separated into `D1`/`D2`/`D3`, recombined as `D4` |
| Relationship graph | **hand-specified** by the operator | **mechanically derived** from filename mentions and shared identifiers |
| Structure control | none | degree-preserving shuffle / permutation null distributions |
| Specificity control | none | neutral question class that no mechanism should help |
| Weight sensitivity | not tested | α swept over {0.25, 0.5, 1.0} |
| Latency | not measured | measured (a declared BENCH-0004 primary metric, unmeasured in R1 and R2) |

The hand-specified graph is the most serious Round 2 threat to validity: an
operator who knows the questions can draw edges that produce the desired ranking.
Round 3 removes operator discretion from graph construction.

## 3. Frozen corpus (21 documents)

Frozen at commit `0d27769`. Document IDs used in all result tables:

| ID | Path |
|---|---|
| README | `README.md` |
| CONSTITUTION | `CONSTITUTION.md` |
| ARCH | `docs/architecture/README.md` |
| DECISIONS | `docs/decisions/README.md` |
| HOTL | `docs/governance/HOTL_GOVERNANCE.md` |
| LESSONS | `docs/governance/LESSONS_LEARNED_2026-08-30-engineering-work-mvp.md` |
| MASTER | `docs/governance/MASTER_SESSION_PROMPT.md` |
| NEXT_UX | `docs/handoff/NEXT_SESSION_PROMPT_ENGINEERING_WORK_UX.md` |
| SESSION_STATE | `docs/handoff/SESSION_STATE.md` |
| LEDGER | `docs/research/ASSET_LEDGER.md` |
| COLD_REVIEW | `docs/research/CLAIM_COLD_REVIEW.md` |
| CLAIM_INVENTORY | `docs/research/CLAIM_INVENTORY.md` |
| RECONCILIATION | `docs/research/CLAIM_RECONCILIATION.md` |
| FB_DESIGN | `docs/research/FALSIFICATION_BENCHMARK.md` |
| BENCH_CASES | `docs/research/P0_BENCHMARK_CASES_v0.1.md` |
| P0_MATRIX | `docs/research/P0_FALSIFICATION_BENCHMARK_MATRIX.md` |
| CORPUS_MAP | `docs/research/RESEARCH_CORPUS_MAP.md` |
| TRACE_MAP | `docs/research/RESEARCH_TO_CLAIM_MAP.md` |
| RECON_STATUS | `docs/research/RESEARCH_TO_CLAIM_RECONCILIATION_STATUS.md` |
| EXEC_R1 | `docs/research/executions/BENCH-0004_RUN_2026-08-31.md` |
| EXEC_R2 | `docs/research/executions/BENCH-0004_R2_2026-08-31.md` |

This predeclaration document is **excluded** from the corpus to avoid
self-reference.

### Known corpus defect (declared before execution)

`TRACE_MAP` contains four dangling AI-tool citation artifacts of the form
`fileciteturnNfileM`. These are unresolvable provenance markers committed into a
traceability document. They are left in place for Round 3 so the corpus matches
the frozen commit. Expected impact: negligible, because these are rare tokens
that appear in no query. They are recorded here so that the defect cannot later
be mistaken for a post-hoc explanation of a result.

## 4. Conditions

All conditions share one tokenizer, one index, and one corpus. Only the scoring
term differs. `α = 0.5` is applied uniformly to every mechanism so that no arm
receives a tuned advantage.

- **B — semantic baseline.** TF-IDF cosine over document body text.
  `tf = 1 + log(count)`, `idf = log(N/df) + 1`, L2-normalised, cosine similarity.
- **C — semantic + metadata.** `B + α · cos(query, metadata_text)` where
  `metadata_text` is the H1 title, bolded field lines (`**Status:**` etc.) and
  path segments. C is the required BENCH-0004 control for "improvement explained
  by better indexing or metadata alone". **C, not B, is the comparison baseline
  for every D arm.**
- **D1 — temporal only.** `C + α · temporal_signal`
- **D2 — relationship only.** `C + α · relationship_signal`
- **D3 — provenance only.** `C + α · provenance_signal`
- **D4 — combined.** `C + α · (temporal_signal + relationship_signal + provenance_signal)`

### 4.1 Mechanism definitions (fixed before execution)

**Relationship signal (D2).** Edges are derived mechanically, with no operator
choice:

1. `mention` edge `d1 → d2` if the body of `d1` contains the basename of `d2`.
2. `shared-identifier` edge `d1 ↔ d2` weighted by the count of identifier tokens
   matching `CLM-\d+`, `BENCH-\d+`, `FB-\d+`, `ASSET-[A-Z0-9*]+`, `HP-\d+`,
   `CLM-\d+[a-c]` present in both documents, divided by the total distinct
   identifiers in the pair.

Edge weights are row-normalised. The signal is one propagation step:
`rel(d) = Σ_{d'} w(d, d') · base_C(d')`, then min-max normalised across documents.

**Temporal signal (D1).** Derived from `git log` over the frozen commit range:
each document receives a first-commit index and a last-commit index. The signal
is gated by temporal cue tokens in the query
(`first, second, initial, latest, prior, previous, before, after, then, next,
changed, change, round, order, sequence, so far, already, subsequent, earlier,
later, updated, current`). When gated on, the signal is the mean of
(a) min-max normalised last-commit recency and (b) commit-adjacency propagation
from the top-1 document under C (documents committed nearer in sequence to the
top-1 document score higher). When no cue token is present the signal is zero.

**Provenance signal (D3).** For each document, provenance text is extracted
mechanically as the lines matching `**Status:**`, `**Date:**`, `**Scope:**`,
`**Purpose:**`, `**Target claim:**`, `**Session:**`, and any `v\d+\.\d+` version
token. The signal is `cos(query, provenance_text)`, gated by provenance cue
tokens (`status, version, date, executed, design-ready, marked, current, state,
provenance, scope, purpose, complete, partial, pilot`). Zero when no cue token
is present.

Cue lists are fixed here and may not be extended after seeing results.

### 4.2 Null-model control arms

For each mechanism, a null arm destroys the encoded structure while preserving
its statistical shape, over **200 seeds** each:

- **D1-shuf** — random permutation of commit order across documents.
- **D2-shuf** — degree-preserving random rewiring of the edge set.
- **D3-shuf** — provenance text randomly reassigned between documents.

If a true arm cannot beat its own null distribution, its apparent gain is
ranking perturbation rather than encoded structure.

## 5. Frozen task set (16 questions)

Questions are frozen here with their required evidence sets **before** the
harness exists. Each question is assigned a class that predicts which mechanism,
if any, should help it.

Class N is a **negative control**: these answers sit inside one topically obvious
document and require no history, no relations and no provenance reasoning. No
mechanism should improve them.

| ID | Class | Question | Required evidence |
|---|---|---|---|
| N1 | NEUTRAL | What fields are required in a minimum APF decision record? | DECISIONS |
| N2 | NEUTRAL | What does the asset record template contain and what adoption values are allowed? | LEDGER |
| N3 | NEUTRAL | Which entities are listed in the candidate domain model of the architecture workspace? | ARCH |
| N4 | NEUTRAL | What is explicitly avoided in the capture-first engineering UX session? | NEXT_UX |
| R1 | RELATION | Which benchmark tests the temporal/provenance-aware retrieval claim, and what did its first execution conclude? | CLAIM_INVENTORY, BENCH_CASES, EXEC_R1 |
| R2 | RELATION | Which claim does the provenance ablation benchmark test, and how was that claim's wording narrowed? | BENCH_CASES, COLD_REVIEW, CLAIM_INVENTORY |
| R3 | RELATION | Which research lesson motivated the structured-retrieval claim, and which benchmark family tests it? | LESSONS, CLAIM_INVENTORY, FB_DESIGN |
| R4 | RELATION | Which explicit relations link a research asset to a claim, a benchmark and evidence? | TRACE_MAP, RECONCILIATION |
| T1 | TEMPORAL | What did the first retrieval ablation conclude, and what did the second round change about that conclusion? | EXEC_R1, EXEC_R2 |
| T2 | TEMPORAL | Which limitation of the first round motivated the cross-document task design of the second round? | EXEC_R1, EXEC_R2 |
| T3 | TEMPORAL | What is the declared benchmark execution order, and which benchmarks have execution records so far? | BENCH_CASES, EXEC_R1, EXEC_R2 |
| T4 | TEMPORAL | What was the claim state before benchmarking and what is its state after the second round? | CLAIM_INVENTORY, EXEC_R2, SESSION_STATE |
| P1 | PROVENANCE | Which benchmark documents are marked design-ready but not executed, and which are marked executed pilot results? | BENCH_CASES, EXEC_R1, EXEC_R2 |
| P2 | PROVENANCE | What is the current corpus reconciliation status and what is its declared exit criterion? | RECON_STATUS, CORPUS_MAP |
| P3 | PROVENANCE | Which provenance fields must engineering evidence retain, and which claim formalises that requirement? | LESSONS, CLAIM_INVENTORY |
| P4 | PROVENANCE | What is the constitution's version and status, and how many architecture decisions does the session state record? | CONSTITUTION, SESSION_STATE |

## 6. Metrics

**Primary — chain coverage@k.** Fraction of a question's required evidence
documents present in the top-k retrieved set. Reported at k = 2, 3, 5, as a mean
over all questions and broken down per class.

**Secondary — complete chain@k.** Binary: all required documents present in top-k.

**Cost — latency.** Mean wall-clock milliseconds per query per condition,
including signal computation. Declared as a BENCH-0004 primary measure and
unmeasured in Rounds 1 and 2. Reported as a fitness cost, per
`FALSIFICATION_BENCHMARK` §3E.

## 7. Predeclared falsifiers

Evaluated at k = 3 on the mean over all 16 questions unless stated otherwise.
The effect threshold is **+0.05 absolute mean chain coverage**.

- **F1 — mechanism independence.** If no individual arm (D1, D2, D3) exceeds C by
  ≥ 0.05, the mechanisms carry no independent retrieval value at this scope, and
  CLM-0004a/b/c are each recorded as unsupported.
- **F2 — replication.** If D4 does not exceed C by ≥ 0.05, the Round 2 positive
  result fails to replicate on a larger corpus with a mechanically derived graph,
  and the broad form of CLM-0004 is **FALSIFIED at this scope**.
- **F3 — structure specificity.** For any arm claiming a gain, if the true arm's
  mean coverage does not exceed the **95th percentile** of its own shuffled null
  distribution, the gain is not attributable to encoded structure and that
  mechanism claim is rejected as confounded.
- **F4 — class specificity.** If an arm's improvement on the NEUTRAL class is
  greater than or equal to its improvement on its targeted class, the effect is
  non-specific ranking perturbation rather than mechanism-specific reasoning, and
  that mechanism claim is rejected.
- **F5 — weight artefact.** If the sign of an arm's effect changes across
  α ∈ {0.25, 0.5, 1.0}, the result is a weight artefact and is reported as
  INCONCLUSIVE regardless of its value at α = 0.5.

## 8. Predeclared claim-state decision rule

| Outcome | Recorded state |
|---|---|
| Mechanism passes F1, F3, F4 and F5 | Corresponding narrow claim provisionally SUPPORTED **within this corpus scope only** |
| Mechanism fails F1 | Corresponding narrow claim UNSUPPORTED at this scope |
| Mechanism fails F3 or F4 | Corresponding narrow claim REJECTED as confounded |
| Mechanism fails F5 | Corresponding narrow claim INCONCLUSIVE |
| D4 fails F2 | Broad CLM-0004 FALSIFIED at this scope |

Independent of outcome, broad CLM-0004 is **SPLIT** into CLM-0004a (temporal),
CLM-0004b (provenance) and CLM-0004c (relationship), because
`FALSIFICATION_BENCHMARK` §9 requires splitting a claim that "contains multiple
independent mechanisms". The split is recorded as a claim-inventory change with
the original wording preserved, per cross-case execution rule 5.

## 9. Declared limits of this round (before results)

These limits hold whatever the outcome and may not be softened afterwards:

1. The corpus remains APF dogfood material and is **not** an independent
   engineering corpus. A positive result cannot generalise beyond it.
2. Ground truth is document-level, not answer-span or expert judgment.
3. No answer generation is performed, so unsupported-claim rate and answer
   utility — both declared BENCH-0004 primary measures — remain **unmeasured**
   after Round 3.
4. n = 16 questions, and the class breakdowns are n = 4 each. Per-class results
   are directional only and carry no statistical power.
5. The questions were written by the same operator who implements the mechanisms.
   The neutral class and null models limit but do not eliminate this bias.
6. No result from this round authorises architecture promotion. Per
   `CLAIM_RECONCILIATION`, an ARCHITECTURE_CANDIDATE additionally requires
   counter-evidence review, scope update and an explicit human decision record.

## 10. Replication

The harness is committed at `tools/bench/bench0004_r3.py`, is dependency-free
(Python standard library only), and is deterministic given the frozen commit and
a fixed seed. Raw per-question output is preserved alongside the execution report.
