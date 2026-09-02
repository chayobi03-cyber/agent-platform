# BENCH-0004 Round 3 — Mechanism Decomposition on an Independent Corpus

**Date:** 2026-09-02
**Status:** Executed / preregistered result
**Claim under test:** CLM-0011 — cross-document evidence chain recovery
**Corpus:** CORPUS-0001 — `python/peps` @ `a4f4971`
**Pre-registration:** commit `132c174`, which contains the falsifiers and `run.py` and no results

## 1. What Round 2 required and what changed

Round 2 section 10 required a decomposition on an independent corpus: separate temporal, relationship, and provenance mechanisms rather than testing them fused, and score against ground truth the benchmark author did not write.

Three things changed from Round 2:

| | Round 2 | Round 3 |
|---|---|---|
| Corpus | APF's own repository, 7 documents | 737 third-party documents |
| Relation graph | hand-specified by the corpus author | extracted from document bodies |
| Ground truth | repository objects chosen by the author | relations declared by PEP authors in headers |
| Tasks | 8 | 113 chain tasks + 100 control |
| Falsifier | stated in prose | 4 predeclared, committed before the run |

Ground truth and mechanism now come from different channels. The benchmark must rediscover, from body text, relations that other people declared in headers. Their overlap is 0.363 — the graph directly covers about a third of the ground-truth pairs, so traversal is not guaranteed by construction.

## 2. Conditions

All conditions rank the same 737 documents against the same mechanically generated queries. A query is the source document's title plus a fixed relation cue, and never contains the target's number or title.

- **C** — TF-IDF cosine baseline.
- **D1** — temporal only: boost documents created after the top-1 anchor, decaying over five years.
- **D2** — relationship only: one-hop score propagation over body-extracted PEP references, `BETA = 0.50`.
- **D3** — provenance only: boost documents sharing the anchor's author, and documents carrying a `Resolution` link.
- **D4** — all three combined.

Parameters were fixed before the run and not tuned. Commit `132c174` is the evidence for that.

## 3. Primary result

**Metric: complete chain@5 on 113 chain tasks. Paired bootstrap over tasks, 2000 resamples.**

| Condition | complete@5 | vs C | 95% CI | P(diff > 0) |
|---|---:|---:|---|---:|
| C | 0.4690 | — | — | — |
| D1 temporal | 0.5044 | +0.0345 | [−0.018, +0.089] | 0.870 |
| D2 relationship | 0.5841 | +0.1171 | [+0.053, +0.195] | 0.999 |
| D3 provenance | 0.5044 | +0.0354 | [+0.000, +0.080] | 0.929 |
| D4 combined | 0.5929 | **+0.1242** | **[+0.044, +0.204]** | 0.999 |

At other k, on the same tasks:

| Condition | complete@3 | complete@5 | complete@10 |
|---|---:|---:|---:|
| C | 0.3186 | 0.4690 | 0.6726 |
| D1 | 0.3274 | 0.5044 | 0.6549 |
| D2 | 0.3717 | 0.5841 | 0.6637 |
| D3 | 0.3540 | 0.5044 | 0.6726 |
| D4 | 0.4248 | 0.5929 | 0.6814 |

**T0 control — single-document retrieval, 100 tasks, hit@5:** C 0.86, D1 0.86, D2 0.84, D3 0.88, D4 0.82.

## 4. Falsifier assessment

Each falsifier as written in `docs/research/claims/CLM-0011.md` before the run.

**F1 — D4 does not exceed C, or the CI includes zero.** D4 = 0.5929 vs C = 0.4690, CI [+0.044, +0.204], excluding zero. **Not met.**

**F2 — the gain is carried by temporal or provenance rather than relationship.** D2 alone gives +0.1171 with CI [+0.053, +0.195]. D1's CI includes zero. D3's lower bound is 0.000. The relationship mechanism is the carrier. **Not met.**

**F3 — C already at ≥ 0.90, no headroom.** C = 0.4690. **Not met.**

**F4 — a winning condition loses more than 5 points on the T0 control.** D2 loses 2.0 points, D4 loses 4.0. **Not met**, but see section 6.

**All four falsifiers survived. CLM-0011 is SUPPORTED on CORPUS-0001, as worded.**

## 5. The prediction that failed

CLM-0011 predicted the margin over C would be larger where the two required documents are topically dissimilar, since that is where semantic retrieval should have no route to the second document.

| Pair similarity | n | C | D4 | margin |
|---|---:|---:|---:|---:|
| below median | 57 | 0.3158 | 0.4386 | +0.1228 |
| above median | 56 | 0.6250 | 0.7500 | +0.1250 |

The margin is flat. **The prediction is not supported.** The falsifiers passed but the mechanistic story attached to them did not: structure is not specifically rescuing the topically dissimilar pairs, it is lifting both halves equally. The effect is real; the stated explanation for it is wrong.

## 6. What the effect actually is

Two exploratory analyses (`posthoc.py`, `results_posthoc.json`) — not part of the verdict.

**The entire gain is confined to tasks where the extracted edge exists.**

| | n | C | D2 | delta |
|---|---:|---:|---:|---:|
| body-reference edge present | 41 | 0.5854 | 0.9024 | **+0.3171** |
| body-reference edge absent | 72 | 0.4028 | 0.4028 | **0.0000** |

Where the mechanism has an edge it works very well; where it does not it does exactly nothing, to four decimal places. So the aggregate +0.117 is not a property of the propagation rule — it is 0.317 diluted by 36% edge coverage. **The binding constraint on this claim is relation extraction coverage, not the retrieval mechanism.** Any effort spent tuning propagation is misdirected relative to effort spent extracting more relations.

**BETA sensitivity**, complete@5 on chain tasks: 0.0 → 0.4690, 0.25 → 0.5487, 0.50 → 0.5841, 1.0 → 0.5398, 2.0 → 0.3805.

The preregistered `BETA = 0.50` happens to be the peak of the sweep. That is luck, not design, and the pre-registration commit is what makes the distinction checkable — otherwise the result would be indistinguishable from a tuned one. At `BETA = 2.0` the mechanism is substantially **worse** than the baseline: strong propagation drags neighbours of anything into the top 5.

## 7. Scope bounds established by this run

1. **Top-of-ranking effect only.** The advantage is present at k=3 and k=5 and gone at k=10, where no condition separates from C (0.6726 / 0.6637 / 0.6814). The mechanism reorders a shortlist; it does not retrieve documents the semantic baseline could not reach at all.
2. **Combining mechanisms buys nothing.** D4 exceeds D2 by +0.0088 while doubling the control cost (−4.0 vs −2.0 points). Relationship-only dominates combined on the cost/benefit trade. Round 2's fused "D" condition was the wrong design.
3. **Temporal weighting is not supported.** D1's interval includes zero. Provenance is marginal at best, lower bound 0.000.
4. **The advantage is bought, not free.** Every winning condition costs something on ordinary single-document retrieval.

## 8. Limitations

1. One corpus. Benchmark rule B6 replication is not satisfied.
2. PEPs are unusually well structured, which biases toward this claim (CORPUS-0001 limitation 3). The 36% edge coverage would likely be lower on messier engineering history, and the effect scales directly with it.
3. Software-process domain, not the EMC/PCB target domain.
4. Retrieval-stage only. No answer generation, no grounding measurement, no expert utility, no latency or maintenance cost.
5. Ground truth is relation-pair level. A retrieved pair is not a correct answer.
6. Queries are synthetic and mechanically generated. Real engineering questions are not title-plus-cue.
7. The 113 chain tasks come from 94 declared relations in one relation family, dominated by supersession.

## 9. Effect on claim states

- **CLM-0011:** `TESTABLE` → **`SUPPORTED`**, on CORPUS-0001, at the retrieval stage, at k ≤ 5, confidence low. The `observable_prediction` field is marked contradicted; the `mechanism` field must be rewritten around edge coverage rather than topical dissimilarity.
- **CLM-0004 (broad):** unchanged, **`WEAKENED / INCONCLUSIVE`**. This run tested the narrow split, not the broad claim. Temporal and provenance mechanisms — both named in CLM-0004's statement — did not separate from the baseline here, which is mild further evidence against the broad wording.

## 10. DEC-0001 gate status for CLM-0011

| Criterion | Status |
|---|---|
| 1. Independent corpus | **Met** — CORPUS-0001 |
| 2. Predeclared falsifier, not met | **Met** — commit `132c174` |
| 3. Claim wording matches tested scope | **Not met** — the current wording omits the k ≤ 5 bound, the edge-coverage dependency, and the control cost |
| 4. Separate promotion decision record | **Not met** — none exists |

**CLM-0011 does not clear the gate.** Criterion 3 requires rewriting the claim to the scope actually tested, and criterion 4 requires a human decision. Rule B6 additionally requires a second corpus in a different domain.

## 11. Required next attack

1. Rewrite CLM-0011 to the tested scope and re-record the mechanism as edge-coverage-bound.
2. Second corpus, different domain, messier structure — the direct test of whether 36% edge coverage was corpus luck.
3. Measure relation-extraction coverage as the primary quantity, since it fully determines the effect size.
4. Add answer-level grounding, so a retrieved pair is scored as a usable answer rather than a hit.
5. Re-run with `BETA` chosen by cross-validation on a held-out task split, not by a fixed guess.

## 12. Verdict

**Round 3 does not falsify CLM-0011, and it is the first APF result that could have.** The relationship mechanism is confirmed as the carrier; temporal weighting is not supported and provenance is marginal.

The result is narrower than it first appears. The effect exists only in the top 5, only where a relation was successfully extracted, and it costs measurable accuracy on ordinary retrieval. The claim's own stated mechanism — that structure rescues topically distant documents — was contradicted by its own predicted test.
