# APF Research Corpus → Claim Map v0.1

**Status:** Canonical corpus reconciliation status
**Important:** This document distinguishes repository-preserved evidence from conversation-derived research that still requires durable capture.

**Absorbed:** `RESEARCH_TO_CLAIM_RECONCILIATION_STATUS.md` merged in on
2026-09-02 under `docs/decisions/DEC-0001-benchmark-id-and-doc-consolidation.md`.

## 1. Scope

The APF research effort has produced material across multiple sessions. The purpose of this map is to prevent useful reasoning from becoming an untraceable memory and to prevent repeated discussion from being mistaken for independent evidence.

## 2. Current corpus clusters

| Corpus cluster | Representative session/source | Main topics | Candidate claims | Durable status |
|---|---|---|---|---|
| APF foundation | 2026-08-29~30 APF architecture / redefinition sessions | work-centric boundary, state separation, governance, evidence-before-architecture | CLM-0001, 0007, 0008 | Partially preserved in repository |
| Research asset synthesis | 2026-08-30 architecture asset sessions | semantic extraction, asset ownership, framework neutrality, flexible promotion | CLM-0008 plus future semantic claims | Partially preserved |
| Engineering work augmentation | 2026-08-30 Engineering Work MVP session | capture-first, engineering history, progressive disclosure, provenance, failed attempts | CLM-0002, 0003, 0004, 0005, 0006, 0009, 0010 | Preserved as lessons learned |
| Architecture verification methodology | 2026-08-30 validation / audit sessions | hypothesis testing, verification, falsification, cold audit | Cross-cutting benchmark methodology | Partially preserved |
| UX / interaction research | 2026-08-30 UI and open-source review sessions | one capture surface, answer-first retrieval, detail-on-demand, desktop-first | CLM-0002, 0003, 0004 | Partially preserved |
| External framework research | APF deep research sessions | LangGraph, OpenHands, MCP, OPA, OpenFGA, Temporal, Backstage, OpenTelemetry, evaluation systems | CLM-0008; supporting evidence for multiple claims | Asset inventory incomplete |
| Prior AgentFactory experience | Referenced explicitly as external material | agent workflows, governance patterns, prior implementation lessons | None automatically | Reference only until reconciled |

## 3. Reconciliation status

### Confirmed repository-preserved assets

- APF Constitution
- Master Session Prompt
- Research Asset Ledger
- HoTL Governance
- Engineering Work MVP lessons learned
- Initial Claim Inventory
- Claim Reconciliation Protocol
- P0 Falsification Benchmark Matrix
- Asset → Claim → Benchmark traceability map

### Conversation-derived material still requiring durable asset records

- Detailed findings from individual external framework reviews
- Contradictory findings between frameworks and APF hypotheses
- Specific UX alternative comparisons
- Detailed verification-method research
- Detailed cold-audit findings and proposed failure cases
- Earlier semantic ownership / reference / domain-specific classification discussions

## 4. Important interpretation rule

A conversation-derived item is **not** treated as independent evidence merely because it appeared in multiple sessions. It becomes an evidence-bearing research asset only after its source, finding, scope, and provenance are captured.

## 5. Sequencing rule and how it was actually applied

This document originally stated:

> Only after corpus reconciliation, execute the P0 benchmarks.

**That rule was not followed.** BENCH-0004 rounds 1 to 3 were executed while
`CORPUS_RECONCILIATION` was, and remains, `PARTIAL`. Recording this rather than
quietly dropping the rule during consolidation, per anti-drift rule 7.

Assessment: the rule is **too strict as written and is hereby narrowed**.
Waiting for complete corpus reconciliation before any falsification attempt
would have delayed the first negative result indefinitely, and BENCH-0004 did
not depend on the unreconciled material — it ran against a frozen, enumerated
21-document corpus whose contents are listed in its predeclaration.

The narrowed rule:

> A benchmark may execute against an explicitly frozen and enumerated corpus at
> any time. Corpus reconciliation must complete before a benchmark result is
> used to promote a claim toward an architecture contract.

The second half is unaffected by what has happened so far: no claim has been
promoted, and BENCH-0004's outcome was falsification rather than promotion.


## 6. Per-source reconciliation coverage

Absorbed from `RESEARCH_TO_CLAIM_RECONCILIATION_STATUS`.

| Source family | Current handling | Confidence |
|---|---|---:|
| Research Asset Ledger | canonical intake/index | High |
| Engineering Work Augmentation lessons | converted into candidate product/engineering claims | Medium |
| Capture-first UX lessons | mapped primarily to CLM-0002 and related claims | Medium |
| History / retrieval lessons | mapped primarily to CLM-0004 | Medium |
| Provenance / trust lessons | mapped primarily to CLM-0006 | Medium |
| Human accountability / HoTL governance | mapped primarily to CLM-0007 | High |
| Automation value thesis | mapped primarily to CLM-0009 | Medium |

## 7. Known limitation

The repository contains the formalized foundation and recent research artifacts,
but this does **not** prove that every research finding from prior conversational
sessions has been recovered. Conversation-derived assets that were never
persisted to the repository remain a reconciliation gap.

The phase is therefore explicitly marked:

```text
CORPUS_RECONCILIATION = PARTIAL
```

## 8. Important negative finding

The current repository structure is not yet sufficient to claim that APF's
architectural thesis has been empirically validated. The evidence base is still
primarily research, governance, and candidate-hypothesis material. This is
expected at this phase and should remain visible.

BENCH-0004 sharpens rather than softens this. The first P0 claim to complete a
falsification attempt was falsified at its tested scope, which means the
evidence base has now produced its first genuine negative result rather than a
confirmation.

## 9. Exit criterion

Declared once, here. This document previously carried a "stop condition" while
`RESEARCH_TO_CLAIM_RECONCILIATION_STATUS` carried a separate "exit criterion"
and `CLAIM_RECONCILIATION` carried a third "exit condition for this phase". They
are merged into the following single criterion.

Do not move `CORPUS_RECONCILIATION` from `PARTIAL` to `COMPLETE` until **all** of:

1. Every material finding has one of: `ASSET` id, `REFERENCE-ONLY`,
   `OUT-OF-SCOPE`, `DUPLICATE`, or `INSUFFICIENT` record.
2. Every P0 claim has traceable source coverage plus a benchmark, or an explicit
   recorded reason why benchmarking is currently impossible.
3. The provenance gap in §7 is addressed with a recorded inventory or an explicit
   statement that the source history is inaccessible.

Do not declare the architecture validated at any point in this phase.

## 10. Required next reconciliation pass

1. Recover every persisted research asset and source note available to the project.
2. Extract atomic claims rather than importing conclusions wholesale.
3. Link each claim to support and counter-evidence.
4. Identify duplicate and contradictory claims.
5. Mark missing source provenance as a gap; do not silently fill it.
6. Give every P0 claim a benchmark or an explicit `INSUFFICIENT` status.
