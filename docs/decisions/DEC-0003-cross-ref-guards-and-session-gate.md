# DEC-0003 — Cross-ref guards and an executable session gate

```yaml
id: DEC-0003
title: Guard cross-ref divergence and run the guard suite at session start and in CI
status: DECIDED
date: 2026-09-02
```

## Context

`DEC-0001` consolidated the research documents and added the first two
executable guards. The recurring-failure investigation asked whether that
generalises. It does not, on its own.

The identifier is `DEC-0003` rather than `DEC-0002` because two different
decisions already carry `DEC-0002` on unmerged refs, and three carry
`DEC-0001`. The guard added by this decision is what reported that; the number
was chosen by running it.

## Problem

Every check this repository had, prose or executable, reads one working tree at
one moment. Every failure it keeps repeating is a disagreement *between* trees
or *between* moments.

`test_docs_integrity.py` was green on `main` on 2026-09-02 while the repository
simultaneously held:

- three different decisions numbered `DEC-0001`, two of them marked `DECIDED`
- two different experiments named `BENCH-0004 Round 3`, run about an hour
  apart, reaching opposite conclusions
- `BENCH-0006` recorded `UNTESTED` and listed as the next action, already
  executed on another ref

None of those is a defect in any single tree, so nothing reading one tree can
find it.

## Evidence

Verified against git, not recollection.

| | |
|---|---|
| commits reachable from all refs | 75 |
| commits on `main` | 35 |
| commits that never reached `main` | 40 |
| distinct paths ever authored | 103 |
| paths on `main` | 37 |
| pull requests opened | 5 |
| pull requests merged | 1 |

`DEC-0001`'s own framing — 21 files added, 0 removed, "growth was strictly
monotonic" — measured `main`'s first-parent line only. Across all refs the
figure is worse, and the additions are not merely redundant: they collide.

Scope is the failing variable, not medium and not target level. Running `main`'s
own `test_docs_integrity.py` against the other branch trees fails four checks on
`claude/handover-eu02yk`, four on `claude/session-governance-decisions-6fi9vf`
and two on `research/architecture-asset-synthesis-v0.1` — including a competing
execution order declared in `SESSION_STATE.md`, which is the exact defect
`DEC-0001` retired. It is alive on three refs and re-enters `main` with whichever
open pull request merges first.

There was also no trigger. No `.github/`, no `.claude/`, no CI on any ref;
`pytest` is not installed. The two guards `DEC-0001` added run only when a
person types the command, which is the property every failed prose rule had.

## Contradictions

- `BENCHMARK_REGISTER` §3 records `BENCH-0001` and `BENCH-0006` as `UNTESTED`.
  Both have preregistered executions on unmerged refs.
- `SESSION_STATE` "Open Questions / Risks" requires an independent corpus before
  generalising from BENCH-0004. `claude/session-governance-decisions-6fi9vf`
  used a 737-document third-party corpus an hour before that risk was written.
- This decision resolves neither. It makes both fail a test until the owner does.

## Alternatives

**A — extend `test_docs_integrity.py` in place.** Rejected: its checks read the
filesystem, and the defects at issue are not in any one filesystem. Mixing ref
queries into it would also hide which failures need a fetch to be meaningful.

**B — fail on any divergence.** Rejected: five real divergences are outstanding,
so the guard would be red on its first run and stay red. A permanently red check
is one people learn to ignore, which is the failure mode under investigation.

**C — a prose rule requiring branch reconciliation each session.** Rejected: the
Session Loop already contains a `CONTRADICTION SCAN` stage that was never run
across 21 commits. Adding a stage predicts recurrence.

**D — fail on *unrecorded* divergence, and give the suite a trigger.** Adopted.

## Risks

- The ledger could become a place to write "known issue" and move on. Three
  properties prevent it: a pinned SHA that moved fails, a row describing nothing
  fails, and a row that gains a new claimant fails. All three are negative-tested.
- The session-start hook only covers Claude Code sessions. CI covers everything
  pushed; both are needed, neither alone.
- The cross-ref checks are only as good as the refs the clone can see. A
  single-ref clone fails the suite rather than passing it silently.

## Recommendation

Adopt alternative D.

## Human decision

Approved by the repository owner (chayobi03@gmail.com) in the working session of
2026-09-02, whose brief required that solutions passing the predeclared ranking
criterion be implemented rather than described, and that a decision record be
left if the session protocol changed.

Per `CONSTITUTION.md` §3 and `HOTL_GOVERNANCE`, the recommendation was produced
by an agent; the decision was not.

**Explicitly not decided here.** The following are the owner's and are recorded
in the ledger as `AWAITING_HUMAN_DECISION`, not resolved:

- which decision keeps the identifier `DEC-0001`, and likewise `DEC-0002`
- whether the `BENCH-0001` and `BENCH-0006` executions on unmerged refs are
  accepted, and therefore whether the register is wrong
- which `BENCH-0004 Round 3` keeps the name, given two experiments, two corpora
  and opposite results
- what becomes of the five divergent refs and the four open pull requests

No claim state is changed by this decision.

## Impact

Changes to the session protocol:

- A session begins with the guard suite already run and its result in context.
  `SESSION_STATE` staleness, unrecorded divergence and unaccounted branches
  surface before a session plans against them.
- A push or pull request that introduces unrecorded divergence fails CI.
- Divergence is no longer resolved by noticing it. It is recorded with a ref, a
  SHA and a disposition, all verified against git, or the suite fails.

Subject ownership becomes a constraint rather than a convention:

- `apfguard/subject_manifest.json` declares which document owns the benchmark
  execution order, the claim state vocabulary, the benchmark identity table and
  the corpus exit criterion. A document declaring a subject it does not own
  fails, on disk before it is committed and on every other ref afterwards.
- `DEC-0001` restored one-subject-one-document by editing the documents, and it
  held on `main` and nowhere else. PR #3 has three documents declaring the
  execution order, `SESSION_STATE.md` among them; PR #4 has four declaring the
  claim state vocabulary, two of which are a per-claim record scheme `DEC-0001`
  did not consider. Both are recorded, not resolved.

Changes to the benchmark contract:

- An executed benchmark must declare, per declared primary measure, whether it
  measured it. `measured:` must name a key in committed raw results.
- Applying this raised BENCH-0004's unmeasured count from the three the register
  named to five of six. Relevant-case precision and false-positive rate were
  unmeasured across three rounds and unmentioned in every record.

## Implementation scope

```text
tools/apfguard/__init__.py            scope rationale
tools/apfguard/refs.py                reading every ref, not the working tree
tools/apfguard/divergence.py          the cross-ref disagreements
tools/apfguard/ledger.py              why the ledger cannot rot
tools/apfguard/measures.py            declared vs measured
tools/apfguard/subjects.py            who owns which subject
tools/apfguard/subject_manifest.json  the ownership declaration itself
tools/apfguard/divergence_ledger.json 12 recorded rows, 5 refs pinned
tools/tests/test_cross_ref_integrity.py
tools/tests/test_declared_measures.py
tools/tests/test_session_state_freshness.py
tools/tests/test_subject_ownership.py
.claude/hooks/session-start.sh        reports into session context
.claude/settings.json                 registers the hook
.github/workflows/apf-guards.yml      refuses a push or PR
docs/research/BENCHMARK_REGISTER.md   BENCH-0004 measurement status block
tools/tests/test_docs_integrity.py    execution-order check retired into the
                                      manifest, after testing equivalence
```

Standard library only, matching `apfbench`: a guard that needs an install step
will not run in the hook that is supposed to make it unskippable.

## Verification plan

Each guard was tested for what it rejects, not only for passing. All pass:

| Case | Expected | Result |
|---|---|---|
| unmodified repository | green | green |
| a fourth `DEC-0001` committed | fail | fails, naming the new claimant |
| an unrelated commit on the working branch | green | green |
| a ledgered branch moves | fail | fails, naming the SHA change |
| a ledgered divergence disappears | fail | fails, demands the row be removed |
| a new execution appears on another ref | fail | fails |
| a clone that can see one ref | fail | fails rather than passing blind |
| freshness guard replayed at `0d27769` | fail | names `d412e45` and `0d27769` |
| a second document declares the execution order | fail | fails, uncommitted |
| a second document declares the state vocabulary | fail | fails, uncommitted |
| an owner stops declaring its own subject | fail | fails |
| a manifest subject names an unimplemented detector | fail | fails |
| a violation appears on a new ref | fail | fails |

The last row is the load-bearing one: run against the repository state the
2026-09-02 session actually opened, the guard reports the two execution commits
that `SESSION_STATE` predated. Had it existed on 08-31, that session would have
opened to a failure instead of a stale plan.

Two defects in the guards were found this way rather than by review. The
subject-ownership check first read the committed ref, so an uncommitted edit
passed it — one commit later than criterion 2 of the brief allows. An
equivalence test against the check it was replacing caught it: the older check
read the filesystem and failed where the newer one passed. It now reads the
filesystem, and the equivalence holds in both directions.

An earlier version of the cross-ref guard passed case 2 — it compared ledger
keys and not who was in them, so a row already marked known absorbed new
divergence silently. The negative test caught it. Recorded here because the
defect is the same class the guard exists to prevent.

## Related assets

- `DEC-0001` — the consolidation this extends, and the template for this record
- `tools/tests/test_docs_integrity.py` — same subject, working-tree scope
- `docs/handoff/NEXT_SESSION_PROMPT_FAILURE_ROOT_CAUSE.md` — the brief; itself
  on an unmerged ref, and recorded in the ledger for that reason

## Related commits

- `6e89d1f` — guards, ledger, hook and CI
