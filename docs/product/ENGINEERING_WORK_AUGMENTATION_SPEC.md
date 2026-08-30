# APF — Engineering Work Augmentation Platform Specification v0.1

**Status:** Candidate / Experimental Product Specification  
**Branch:** `feat/engineering-work-augmentation-spec`  
**Date:** 2026-08-30  
**Decision state:** Architecture remains hypothesis-driven; no runtime/framework is mandated by this document.

---

## 1. Purpose

This specification defines the first concrete product/work domain used to validate APF's core premise:

> APF should reduce and improve real engineering work by combining deterministic engineering tools, domain knowledge, project history, agentic orchestration, and human judgment.

The initial target domain is **engineering project execution**, with a first practical specialization in **EMC / PCB development**.

The system is not primarily a project-management application. Project, milestone, issue, and schedule data exist to provide context for engineering work.

The product's primary objective is to shorten the path from:

```text
Requirement
  ↓
Design
  ↓
Review / Verification
  ↓
Problem
  ↓
Investigation
  ↓
Experiment / Simulation / Measurement
  ↓
Decision
  ↓
Design Change
  ↓
Verification
  ↓
Release / Learning
```

while preserving auditable evidence and human accountability.

---

## 2. Product Thesis

The product hypothesis is:

> A temporal, provenance-aware engineering history model can become a shared context layer through which validation tools, simulation tools, knowledge retrieval, communication retrieval, and agents cooperate; this can reduce engineer effort without removing engineering judgment.

The system therefore has two distinct goals:

1. **Work reduction:** eliminate repetitive search, checking, data preparation, analysis preparation, reporting, and record reconstruction.
2. **Work enhancement:** improve context quality, traceability, evidence grounding, experiment selection, and reuse of prior engineering knowledge.

The product must not assume that an agent is always the correct automation mechanism.

---

## 3. Problem Definition

Engineering work is fragmented across tools and artifacts:

```text
CAD / ODB++
Schematic
Simulation
Measurement
Issue tracker
Git / revision systems
Email
Reports
Specifications
Design rules
Personal notes
```

The engineer must repeatedly reconstruct context across these systems.

Typical recurring work includes:

- locating similar historical problems
- determining which design revision was involved
- reconstructing what was tested and why
- checking PCB and schematic constraints
- preparing simulations
- comparing simulation and measurement results
- searching emails for decisions and exceptions
- writing reports from scattered evidence
- repeating previously solved troubleshooting paths
- documenting conclusions after the actual work is complete

The system should target these burdens rather than merely adding another repository for manual documentation.

---

## 4. Product Boundary

### In scope

- engineering project and milestone context
- requirements and acceptance criteria
- engineering events and history
- issue / problem tracking
- design revisions and configuration provenance
- evidence and artifact linkage
- engineering decisions and rationale
- experiments, simulations, measurements, and verification
- deterministic rule-based checks
- EMC / PCB domain analysis tools
- internal engineering knowledge retrieval
- external engineering knowledge retrieval
- email / communication retrieval where authorized
- report and engineering summary generation
- agentic orchestration where it demonstrably reduces work
- human approval and decision checkpoints
- architecture fitness measurement

### Out of scope for the initial product

- replacing existing enterprise PLM/ALM/PM systems wholesale
- unrestricted autonomous design decisions
- autonomous production release
- treating LLM output as authoritative engineering evidence
- requiring engineers to manually create every graph node/edge
- forcing a specific graph database or orchestration framework
- creating a single monolithic "EMC Super Agent"

---

## 5. Core Operating Model

```text
                    REAL ENGINEERING WORK
                             │
                             ▼
                    WORK CONTEXT ASSEMBLY
                             │
           ┌─────────────────┼─────────────────┐
           ▼                 ▼                 ▼
      Validation          Analysis         Knowledge
           │                 │                 │
   HyperLynx / Python     CST / Python       RAG / Email
           │                 │                 │
           └─────────────────┼─────────────────┘
                             ▼
                  ENGINEERING HISTORY MODEL
                             │
                             ▼
                    AGENT / WORKFLOW
                             │
                    Human Judgment Gate
                             │
                             ▼
                     Action / Experiment
                             │
                             ▼
                     Evidence / Result
                             │
                             ▼
                   Verification / Closure
                             │
                             ▼
                         Learning
```

The system should continuously convert actual work artifacts and decisions into structured, queryable history.

---

## 6. Engineering History Graph — Candidate Core Model

### 6.1 Model intent

`Engineering History Graph` is a **candidate semantic model**, not yet a mandated implementation technology.

Its purpose is to preserve relationships that are difficult to recover reliably from isolated documents or flat project records.

### 6.2 Candidate entities

```text
Project
Requirement
Specification
Constraint
Milestone
Design
DesignRevision
Artifact
Issue
Observation
Hypothesis
Experiment
Simulation
Measurement
Decision
Action
Change
Result
Verification
Violation
Recommendation
Lesson
Communication
Actor
ToolRun
Release
```

### 6.3 Candidate relationships

```text
contains
satisfies
constrained_by
depends_on
related_to
occurred_in
observed_in
derived_from
supports
contradicts
investigates
tested_by
caused_by
resolves
verified_by
supersedes
implements
violates
recommends
resulted_in
changed_to
communicated_in
similar_to
```

### 6.4 Required metadata for consequential relationships

Where applicable:

```text
time
actor
source
source_artifact
revision
confidence
status
verification_state
```

Relationships must not silently imply causality when only correlation or engineering suspicion exists.

For example:

```text
Hypothesis A
  --supported_by--> Evidence E1
```

is preferable to automatically asserting:

```text
Hypothesis A
  --caused_by--> Evidence E1
```

unless the engineering process has sufficient evidence to justify the stronger relation.

---

## 7. Evidence and Provenance Model

Evidence is a first-class concept.

The system must distinguish:

```text
Raw Artifact
Processed Observation
Engineering Interpretation
Hypothesis
Decision
Verification Result
```

For each important claim, the system should be able to answer:

```text
What was observed?
Where did it come from?
Which revision/configuration was involved?
Who or what produced it?
When was it produced?
Was it independently verified?
```

### Evidence classes

```text
MEASUREMENT
SIMULATION
DESIGN_ARTIFACT
RULE_CHECK
DOCUMENT
COMMUNICATION
CODE / REVISION
HUMAN_DECISION
AI_INFERENCE
```

AI inference must never be represented as equivalent to primary engineering evidence.

---

## 8. Engineering Reasoning Chain

A core history pattern is:

```text
Problem
  ↓
Observation
  ↓
Hypothesis
  ↓
Experiment
  ↓
Evidence
  ↓
Conclusion
  ↓
Decision
  ↓
Action / Design Change
  ↓
Verification
```

Multiple competing hypotheses and failed experiments must be supported.

Example:

```text
Issue: RE peak at 240 MHz

Hypothesis A: DDR harmonic coupling
    ↓
Experiment: clock disable
    ↓
Result: -4.8 dB
    ↓
Supported

Hypothesis B: connector coupling
    ↓
Experiment: temporary shield modification
    ↓
Result: +0.2 dB
    ↓
Not supported
```

The failed path is retained because it can prevent repeated investigation cost.

---

## 9. Revision / Configuration Provenance

Engineering conclusions are meaningful only in configuration context.

The model must therefore support:

```text
PCB Revision
Schematic Revision
Firmware Revision
Stackup Revision
Rule Version
Simulation Setup Version
Measurement Setup
Instrument / Calibration Context
Tool Version
Dataset Version
```

A verification result should be traceable to the configuration that produced it.

This enables:

```text
Rev A → Issue → Experiment → Result
Rev B → Change → Re-test → Result
```

and ultimately revision-to-revision impact analysis.

---

## 10. Initial EMC / PCB Automation Domain

The first domain specialization is EMC / PCB engineering.

### 10.1 HyperLynx DRC

HyperLynx DRC is treated as an existing baseline automation capability.

The product should not rebuild functionality already covered adequately by the commercial tool.

Its role is:

```text
Commercial deterministic baseline
        ↓
Known-rule violation set
        ↓
Evidence imported into APF
```

### 10.2 Python engineering validation layer

Python should extend rather than unnecessarily duplicate the baseline.

Candidate responsibilities:

- organization-specific EMC rules
- cross-domain checks
- ODB++ structure inspection
- schematic/PCB consistency checks
- topology analysis
- contextual heuristics
- historical risk checks
- result normalization
- issue/evidence generation

Pattern:

```text
ODB++ / Schematic
        ↓
Parser / Normalizer
        ↓
Deterministic checks
        ↓
Engineering finding
        ↓
Evidence + History
```

### 10.3 ODB++ validation

Candidate checks include:

```text
layer / stackup consistency
net connectivity
design-rule measurements
via / return-path characteristics
component / pin / net relationships
trace geometry
special EMC topology patterns
```

### 10.4 Schematic ↔ PCB consistency

The system should identify mismatches such as:

```text
schematic intent
       ↕
implemented PCB topology
```

rather than treating the two artifacts as unrelated documents.

### 10.5 RE-focused checklist automation

The initial rules should be categorized by:

```text
Rule
Scope
Evidence requirement
Severity
Applicability
Exception policy
Verification method
```

A rule result must be explainable and traceable to the source geometry/net/component data.

---

## 11. CST Analysis Automation

CST is treated as an analysis execution capability, not as the center of the platform.

Candidate workflow:

```text
Engineering Hypothesis
        ↓
Experiment Definition
        ↓
CST Configuration
        ↓
Simulation Run
        ↓
Result Extraction
        ↓
Comparison / Evaluation
        ↓
History Update
```

A future agent may propose or select experiments, but the system must preserve:

```text
why the simulation was run
what configuration was used
what changed
what result was observed
what conclusion was drawn
```

Simulation and measurement must be representable separately and correlated explicitly.

---

## 12. EMC Expert System

The EMC expert capability is a candidate hybrid of:

```text
Deterministic Rules
+
Internal Engineering History
+
External Domain Knowledge
+
Agent Reasoning
+
Human Review
```

### Internal knowledge

```text
past projects
past issues
validated countermeasures
failed attempts
engineering decisions
measurement results
```

### External knowledge

```text
standards
application notes
datasheets
technical papers
vendor guidance
other approved references
```

Internal and external knowledge must remain source-distinguishable.

The system should answer not only:

> "What does the knowledge base say?"

but, where evidence permits:

> "Which previous engineering cases support this recommendation, and what happened when the recommendation was applied?"

---

## 13. Email / Communication RAG

Email is treated as a potentially valuable engineering source, but not as authoritative by default.

Candidate extraction:

```text
Email
 ↓
Project / product identification
 ↓
Issue / decision / action extraction
 ↓
Candidate relations
 ↓
Human confirmation for consequential facts
```

Examples of useful extracted information:

```text
customer requirement
exception approval
test-house feedback
countermeasure result
design change request
engineering decision rationale
```

Original communication must remain retrievable for provenance.

---

## 14. Agent / Workflow Architecture

No single runtime is mandated.

Potential runtime compositions include:

```text
Deterministic workflow
LangGraph-style stateful orchestration
OpenHands-style tool-using agent
MCP-based tool integration
Custom orchestration
Hybrid combinations
```

The framework is selected per workload based on measurable fitness.

### Recommended separation

```text
Rule Engine
    = deterministic judgement

Analyzer
    = computation / transformation

RAG
    = retrieval

Agent
    = reasoning / planning / orchestration

Human
    = consequential engineering judgement
```

This separation is an architectural principle under test, not a frozen implementation contract.

---

## 15. Human-in-the-Loop Boundaries

Human approval is mandatory for consequential actions such as:

- final root-cause acceptance
- design changes with material impact
- release decisions
- rule exceptions
- production-impacting actions
- access to sensitive engineering data
- adoption of consequential AI recommendations

The system should optimize for:

```text
Automatic capture
→ AI proposal
→ Human confirmation
```

not:

```text
Manual graph construction
```

---

## 16. Product Workflows

### Workflow A — Design validation

```text
Design Revision
 ↓
HyperLynx DRC
 ↓
Python checks
 ↓
Schematic/PCB consistency
 ↓
Findings
 ↓
Issue generation
 ↓
Engineering History
```

### Workflow B — EMC problem investigation

```text
Measurement FAIL
 ↓
Context assembly
 ↓
Historical case retrieval
 ↓
Expert knowledge retrieval
 ↓
Hypothesis candidates
 ↓
Human selection
 ↓
Experiment
 ↓
CST / Measurement
 ↓
Result
 ↓
Verification
 ↓
Closure
```

### Workflow C — Engineering report

```text
Evidence
 ↓
Issue / Decision / Experiment chain
 ↓
Grounded synthesis
 ↓
Draft report
 ↓
Human review
 ↓
Approved report
```

### Workflow D — Project memory

```text
Project completion
 ↓
Validated decisions
 ↓
Successful countermeasures
 ↓
Failed approaches
 ↓
Lessons
 ↓
Reusable patterns
```

---

## 17. Minimum Viable Product

MVP must test the core value proposition, not build the final platform.

### MVP-1 — Validation + History

```text
Project
Design Revision
ODB++
Schematic
HyperLynx result
Python validation
Issue
Evidence
Timeline / History
```

Success question:

> Does integrated evidence/history reduce validation and issue-triage effort compared with the current workflow?

### MVP-2 — Historical EMC Recall

```text
MVP-1
+
Historical case retrieval
+
EMC knowledge retrieval
+
Grounded recommendation
```

Success question:

> Can an engineer recover relevant prior engineering reasoning faster and with acceptable accuracy?

### MVP-3 — Simulation Loop

```text
MVP-2
+
CST execution
+
experiment recording
+
result extraction
```

Success question:

> Can the system remove meaningful preparation / analysis / recording work while preserving engineer control?

### MVP-4 — Unified Engineering Context

```text
Project
+ History
+ ODB/Schematic
+ CST
+ Measurement
+ EMC knowledge
+ Email
```

Success question:

> Does the combined context enable materially better engineering work than isolated tools?

---

## 18. Architecture Hypotheses

### H1 — Conventional Engineering Application

```text
Relational project DB
+ deterministic tools
+ document links
```

Purpose: baseline.

### H2 — Engineering History Model

```text
H1
+
explicit event/evidence/decision relationships
+
temporal/provenance-aware history
```

Purpose: test whether structured engineering history itself creates measurable value.

### H3 — History + Agent

```text
H2
+
retrieval
+
reasoning
+
workflow orchestration
+
human checkpoints
```

Purpose: test whether agentic capabilities create additional value over H2.

### H4 — Autonomous experiment loop

```text
H3
+
next-best-experiment selection
+
tool execution
+
iterative evaluation
```

Purpose: later-stage test only; not part of MVP commitment.

---

## 19. Architecture Fitness

Fitness must measure engineering outcomes, not framework preference.

### Work reduction

```text
search time
context reconstruction time
validation time
experiment preparation time
report preparation time
manual record-keeping time
```

### Engineering quality

```text
finding precision / recall
historical-case recall
root-cause reconstruction accuracy
evidence grounding
verification completeness
```

### Trust / safety

```text
unsupported-claim rate
false relationship rate
false causal inference rate
human correction rate
permission violations
```

### System economics

```text
latency
LLM cost
simulation cost
maintenance effort
rule maintenance effort
data-ingestion effort
```

### Adoption

```text
engineer interaction burden
repeat usage
workflow interruption
user override rate
```

The primary product metric is **engineering work reduced without unacceptable loss of correctness or accountability**.

---

## 20. Falsification Criteria

The Engineering History Graph hypothesis should be considered weakened or rejected if controlled experiments show that:

1. engineers do not retrieve relevant prior reasoning materially faster;
2. relationship modeling adds more capture/maintenance burden than it removes;
3. a conventional relational/document architecture performs equivalently for target use cases;
4. graph-derived recommendations do not improve engineering outcomes over baseline retrieval;
5. provenance complexity makes the system unusable in practice;
6. the resulting automation does not reduce measurable engineering effort.

A visually impressive graph is not evidence of product value.

---

## 21. Key Design Principles

1. **Real work before abstraction.**
2. **Evidence before architecture commitment.**
3. **Relationship before visualization.**
4. **Human judgment remains authoritative for consequential engineering decisions.**
5. **Deterministic checks before LLM judgement where deterministic checks are possible.**
6. **Automatic capture over manual documentation.**
7. **Failed attempts are first-class knowledge.**
8. **Revision/configuration context is mandatory for consequential results.**
9. **Internal history and external knowledge remain distinguishable.**
10. **Tools are capabilities; they are not the domain model.**
11. **Frameworks are replaceable implementation candidates until fitness evidence establishes otherwise.**
12. **Every major automation capability must have measurable work-reduction and quality criteria.**

---

## 22. Expected Long-Term Capability

The target end state is not merely an engineering historian.

It is a closed-loop engineering augmentation system:

```text
Engineer Work
    ↓
Automatic Context Capture
    ↓
Engineering History
    ↓
Relevant Knowledge / History Recall
    ↓
Recommendation / Planning
    ↓
Human Decision
    ↓
Tool Execution
    ↓
Evidence
    ↓
Verification
    ↓
History Update
    ↓
Improved Future Assistance
```

This creates a learning loop in which each completed project increases the usefulness of future engineering assistance.

---

## 23. Current Architecture Status

The following are **candidate concepts**, not frozen platform contracts:

```text
Engineering History Graph
Engineering Event
Evidence as first-class concept
Temporal / provenance-aware relationships
Hybrid Rule + Analyzer + RAG + Agent architecture
Human-confirmed relationship extraction
EMC engineering augmentation workflow
```

The following are **implementation candidates only**:

```text
LangGraph
OpenHands
MCP
Neo4j / graph database
PostgreSQL
Vector database
Specific LLM provider
Specific simulation automation mechanism
```

Any candidate can be replaced when evidence demonstrates a better fitness profile.

---

## 24. First Engineering Experiment

The first controlled experiment should use a real historical EMC/PCB problem and compare:

```text
H1: conventional project records
H2: Engineering History model
H3: Engineering History + Agent
```

The experiment should measure:

```text
context reconstruction time
historical case retrieval quality
engineering recommendation quality
manual effort
verification traceability
human correction rate
```

The output is not merely a product feature decision. It becomes APF evidence for or against the underlying architecture assets.

---

## 25. Relationship to APF

This project is an APF experimental workload.

Its purpose is to exercise the APF loop:

```text
REAL WORK
  ↓
ARCHITECTURE HYPOTHESIS
  ↓
PROFILE
  ↓
ARCHITECTURE COMPOSITION
  ↓
ACTUAL TOOL / AGENT
  ↓
EXECUTION
  ↓
ARCHITECTURE FITNESS
  ↓
EVIDENCE
  ↓
ASSET REVISION
```

Therefore this specification must evolve through evidence rather than become a premature final architecture contract.

---

## 26. Initial Research / Evidence Inputs

The product concept was informed by validated patterns from:

- modern project/issue management systems
- Architectural Decision Records
- software engineering knowledge management research
- lessons-learned retrieval research
- software traceability research
- engineering / maintenance knowledge graph research
- existing engineering notebook patterns

These sources justify investigation of the model, but do **not** by themselves establish that this specific integrated product is valuable. Product value remains an empirical APF hypothesis.
