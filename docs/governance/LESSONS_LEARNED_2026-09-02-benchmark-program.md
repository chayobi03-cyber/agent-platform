# APF Session Lessons Learned — 2026-09-02

**Scope:** Governance decisions, BENCH-0004 Round 3, and a cold review of the benchmark program
**Status:** Session learning / candidate guidance

## 1. Method lessons

### M1 — Pre-registration is a commit boundary, not a paragraph

The falsifiers and the script were committed with no results, then the run followed. `BETA = 0.50` turned out to be the peak of the post-hoc sweep (0.25 → 0.549, 0.50 → 0.584, 1.0 → 0.540, 2.0 → 0.381, worse than baseline). Without the separate commit, that result is indistinguishable from a tuned one, and no amount of prose asserting "we did not tune" fixes it.

Cost: one extra commit. Make it standard for every execution.

### M2 — Preserve the instrumentation, not just the numbers

Rounds 1 and 2 recorded results and no code. A project whose CLM-0006 asserts that evidence without provenance is materially less trustworthy produced two pieces of evidence without provenance. The claim condemned its own executions and nobody noticed for two rounds.

Every execution preserves its script and raw output, or it is not an execution.

### M3 — Ground truth and mechanism must not share an author

Round 2's relationship graph was hand-specified by the same author as the corpus, so traversal success was partly guaranteed by construction. Round 3 split the channels: ground truth from author-declared headers, mechanism from body-extracted references, overlap measured at 36% rather than assumed.

The general form: if the thing being tested and the thing scoring it come from the same hand, the benchmark measures that hand's consistency.

### M4 — Falsifiers can pass while the explanation fails

Round 3 survived all four predeclared falsifiers and contradicted its own stated mechanism: the margin was flat across the topical-similarity split, where the claim predicted it would concentrate on dissimilar pairs. A surviving claim is not an understood claim. Record both outcomes; do not let the passing falsifier absorb the failing prediction.

### M5 — Ask whether a finding could have come out otherwise

"+0.3171 where a relation edge exists, 0.0000 where it does not" reads as a discovery and is closer to arithmetic: score propagation cannot boost a document with no relevant neighbour. The genuinely unknown quantities were narrower — extraction coverage, baseline headroom, and the control cost.

Before writing up a result, ask what value would have falsified it. If none, it is the algorithm's definition restated, and the write-up should say so.

### M6 — Record the gap instead of filling it

DEC-0001's subject was not recoverable from repository evidence. One question produced a correct record; inference would have produced a plausible fabrication that later sessions would cite as governance authority. The cost of asking was one round trip.

## 2. The structural lesson

### S1 — Testability and consequence are anti-correlated here

All three executions to date went to BENCH-0004, because documents alone can run it. CLM-0002 — the actual product thesis, P0, testable in about a week with three engineers and a shared notes file — has never been touched, because it needs people.

This is not an accident of scheduling. The claims that are cheap to test are cheap precisely because they need no external input, and the claims that decide whether the platform is worth building need users, engineers, or real domain artifacts. **Left unmanaged, a falsification program drifts toward its least consequential claims while appearing rigorous throughout.**

The queue must be ordered by consequence × uncertainty, and the ordering must be revisited when it drifts back.

### S2 — Governance grows unless it is budgeted

Roughly twenty process documents, one tested claim of eleven, no product code, no contact with the EMC/PCB target domain. This session added about 700 lines of governance against about 450 lines of benchmark.

Proposed budget, not yet decided: a new process document must fit one page or retire an existing one.

## 3. ROI of the available next actions

Cost is session-equivalents. Consequence is what breaks if the claim is false.

| Action | Cost | Consequence if false | Uncertainty | External dependency |
|---|---|---|---|---|
| **BENCH-0001** CLM-0001 work-centric abstraction | ~1 | **Constitution §2 collapses; APF is an agent framework after all** | High | **None** |
| BENCH-0002 CLM-0002 capture value | 1 week + 3 engineers | Product thesis dies | High | People — owner only |
| BENCH-0007 CLM-0007 approval boundary | ~2 | Constitution §3 invariant unsupported | High | Honest scenario design is hard |
| BENCH-0006 CLM-0006 provenance | ~1 | Record-keeping burden unjustified | Medium | Corpus with real provenance |
| Second retrieval corpus | ~1 | Bounds an already-bounded, cheap-to-reverse choice | Low | None |
| Governance consolidation | ~0.5 | Reduces every future session's overhead | Low | None |
| E2b Stage 2 | small | — | — | Credentials — owner only |
| DEC-0001 tiering | one decision | Gate stalls the claims that matter most | — | Human decision |

### Verdict

**CLM-0001 is the highest-consequence claim in the inventory, requires no external dependency, and has never been tested.** The Constitution's work-centric boundary — the sentence that makes APF something other than an agent framework — rests entirely on it. BENCH-0001 is a modelling exercise over real third-party workflow specifications, not a user study.

It was last in the execution order. Nothing about consequence justified that placement; it was ordered behind retrieval and provenance because those looked more tractable, which is exactly S1.

Two actions belong to the owner and cannot be done in-session: scheduling BENCH-0002 (three engineers, one week) and supplying E2b credentials. Everything else declines in value relative to BENCH-0001.

**The retrieval track closes at Round 3.** Three rounds bounded the claim to a top-of-ranking effect proportional to extraction coverage, on a cheap-to-reverse indexing decision that is settled practice elsewhere. A fourth round buys less than any row above it.

## 4. Carried forward

- BENCH-0001 is next, preregistered per M1, on an independent third-party workflow corpus per M3.
- The self-scoring risk in BENCH-0001 is the M3 problem in its sharpest form: the same author would write both representations and score them. The rubric must be mechanical and predeclared, and the "essential information" set must come from the source specifications rather than from the modeller.
