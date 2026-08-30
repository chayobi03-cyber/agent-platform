# APF — Next Session Prompt: Engineering Work UX / Capture-first MVP

## Session Purpose

Continue the APF Engineering Work Augmentation experimental workload.

This session must focus on **user friction, desktop/Web UX, and falsifiable MVP design**, not on expanding the technology stack.

Current product thesis:

> Build an Engineering Workspace that lets engineers capture work with near-zero ceremony and retrieve the right context when needed; progressively add structured history, expert retrieval, deterministic validation, simulation automation, and agents only when each step demonstrates measurable engineering-work reduction.

## Current Decisions / Constraints

- Desktop/Web is the first priority.
- Mobile is deferred. Later mobile interaction may be exposed through a messaging/chatbot interface over shared APIs.
- HyperLynx DRC is an existing first-line baseline. Do not rebuild adequate commercial functionality unnecessarily.
- Python is the planned extension layer for organization-specific and cross-domain engineering validation.
- Engineering History Graph remains a candidate semantic model, not a mandated graph database or UI.
- No framework/runtime is approved as an APF contract. LangGraph, OpenHands, MCP, graph DBs, vector DBs, etc. remain candidates.
- Human accountability remains mandatory for consequential engineering decisions.

## Session Goals

### 1. Design the Capture-first UX

Produce a concrete desktop/Web interaction model for:

```text
Capture
Search / Ask
Current Work
Detail
History
Evidence
```

The core interaction should feel like:

```text
Drop / Paste / Type / Attach
→ done
```

Do not require the user to classify an item before capture.

### 2. Design progressive disclosure

Default view should be low-density and task-oriented.

Required information depth:

```text
Level 1: concise answer / summary
Level 2: context and related work
Level 3: reasoning / history / evidence
Level 4: raw artifact / source
```

The user must be able to intentionally drill down without being forced to see all information initially.

### 3. Design one unified retrieval surface

Define how a user can enter queries such as:

- "지난번 240MHz 문제 어떻게 해결했지?"
- "이 프로젝트에서 아직 안 닫힌 문제"
- "왜 이 설계 변경을 했지?"
- "이 결과의 근거 보여줘"

The UI should hide lexical/semantic/relationship retrieval complexity.

### 4. Define the minimum semantic model

Do not freeze a full graph schema.

Determine the smallest useful set of concepts needed for the MVP, likely around:

```text
Project
Work Item / Event
Artifact / Evidence
Decision
Experiment
Result
Relation
Time / Revision / Source
```

Explicitly test whether all proposed entities are necessary.

### 5. Define the first experiment

Compare at minimum:

```text
H0: ordinary project notes / flat records
H1: low-friction capture + structured history
H2: H1 + relationship-aware retrieval
```

Define measurable metrics around:

- capture completion time
- manual fields required
- capture abandonment
- context reconstruction time
- historical search time
- answer accuracy
- evidence grounding
- repeated-work / repeated-investigation rate
- user-perceived interruption / burden

Do not assume improvement percentages before measurement.

### 6. Dogfood with APF itself

Use the APF project as the first practical dataset where feasible.

Capture:

```text
research findings
architecture hypotheses
decisions
implementation attempts
failed approaches
session lessons
next actions
```

The product should be capable of recording its own engineering history.

## Required Review Questions

1. Is Capture actually faster than writing a normal note?
2. Can the system infer project/context reliably enough without mandatory user classification?
3. What minimum metadata must be explicit rather than inferred?
4. When should the UI interrupt the user for confirmation?
5. Can a user get to a useful answer in one interaction?
6. Can the user reliably drill down to evidence without drowning in data?
7. Is the Engineering History model providing measurable value, or only structural elegance?
8. Which part of the workflow should be automated next based on observed burden?

## Explicitly Avoid

- mobile-first design
- graph visualization as an MVP goal
- large project-management dashboards
- mandatory form-heavy capture
- premature Neo4j / graph database commitment
- monolithic EMC super-agent
- technology selection before workload evidence

## Expected Deliverables

1. Desktop/Web UX specification.
2. Capture interaction flow.
3. Search / Ask interaction flow.
4. Progressive-disclosure information architecture.
5. Minimal semantic model proposal.
6. Falsifiable H0/H1/H2 experiment protocol.
7. MVP implementation slice recommendation.
8. Updated APF research assets / decision candidates, clearly separated by state:

```text
Finding ≠ Candidate Asset ≠ Accepted Asset ≠ Decision ≠ Implementation
```

## Governing Principle

The session succeeds only if it increases the probability that the resulting product will **reduce engineering work rather than create another documentation burden**.
