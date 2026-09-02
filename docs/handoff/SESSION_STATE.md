# APF Session State

**Last updated:** 2026-09-02
**Branch:** `claude/session-governance-decisions-6fi9vf` · **PR:** #4 open

## Start Here

**The tool exists. The trial is running. Do not start anything else until it concludes.**

`tools/apf/` — capture and find, single file, stdlib only, plain-file storage. Built 2026-09-02. It is a trial instrument, not APF implementation; it commits to no architecture and carries no claim.

### The self-falsifier

This project attached a predeclared falsifier to eleven claims and none to itself. It has one now:

> Use `apf` on real engineering work for two weeks. **If you did not reach for it unprompted, stop the project.**
> Evidence is `apf stats` — active-day rate and searches run. "It was fine" is not a pass.

Threshold is use frequency, not satisfaction. Nothing about this is a benchmark and it must not be turned into one.

### One thing before the trial means anything

Nobody has established that context reconstruction is actually the largest cost in the owner's week. L1 and CLM-0002 are research inferences, not observations. **One hour** of honest accounting of where last month's engineering time went settles it. If context reconstruction is not in the top three, the target changes and the tool is aimed wrong.

One hour. It must not become a project.

### Still not a session task

Engineers for BENCH-0002 (a week, three people) and E2b Stage 2 credentials. Owner only.

**Do not, without an explicit reason:** run another benchmark round, add another process document, acquire another corpus, extend the claim inventory, or add a feature to `apf` that two weeks of use has not asked for. Those are the moves this project reaches for when the useful work needs someone else's time.

## Where This Stands

| | |
|---|---|
| Constitution | v0.1, with a standing contradiction against section 2 |
| Architecture contract | none — nothing has cleared DEC-0001 |
| Product code | `tools/apf/` — trial instrument, on trial |
| Claims | 11; 1 contradicted, 1 supported-and-narrow, 9 untested |
| Benchmarks executed | BENCH-0004 (3 rounds), BENCH-0001 |
| Corpus reconciliation | PARTIAL |

## Standing Contradiction — CONSTITUTION.md section 2

BENCH-0001 fired falsifier F4 against CLM-0001, the claim the work-centric boundary rests on. Work-centric core coverage on agentic workloads is 0.664 against the agent-centric core's 0.900; it escapes on in-flight state, inbound signals, and prompt content. It still wins overall (+0.142) and on the other five workload classes.

What is contradicted is the generality — the word "both" — not the direction. **Not amended:** Constitution section 9 requires explicit review for invariant changes, and DEC-0001 puts that with a human. Until decided, section 2 carries a known exception for agentic workloads.

Detail: `docs/research/executions/BENCH-0001/EXECUTION.md`.

## Closed

- **Retrieval track (CLM-0004 / CLM-0011).** Three rounds. Bounded to a top-of-ranking effect proportional to relation-extraction coverage, on a cheap-to-reverse indexing decision. A fourth round buys less than anything else available. CLM-0011 is `SUPPORTED` on one corpus and does not clear DEC-0001.
- **Governance foundation.** DEC-0001 and DEC-0002 are recorded and in force. The skeleton is done; further process work is subtraction, not addition.

## State Records

- Claim states and record status: `docs/research/claims/README.md`
- Decisions: `docs/decisions/` (DEC-0001 evidence gate, DEC-0002 claim record timing)
- Corpora: `docs/research/corpora/` (CORPUS-0001 PEPs, CORPUS-0002 workflow specs)
- Executions: `docs/research/executions/`
- Method and structural lessons: `docs/governance/LESSONS_LEARNED_2026-09-02-benchmark-program.md`

## Governance In Force

DEC-0001 blocks nothing mechanically and everything consequential in governance terms: no architecture contract, no implementation justified by a benchmark result, until four exit criteria hold for that claim. The absence of a mechanical block is not permission. Benchmark, corpus, and claim work are not blocked; **a small tool the owner uses is not an architecture contract and is not blocked either.**

DEC-0002: claim records are completed when their benchmark is prepared, not batched.

Open decision candidate, not decided: tiering DEC-0001 so cheap-to-reverse decisions do not need all four criteria. As written, the gate is hardest to pass for exactly the claims that matter most.

## Unresolved References

Recorded as gaps rather than filled by inference.

- **CLM-0001's binding table was authored by someone not neutral between the two schemas.** The falsifier firing against the author's own platform is weak evidence against bias in one direction, not evidence of neutrality. The fix is an independent second annotator re-binding the 26 concepts blind.
- **DEC-0002's rejected alternatives are a reconstruction**, marked as such in the record.
- **"L9" is ambiguous.** The lessons-learned L9 is about authority levels; the corpus-independence problem is BENCH-0004 R2 limitation 1. Records cite the limitation directly.
- **BENCH-0006 has no execution record.** CLM-0006 stays untested until it is established whether the run happened.

## Non-Goals

- Do not freeze architecture from the current claim list.
- Do not select a runtime, graph DB, or vector store as an APF contract because research mentions it.
- Do not treat repeated source agreement as proof.
- Do not run further benchmarks as a substitute for building something used on real work.
- Do not add a process document that neither fits one page nor retires an existing one.
