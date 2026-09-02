# DEC-0002 — Claim Record Completion Timing

## Minimum Decision Record

```yaml
id: DEC-0002
title: Claim records are completed individually at benchmark preparation time
status: DECIDED
date: 2026-09-02
context: >
  docs/research/CLAIM_INVENTORY.md defines a required claim record with 24
  fields and a quality gate that a claim must pass to be TESTABLE. Ten claims
  (CLM-0001..CLM-0010) are formulated as narrative candidates; none has a
  completed record in that form. Four unverified P0 claims remain queued
  (BENCH-0002, BENCH-0007, BENCH-0009, BENCH-0001).
problem: >
  When are claim records completed — as a batch before further benchmark work,
  as a reconciliation pass after execution, or individually as each benchmark
  is prepared? The choice determines whether falsifiers are written before or
  after results are seen.
evidence:
  - REPOSITORY_EVIDENCE: docs/research/CLAIM_INVENTORY.md sections 4 and 5 — required record and TESTABLE quality gate
  - REPOSITORY_EVIDENCE: docs/research/P0_FALSIFICATION_BENCHMARK_MATRIX.md rule B3 — predeclared falsifiers
  - EVALUATION_EVIDENCE: docs/research/executions/BENCH-0004_R2_2026-08-31.md — execution forced CLM-0004 to split into a broad claim and a narrower surviving subclaim
  - REPOSITORY_EVIDENCE: docs/research/CLAIM_COLD_REVIEW.md — CLM-0006, CLM-0007, CLM-0009 required rewording before testing
contradictions:
  - Completing records lazily risks leaving never-benchmarked claims permanently incomplete; this is accepted and handled by marking them INSUFFICIENT rather than blank.
  - Per-benchmark completion produces records written at different times against evolving understanding, so record quality is less uniform than a single batch pass would give.
alternatives:
  - "A: Batch up front — complete all claim records (or all six P0 records) before executing any further benchmark. Rejected: front-loads precision onto claims that execution then rescopes. BENCH-0004 already split CLM-0004 after the run; records written before that would have had to be rewritten."
  - "B: Execute first, reconcile records afterwards in one pass. Rejected: benchmark preparation is exactly where the falsifier and scope must be pinned. Writing the record after the run means the falsifier is authored with the result already visible, violating benchmark design rule B3."
  - "C: Complete each claim record individually at the point its benchmark is prepared. Selected."
risks:
  - Claims never queued for a benchmark (CLM-0003, CLM-0005, CLM-0008, CLM-0010) keep incomplete records indefinitely.
  - Record quality varies across claims completed at different times.
  - Discipline is required not to start a run before its record is finished; nothing enforces the ordering mechanically.
recommendation: >
  Adopt option C, with record completion as a hard precondition step inside the
  benchmark preparation checklist rather than a separate later cleanup pass.
human_decision: >
  ACCEPTED. Option C. Preparing a benchmark is the trigger for completing the
  corresponding claim record.
impact: >
  No batch claim-record pass is scheduled. Each queued benchmark carries the
  cost of completing its own claim record first. Non-benchmarked claims stay
  explicitly incomplete and are marked INSUFFICIENT rather than left blank.
implementation_scope: >
  Documentation and session protocol only. No code, no tooling, no CI check.
verification_plan: >
  Before any execution record is committed, the corresponding claim record must
  already exist, pass the CLAIM_INVENTORY section 5 quality gate, and carry a
  falsifier authored before the run. A session audit that finds an execution
  record without a preceding claim record treats the run as unscoped.
related_assets:
  - docs/research/CLAIM_INVENTORY.md
  - docs/research/CLAIM_COLD_REVIEW.md
  - docs/research/P0_BENCHMARK_CASES_v0.1.md
related_decisions:
  - DEC-0001
related_commits:
  - 47c8b20 research: cold review APF claims before benchmark execution
  - 9a90e46 docs: record next-session entry points and governance gate in session state
```

## 1. Decision

Claim records are not completed as a batch. Each claim record is completed individually, at the point that claim's benchmark is being prepared, and before that benchmark is executed.

## 2. Order of work for a queued benchmark

```text
select next benchmark from queue
  ↓
complete the claim record  (CLAIM_INVENTORY section 4 fields)
  ↓
verify the section 5 quality gate passes
  ↓
predeclare falsifier + baseline controls
  ↓
execute
  ↓
preserve raw result
  ↓
revise claim scope / state from the outcome
```

The record completion step is inside benchmark preparation, not adjacent to it. A benchmark whose claim record is not finished is not ready to run.

## 3. Why not batch up front

The claim inventory's required record asks for `scope`, `non_scope`, `observable_prediction`, `falsifier`, and `minimum_evidence`. Those fields are cheap to write badly and expensive to write well, and execution changes them.

BENCH-0004 is the worked example. Before execution, CLM-0004 was one claim about temporal/provenance-aware retrieval. Round 1 falsified the document-level recall proposition. Round 2 supported a narrower cross-document chain proposition while leaving the broad claim WEAKENED / INCONCLUSIVE. A record written up front would have carried one scope statement that two runs then invalidated. Ten such records written before any execution is ten opportunities to record precision the project does not have.

The cold review makes the same point from the other direction: CLM-0006, CLM-0007, and CLM-0009 needed rewording before they were testable at all, and that rewording came from examining them one at a time against what a test could actually measure.

## 4. Why not defer to after execution

Option B is the more dangerous failure. Benchmark design rule B3 requires the falsifier to be written before the result is seen. If claim records are completed in a reconciliation pass after runs, the `falsifier` field gets authored by someone who already knows the outcome. The record would then look complete and be worthless as a falsification instrument — the specific failure this project's whole benchmark layer exists to avoid.

Option C keeps the falsifier upstream of the result by construction.

## 5. Accepted cost

Claims with no queued benchmark keep incomplete records. As of this decision that is CLM-0003, CLM-0005, CLM-0008, and CLM-0010, none of which are P0.

This is accepted, on one condition: those claims are marked `INSUFFICIENT` per the corpus map stop condition rather than left silently blank. An incomplete record that is labelled incomplete is a tracked gap. An incomplete record that looks unstarted is indistinguishable from an oversight.

## 6. Provenance note

Only the selection of option C is recoverable from the session handoff that carried this decision forward. The wording of options A and B above is a reconstruction of the option space from repository evidence — the claim inventory's record requirements, benchmark rule B3, and the BENCH-0004 outcome — not a verbatim transcript of the original deliberation. If the original A/B framing differed, the selection of C and its rationale in sections 3 and 4 still hold, since both rest on committed repository evidence rather than on the rejected options' exact wording.
