# BENCH-0001 — Work Abstraction Coverage

**Date:** 2026-09-02
**Status:** Executed / preregistered result
**Claim under test:** CLM-0001 — work-centric abstraction is more general than agent-centric
**Corpus:** CORPUS-0002 — 16 third-party workflows, four ecosystems
**Pre-registration:** commit `e3dd94c`, containing the falsifiers, both schemas, and the binding table, and no results

## 1. Result

Mean concept coverage per workflow — the fraction of a workflow's source-declared concepts that a core schema binds without importing a runtime-specific concept.

| | A agent-centric | B work-centric | delta |
|---|---:|---:|---:|
| **Overall (n=16)** | 0.6761 | **0.8184** | **+0.1422** |
| Boundary violations per workflow | 2.06 | **1.06** | −1.00 |

Per class:

| Class | n | A | B | delta |
|---|--:|---:|---:|---:|
| C1 deterministic | 2 | 0.500 | 0.944 | +0.444 |
| C4 scheduled | 2 | 0.607 | 1.000 | +0.393 |
| C6 validation | 3 | 0.597 | 0.880 | +0.282 |
| C5 external orchestration | 2 | 0.583 | 0.750 | +0.167 |
| C3 human-in-the-loop | 3 | 0.682 | 0.803 | +0.121 |
| **C2 agentic** | **4** | **0.900** | **0.664** | **−0.236** |

## 2. Falsifier assessment

**F1 — B does not exceed A.** B 0.8184 vs A 0.6761. **Not met.**

**F2 — B escapes the core on more than one third of concepts.** B's escape rate is 0.1816. **Not met.**

**F3 — both above 0.95, no discrimination.** 0.676 and 0.818. **Not met.**

**F4 — B's agentic-class coverage is below A's by more than 0.10.** B 0.664 vs A 0.900, a gap of **−0.236**, more than double the threshold. **MET. The falsifier fired.**

**CLM-0001 is CONTRADICTED as worded.**

### Robustness of F4

W16 contributes only two extracted concepts, so it could be argued the extractor barely saw it and is distorting a four-workflow average. Excluding it:

| agentic class, n=3 | A | B | delta |
|---|---:|---:|---:|
| excluding W16 | 0.8667 | 0.7190 | −0.1476 |

Still past the −0.10 threshold. F4 fires either way, so the verdict does not depend on the weakest workflow in the class.

## 3. What actually failed

The work-centric core escapes on these concepts in the agentic class:

| Concept | workflows affected | Why B has no slot |
|---|--:|---|
| `STATE_SCHEMA` | 3 of 4 | The Constitution's chain names lifecycle stages, not in-flight typed state |
| `EVENT_SIGNAL` | 2 of 4 | No core slot for asynchronous inbound messages during execution |
| `PROMPT_CONTENT` | 1 of 4 | No core slot for instruction content as a first-class object |
| `TIMEOUT` | 1 of 4 | Escapes both cores |

The agent-centric core escapes on only `HUMAN_APPROVAL` and `TIMEOUT` in this class — one workflow each.

The gap is specific and nameable: **`Work → Opportunity → Automation Decision → Engineering → Control → Execution → Evidence → Evaluation → Outcome` has no slot for the state a running execution carries, nor for the messages it exchanges while running.** It describes the lifecycle around an execution and is silent on what an execution holds while it is in flight. For deterministic, scheduled, and validation workloads that silence costs nothing, because their in-flight state is trivial. For agentic workloads it is most of the workload.

## 4. What this does and does not overturn

**Does not:** B wins overall by +0.142 and wins on five of six classes, on some by a wide margin. Nothing here says APF should become an agent framework, and the agent-centric core's own escape rate is worse overall — 2.06 boundary violations per workflow against 1.06.

**Does:** the word **both** in CLM-0001, and with it the generality claim in `CONSTITUTION.md` section 2. A work-centric core that cannot hold agentic workloads without importing state and messaging concepts is a good general abstraction *with a named exception*, not an abstraction that spans both without importing agent-runtime concepts. That is a different and weaker claim than the one the Constitution currently makes.

## 5. Candidate implication — not a recommendation, not a decision

The finding points at a specific gap rather than a general failure, which suggests the claim is repairable rather than dead: a core that added an in-flight execution-state concept and an inbound-signal concept would, on this corpus, close most of the agentic gap while keeping B's advantage elsewhere.

Whether to do that is an architecture question and belongs to a human under DEC-0001. This record does not propose an amendment to the Constitution, and none should be inferred from it.

## 6. Limitations

1. **The binding table is authored by the benchmark author.** Stated in CLM-0001 before the run and not resolved by the result. That the falsifier fired against the author's own platform is weak evidence against bias in one direction; it is not evidence of neutrality.
2. **Small classes.** Two workflows in three of six classes. The per-class deltas are directional, not estimates.
3. **Concept extraction is bounded by a hand-written surface-form map.** Concepts it does not name are invisible to both conditions.
4. **Code and configuration, not engineering work.** Nothing here transfers to the EMC/PCB target domain.
5. **Coverage is not usability.** A schema can bind every concept and still be miserable to work with. `non_scope` excluded ergonomics, migration cost, and implementation complexity, and this run measured none of them.
6. **No second annotator.** The preferred evidence in CLM-0001 was independent re-binding. It was not available.

## 7. Effect on claim states

- **CLM-0001:** `TESTABLE` → **`CONTRADICTED`** as worded, on CORPUS-0002. The generality-across-both-classes claim is not supported. A narrower claim — work-centric is more general across non-agentic automation strategies, and requires additional state and messaging concepts for agentic ones — is consistent with this result but has not itself been tested and must not be recorded as supported.
- **CONSTITUTION.md section 2:** now has a recorded contradiction against it. It is not amended here; that is a human decision under DEC-0001, and the Constitution's own section 9 requires explicit review for changes to its invariants.

## 8. Required next attack

1. An independent second annotator re-binds the 26 concepts blind to this result. If the agentic gap survives an annotator with no stake in APF, the finding stands; if it does not, the finding was the author's judgment.
2. Test the repaired claim rather than asserting it: add the two candidate concepts to schema B and re-run, on a corpus fixed before the repair was designed.
3. Widen the corpus classes that have only two workflows.

## 9. Verdict

**The falsifier this benchmark existed for fired, against the platform's founding assumption, on the first run.**

CLM-0001's overall direction held and its generality claim did not. The Constitution's work-centric boundary is supported for five workload classes and contradicted for the sixth, and the sixth is the one the platform is most often asked about. The failure is specific enough to name — no core slot for in-flight execution state or inbound signals — which makes it a repair target rather than a refutation of the work-centric framing.
