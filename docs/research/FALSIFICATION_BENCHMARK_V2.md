<!-- Track B of two parallel falsification instruments. See docs/research/CLAIM_HYPOTHESIS_MAP.md -->

**Status:** Candidate / no executed evidence
**Track:** B — architecture hypothesis level (`H01`…`H12`)
**Parallel to:** `FALSIFICATION_BENCHMARK.md` (v0.1, claim level). v0.2 does **not** supersede v0.1.
**Provenance:** Entered the repository 2026-09-01 from the 2026-09-02 BENCH-0004-E2 handoff bundle, unmodified below this header.
**Adjudication boundary:** BENCH-0004-E2 does not produce evidence for H07 or H11. See `CLAIM_HYPOTHESIS_MAP.md` §4.
**Identifier warning:** `T01`…`T12` are test IDs. They are unrelated to the `T`/`R`/`P` retrieval factor codes used in BENCH-0004-E2.

---

# APF Falsification Benchmark v0.2

## Benchmark objective
Attempt to **disprove** the APF architecture hypothesis, not demonstrate it.

A benchmark result should distinguish:
- `SURVIVED` — no predefined falsification condition observed.
- `PARTIALLY_SURVIVED` — claim holds only under explicit scope constraints.
- `FALSIFIED` — predefined failure condition observed.
- `INCONCLUSIVE` — insufficient evidence or reproducibility.

## Dataset axes
- Domains: EMC/engineering analysis, document/review automation, general business operation.
- Executors: agent runtime, deterministic script/tool, human operator; optionally a second agent/workflow engine.
- Workflow classes: one-shot, multi-step, long-running, approval-gated, tool-using, failure/restart.
- Evidence regimes: strong evidence, conflicting evidence, missing evidence, stale asset.

## Test matrix

| Test | Target claim | Experiment | Pass / survive | Falsifier |
|---|---|---|---|---|
| T01 Portable execution overhead | H01 | Compare one-shot vs multi-step through same contract | trivial task overhead stays within predefined budget and semantics remain stable | contract forces heavyweight lifecycle or meaningful latency/complexity penalty |
| T02 Executor substitution | H02 | Same work via Agent A, Agent B, script, human | semantic record identical modulo executor-specific trace fields | core schema/policy changes with executor framework |
| T03 Evidence/provenance separation | H03 | Create evidence-only, provenance-only, trace-only and combined cases | all states represented without semantic collapse; linkage preserved | model cannot represent a valid domain case without conflation |
| T04 Validation separation | H04 | Permit runtime call but make domain outcome wrong | validation independently rejects outcome | guardrail/telemetry is treated as sufficient validation |
| T05 Decision durability | H05 | Pause at approval; restart host; approve once | one attributable state transition, no duplicate effect | decision lost, duplicated or represented only in UI |
| T06 Domain substitution | H06 | Run 3 materially different domains with unchanged core | only domain declarations/adapters change | core schema/runtime must be redesigned |
| T07 Asset reuse | H07 | Run #1 → validate finding → create asset → Run #2 | asset changes planning/execution and outcome measurably | asset is just retrieved text/no operational effect |
| T08 Capability ablation | H08 | Replace/remove durable engine, telemetry backend, agent runtime one at a time | APF semantic model remains usable through adapters | APF loses its claimed meaning when an existing capability is removed |
| T09 Identity substitution | H09 | Swap user/service/agent identities and identity provider | core work semantics stable; identity boundary adapts | identity-provider object model contaminates core |
| T10 Authorization substitution | H10 | Evaluate equivalent policy with ReBAC and policy engine | authorization decision can be represented through stable boundary | core semantics require one authorization model/vendor |
| T11 Asset invalidation | H11 | Inject counterexample/context change after asset promotion | asset becomes revised/deprecated and stale reuse is blocked or qualified | stale asset remains indistinguishable from valid asset |
| T12 Living-spec integrity | H12 | Intentionally falsify a hypothesis and revise spec | traceable asset→claim→test→decision→revision chain remains intact | normative spec cannot absorb falsification without losing provenance/traceability |

## Quantitative scorecard

### Required metrics
- Semantic preservation rate across executor substitutions.
- Core-schema mutation count per domain.
- Duplicate side-effect rate after restart/resume.
- Decision attribution completeness.
- Claim→evidence linkage completeness.
- Validation false-accept rate on intentionally wrong outcomes.
- Asset reuse lift: difference in success/latency/error rate with vs without asset.
- Stale-asset escape rate.
- APF-specific code/contract added when swapping mature capability.
- Reproduction rate across independent runs.

### Suggested initial gates
These are **benchmark defaults**, not architecture invariants:
- ≥95% semantic record preservation in executor substitution.
- 0 unintended duplicate irreversible side effects in the durability test.
- 100% of benchmark claims linked to explicit evidence or marked unsupported.
- 100% stale-asset cases either blocked, downgraded, or escalated according to policy.
- ≤1 core-runtime semantic change across three domains; domain-specific logic should remain outside the core.
- Asset reuse must show a predefined non-trivial effect size on at least one outcome metric in two domains before H07 is considered `SURVIVED`.

Thresholds must be calibrated after the first dry run; changing thresholds after seeing results requires a decision record.

## Critical anti-bias rules
1. Do not use only the optimization/golden set to score the architecture.
2. Reserve hidden cases for stale assets, contradictory evidence, executor replacement and adversarial boundary conditions.
3. Do not redesign the benchmark after a failure unless the change itself is recorded and justified.
4. Do not count implementation convenience as architectural validity.
5. A capability being mature externally is evidence **against reimplementation**, not evidence that APF needs no contract around it.

## Promotion logic
- H07/H11 require survival in at least two domains before strategic promotion.
- H02/H06/H08 require cross-executor evidence.
- H03/H04/H05 require at least one intentionally adversarial case each.
- Any falsified high-level claim triggers review of dependent claims/assets before implementation contracts are changed.
