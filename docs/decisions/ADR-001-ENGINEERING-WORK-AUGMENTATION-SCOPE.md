# ADR-001 — Engineering Work Augmentation Scope

```yaml
id: ADR-001
status: DECIDED
date: 2026-08-30
```

## Context

APF began as a work-centric internal agent platform. Research into project management, engineering knowledge management, ADRs, traceability, engineering notebooks, lessons learned, and engineering knowledge graphs indicates that a concrete engineering workload is required to validate APF's architecture empirically.

The selected workload is engineering project execution with an initial focus on EMC / PCB development.

## Problem

A project-history-only tool risks becoming a documentation system that adds record-keeping work without materially reducing engineering effort. The product therefore needs to connect project history to actual engineering validation, analysis, knowledge retrieval, and workflow execution.

## Evidence

The current research indicates independently validated patterns for project history, decision context, traceability, lessons learned, and evidence-linked engineering knowledge. The research does not yet prove that an integrated Engineering History Graph materially outperforms conventional relational/document approaches for engineering work.

## Alternatives

### A — Conventional project history tool

Project, milestone, issue, document, and timeline management with conventional relational storage.

### B — Engineering History model

Conventional project context plus explicit engineering events, evidence, decisions, experiments, relationships, time, and provenance.

### C — Engineering Work Augmentation Platform

Engineering History model plus deterministic validation tools, simulation/measurement tools, domain knowledge retrieval, communication retrieval, workflow orchestration, agentic assistance, and human approval.

## Risks

- Graph modeling may introduce unnecessary data-capture and maintenance cost.
- Agentic workflows may add complexity without measurable benefit.
- LLM-generated relations or conclusions may be mistaken for verified engineering evidence.
- Commercial tools may already cover portions of the target workflow.
- The integrated platform could become a large replacement system instead of an augmentation layer.

## Recommendation

Adopt **C as the product experiment scope**, while keeping B and all underlying semantic constructs as hypotheses requiring empirical validation.

The first specialization will leverage the existing **HyperLynx DRC baseline** and extend it through Python rather than recreate existing commercial checks unnecessarily.

Candidate future capabilities include:

```text
HyperLynx baseline DRC
Python ODB++ / schematic validation
RE-focused checks
CST automation
EMC expert retrieval
Email / communication retrieval
Measurement / simulation correlation
Engineering history
Workflow orchestration
Agent assistance
```

## Human Decision

**APPROVED** — proceed with the Engineering Work Augmentation Platform as APF's first concrete experimental workload, while preserving framework neutrality and hypothesis-driven architecture evolution.

This approval is a product-scope decision; it does not approve a specific graph database, agent runtime, framework, schema, or autonomous operating policy.

## Impact

The project specification should treat:

```text
Engineering History Graph
+
Validation
+
Analysis
+
Knowledge
+
Workflow / Agent
+
Human Judgment
```

as the candidate integrated system under test.

## Implementation Scope

Initial implementation priority:

1. Existing HyperLynx DRC as baseline evidence source.
2. Python extension for organization-specific / cross-domain validation.
3. Engineering History capture for validation findings.
4. Historical EMC case retrieval.
5. Controlled CST automation experiment.
6. Broader communication / email retrieval after provenance and permission design.

## Verification Plan

Compare H1/H2/H3 using real engineering cases and measure:

- task/search time
- context reconstruction time
- validation effort
- historical retrieval quality
- evidence grounding
- human correction rate
- engineering outcome quality
- maintenance/data-capture burden

## Related Assets

- EHG-001 through EHG-010 in `docs/research/ASSET_LEDGER.md`

## Related Specification

- `docs/product/ENGINEERING_WORK_AUGMENTATION_SPEC.md`
