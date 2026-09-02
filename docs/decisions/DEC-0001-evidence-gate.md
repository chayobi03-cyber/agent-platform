# DEC-0001 — Evidence Gate on Architecture Promotion and Implementation

## Minimum Decision Record

```yaml
id: DEC-0001
title: Evidence gate on architecture contract promotion and implementation start
status: DECIDED
date: 2026-09-02
context: >
  APF holds a claim inventory (CLM-0001..CLM-0010), a cold review, a P0
  falsification benchmark matrix, operationalized P0 cases, and two executed
  BENCH-0004 rounds. No architecture contract exists. Corpus reconciliation is
  PARTIAL. Round 2 produced the project's first positive retrieval signal,
  creating pressure to convert benchmark output into architecture.
problem: >
  Nothing in the repository states at what point claim and benchmark work is
  allowed to become an architecture contract or an implementation. The
  Constitution states evidence-before-architecture as a principle but names no
  gate, and there is no mechanical enforcement of any kind.
evidence:
  - REPOSITORY_EVIDENCE: CONSTITUTION.md sections 4, 5, 7 (state separation, evidence before architecture, change governance)
  - REPOSITORY_EVIDENCE: docs/governance/HOTL_GOVERNANCE.md human decision boundary and evidence rule
  - EVALUATION_EVIDENCE: docs/research/executions/BENCH-0004_RUN_2026-08-31.md — no document-level recall gain for the structured condition
  - EVALUATION_EVIDENCE: docs/research/executions/BENCH-0004_R2_2026-08-31.md — conditional cross-document advantage; broad CLM-0004 WEAKENED / INCONCLUSIVE
  - REPOSITORY_EVIDENCE: docs/research/RESEARCH_CORPUS_MAP.md — CORPUS_RECONCILIATION = PARTIAL, with an explicit stop condition
  - REPOSITORY_EVIDENCE: docs/research/RESEARCH_TO_CLAIM_RECONCILIATION_STATUS.md — negative finding that the thesis is not empirically validated
contradictions:
  - BENCH-0004 Round 2 is a positive result and is the strongest argument against gating; its own limitation 1 states the corpus is not independent of APF development, which is what makes it insufficient for promotion.
  - The gate slows delivery and can be read as indefinite deferral; this is mitigated by the exit criteria below, not by weakening the gate.
alternatives:
  - "A: No explicit gate — rely on CONSTITUTION.md section 5 as written. Rejected: a principle is not a decision point, and sessions had already started treating an executed benchmark as promotion evidence."
  - "B: Mechanical gate — CI check or required-file check blocking merges that add architecture contract material. Rejected for now: enforcement would have to encode what counts as architecture promotion, which is not yet stable, and a passing check would give false assurance. Retained as a future option once the contract boundary is defined."
  - "C: Normative gate recorded as a decision record and enforced through session protocol and review. Selected."
risks:
  - No mechanical enforcement means a later session can violate the gate without any tool objecting.
  - A future session may read the absence of a block as permission.
  - Without exit criteria the gate becomes indefinite deferral.
  - Over-broad reading could stall benchmark, corpus, and claim work that the gate does not intend to block.
recommendation: >
  Adopt the normative gate (alternative C) with explicit scope, explicit
  exit criteria, and an explicit statement that missing enforcement is not
  permission.
human_decision: >
  ACCEPTED. The evidence gate is in force. It blocks nothing mechanically and
  everything consequential in governance terms.
impact: >
  Architecture contract promotion and implementation start are blocked until
  the exit criteria are met per claim. Benchmark execution, claim scoping,
  corpus acquisition, and research assetization remain open and are the
  intended work.
implementation_scope: >
  Documentation and session protocol only. No code, no tooling, no CI check.
verification_plan: >
  Each session audit checks that no architecture contract or implementation
  artifact exists without a decision record authorizing it, and that any
  promotion cites a benchmark run meeting all four exit criteria.
related_assets:
  - docs/research/CLAIM_INVENTORY.md
  - docs/research/P0_FALSIFICATION_BENCHMARK_MATRIX.md
  - docs/research/P0_BENCHMARK_CASES_v0.1.md
  - docs/research/RESEARCH_CORPUS_MAP.md
related_decisions:
  - DEC-0002
related_commits:
  - 0d27769 research: execute BENCH-0004 round 2 cross-document temporal attack
  - 9a90e46 docs: record next-session entry points and governance gate in session state
```

## 1. Decision

No claim in the APF claim inventory may be promoted to an architecture contract, and no implementation may be started on the strength of that claim, until the exit criteria in section 4 are met for that specific claim.

The gate is normative. There is no CI check, hook, commit guard, or tooling that enforces it.

## 2. Why the gate is stated separately from the Constitution

`CONSTITUTION.md` section 5 already says architecture conclusions require evidence. That is a principle, and a principle does not answer the operational question of *when* evidence is sufficient. The practical failure mode this decision addresses is a session that executes a benchmark, obtains a positive number, and treats that number as authorization — which is the exact transition (`PROPOSED → DECIDED`) the Master Session Prompt forbids AI from performing silently.

BENCH-0004 Round 2 is the concrete case. It produced a real positive result (+0.21 chain coverage at k=2). It is also, by its own recorded limitation, run on a corpus that is not independent of APF development. Both statements are true simultaneously. Without a stated gate, the first statement is the one that gets carried forward.

## 3. Scope — what is and is not blocked

**Blocked:**

- Promoting any claim to an APF architecture contract or platform invariant.
- Starting implementation justified by a claim's benchmark result.
- Selecting a runtime, graph database, vector store, or framework as an APF contract.
- Treating a claim's tested scope as broader than the scope the benchmark actually covered.

**Not blocked:**

- Executing benchmarks, including on non-independent corpora, provided the result is recorded with its scope.
- Acquiring or constructing an independent engineering corpus.
- Narrowing, splitting, or rescoping claims based on results.
- Research assetization, corpus reconciliation, and claim record completion.
- Throwaway experimental code built to run a benchmark, provided it is not presented as APF implementation.

The gate blocks promotion, not investigation.

## 4. Exit criteria — how a claim leaves the gate

All four must hold for the specific claim being promoted:

1. **Independent corpus.** The deciding benchmark ran on a corpus that is not APF's own development history — real revision, configuration, and evidence transitions from outside this project.
2. **Predeclared falsifier.** The falsifier was recorded before the run (benchmark design rule B3) and was not met.
3. **Scope match.** The claim's wording matches the scope the run actually tested. A claim that survived a narrow test is promoted only in its narrow form.
4. **Explicit decision record.** A separate decision record authorizes the promotion, citing the run. This record does not itself authorize any promotion.

A benchmark that fails criterion 1 can still weaken, falsify, or rescope a claim. It cannot promote one.

## 5. Enforcement reality

This is the part that is easy to lose between sessions:

> Nothing will stop a later session from writing an architecture contract. The repository will accept the commit. CI will not complain. That is not approval.

`CONSTITUTION.md` section 4 already states `Commit != human decision`. DEC-0001 makes the consequence explicit: a contract committed without a promotion decision record is not in force, regardless of it being merged, and must be reverted or retroactively decided rather than inherited.

Alternative B (mechanical enforcement) was rejected for now, not permanently. It becomes appropriate once the architecture contract boundary is defined well enough that a check can identify what it is guarding. Until then a green check would assert more than it can verify.

## 6. Open item

The corpus-independence requirement in criterion 1 is recorded in this project under an ambiguous label. `docs/governance/LESSONS_LEARNED_2026-08-30-engineering-work-mvp.md` section L9 concerns keeping internal history and external knowledge distinguishable by authority level; the corpus-independence problem is stated as limitation 1 of BENCH-0004 Round 2. This record deliberately cites the Round 2 limitation rather than the L9 label. The label question is tracked in `docs/handoff/SESSION_STATE.md` under Unresolved References.
