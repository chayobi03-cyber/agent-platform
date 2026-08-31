# APF Research Corpus → Claim Map v0.1

**Status:** Working reconciliation record
**Important:** This document distinguishes repository-preserved evidence from conversation-derived research that still requires durable capture.

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

## 5. Immediate reconciliation work

Prioritize the following:

1. Recover durable source references for each external research track.
2. Convert each meaningful finding into `ASSET-*` records.
3. Link each asset to one or more claims.
4. Record contradiction links explicitly.
5. Mark unsupported claims as `INSUFFICIENT` rather than filling gaps with assumptions.
6. Only after corpus reconciliation, execute the P0 benchmarks.

## 6. Stop condition

Do not call the research corpus complete until each material finding has one of:

```text
ASSET ID
REFERENCE-ONLY record
OUT-OF-SCOPE record
DUPLICATE record
INSUFFICIENT record
```

and every P0 claim has traceable source coverage plus a benchmark or an explicit reason why benchmarking is currently impossible.
