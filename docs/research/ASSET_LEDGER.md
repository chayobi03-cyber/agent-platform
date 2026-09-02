# APF Research Asset Ledger

**Status:** Populated 2026-09-02 with repository-derived assets only; no asset is accepted by default.

## State Model

```text
RAW_FINDING → ASSET_CANDIDATE → REVIEWED → ACCEPTED_ASSET
```

A research finding is not an APF rule. Adoption requires evidence, analysis, and an explicit human decision where consequential.

## Asset Record Template

```yaml
asset_id:
title:
status:
source:
source_type:
primitive:
entities:
relationships:
lifecycle:
control:
execution:
evidence:
ownership:
failure_mode:
security_boundary:
finding:
counter_evidence:
apf_relevance:
architectural_impact:
recommendation:
adoption: ADOPT | REFERENCE | DEFER | REJECT
confidence:
related_assets:
related_decisions:
evidence_links:
```

## Evidence Classes

- EXTERNAL_EVIDENCE
- REPOSITORY_EVIDENCE
- RUNTIME_EVIDENCE
- EVALUATION_EVIDENCE
- HUMAN_DECISION_EVIDENCE

## Initial Research Tracks

### P0

- Work / Opportunity
- Backstage
- Temporal
- LangGraph
- OpenFGA
- OPA
- MCP
- OpenTelemetry
- Phoenix / Evaluation
- Identity / Authorization

### P1

- A2A
- OpenHands / Sandbox
- Agent Security
- FinOps
- Agent Governance
- Operational Knowledge

## Research Rule

For every external source, extract architectural primitives rather than copying its framework-specific model. Cross-source agreement increases confidence; contradictions must be recorded explicitly.


---

## Asset Records

Populated 2026-09-02 to close audit finding F2. **Scope limit:** only findings actually produced
and preserved in this repository are recorded with content. The external research tracks listed
above are conversation-derived and absent from this repository; they are registered below as
pending recovery with **no content**, because inventing their findings would be fabrication and
would defeat the purpose of the ledger.

Every record below is `ASSET_CANDIDATE`. None is accepted. Per the state model, adoption requires
review and an explicit human decision.

### ASSET-0001 — Added retrieval structure does not guarantee recall gain

```yaml
asset_id: ASSET-0001
title: Structure layered on a competent semantic retriever does not guarantee recall improvement
status: ASSET_CANDIDATE
source: docs/research/executions/BENCH-0004_RUN_2026-08-31.md
source_type: REPOSITORY_EVIDENCE
primitive: retrieval mechanism evaluation
finding: >
  Adding explicit temporal/relationship/provenance routing on top of a semantic+metadata
  retriever produced no document-level recall gain. B, C and D all scored 90% top-1 and
  100% top-2 on a frozen 10-question set. D changed which document ranked first without
  improving the declared metric.
counter_evidence: ASSET-0002 shows a gain appears at a different metric level.
evidence: EVALUATION_EVIDENCE
apf_relevance: >
  Directly constrains CLM-0004. Retrieval structure must be justified against a specific
  metric, not asserted generally.
failure_mode: >
  Treating a mechanism as valuable because it changes behaviour, when the declared metric
  is unchanged.
architectural_impact: >
  Argues against making relationship/temporal routing a core contract on recall grounds alone.
recommendation: Keep as a standing constraint on retrieval claims.
adoption: DEFER
confidence: moderate — n=10, APF-dogfood corpus, prototype D
related_assets: [ASSET-0002, ASSET-0004]
evidence_links: [docs/research/executions/BENCH-0004_RUN_2026-08-31.md]
```

### ASSET-0002 — Chain coverage separates from document recall

```yaml
asset_id: ASSET-0002
title: Cross-document chain coverage is a distinct metric from document-level recall
status: ASSET_CANDIDATE
source: docs/research/executions/BENCH-0004_R2_2026-08-31.md
source_type: REPOSITORY_EVIDENCE
primitive: evaluation metric design
finding: >
  On questions whose answer spans multiple documents, chain coverage@2 rose from 0.4792 to
  0.6875 and complete chains from 1/8 to 3/8, while document recall had shown no difference.
  A mechanism can be invisible at one metric level and material at another.
counter_evidence: ASSET-0001 — no gain at document-recall level on the same corpus.
evidence: EVALUATION_EVIDENCE
apf_relevance: >
  Benchmarks must state which level they measure. A null at one level is not a null at all
  levels, and a gain at one level is not a gain at all levels.
failure_mode: Declaring a mechanism dead or proven from a single metric level.
architectural_impact: Method-level, not structural.
recommendation: Apply to every future retrieval benchmark.
adoption: DEFER
confidence: moderate — n=8, hand-specified relation graph
related_assets: [ASSET-0001]
evidence_links: [docs/research/executions/BENCH-0004_R2_2026-08-31.md]
```

### ASSET-0003 — Provenance is the largest retrieval mechanism, and it replicates

```yaml
asset_id: ASSET-0003
title: Provenance-aware ranking is the largest of the three retrieval mechanisms across two independent case sets
status: ASSET_CANDIDATE
source: docs/research/executions/BENCH-0004_E2b_2026-09-02.md
source_type: REPOSITORY_EVIDENCE
primitive: retrieval mechanism ranking
finding: >
  In the original factorial P was the largest main effect (+0.2433, p=0.001). In an
  independently constructed factorial over a different case set, P was again the largest
  (+0.1406, p<0.0001). Direction, significance and rank all replicate. R also replicates.
counter_evidence: >
  Both measurements are context sufficiency, not answer quality. The generic-context
  alternative explanation — that the authority/locator text helps as bulk context rather than
  as provenance — is excluded by neither run.
evidence: EVALUATION_EVIDENCE
apf_relevance: Supports CLM-0004b and CLM-0006 within retrieval scope.
failure_mode: Reading a replicated context-level effect as an answer-quality effect.
architectural_impact: >
  If it survives Stage 2, provenance carriage becomes a candidate retrieval contract element.
  Not before.
recommendation: Carry into BENCH-0006 as the prior.
adoption: DEFER
confidence: moderate-high on rank; low on transfer
related_assets: [ASSET-0004]
evidence_links:
  - docs/research/executions/BENCH-0004_E2b_2026-09-02.md
  - docs/research/CLAIM_INVENTORY.md
```

### ASSET-0004 — Temporal filtering acts without improving sufficiency

```yaml
asset_id: ASSET-0004
title: Temporal filtering changes what is retrieved without improving evidence sufficiency
status: ASSET_CANDIDATE
source: docs/research/executions/BENCH-0004_E2b_2026-09-02.md
source_type: REPOSITORY_EVIDENCE
primitive: retrieval mechanism evaluation
finding: >
  T failed to replicate: +0.0191 at p=0.438 against the original +0.1683 at p=0.023. It was
  not inert — it changed the retrieved set in 92% of comparisons and in every temporally
  dependent case. The same shape as ASSET-0001 one level down: the mechanism acts, the metric
  does not move.
counter_evidence: >
  The original factorial found T significant. Neither result can adjudicate the other: the
  original observations are unavailable, and E2b's corpus has ten of sixteen paths at a single
  version, capping what temporal filtering could add.
evidence: EVALUATION_EVIDENCE
apf_relevance: Weakens CLM-0004a. Cautions against temporal machinery as a core contract.
failure_mode: >
  Building version-awareness into a core contract on the strength of one unreplicated result.
architectural_impact: Defer any temporal retrieval contract until a deeper-history corpus tests it.
recommendation: Re-test on a corpus with genuine version depth before any promotion.
adoption: DEFER
confidence: moderate — one non-replication, bounded by corpus version depth
related_assets: [ASSET-0001, ASSET-0003]
evidence_links: [docs/research/executions/BENCH-0004_E2b_2026-09-02.md]
```

### ASSET-0005 — Evidence outside the evidence chain is unverifiable and unresumable

```yaml
asset_id: ASSET-0005
title: A benchmark artifact stored outside the repository cannot be verified, resumed, or recovered
status: ASSET_CANDIDATE
source: docs/research/executions/BENCH-0004_E2_2026-09-01.md
source_type: REPOSITORY_EVIDENCE
primitive: evidence lifecycle / governance
finding: >
  BENCH-0004-E2 froze a 96-context fixture and published four SHA-256 values, but the fixture
  bytes were never committed. The result is a benchmark that cannot be verified (no bytes to
  hash), cannot be executed (no request payload), and cannot be recovered (no commit, stash or
  dangling object holds it). Published hashes without their artifact establish only that the
  documents citing them agree with each other.
counter_evidence: none
evidence: REPOSITORY_EVIDENCE
apf_relevance: >
  Direct instance of Constitution section 5. An artifact referenced by an evidence chain must
  live inside it.
failure_mode: Treating a hash manifest as a substitute for the artifact.
architectural_impact: >
  Argues for a rule that any frozen benchmark artifact is committed with its lock, or is not
  considered frozen.
recommendation: >
  Adopt as a benchmark precondition. Already applied: BENCH-0004-E2b commits its fixture and
  passes byte-level verification, which E2 has never done.
adoption: DEFER
confidence: high — the failure was observed directly and the remedy was executed
related_assets: [ASSET-0006]
evidence_links:
  - docs/research/executions/BENCH-0004_E2_2026-09-01.md
  - docs/research/benchmarks/BENCH-0004-E2b/FIXTURE_LOCK.json
```

### ASSET-0006 — Deterministic pinned-corpus fixture construction with tiered verification

```yaml
asset_id: ASSET-0006
title: Pin the corpus, build deterministically, verify in tiers
status: ASSET_CANDIDATE
source: tools/bench0004_e2b/build_fixture.py
source_type: REPOSITORY_EVIDENCE
primitive: benchmark construction method
finding: >
  A fixture built from repository history changes as the repository grows, so it must be
  pinned to a commit or it cannot be rebuilt identically. Verification separates Tier 1
  (byte hashes of frozen files, authoritative) from Tier 2 (derived cross-checks, which can
  differ through canonicalization drift without indicating corruption). Determinism lets a
  reviewer recompute a result rather than trust it.
counter_evidence: >
  Determinism does not remove construction bias. E2b was built and analysed by the same
  session; determinism makes that bias auditable, not absent.
evidence: RUNTIME_EVIDENCE
apf_relevance: Reusable for every future benchmark fixture.
failure_mode: >
  An unpinned builder silently producing a different fixture on re-run, making a published
  lock meaningless.
architectural_impact: Method-level.
recommendation: Use for BENCH-0006 and subsequent benchmarks.
adoption: DEFER
confidence: high — determinism verified by rebuild comparison
related_assets: [ASSET-0005]
evidence_links: [tools/bench0004_e2b/README.md, tools/bench0004_e2/README.md]
```

## Pending Recovery Register

The following research tracks are named in `RESEARCH_CORPUS_MAP.md` as conversation-derived
material still requiring durable asset records. They are registered here so the gap is visible
and countable, **without content**. No finding, recommendation or confidence may be written for
any of them until its durable source is recovered.

| Placeholder | Track | State |
|---|---|---|
| ASSET-1001 | Backstage | `PENDING_RECOVERY` — no durable source in repository |
| ASSET-1002 | Temporal | `PENDING_RECOVERY` |
| ASSET-1003 | LangGraph | `PENDING_RECOVERY` |
| ASSET-1004 | OpenFGA | `PENDING_RECOVERY` |
| ASSET-1005 | OPA | `PENDING_RECOVERY` |
| ASSET-1006 | MCP | `PENDING_RECOVERY` |
| ASSET-1007 | OpenTelemetry | `PENDING_RECOVERY` |
| ASSET-1008 | Phoenix / Evaluation | `PENDING_RECOVERY` |
| ASSET-1009 | Identity / Authorization | `PENDING_RECOVERY` |
| ASSET-1010 | Work / Opportunity | `PENDING_RECOVERY` |

Recovery requires the source, finding, scope and provenance of each, per `RESEARCH_CORPUS_MAP.md`
§4. Until then these count as **unrecovered**, not as assets.

## Effect on T07 and T11

Populating this ledger does **not** unblock `T07` (asset reuse) or `T11` (asset invalidation).
Those benchmarks need a population of assets whose reuse changes downstream planning and
execution outcomes. `ASSET-0001` through `ASSET-0006` are research findings, not operational
assets of that kind, and all six are `ASSET_CANDIDATE` rather than accepted.

One partial instance is worth recording. `ASSET-0005` did change execution within this session:
the finding that a fixture outside the evidence chain cannot be verified is why BENCH-0004-E2b
commits its fixture and consequently passes byte-level verification. That is a single
uncontrolled observation, not a T07 result — there was no control arm, no inert-asset arm, and
the same session both produced the finding and acted on it.
