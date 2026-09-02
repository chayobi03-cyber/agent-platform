# APF Session Lessons Learned — 2026-09-02

**Scope:** BENCH-0004-E2 handoff integration, full project audit, BENCH-0004-E2b, BENCH-0006
**Status:** Session learning / candidate guidance

## 1. Session Summary

The session began with a handoff bundle declaring BENCH-0004-E2 "ready", with one remaining
gate: a single real generator run over 96 frozen contexts. The bundle contained six protocol
documents and none of the fixture. The four SHA-256 values it published could not be recomputed,
and the protocol's "one frozen context per request" had no request payload.

What followed was not the planned generation run. It was: establishing what the handoff actually
proved, auditing the whole project against its own rules, closing the linkage gap the audit
found, building a replacement benchmark whose fixture lives inside the evidence chain, and
executing the next benchmark in the queue.

Two results were produced. Provenance replicates as the largest retrieval mechanism across two
independent factorials; temporal filtering does not replicate. And provenance cannot be recovered
from document content — zero of fifty evidence items survive ablation fully auditable.

No claim was promoted, no asset accepted, no architecture derived.

## 2. Key Lessons

### L1 — A hash manifest is not an artifact

BENCH-0004-E2 published four SHA-256 values and declared its fixture frozen. The bytes were never
committed. The result is a benchmark that cannot be verified, cannot be executed, and cannot be
recovered.

Cross-document hash agreement was the trap. All four values appear identically in every handoff
document that cites them, which reads like verification and is not: it establishes only that the
documents agree with each other. An artifact-free manifest proves internal consistency of the
paperwork.

**Rule candidate:** a frozen benchmark artifact is committed with its lock, or it is not frozen.

### L2 — "Roll back and recover" is a claim to verify, not a plan to assume

When recovery by git rollback was proposed, the check cost one command set and settled it
conclusively: no commit on any branch held the fixture, there were no stashes, and both dangling
objects were this session's own compiled bytecode. The repository's first commit predated the
fixture lock; the artifact was built outside the repository entirely.

Asserting impossibility without checking would have been careless. Attempting recovery without
checking would have wasted the session. The check is cheap; run it.

### L3 — Reconstruction is not recovery, and saying so is the whole value

BENCH-0004-E2b answers the same question over a corpus that exists. It is not the E2 fixture and
its hashes must never be compared to the E2 lock. That distinction is stated in the lock file, the
execution record, the builder README, and the commit message — because the one thing that would
destroy its value is a later reader treating it as the recovered original.

A replacement experiment is legitimate. A replacement experiment wearing the original's identity
is contamination.

### L4 — Evidence with no claim to attach to silently drifts

The E2 factorial had already measured three retrieval mechanisms separately and produced
per-mechanism effects with p-values. `CLM-0004a/b/c` did not exist in the claim inventory. The
strongest quantitative result the project held had nothing to update.

The split had been proposed in the v0.1 benchmark document and required by the R2 execution
record. It was executed. It was never entered. Each further execution would have widened the gap
between what had been measured and what the inventory said was known.

**Rule candidate:** an execution that measures a mechanism the inventory does not name is
incomplete until the inventory names it.

### L5 — Build defects hide inside plausible-looking results

Three were caught this session. Each would have produced a publishable number.

1. **P suppressed T.** The provenance header overwrote the version annotation, so `T=0` and `T=1`
   rendered identical bytes when selection matched. Two factors are not separable if one can mask
   the other.
2. **The context omitted its own question.** Different questions retrieving the same documents
   produced byte-identical contexts — and the fixture would have been unusable as a generator
   input, since the contract forbids supplying the question separately.
3. **The BENCH-0006 currency proxy matched any `**Status:**` string.** It returned a 0.000
   stale-escape rate.

The third is the dangerous one: it produced a *better* number than the truth. A document having a
status field says nothing about whether the copy in hand was superseded. Corrected to require an
explicit supersession marker, the rate was 0.667.

### L6 — Test the proxy against what it claims to measure

L5's third defect was one substitution: "document has a status field" standing in for "reader can
tell this version is stale". The proxy was plausible, cheap, and wrong, and nothing about the
output looked wrong.

Before recording a measurement, state what the proxy claims to detect and construct the case where
it would be fooled. If that case is common in the corpus, the proxy is not usable.

### L7 — Self-audit bias is mitigable into auditability, not out of existence

The same session designed E2b, built it, and analysed it. Mitigations applied: the case set and
its scoring requirements were frozen before any context was constructed, the corpus was pinned to
a commit, the build was made deterministic so a reviewer can recompute rather than trust, and the
finding most damaging to the session's own prior work — temporal failing to replicate — was
reported first and unqualified.

Those make the bias inspectable. They do not remove it. An independent party should rebuild E2b
before its result carries weight.

### L8 — Depth on one claim is not progress on the thesis

BENCH-0004 accumulated four executions while five other benchmarks had zero. The queue had not
advanced past its first entry, and five of six P0 claims — the ones whose failure would invalidate
broad portions of the platform thesis — had no evidence at all.

Four executions of one benchmark on one corpus reads as rigour and is also a single point of
failure. BENCH-0006 was run partly to break that pattern.

### L9 — Corpus independence is now the load-bearing limitation

Every result the project holds runs on APF's own documentation. BENCH-0004 R1 flagged this; R2
flagged it; E2b inherits it; BENCH-0006 has it too. The limitation has been recorded honestly
each time and never removed.

At one benchmark this is a caveat. At five it is the project's largest structural risk: a
correlated weakness across the entire evidence base, where each new result adds confidence
without adding independence.

### L10 — A commit is not a decision, and the gap must be recorded

The v0.1/v0.2 parallel-track structure was decided conversationally and committed. The
Constitution states explicitly that a commit is not a human decision. Two decision records were
raised as `PROPOSED` and neither was self-approved.

Governance that only applies to other people's changes is not governance.

### L11 — Refusing to fabricate has a cost; make the cost countable

Ten external research tracks could not be recovered — their findings exist only in prior
conversations. They were registered as `PENDING_RECOVERY` with no content.

Writing plausible findings would have made the ledger look complete and destroyed its purpose.
Leaving them out entirely would have made the gap invisible. Registering them empty makes the
gap countable, which is the only form in which it can be closed later.

## 3. Method Principles Emerging From the Session

```text
Freeze the artifact, not just its hash.
Pin the corpus, or the fixture cannot be rebuilt.
Verify in tiers: byte hashes are authoritative, derived checks are diagnostic.
Declare the case set and its scoring before constructing anything.
Report the result that most damages your prior position first.
Register what you could not recover; do not fill it in.
```

## 4. Next Session Preparation

1. **Decide `DEC-0001` and `DEC-0002`.** Both are `PROPOSED` and neither may be self-approved.
   They block nothing mechanically and everything governance-wise.
2. **Acquire an independent engineering corpus.** This is the highest-value next action. Every
   current result is bounded by L9, and no amount of further APF-corpus work relaxes that bound.
3. **Run Stage 2** for E2b when a model can be pinned and a credential exists. Fixture, protocol,
   runner and analysis are ready and dry-run clean; nothing else blocks it.
4. **Continue the queue** — `BENCH-0002`, `BENCH-0007`, `BENCH-0009`, `BENCH-0001` remain at zero
   executions, covering four untested P0 claims.
5. **Complete claim records as each benchmark is prepared**, per `DEC-0002` option C, rather than
   in bulk.

## 5. Explicit Non-Goals for Next Session

- Do not promote `CLM-0004`, `CLM-0004a/b/c`, or `CLM-0006`. `SUPPORTED (narrow)` is not
  promotion, and the two non-scope limitations on CLM-0006 must travel with every citation.
- Do not accept any asset. All six records are `ASSET_CANDIDATE`.
- Do not treat `BENCH-0004-E2b` as a recovery of `BENCH-0004-E2`, or compare their hashes.
- Do not run `T07` or `T11`. There are no accepted assets, and research findings are not the
  operational assets those benchmarks require.
- Do not derive architecture from any result in this repository.
