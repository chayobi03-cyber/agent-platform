# APF Session Lessons Learned — 2026-08-30

**Scope:** Engineering Work Augmentation experimental workload
**Status:** Session learning / candidate guidance

## 1. Session Summary

The workload was initially framed as an engineering project history-management tool. Review and research shifted the product thesis toward an **Engineering Work Augmentation Platform** whose purpose is to reduce real engineering effort while preserving human engineering judgment.

The initial EMC/PCB workload includes existing HyperLynx DRC baseline automation, planned Python extensions, ODB++ and schematic validation, CST automation, EMC expert retrieval, email/communication retrieval, and a shared engineering history/context layer.

## 2. Key Lessons

### L1 — Capture-first is a better initial MVP than automation-first

Building the full ODB/CST/RAG/Agent stack first risks validating technology integration rather than user value.

A lower-risk first experiment is an **Engineering Capture Inbox / Project Memory** that allows engineers to drop text, screenshots, files, links, and later other sources with near-zero ceremony.

The first question should be whether passive/low-friction capture creates usable project memory and reduces context reconstruction, search, and reporting work.

### L2 — The user must not manage the semantic model

Users should not be required to choose Issue / Decision / Experiment / Document before capturing information or manually construct graph nodes and edges.

Preferred flow:

```text
Capture
→ AI extraction / classification
→ candidate context / relations
→ selective human correction or approval
→ history
```

### L3 — Engineering History Graph is a semantic backbone, not the UI

The Graph hypothesis remains valuable, but graph visualization and graph-database technology must not become the product objective.

The useful abstraction is a **temporal, provenance-aware, evidence-linked engineering history model**. The UI should expose concise summaries first and reveal deeper context only on demand.

### L4 — Progressive disclosure is a product invariant candidate

Default screens should show only the information needed for the current task. Users must still be able to drill down into:

```text
Summary
→ Context
→ History
→ Evidence
→ Raw artifact
```

Search should be answer-first, with deeper evidence available on demand.

### L5 — One capture surface should support many input types

Desktop/Web is the initial priority. Mobile is explicitly deferred and can later be implemented through a messaging/chat interface over the same capture/retrieval APIs.

Initial capture candidates:

```text
text / paste / screenshot / image / file / link
```

Later:

```text
email / Git / CST / ODB++ / measurement / external communication
```

### L6 — Existing commercial automation must be treated as baseline, not duplicated

HyperLynx DRC already provides first-line automated checking. Python should primarily extend the baseline through organization-specific rules, cross-domain checks, topology analysis, normalization, evidence generation, historical checks, and issue creation.

### L7 — The missing engineering loop is broader than Issue tracking

The semantic model must be able to represent at least:

```text
Requirement
→ Design / Revision
→ Validation
→ Problem / Observation
→ Hypothesis
→ Experiment
→ Evidence / Result
→ Decision
→ Change
→ Verification
→ Learning
```

Failed attempts and rejected hypotheses are valuable history and must not be discarded.

### L8 — Provenance and configuration are mandatory for engineering trust

Engineering evidence must retain, where applicable:

```text
revision
configuration
rule version
tool version
simulation setup
measurement setup
source artifact
time
actor
verification state
```

AI inference must remain distinguishable from primary engineering evidence.

### L9 — Internal history and external knowledge must remain distinguishable

EMC expert capability should combine internal validated project experience with external standards, application notes, datasheets, papers, and vendor guidance without collapsing their authority levels.

### L10 — Agent/framework selection remains experimental

LangGraph, OpenHands, MCP, graph databases, vector stores, and other technologies remain implementation candidates. The APF principle remains:

```text
Work → Hypothesis → Implementation → Evidence → Fitness → Asset revision
```

No runtime is promoted to an APF contract merely because it is convenient or popular.

## 3. Product/UX Principles Emerging From the Session

1. **Zero-Ceremony Capture** — capture should feel like dropping information into an inbox, not filling out a form.
2. **Context by Default** — current project/work context should be inferred where possible.
3. **One Search / Ask Surface** — exact, semantic, and relational retrieval should be hidden behind one user-facing interaction.
4. **Summary-first, Detail-on-demand** — low information density by default, full evidence available when requested.
5. **AI as Infrastructure** — AI should quietly structure, retrieve, summarize, and propose; it should not dominate the UI.
6. **Human decision at consequential boundaries** — consequential facts, root causes, rule exceptions, design changes, and releases remain human-owned.

## 4. New Falsifiable Product Hypotheses

### HP-1 — Capture reduces work

Low-friction capture plus automatic structuring reduces project-context reconstruction and reporting effort compared with manual notes.

### HP-2 — Structured history improves retrieval

Explicit relationships between engineering events improve recovery of prior engineering reasoning compared with flat documents/project records.

### HP-3 — Graph-aware retrieval improves engineering usefulness

Temporal/provenance/relationship-aware retrieval improves relevant-case recall and evidence grounding compared with conventional semantic RAG alone.

### HP-4 — Automation should be added where measurable work reduction exists

Validation, simulation, retrieval, and reporting automation should only be promoted when they measurably reduce engineer effort without unacceptable quality or trust degradation.

## 5. Next Session Preparation

The next session should not expand feature scope first. It should convert this learning into a **concrete desktop/Web UX and first experiment specification**.

Priority sequence:

```text
1. Capture interaction model
2. Information architecture
3. Search / Recall interaction
4. Detail / progressive-disclosure model
5. Minimal semantic data model
6. Baseline user workflow
7. H0/H1/H2 experiment design
8. First implementation slice
```

The primary initial test should use the APF project itself as dogfooding data where practical.

## 6. Explicit Non-Goals for Next Session

- Do not start with a graph visualization.
- Do not choose Neo4j or another graph DB merely because the model is graph-shaped.
- Do not force a project-management dashboard into the first screen.
- Do not require manual taxonomy selection during capture.
- Do not prioritize mobile UI in the first experiment.
- Do not build a monolithic EMC super-agent.
