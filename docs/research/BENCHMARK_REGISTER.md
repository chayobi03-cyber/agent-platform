# APF Benchmark Register v1.0

**Status:** Canonical register
**Supersedes:** `P0_FALSIFICATION_BENCHMARK_MATRIX.md`, `P0_BENCHMARK_CASES_v0.1.md`, and the benchmark matrix and execution order formerly in `FALSIFICATION_BENCHMARK.md` §5 and §12
**Decision record:** `docs/decisions/DEC-0001-benchmark-id-and-doc-consolidation.md`

This is the single place that declares which benchmarks exist, what each one
tests, in what order they run, and what state each one is in. Benchmark
*method* — how to design a falsification benchmark at all — lives in
`FALSIFICATION_BENCHMARK.md`. Claim wording and claim state live in
`CLAIM_INVENTORY.md`.

## 1. Identifier scheme

Benchmarks use `BENCH-NNNN`, numbered to match the claim they test
(`BENCH-0004` tests `CLM-0004`).

The repository previously carried two identifier systems for the same
benchmarks. `FB-NNNN` is retired.

| Retired | Canonical | Claim |
|---|---|---|
| FB-0001 | BENCH-0001 | CLM-0001 |
| FB-0002 | BENCH-0002 | CLM-0002 |
| FB-0003 | BENCH-0003 | CLM-0003 |
| FB-0004 | BENCH-0004 | CLM-0004 |
| FB-0005 | BENCH-0005 | CLM-0005 |
| FB-0006 | BENCH-0006 | CLM-0006 |
| FB-0007 | BENCH-0007 | CLM-0007 |
| FB-0008 | BENCH-0008 | CLM-0008 |
| FB-0009 | BENCH-0009 | CLM-0009 |
| FB-0010 | BENCH-0010 | CLM-0010 |

`BENCH-*` was chosen because every execution record on disk is already named
`BENCH-0004_*` and evidence filenames cannot be rewritten. `FB-*` appears in
this table only; any other occurrence in the repository is a defect.

## 2. Execution order

```text
1. BENCH-0004  retrieval ablation              DONE   — CLM-0004 falsified at tested scope
2. BENCH-0006  provenance ablation             NEXT
3. BENCH-0002  capture / context reconstruction
4. BENCH-0007  approval boundary
5. BENCH-0009  automation promotion threshold
6. BENCH-0001  work abstraction coverage
```

Rationale: retrieval and provenance are narrower and cheaper to falsify;
capture and control experiments depend more heavily on operator behaviour; work
abstraction is the broadest and should be tested after concrete evidence has
matured.

Two earlier orders are superseded and must not be followed:
`P0_FALSIFICATION_BENCHMARK_MATRIX` declared 0001→0002→0004→0006→0007→0009, and
`FALSIFICATION_BENCHMARK` §12 declared FB-0002→0004→0006→0009→0007. The order
above is the one `SESSION_STATE` already follows and under which BENCH-0004 was
actually executed.

## 3. Register

| ID | Claim | Core question | Baseline | Candidate | Primary metric | Falsifier | Priority | State |
|---|---|---|---|---|---|---|---|---|
| BENCH-0001 | CLM-0001 | Is Work a more stable organising abstraction than Agent/Framework? | agent/tool-centric task record | work-centric record linking opportunity, strategy, execution, outcome | task-model coverage; boundary violations; rework | work-centric model shows no measurable coverage/clarity advantage | P0 | UNTESTED |
| BENCH-0002 | CLM-0002 | Does zero-ceremony capture reduce context reconstruction effort? | manual notes + conventional project search | capture + automatic structuring + retrieval | time-to-context; omissions; user actions | no meaningful reduction, or quality regresses | P0 | UNTESTED |
| BENCH-0003 | CLM-0003 | Does progressive disclosure reduce interaction cost without hiding evidence? | evidence-dense UI | progressive disclosure | completion time; error rate; evidence lookup time | more incorrect judgments, or interaction cost not improved | P1 | UNTESTED |
| BENCH-0004 | CLM-0004 | Does relationship/time-aware retrieval improve engineering recall? | keyword + semantic retrieval | relationship + temporal + provenance retrieval | evidence-grounded recall; answer utility; false-positive rate | improvement absent or explained by better indexing alone | P0 | **FALSIFIED at tested scope** |
| BENCH-0005 | CLM-0005 | Does retaining failed attempts reduce repeated work? | current-record-only workflow | failure-aware history | repeated-issue rate; time-to-resolution | no measurable reduction, or false-history contamination dominates | P1 | UNTESTED |
| BENCH-0006 | CLM-0006 | Does provenance retention improve trust and diagnosability? | evidence without full provenance | evidence with revision/config/tool/time/actor metadata | reproduction success; diagnosis time; trust calibration | no improvement, or collection burden dominates | P0 | UNTESTED |
| BENCH-0007 | CLM-0007 | Do explicit human decision boundaries improve workflow quality? | unrestricted automation / implicit approval | boundary-specific approval gates | unsafe action rate; correction rate; latency | no safety benefit, or approval burden dominates | P0 | UNTESTED |
| BENCH-0008 | CLM-0008 | Does framework-neutral primitive extraction beat direct adoption? | framework-specific adoption | primitive extraction | migration/extension cost; semantic leakage; lock-in | direct adoption is consistently superior | P1 | UNTESTED |
| BENCH-0009 | CLM-0009 | Can net automation value be measured reliably enough to promote on? | automation chosen by intuition | thresholded evidence-based promotion | effort saved; quality delta; failure cost | net value non-positive or threshold not operationalisable | P0 | UNTESTED |
| BENCH-0010 | CLM-0010 | Which product framing yields stronger validated work reduction? | generic agent-builder thesis | engineering-work augmentation | validated workflows; effort to validate | generic framing attracts more validated high-value workflows | P1 | UNTESTED |

`UNTESTED` means no falsification attempt has been run, not that the claim is
doubted. The claim-state vocabulary is defined once, in `CLAIM_INVENTORY.md` §2.

## 4. Cases

Each case is executable against a simple baseline and assumes no APF
implementation.

### BENCH-0001 — Work abstraction coverage

**Question:** Can a work-centric representation preserve essential information
and control boundaries across heterogeneous automation workloads without
materially greater modelling complexity?

**Task population:** At least 12 representative workflows spanning deterministic
automation, agentic workflow, human-in-the-loop workflow, scheduled workflow,
external-system orchestration, and validation/checking workflow.

**Conditions:** A agent/tool-centric representation · B work-centric representation

**Measures:** essential-information coverage; unresolved concepts; boundary
violations; representation effort; rework after new workflow requirements

**Falsifier:** B shows no meaningful coverage/clarity advantage, or repeatedly
requires agent/runtime concepts at the core boundary.

**Critical control:** Neither representation may use undocumented
target-platform-specific concepts.

### BENCH-0002 — Capture / context reconstruction

**Question:** Does lower-friction capture create more retained, later-usable
engineering context at acceptable noise/correction cost?

**Task population:** Historical engineering tasks where the operator must
reconstruct prior context from available material.

**Conditions:** A manual notes + conventional project search · B zero-ceremony
capture + automatic structuring + retrieval

**Measures:** capture completion rate; time-to-context; omission rate;
correction actions; irrelevant/noisy records; successful reuse rate

**Guardrail:** correctness of the reconstructed context.

**Falsifier:** No meaningful reduction in reconstruction effort, or added
noise/correction outweighs the retention benefit.

### BENCH-0004 — Retrieval ablation

**Question:** Is any retrieval improvement attributable specifically to
temporal/relationship/provenance reasoning rather than better indexing or
metadata?

**Conditions:** A lexical/keyword · B semantic · C semantic + metadata filters ·
D relationship + temporal + provenance aware

**Measures:** evidence-grounded recall; relevant-case precision; false-positive
rate; unsupported-claim rate; answer utility; retrieval latency

**Required ablation:** Compare C vs D on the same corpus and metadata availability.

**Falsifier:** D does not outperform C, or the improvement disappears after
controlling for indexing/metadata quality.

**Executions:**

| Round | Design | Result |
|---|---|---|
| R1 `executions/BENCH-0004_RUN_2026-08-31.md` | document-level recall, 4-doc corpus | no gain |
| R2 `executions/BENCH-0004_R2_2026-08-31.md` | cross-document chains, 7-doc corpus, hand-specified graph | +0.208 coverage@2 — **superseded** |
| R3 `executions/BENCH-0004_R3_2026-09-02.md` | mechanism decomposition, 21-doc corpus, derived graph, null models | **−0.135 coverage@3**; broad claim falsified |

Predeclaration: `executions/BENCH-0004_R3_PREDECLARATION.md`.
Harness: `tools/bench/bench0004_r3.py`. Raw results: `executions/raw/`.

Unmeasured after three rounds: unsupported-claim rate, answer utility, and
answer-level grounding. A benchmark that has never measured its own declared
primary metrics cannot settle its claim.

### BENCH-0006 — Provenance ablation

**Question:** Does relevant provenance reduce reproduction/diagnosis time or
error for engineering evidence reuse?

**Conditions:** A evidence record without relevant provenance · B same evidence
plus revision/configuration/tool/setup/time/actor metadata as applicable

**Measures:** successful reproduction rate; diagnosis time; wrong-reuse rate;
expert confidence calibration; metadata capture/review burden

**Falsifier:** No material reduction in reproduction/diagnosis error or time, or
burden dominates the benefit.

**Important:** Do not claim universal necessity from a positive result.

**Scope note:** This tests provenance for *evidence reuse and reproduction*. It
is a different claim from CLM-0004b, provenance for *retrieval ranking*, which
BENCH-0004 R3 found unsupported. That result says nothing about this one.

### BENCH-0007 — Approval boundary experiment

**Question:** Does explicit human approval at consequential boundaries improve
safety/quality relative to no gate or poorly placed approval?

**Conditions:** A no approval gate · B late/general approval · C
boundary-specific approval at permission/policy/release/business-acceptance events

**Measures:** harmful/unacceptable action rate; prevented harmful action rate;
false approval rate; correction/reversal rate; approval latency; escalation load

**Falsifier:** C provides no meaningful risk reduction over the best
alternative, or approval cost dominates without compensating risk reduction.

**Critical control:** Keep underlying agent capability constant across
conditions. Otherwise a safety gain is confounded with simply reducing autonomy.

### BENCH-0009 — Automation promotion threshold

**Question:** Can net value of an automation candidate be measured reliably
enough to support a promotion decision?

**Conditions:** baseline/manual workflow · augmented/automated workflow

**Measures:** engineer effort saved; rework cost; correctness delta; evidence
completeness; failure/recovery cost; escalation cost; net value estimate

**Falsifier:** Net benefit is not reproducible, or positive time savings require
unacceptable quality/trust degradation.

**Governance separation:** The experiment estimates evidence for promotion. The
decision to *require* a threshold is a separate human policy decision.

Cases for BENCH-0003, BENCH-0005, BENCH-0008 and BENCH-0010 are not yet
operationalised. Their register rows above state the intended comparison.

## 5. Cross-case execution rules

1. Declare falsifiers before observing results.
2. Freeze task populations before comparing conditions.
3. Record negative and null results.
4. Preserve raw evidence for every benchmark result.
5. Do not change claim scope to rescue a failed result without recording the
   original claim and the reason for splitting or weakening it.
6. Replicate successful findings on at least one independent task set before
   architectural promotion.

Execution records under `executions/` are append-only evidence. Correct a
superseded conclusion by recording the supersession, never by editing the
original record.

## 6. Corpus caveat for future rounds

Every BENCH-0004 round so far used APF's own governance corpus as its dataset.
The Round 3 finding — hub amplification, where the best-connected documents are
indexes rather than answers — is a property of that corpus's topology.

The document consolidation recorded in DEC-0001 **changes that topology**:
merging four overlapping documents into two removes cross-references that were
themselves hub edges. Recorded R3 results are unaffected, because the harness
reads its corpus from the frozen commit `0d27769`. But any future round run
against the current corpus is measuring a **different corpus** and is not
directly comparable to R1–R3.

A future round must either pin the same frozen commit or declare a new frozen
corpus and treat prior rounds as historical baselines only.
