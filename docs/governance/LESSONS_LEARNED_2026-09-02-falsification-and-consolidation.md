# APF Session Lessons Learned — 2026-09-02

**Scope:** BENCH-0004 Round 3 execution, structure refactor (DEC-0001), root-cause investigation setup
**Status:** Session learning / candidate guidance

## 1. Session Summary

Three blocks of work. BENCH-0004 Round 3 decomposed the retrieval claim into its
three mechanisms and **falsified the broad form of CLM-0004 at its tested scope**
— the first P0 claim in the project to complete a falsification attempt, and it
did not survive. A full refactor then consolidated seven overlapping research
documents into four canonical ones, retired the duplicate identifier scheme, and
split the benchmark harness into a reusable framework. Finally, the recurring
work-failure investigation was prepared as the next session's agenda.

The session's most useful output is arguably not the falsification but the
evidence that the project's failures are systematic rather than incidental.

## 2. Key Lessons

### L1 — A predeclaration is only worth what its timestamp proves

Round 3's falsifiers, corpus, task set and weights were committed at `88aed05`,
**before** the harness existed at `1618c53`. That ordering is what makes the
negative result credible: no threshold could have been chosen to fit an observed
number, and the git history proves it rather than asserting it.

A predeclaration written after the first look at results is a rationalisation
wearing a predeclaration's clothes, and nothing in the document itself would
reveal the difference.

### L2 — Operator-constructed structure is a confound class, not a detail

Round 2 reported the relationship mechanism beating baseline by +0.208. Round 3
changed exactly one thing — edges derived mechanically instead of drawn by the
operator who also wrote the questions — and the effect **reversed** to −0.104.

Whenever the person who knows the evaluation also builds the structure being
evaluated, that structure is a suspect variable. This generalises well past
retrieval graphs: it covers hand-tuned weights, curated example sets, and
hand-picked test corpora.

### L3 — A null model separates "the structure is real" from "the structure helps"

The relationship arm **passed** its null-model test at the 99.5th percentile:
the derived graph is decisively better than a degree-preserving random rewiring.
It also **lost** to using no graph at all.

Both are true and neither alone is the finding. Without the null model the loss
would have read as "the graph is noise", which is false. The real conclusion —
real structure, wrong consumption mechanism — was only reachable because two
different controls disagreed.

### L4 — The simplest control was the strongest competitor

Across three rounds the largest positive retrieval effect came from plain
metadata weighting (+0.063), beating every temporal, relationship and provenance
mechanism tested. `BENCH-0004` had named this exact possibility as its own
falsifier — "improvement explained by better indexing alone" — two days before
it happened.

Naming the boring alternative in advance is what let it be recognised instead of
explained away.

### L5 — A test committed before a refactor is a baseline; one written after is a fit

`test_reproducibility.py` was committed at `c825c76`, passing, before any
refactoring began. It then held through a framework extraction, two document
consolidations and a corpus edit, proving every recorded number unchanged.

Had it been written afterwards it would have proved only that the code agrees
with itself. The sequence is the whole value, and it costs one extra commit.

### L6 — Executable checks caught in seconds what prose missed for 21 commits

`test_docs_integrity.py` found a real violation on its **first run**. The defect
classes it guards had survived 21 commits as written rules that nothing executed.

This is one observation, not a proven law — see §4 — but it is the sharpest
single contrast the session produced.

### L7 — A guard must assert the measurement, not the mention

While assembling failure evidence, a keyword search for "unsupported-claim rate"
matched all three execution records — because each record *states that the metric
is unmeasured*. A naive check would have reported full metric coverage.

Any check that greps for a term is testing vocabulary, not compliance. This
failure mode was reproduced during this session and is not hypothetical.

### L8 — Retaining a superseded path beats deleting it

Four consolidated documents were kept as five-line supersession stubs rather than
deleted, because execution records cite their paths and are append-only evidence.
Deleting them would have created dangling references *inside evidence documents* —
the same provenance defect as the `fileciteturn` markers removed earlier the same
day.

Consolidation must not be allowed to break the evidence that motivated it.

### L9 — Incidental implementation details can be load-bearing

Two properties of the harness turned out to be part of the specification rather
than free choices: the order in which mechanism signals are added (floating-point
addition is not associative, so reordering shifts recorded results in their last
bits), and the null-model driver seeding one generator advanced sequentially
rather than reseeding per draw.

Both were accidentally correct before the refactor and are now documented as
constraints. A refactor is where such properties either get written down or get
silently destroyed.

### L10 — This session's own defects were caught by attention, not by mechanism

Two real defects were introduced and fixed within the session: a latency
measurement that made one arm perform another's work before discarding it, and a
harness reading its corpus from the working tree instead of the frozen commit —
which would have silently broken replay the moment a corpus document changed, as
one did in the very next commit.

Both were caught by looking, not by a check. That is exactly the fragile mode the
next session is convened to examine, and it happened here too.

## 3. Claim and hypothesis status changes

### HP-3 is closed — the loop from 2026-08-30 completes

The 2026-08-30 lessons recorded four falsifiable product hypotheses. `HP-3 —
Graph-aware retrieval improves engineering usefulness` was formalised as
`CLM-0004`, benchmarked as `BENCH-0004`, and **falsified at its tested scope** on
2026-09-02.

That is the intended lifecycle working end to end for the first time:

```text
session lesson → falsifiable hypothesis → bounded claim → benchmark → result → claim state
```

The result was negative. A pipeline that can only produce confirmations would not
have been worth building.

The 2026-08-30 document is **not** edited. It is a record of what was believed at
that date, and the status change is recorded here and in `CLAIM_INVENTORY`.

`HP-1`, `HP-2` and `HP-4` remain untested. `HP-2` (structured history improves
retrieval) is close enough to `CLM-0004c` that it should be re-scoped before
being tested independently.

## 4. Rules inspection — 2026-09-02

Conducted as part of session closeout. **No rule text was changed**, by explicit
decision (see §5).

### Scope inspected

`CONSTITUTION.md`, `docs/governance/MASTER_SESSION_PROMPT.md`,
`docs/governance/HOTL_GOVERNANCE.md`, `docs/decisions/README.md`.

### Clean

None of the governance documents reference individual research document
filenames. The DEC-0001 consolidation therefore **invalidated no rule text**. The
governance layer was written abstractly enough to survive a restructuring of the
layer beneath it, which is worth noting as a design property that held.

### Compliance gaps — not rule defects

| Existing rule | Status |
|---|---|
| Session Loop contains a `CONTRADICTION SCAN` stage | Present, not executed. Three contradictions accumulated across 21 commits |
| `Session Closeout` checklist enumerates 13 required records | Present, not executed. `SESSION_STATE` was stale, predating the R1/R2 commits |
| Git Governance: "research and implementation should use separate semantic commits" | Followed this session |
| `CONSTITUTION` §3: consequential changes require a human decision record | Followed — DEC-0001, the project's first |

The pattern is that the rules were adequate and unexecuted. This is a finding
about execution, not about drafting, and it is the central evidence handed to the
next session.

### Deferred, with reason

`MASTER_SESSION_PROMPT`'s Session Loop has **no consolidation or retirement
stage**, which is hypothesis H-C in the root-cause handoff. Adding one now was
considered and rejected:

1. It would pre-commit solution S4 before the session convened to evaluate it.
2. It would add one more prose rule that nothing executes, before determining
   whether unexecuted prose rules are the root cause — a recurrence of the exact
   pattern under investigation.

`MASTER_SESSION_PROMPT` stays at v0.3. No version bump, because nothing changed.

## 5. Principles emerging from this session

1. **Predeclare, and let the timestamp carry the proof.** Order in git is
   evidence; a claim of having predeclared is not.
2. **Control the thing you built.** If you constructed the structure under test,
   a null model is not optional.
3. **Name the boring alternative first.** It won here.
4. **Baseline before you change.** A test written after the change tests nothing
   about the change.
5. **Prefer the check that fails to the rule that asks.** Provisional — this is
   the proposition the next session exists to test, not an adopted principle.
6. **Consolidation must not break the evidence that motivated it.**

Principle 5 is deliberately marked provisional. Adopting it now, on the strength
of one session's observation, would be the same error as promoting a claim from a
single positive benchmark — which this session spent its first half demonstrating
is unsafe.

## 6. Next Session Preparation

The agenda is `docs/handoff/NEXT_SESSION_PROMPT_FAILURE_ROOT_CAUSE.md`, which
carries a copy-pasteable opening prompt, the evidence inventory, four competing
hypotheses with discriminating tests, five candidate solutions and a predeclared
ranking criterion.

`BENCH-0006` is deferred behind that work. Mixing a benchmark execution with a
governance investigation would confound both.

## 7. Explicit Non-Goals for Next Session

- Do not name the root cause from this document. §4 supplies evidence, not a
  verdict, and §2 L6 is one observation.
- Do not adopt principle 5 without testing it.
- Do not modify `docs/research/executions/**`.
- Do not produce a new governance document as the deliverable. A document about
  the failure to integrate documents would be the most on-the-nose recurrence
  available.
