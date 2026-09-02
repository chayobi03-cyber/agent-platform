# APF Claim Inventory v0.1

**Status:** Working inventory / non-normative
**Purpose:** Convert APF research and design assertions into explicit, falsifiable claims before architecture adoption.

## 1. Why a Claim Inventory exists

The Research Asset Ledger records reusable findings and candidate assets. It is insufficient by itself for evaluating whether an APF assertion is actually supported.

A Claim is the smallest reviewable statement that can be:

```text
supported / weakened / contradicted / falsified / left unresolved
```

The Claim Inventory therefore sits between research assets and architecture decisions:

```text
Research Finding
      ↓
Research Asset Candidate
      ↓
CLAIM INVENTORY
      ↓
Evidence + Counter-evidence
      ↓
Falsification Benchmark
      ↓
Human Decision
      ↓
Architecture / Implementation
```

A claim does **not** become an APF invariant merely because it is repeated across sources.

## 2. Claim state model

```text
DISCOVERED
  ↓
FORMULATED
  ↓
TESTABLE
  ↓
UNDER_TEST
  ├── SUPPORTED
  ├── WEAKENED
  ├── CONTRADICTED
  ├── FALSIFIED
  └── INCONCLUSIVE
```

A state transition requires an evidence reference. `SUPPORTED` does not mean `PROVEN`; it means the current evidence has not defeated the claim and supports the stated scope.

## 3. Claim taxonomy

Use the smallest useful class:

- PRODUCT — user/workflow value claim
- SEMANTIC — claim about a reusable domain concept or relation
- ARCHITECTURAL — claim about system structure or boundaries
- OPERATIONAL — claim about runtime behavior, reliability, or maintainability
- CONTROL — claim about permission, policy, governance, or human accountability
- EVALUATION — claim about measurement, benchmark validity, or fitness
- SECURITY — claim about threat resistance or isolation

## 4. Required claim record

```yaml
claim_id: CLM-0001
title:
statement:
claim_type: PRODUCT | SEMANTIC | ARCHITECTURAL | OPERATIONAL | CONTROL | EVALUATION | SECURITY
scope:
non_scope:
source_assets: []
origin:
mechanism:
preconditions: []
observable_prediction:
falsifier:
minimum_evidence:
preferred_evidence:
counter_evidence: []
benchmark_refs: []
related_claims: []
related_decisions: []
current_state: DISCOVERED | FORMULATED | TESTABLE | UNDER_TEST | SUPPORTED | WEAKENED | CONTRADICTED | FALSIFIED | INCONCLUSIVE
confidence:
owner:
last_reviewed:
notes:
```

## 5. Quality gate for a usable claim

A claim is `TESTABLE` only when all of the following are present:

1. A bounded statement rather than a slogan.
2. A defined scope and explicit non-scope.
3. An observable prediction or expected behavior.
4. At least one plausible falsifier.
5. A minimum evidence requirement.
6. A way to distinguish the claim from a nearby competing explanation.

Claims that cannot satisfy these conditions remain research observations, not architecture inputs.

## 6. Initial APF claim candidates

These are intentionally hypotheses, not accepted APF invariants.

### CLM-0001 — Work-centric abstraction is more general than agent-centric abstraction

**Statement:** A platform organized around work, automation opportunity, execution, evidence, and outcome can support both agentic and non-agentic automation without making an agent runtime the core abstraction.

**Falsifier:** Important target workloads require agent-specific concepts at the core boundary such that the work-centric model consistently loses essential information or creates materially worse implementation/control complexity.

**Benchmark direction:** Compare a representative workload matrix modeled with a work-centric core versus an agent-centric core.

### CLM-0002 — Zero-ceremony capture increases usable engineering memory

**Statement:** Reducing capture friction while automatically structuring content increases the amount of project history that is actually retained and later reusable.

**Falsifier:** Lower-friction capture does not increase retained/retrievable engineering context, or the resulting semantic noise offsets the benefit.

**Benchmark direction:** Capture rate, reconstruction time, retrieval usefulness, correction burden, and noise rate versus a manual-note baseline.

### CLM-0003 — Progressive disclosure improves engineering usability without reducing evidence access

**Statement:** Showing summary/context first and allowing drill-down to history, evidence, and raw artifacts reduces interaction burden while preserving access to verification detail.

**Falsifier:** Users make materially more incorrect judgments, cannot reach evidence efficiently, or interaction cost remains equal/worse than an evidence-dense interface.

**Benchmark direction:** Task completion time, error rate, evidence lookup time, and drill-down frequency.

### CLM-0004 — Temporal/provenance-aware history improves engineering retrieval

**Statement:** Retrieval that understands chronology, provenance, configuration, and relationships recovers useful engineering reasoning better than flat semantic retrieval alone for target engineering questions.

**Falsifier:** A conventional semantic baseline matches or exceeds useful-case recall/precision and grounding on representative tasks, or the added structure creates unacceptable maintenance cost.

**Benchmark direction:** Same corpus and questions; compare flat semantic retrieval with relationship/provenance-aware retrieval.

**Split:** This broad claim is decomposed into `CLM-0004a` (temporal), `CLM-0004b` (provenance)
and `CLM-0004c` (relationship) below, per §9 of `FALSIFICATION_BENCHMARK.md` and the
decomposition required by `executions/BENCH-0004_R2_2026-08-31.md` §10. The broad claim is
retained as the parent; evidence attaches to the mechanism claims.

**Current state:** `INCONCLUSIVE`. R1 produced a negative result at document-recall level; R2
showed conditional advantage on cross-document chain coverage; the downstream transfer to LLM
answer quality is untested (BENCH-0004-E2 blocked at G1). **Not promoted.**

---

The three mechanism claims below were entered on 2026-09-02 to close the linkage gap recorded
as F1 in `APF_PROJECT_AUDIT_2026-09-02.md`: the BENCH-0004-E2 factorial had already measured
these three mechanisms separately, but no claim record existed for the result to attach to.

They share a scope, a non-scope, and an evidence base, stated once here rather than repeated
three times.

**Shared scope.** Context-sufficiency score in the BENCH-0004-E2 2^3 factorial: 8 cells x 12
cases, n=96, case-blocked. The artifact is an explicitly **controlled reconstruction**, not the
historical CLM-0004 fixture.

**Shared non-scope.** These claims say nothing about: LLM answer quality (that is E2, not yet
executed); independent non-APF engineering corpora; production graph or vector retrieval
implementations; latency, indexing cost, or maintenance burden; and any interaction between the
three mechanisms — the factorial found no interaction term reaching significance.

**Shared evidence — `BENCH-0004-E2` factorial, case-blocked OLS `context_score ~ C(case) + T*R*P`:**

| Mechanism | Factor | Coefficient | p | Raw main effect |
|---|---|---:|---:|---:|
| CLM-0004a temporal | T | +0.1683 | 0.023 | +0.1429 |
| CLM-0004c relationship | R | +0.1675 | 0.024 | +0.1282 |
| CLM-0004b provenance | P | +0.2433 | 0.001 | +0.2040 |

Case block p < 1e-13; model R² = 0.733. All interaction terms p > 0.66.

**Shared evidence limitation — why no state advances past `UNDER_TEST`.** The underlying 96
observations are not available in this repository; only the cell means and the OLS output were
transmitted in the 2026-09-02 handoff. The factorial arithmetic was independently rechecked and
reproduces exactly from the published cell means (all 7 effects, deviation < 5e-5), but that
verifies internal consistency, not the observations. Until the fixture bytes are delivered and
`tools/bench0004_e2/verify_fixture.py` passes, no mechanism claim may transition to `SUPPORTED`.

### CLM-0004a — Temporal validity filtering improves retrieval context sufficiency

**Statement:** Filtering retrieval by temporal validity and version currency increases the
sufficiency of the retrieved context for engineering questions whose answer depends on which
state was current at a given time.

**Scope / Non-scope:** shared, above.

**Observable prediction:** Enabling temporal filtering raises the context-sufficiency score
relative to the same configuration without it, after blocking on case.

**Falsifier:** Temporal filtering produces no measurable context-sufficiency gain after case
blocking, or its gain disappears once relationship and provenance mechanisms are present.

**Minimum evidence:** One case-blocked factorial showing a positive main effect. **Met at
context level** by the shared evidence above.

**Preferred evidence:** The same effect on answer quality across evaluator replacement (E2), on
a corpus independent of APF.

**Counter-evidence:** `executions/BENCH-0004_E2b_2026-09-02.md` — on an independently
constructed 96-context factorial over the repository's own committed history, temporal
filtering produced **+0.0191 at p=0.438**, indistinguishable from zero, against the original
factorial's +0.1683 at p=0.023. The falsifier stated above was observed. Temporal filtering was
not inert: it changed the retrieved set in 92% of comparisons and in all eight temporally
dependent cases, so the null is a failure to improve sufficiency rather than a failure to act.
Bounding limitation: ten of sixteen corpus paths carry a single committed version, capping how
much sufficiency temporal filtering could add.

**Current state:** `WEAKENED`. One non-replication on a corpus with shallow version depth does
not falsify, and the original factorial's observations remain unavailable, so neither result can
adjudicate the other. Promotion is out of the question until at least one of the two is
reproducible.

### CLM-0004b — Provenance-aware ranking improves retrieval context sufficiency

**Statement:** Ranking retrieval by provenance and supplying authority/locator context increases
the sufficiency of the retrieved context for engineering questions whose answer depends on where
evidence came from and under what configuration it was produced.

**Scope / Non-scope:** shared, above.

**Observable prediction:** Enabling provenance-aware ranking raises the context-sufficiency score
relative to the same configuration without it, after blocking on case.

**Falsifier:** Provenance-aware ranking produces no measurable context-sufficiency gain after
case blocking, or the gain is explained by the authority/locator text acting as generic
additional context rather than by provenance.

**Minimum evidence:** One case-blocked factorial showing a positive main effect. **Met at
context level** by the shared evidence above, where P is the largest of the three main effects.

**Preferred evidence:** As CLM-0004a, plus an arm that supplies length-matched non-provenance
context to rule out the generic-context explanation named in the falsifier.

**Replication:** `executions/BENCH-0004_E2b_2026-09-02.md` — +0.1406 at p<0.0001 on an
independently constructed case set, again the largest of the three main effects. The direction
and the ranking both replicate.

**Current state:** `UNDER_TEST`. Replicated at context level, but the generic-context
alternative explanation is still not excluded by any executed run, and context-level gain is not
answer-quality gain until Stage 2 runs.

### CLM-0004c — Relationship expansion improves retrieval context sufficiency

**Statement:** Expanding retrieval across declared relationships increases the sufficiency of the
retrieved context for engineering questions whose answer spans more than one document.

**Scope / Non-scope:** shared, above.

**Observable prediction:** Enabling one-hop relationship expansion raises the context-sufficiency
score relative to the same configuration without it, after blocking on case.

**Falsifier:** Relationship expansion produces no measurable context-sufficiency gain after case
blocking, or the gain is an artifact of the hand-specified relationship graph rather than of
relationship structure in the corpus.

**Minimum evidence:** One case-blocked factorial showing a positive main effect. **Met at
context level** by the shared evidence above.

**Supporting evidence:** `executions/BENCH-0004_R2_2026-08-31.md` — chain coverage@2 rose from
0.4792 to 0.6875 and complete chains from 1/8 to 3/8. That run used a hand-specified graph and
therefore illustrates rather than excludes the artifact explanation in the falsifier.

**Counter-evidence:** `executions/BENCH-0004_RUN_2026-08-31.md` — at document-recall level,
adding structure to a competent semantic+metadata retriever produced **no** gain (B/C/D all 90%
top-1, 100% top-2). This is retained as a linked negative result, per §7.

**Replication:** `executions/BENCH-0004_E2b_2026-09-02.md` — +0.0990 at p=0.0001 on an
independently constructed case set.

**Current state:** `UNDER_TEST`. Replicated at context level. Supporting and counter-evidence
coexist at different metric levels and must not be collapsed.

### CLM-0005 — Failed attempts are first-class engineering evidence

**Statement:** Preserving rejected hypotheses, failed experiments, and superseded decisions improves future engineering decisions by preventing repeated dead ends and clarifying decision history.

**Falsifier:** Failure-history access produces no measurable reduction in repeated work/errors, or false-history contamination creates larger costs than its benefit.

**Benchmark direction:** Repeated-issue rate, time-to-resolution, decision confidence, and false-recall rate.

### CLM-0006 — Provenance/configuration is necessary for trusted engineering evidence

**Statement:** Engineering evidence lacking relevant revision/configuration/tool/setup provenance is materially less trustworthy for reuse and audit than evidence carrying that context.

**Falsifier:** Target decisions remain equally reliable without provenance, or provenance collection imposes disproportionate burden without measurable benefit.

**Benchmark direction:** Blind provenance ablation versus full-provenance condition; assess expert agreement and reuse error.

### CLM-0007 — Human approval belongs at consequential boundaries

**Statement:** Explicit human ownership/approval at architecture, permission, policy exception, release, and business-acceptance boundaries reduces unacceptable autonomous outcomes relative to unrestricted execution.

**Falsifier:** Approval gates do not reduce material risk/error, or their latency/operational cost overwhelms the benefit for the intended workload class.

**Benchmark direction:** Controlled scenarios measuring prevented harmful actions, false approvals, latency, and escalation load.

### CLM-0008 — External frameworks should be extracted into primitives rather than copied into APF contracts

**Statement:** Framework-neutral primitives preserve more portability and reduce accidental coupling while retaining the reusable value of external systems.

**Falsifier:** Direct adoption of a framework abstraction consistently provides superior portability, clarity, operability, and lifecycle fitness for target workloads.

**Benchmark direction:** Cross-framework capability matrix plus implementation migration/extension exercise.

### CLM-0009 — Automation should be promoted only when measured work reduction exists

**Statement:** Candidate automation should be promoted when it reduces engineer effort while maintaining required correctness, evidence quality, and trust.

**Falsifier:** Work reduction is not reproducible, or gains require unacceptable quality/trust degradation.

**Benchmark direction:** Baseline/manual versus augmented workflow with time, rework, correctness, evidence completeness, and escalation metrics.

### CLM-0010 — Engineering Work Augmentation is a more testable initial product thesis than a generic Agent Platform

**Statement:** Framing APF around concrete engineering-work augmentation produces more measurable user value and lower validation risk than starting from a generic agent-building surface.

**Falsifier:** Generic agent-builder framing attracts more validated high-value workflows with equal/lower effort and stronger evidence, or engineering augmentation does not generalize beyond the initial domain.

**Benchmark direction:** Compare opportunity discovery and validation outcomes across representative non-agentic, agentic, and engineering-augmentation workflows.

## 7. Claim-to-Asset relation

A research asset may support multiple claims; a claim may depend on multiple assets. Do not collapse either relation.

```text
Asset A ─┬─→ Claim 1
Asset B ─┼─→ Claim 1
Asset C ─└─→ Claim 2

Claim 1 ─→ Benchmark B1
Claim 1 ─→ Decision D1
```

Contradictory assets must remain linked to the claim rather than being silently discarded.

## 8. Promotion rule

No claim should be promoted to:

```text
APF invariant / architecture contract / implementation dependency
```

without:

```text
claim record
+ supporting evidence
+ explicit counter-evidence review
+ falsification attempt
+ scope statement
+ human decision where consequential
```

## 9. Initial review priority

P0 claims should be tested first where failure would invalidate broad portions of the platform thesis:

```text
CLM-0001  Work-centric generality
CLM-0002  Capture value
CLM-0004  Structured retrieval value   → split into 0004a/b/c, evidence attaches to the children
CLM-0006  Provenance trust
CLM-0007  Human boundary value
CLM-0009  Measured automation value
```

The inventory should remain editable. New evidence may split one claim into narrower claims rather than forcing a single broad claim to survive.

## 10. Record-completeness status

`CLM-0004a`, `CLM-0004b` and `CLM-0004c` are the only claims currently satisfying all six §5
conditions, and they are the reference form for the rest. The remaining ten carry a statement
and a falsifier but no explicit scope, non-scope, observable prediction, or minimum evidence,
and the §4 record template is unpopulated throughout.

This gap between §5 as written and the inventory as practised is recorded as finding F3 in
`APF_PROJECT_AUDIT_2026-09-02.md` and is pending an owner decision — see
`../decisions/DEC-0002_claim_record_completeness.md`. It is not closed by filling the five
remaining P0 claims speculatively: scope, prediction, and minimum evidence are claim
definitions, and inventing them for claims that have no evidence would put untested
assertions into the inventory under the appearance of rigour. `CLM-0004a/b/c` could be
completed only because an executed factorial defined what was actually measured.
