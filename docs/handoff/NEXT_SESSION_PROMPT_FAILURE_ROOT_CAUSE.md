# APF — Next Session Prompt: Recurring Work-Failure Root Cause

**Status:** Session agenda / evidence assembled, conclusion deliberately open
**Prepared:** 2026-09-02
**Supersedes as the active handoff:** `NEXT_SESSION_PROMPT_ENGINEERING_WORK_UX.md`

## Session purpose

Find the root cause of the work failures that keep recurring in this project,
and produce **at least three solutions that prevent recurrence** rather than
repairing the current instance.

This document assembles the evidence and frames competing hypotheses. It does
**not** name the root cause. A root cause is a claim, and this project's own
method (`CLAIM_INVENTORY` §5, `FALSIFICATION_BENCHMARK` §3C) requires a claim to
carry a falsifier and to be distinguished from a nearby competing explanation
before it is adopted. Pre-writing the answer here would guarantee the next
session confirms it.

## 1. Evidence — the failure inventory

Every row is drawn from repository state or git history, not from recollection.

| # | Failure | Evidence |
|---|---|---|
| F1 | 9 research-protocol documents authored in **15 minutes** (08-31 11:55→12:10); **4 of 9 (44%)** became superseded stubs two days later | commits `8383bd4`…`aeeacd4` |
| F2 | **Three conflicting benchmark execution orders**, authored **14 minutes apart in one session** | `6a44c5a` 11:56, `cdd6150` 12:00, `aeeacd4` 12:10 |
| F3 | Three incompatible claim/result state vocabularies coexisting | `CLAIM_INVENTORY` §2 · `P0_MATRIX` · `FALSIFICATION_BENCHMARK` §7 |
| F4 | Two identifier schemes for the same benchmarks; `RESEARCH_TO_CLAIM_MAP` §4 used **both in one table row** | fixed `184139b`, `2297385` |
| F5 | Unresolvable AI-tool citation markers committed into the traceability document | fixed `184139b` |
| F6 | Of six declared BENCH-0004 primary measures, **three were never measured across three rounds** (unsupported-claim rate, answer utility, answer-level grounding) | R1/R2/R3 records |
| F7 | Retrieval latency declared a primary measure; unmeasured in R1 and R2 | added only in R3 |
| F8 | `RESEARCH_CORPUS_MAP` declared "only after corpus reconciliation, execute the P0 benchmarks". R1–R3 all ran at `PARTIAL` | recorded `38d59e7` |
| F9 | `SESSION_STATE` is the most-churned file (5 edits) and was **stale at the start of this session**, predating the R1/R2 execution commits | `2a9d10d` vs `d412e45` |
| F10 | R2's operator-drawn relationship graph produced a result that R3 reversed once the graph was derived mechanically | `CONTRA-0001` |
| F11 | `MASTER_SESSION_PROMPT` requires a contradiction audit **every session**. Three contradictions (F2, F3, F4) accumulated across 21 commits undetected | first audited 2026-09-02 |

### The structural fact underneath the table

```text
Commits before this session:  23
Files added:                  21
Files removed or merged:       0
```

**No commit in the project's history had ever integrated, merged, or retired a
document until this session.** Growth was strictly monotonic. Consolidation was
not slow or under-prioritised — it had never happened once.

A second timing fact constrains the explanations: the protocol phase ran
11:55→12:10 and the first benchmark executed at 12:22. R1 and R2 were committed
**three minutes apart** (12:22, 12:25).

## 2. Competing root-cause hypotheses

Each hypothesis must explain F1–F11 and be distinguishable from the others.
Discriminating evidence is listed so the session can attack rather than confirm.

### H-A — Prose rules with no executable check

Every rule that failed existed only as Markdown prose. Nothing executed it, so
violation was silent.

*Supporting:* F6, F7, F8, F11 are all declared-but-unenforced rules.
*Discriminating test:* the one executable check added this session
(`test_docs_integrity.py`) caught a real violation on its **first run**, seconds
after being written, in a defect class that had survived 21 commits as prose.
*Would be weakened if:* prose rules that were checked by hand also failed, or
executable checks also drift.

### H-B — Authoring velocity exceeds reading velocity

Nine documents in fifteen minutes is roughly 100 seconds per document. There is
no interval in which the author could have re-read what was just written.

*Supporting:* F1, F2 — the three conflicting orders were written 4 and 10
minutes apart. Re-reading `FALSIFICATION_BENCHMARK` before writing `P0_MATRIX`
would have made the duplicate matrix obvious.
*Discriminating test:* compare defect density in the 15-minute burst against the
slower 09-02 work. If slowing down alone fixed it, the later work should be
clean — it is not entirely (the latency measurement defect, the working-tree
corpus read).
*Would be weakened if:* defects are evenly distributed across fast and slow work.

### H-C — The workflow has a produce step and no integrate step

Not speed, but missing structure: every commit adds an artifact, and no stage
ever asks whether the new artifact overlaps an existing one.

*Supporting:* the 21-added / 0-removed fact. `MASTER_SESSION_PROMPT`'s Session
Loop lists `RESEARCH → ASSETIZATION → PROPOSAL → … → RECORD → HANDOFF` — there
is no consolidation or retirement step anywhere in it.
*Discriminating test:* H-B predicts slowing down fixes it; H-C predicts that
even slow work accumulates duplicates without an explicit integrate step.
*Would be weakened if:* duplicates were caught and merged in ordinary work
despite no formal step.

### H-D — Asymmetric rigor: the method is applied to the research object, never to itself

The project demands evidence-before-architecture, cold review, predeclared
falsifiers, contradiction registers and provenance — for `CLM-*` claims. None of
that machinery was ever pointed at the documents that declare the machinery.
Claims got a cold review; the document defining cold review got none.

*Supporting:* F11 most directly, and it subsumes F2–F5, F8.
*Discriminating test:* H-A says the failure is the *medium* (prose vs code);
H-D says it is the *target* (object level vs meta level). These come apart on a
prose rule that **is** habitually applied to the meta level, or an executable
check that is only ever pointed at the object level.
*Would be weakened if:* meta-level rules were in fact applied and still failed.

H-A and H-D are not mutually exclusive and may be one cause described at two
altitudes. Deciding whether to merge them is part of the session's work, not a
foregone conclusion.

## 3. Candidate solutions

The brief asks for solutions that do not recur. Propose at least three; five
candidates are seeded below. They are **candidates**, not recommendations — rank
them against the criterion in §4 after the root cause is settled.

### S1 — Extend executable governance checks to the project's own declared rules

`tools/tests/test_docs_integrity.py` already guards dangling references,
citation artifacts, duplicate order declarations and retired identifiers. Extend
to the rules that failed: does each executed benchmark measure what its case
declares (F6, F7)? Does `SESSION_STATE` reference the current HEAD (F9)? Is a
declared sequencing rule satisfied or explicitly waived (F8)?

**Design caution learned while preparing this document.** A keyword grep for
"unsupported-claim rate" across the three execution records returns a hit in all
three — because each record *says the metric is unmeasured*. A naive check would
have reported full metric coverage. A guard must assert the measurement, not the
mention. This failure mode was reproduced during preparation and is not
hypothetical.

### S2 — Machine-readable subject-ownership manifest

One registry declaring which document owns which subject (execution order,
claim state vocabulary, benchmark identity, exit criterion), plus a test
asserting that no other document declares an owned subject. Converts "one
subject per document" from a convention that was violated three times into a
constraint that fails a test.

### S3 — Session-start gate

The repository has no `.claude/` directory and no SessionStart hook. Run the
guard suite at session start so a session cannot begin work on a repository that
is already in violation, and so `SESSION_STATE` staleness (F9) surfaces before
it misleads the session — as it did at the start of this one. A
`session-start-hook` skill exists for this.

### S4 — An explicit integrate step in the session loop

If H-C survives, the fix is structural: add a consolidation/retirement stage to
`MASTER_SESSION_PROMPT`'s Session Loop, with a bounded obligation — for example,
a new research document may not be added while an existing document declares the
same subject. Targets the 21-added/0-removed pattern directly.

### S5 — Periodic meta-level cold review

Apply `CLAIM_COLD_REVIEW`'s method to the governance documents themselves.

**Flagged as the weak candidate deliberately.** S5 is prose that asks people to
apply prose. If H-A survives, S5 is predicted to recur, and it is included so
the ranking criterion has something to reject. If S5 ranks well, the criterion
in §4 is wrong.

## 4. Predeclared ranking criterion

Declare this before evaluating, per cross-case execution rule 1.

A solution qualifies as **non-recurring** only if it satisfies all of:

1. **Fails loudly.** Violation produces a failure someone must act on, not a
   document someone must notice.
2. **Fails at the right time.** The failure surfaces before the defect is
   committed or before a session builds on it, not two days later.
3. **Cannot be satisfied by restating it.** Adding a sentence to a document does
   not make it pass.
4. **Survives its own absence of attention.** It works when nobody remembers it
   exists — this is the property every failed rule in §1 lacked.

A solution meeting fewer than all four is a mitigation. Record it as such rather
than promoting it.

## 5. A caution about this session's own evidence

This session repaired F2–F5 and F9. That repair is **not** evidence that the
root cause is fixed — it is one more instance of the pattern under
investigation: a person noticed a problem and fixed that instance by hand.

The genuinely new thing is that two executable guards now exist where none did
before. Whether that generalises is the question, not the answer.

Note also that the recurring-failure inventory includes defects introduced
during this session (a latency measurement defect, a harness reading the working
tree instead of the frozen commit). Both were caught, but by attention, not by a
mechanism — which is exactly the fragile mode under examination.

## 6. Non-goals

- Do not execute BENCH-0006 in this session. It is next in the register, but
  mixing a benchmark execution with a governance investigation confounds both.
- Do not modify anything under `docs/research/executions/`. Append-only evidence.
- Do not change claim states. Nothing here bears on CLM-* results.
- Do not add a new governance document as the deliverable unless it passes §4.
  A document *about* the failure to integrate documents would be the most
  on-the-nose recurrence available.

## 7. Deliverables

1. Failure inventory validated or corrected against the repository.
2. Root cause named, with the hypotheses it defeats and the evidence that
   discriminated them.
3. At least three solutions scored against §4, with mitigations labelled as such.
4. Implementation of whichever solutions pass, given that a passing solution is
   by definition executable rather than declarative.
5. A decision record if any solution changes a contract or the session protocol
   (`CONSTITUTION` §3). `DEC-0001` is the template.
