# Ambient Intelligence Engineering & Application — Research and PoC Plan v1.0

**Status:** ASSET_CANDIDATE / RESEARCH_ONLY  
**Prepared:** 2026-10-18  
**Scope:** Agentic Engineering  
**Decision status:** No architecture decision or implementation authorization is implied by this document.

## 1. Executive summary

GitHub's “The next developer interface is ambient intelligence” proposes shifting developer interaction from issuing commands to expressing intent, while AI agents plan and act within boundaries the developer controls. It describes three layers: modality, harness, and control plane.

Recommendation: evaluate Ambient Intelligence as an external research asset, not as an APF platform rule. The first practical experiment should be a small, auditable intent-to-evidence workflow around an existing synthetic AgentFactory demo. Do not introduce a new agent framework, physical keypad, voice input, broad MCP access, or autonomous production writes in the first PoC.

The first experiment should prove that a task request can be converted into a bounded plan, produce a traceable artifact and test evidence, and stop for human review at a defined gate. It should compare end-to-end human effort and result quality against the current manual workflow.

## 2. Source and evidence register

### 2.1 Primary external source

- GitHub Blog, Martin Woodward, “The next developer interface is ambient intelligence,” published 2026-10-15.
- URL: https://github.blog/news-insights/company-news/the-next-developer-interface-is-ambient-intelligence/
- Source class: EXTERNAL_EVIDENCE.
- Scope of review: article text retrieved and reviewed on 2026-10-18.

### 2.2 Source-backed findings

| ID | Finding | Evidence class | Confidence / limitation |
|---|---|---|---|
| AI-01 | The intended shift is from commands to expressing intent and having agents act within developer-controlled boundaries. | SOURCE_FACT | High; statement of the article's thesis, not proof of productivity gains. |
| AI-02 | The proposed interface has three layers: modality, harness, control plane. | SOURCE_FACT | High; terminology is from GitHub's article. |
| AI-03 | MCP connects agents to tools/services; repository instructions and skills provide context; hooks can enforce policy and validate output. | SOURCE_FACT | High; implementation details depend on the selected runtime. |
| AI-04 | Developer accountability remains even when mechanical work is delegated. | SOURCE_FACT | High; governance principle, not a measured benchmark. |
| AI-05 | Physical controls are an experiment for repeated actions, not a universal requirement. | SOURCE_FACT | High; article explicitly says not every developer needs another device. |
| AI-06 | The article raises open engineering questions around context retention, tool-call autonomy, credentials, network access, evidence, and multi-agent coordination. | SOURCE_FACT | High; these are acknowledged questions, not solved by the concept itself. |

### 2.3 Repository evidence reviewed

**APF — `chayobi03-cyber/agent-platform`**
- `README.md`: work-centric automation loop; Research ≠ Asset ≠ Decision ≠ Implementation; human accountability invariant.
- `CONSTITUTION.md`: consequential architecture, permission, release, and policy decisions require human ownership; evidence precedes architecture.
- `docs/governance/MASTER_SESSION_PROMPT.md`: recommendation is not a decision; architecture changes require evidence, alternatives, risk analysis, and a decision record.
- `docs/architecture/README.md`: platform contracts remain candidate/proposal state until evidence and explicit human decision.
- `docs/research/ASSET_LEDGER.md`: research findings progress through RAW_FINDING → ASSET_CANDIDATE → REVIEWED → ACCEPTED_ASSET.

**AgentFactory — `chayobi03-cyber/agent-factory`**
- `README.md`: domain-agnostic agent factory for evidence-grounded workflows, HOTL, benchmarking, and continuous optimization.
- `docs/FACTORY_HOTL_DEMO.md`: existing synthetic PASS / REVIEW / BLOCK paths and human-decision semantics.
- `scripts/factory_demo.py`: current demo uses synthetic evidence and claims; it is not a real engineering-domain integration.
- `docs/governance/CER_ARCHITECTURE_CONTRACT_V1.md`: defines evidence, verification, immutable run snapshots, fail-closed BLOCK, workflow state, and learning-loop contracts.

These repository findings establish that there are relevant existing concepts and a synthetic demonstration to investigate. They do **not** establish that the demo has been executed in this session, that a production runtime exists, or that the target workflow is ready for deployment.

## 3. Interpretation and design boundary

Ambient Intelligence is treated as a workflow design pattern, not as a requirement to adopt a particular vendor, model, framework, device, or UI.

| Layer | Proposed APF / Agentic Engineering interpretation | Minimum capability |
|---|---|---|
| Modality | Task intake through a structured issue, form, or natural-language request | Capture intent, constraints, expected output, and risk |
| Harness | Bounded workflow that loads project rules, plans work, invokes permitted tools, runs checks, and packages results | Explicit inputs/outputs, timeout, budget, trace, and failure states |
| Control plane | Human-visible status, evidence, review decision, cancellation, and controlled resumption | Review/approve/reject/request changes/block; immutable decision record |
| Evidence handoff | Practical bridge between Harness and Control Plane | Diff/artifact, test output, source references, known gaps, and reproducibility metadata |

The evidence-handoff row is an implementation proposal, not a fourth layer attributed to GitHub.

### Non-goals for the first PoC
- No production deployment or automatic merge.
- No broad write access to repositories, accounts, or external services.
- No real credentials or secrets in prompts, logs, fixtures, or test artifacts.
- No physical keypad or voice integration.
- No multi-agent coordination until the single-agent control path is measured.
- No change to APF Constitution or canonical architecture contracts.
- No automatic adoption of AgentFactory code or concepts into APF; the repositories remain independent.

## 4. Candidate PoC

### 4.1 Working title

**Intent-to-Evidence Workflow (IEW) — Synthetic Engineering Task v0.1**

### 4.2 Objective

Test whether a user can express a bounded engineering task once and receive a reviewable package containing:
1. parsed intent and constraints;
2. a proposed plan;
3. a generated artifact or simulated change;
4. test/validation evidence;
5. risk and unresolved-question summary;
6. an explicit human decision point;
7. a durable run trace.

The experiment should reuse the existing synthetic AgentFactory demo as a candidate test surface rather than starting with a new runtime. Reuse remains a proposal until the repository owner explicitly approves the cross-repository implementation scope.

### 4.3 Minimal workflow

```text
Intent Request
  → Validate Required Inputs
  → Load Pinned Context / Rules
  → Create Plan
  → Human Review of Plan (if risk/ambiguity requires)
  → Execute in Synthetic or Isolated Environment
  → Run Structural + Evidence + Policy Checks
  → Produce Artifact + Evidence Bundle
  → CER / Decision Gate
      ├─ PASS   → Mark candidate complete; no production write
      ├─ REVIEW → Wait for explicit HumanDecision
      ├─ CHANGE → Return to controlled revision path
      └─ BLOCK  → Stop; no bypass
  → Append Run Trace and Evaluation
```

### 4.4 Suggested input contract

```yaml
task_id: required
intent: required
expected_output: required
constraints: []
context_refs: []
risk_level: low | medium | high | unknown
allowed_actions: []
forbidden_actions: []
acceptance_criteria: []
requester_id: required
requested_at: required
```

The schema is a proposal and must be reconciled with existing canonical schemas before implementation.

### 4.5 Suggested evidence bundle

```yaml
run_id: required
task_id: required
source_commit: required
context_version: required
policy_snapshot_id: required
plan_ref: required
artifact_refs: []
test_results: []
claims_and_evidence: []
risk_findings: []
unresolved_questions: []
decision_state: DATA_NOT_READY | PASS | REVIEW | CHANGE | BLOCK
human_decision_ref: null
started_at: required
finished_at: required
```

Do not duplicate existing canonical contracts if a compatible schema already exists. First map these proposed fields to AgentFactory's existing interfaces and schemas.

## 5. Work packages and gates

| Milestone | Work | Deliverable | Exit gate |
|---|---|---|---|
| M0 — Recon | Confirm actual branch/HEAD, existing schemas, demo, test command, current CI, and repository permissions | Environment baseline | Repository facts captured; unknowns explicit |
| M1 — Baseline | Run existing synthetic PASS / REVIEW / BLOCK demo and relevant tests in a controlled environment | Baseline log and hashes | Reproducible run or documented blocker |
| M2 — Contract mapping | Map intent, context, plan, evidence, run, decision, and human decision to current schemas | Mapping table and gaps | No conflicting duplicate contract |
| M3 — UX / interaction | Design a minimal task intake and status/review surface; CLI or existing issue workflow is sufficient | Wireframe or CLI interaction spec | User can see status, required action, evidence |
| M4 — Thin PoC | Implement only missing orchestration needed to connect intent → run → evidence → review; use isolated/synthetic work | Feature branch and test artifacts | No production writes; fail-closed behavior verified |
| M5 — Adversarial validation | Test missing input, unsupported claim, tool failure, timeout, invalid approval, repeated run, and BLOCK bypass attempt | Test report | All mandatory safety tests pass |
| M6 — Human evaluation | Compare baseline and PoC using representative repeated tasks | Evaluation record | Human accepts the trade-off or rejects the approach |
| M7 — Decision | Review evidence, risks, costs, and alternatives | Human decision record | Explicit ACCEPT / DEFER / REJECT |
| M8 — Promotion (conditional) | Only if approved, define a separate implementation plan and release boundary | Versioned proposal / approved work item | No implicit promotion from research to production |

Dates, staffing, model provider, hosting, and cost are not set because the required environment details are unconfirmed.

## 6. Test matrix

| Case | Expected behavior | Mandatory evidence |
|---|---|---|
| Complete low-risk request | Plan and synthetic task run complete | Input, plan, result, tests, trace |
| Missing required input | DATA_NOT_READY; request clarification; no execution | Missing-field report |
| Unsupported factual claim | BLOCK or abstain according to existing CER contract | Claim-to-evidence mismatch |
| High-risk request | REVIEW_REQUIRED; wait for a human decision | Gate ID, snapshot ID, actor, reason |
| Human rejects | Stop or return to controlled change path | Rejection decision and state transition |
| BLOCK path | Execution cannot resume through a retry or alternate path | Negative bypass test |
| Tool/test failure | Fail safely; record error; no false PASS | Error trace and terminal state |
| Duplicate request / retry | Idempotency or explicitly documented new run | Run lineage and duplicate behavior |
| Context or policy changes mid-run | Current run remains pinned; new context applies to a new run | Snapshot/version comparison |
| Prompt injection in task/context | Untrusted instructions do not override policy or permissions | Adversarial fixture and policy result |
| Missing evidence or invalid source reference | No unsupported claim promoted to PASS | Evidence validation output |
| Timeout or budget limit | Run stops or enters defined recovery state | Timeout, budget, and final state |

## 7. Evaluation metrics

Measure the same task set with the current workflow and PoC. Do not infer success from one demonstration.

| Metric | Definition | Baseline / target |
|---|---|---|
| End-to-end time | Request accepted to reviewable output | Measure baseline first |
| Human active time | Actual user time spent entering, correcting, and reviewing | Measure baseline first |
| Rework rate | Tasks needing material correction / completed tasks | Measure baseline first |
| Evidence completeness | Required evidence fields present and valid / required fields | Define mandatory fields before run |
| Test pass rate | Passed required tests / required tests executed | Establish fixed test set |
| Unsafe transition count | Unauthorized gate bypasses or writes | Target = 0 in test suite |
| Reproducibility | Same pinned input/context reproduces equivalent decision state | Define deterministic fields and tolerance |
| Cost per accepted task | Model, compute, and human effort cost / accepted task | Measure only after usage/cost telemetry exists |
| Review latency | Time waiting for human review, reported separately from active work | Measure baseline first |

Numeric improvement thresholds must be agreed after baseline measurement. Any unauthorized state transition, false PASS on an unsupported claim, or successful bypass of BLOCK is an immediate failure regardless of productivity gain.

## 8. Risk register

| Risk | Control |
|---|---|
| Scope creep into a new agent platform | Start with one task path and existing contracts |
| Cross-repository coupling | Keep APF research and AgentFactory implementation separate; require explicit decision for shared changes |
| Agent-generated output mistaken for verified truth | Independent checks and evidence lineage |
| Permission escalation or unintended writes | Read-only/synthetic first; allowlisted tools; separate approval for writes |
| Stale context or policy drift | Pin repository commit, context version, and policy snapshot per run |
| Silent failure or false success | Explicit terminal states, structured logs, fail-closed gates |
| Unmeasured productivity claim | Baseline and comparative evaluation before promotion |
| Human approval becomes a rubber stamp | Show diff, tests, evidence, unresolved risks, and rejection path |
| Excessive orchestration overhead | Compare with a simple script / existing issue + PR workflow |
| Provider lock-in | Keep the proposed workflow contract provider-neutral; defer provider-specific adapters |

## 9. Unknowns — DATA_NOT_READY

The following were not established by source inspection alone:

- Whether the local execution environment has the repository cloned and tests can be run.
- Current CI status and whether all tests pass on the current branch.
- Which model provider, agent runtime, IDE, or MCP servers are actually enabled.
- Available credentials, network policy, sandbox guarantees, and spend limits.
- Whether the intended first user interface is GitHub Issues, CLI, IDE, web UI, voice, or physical control.
- Actual task frequency, baseline duration, error rate, and review burden.
- Whether the existing synthetic demo is the correct PoC host after owner review.
- Whether any existing session/event store can persist the proposed evidence bundle.

No claim of runtime verification or production readiness is made.

## 10. Decision recommendation

**Current status: RESEARCH_ONLY / READY_FOR_REVIEW of the proposal; implementation remains BLOCKED pending environment discovery and an explicit human decision.**

Recommended next sequence:
1. Review this research proposal in APF.
2. Inspect the actual AgentFactory main branch, canonical schemas, and current tests.
3. Run the existing synthetic demo and capture reproducible baseline evidence.
4. Decide whether to extend AgentFactory, prototype a separate thin adapter, or reject the approach in favor of a simpler workflow.
5. Implement only after a human decision record identifies scope, repository, branch, permissions, acceptance criteria, and rollback plan.

## 11. References

- GitHub Blog — The next developer interface is ambient intelligence (2026-10-15): https://github.blog/news-insights/company-news/the-next-developer-interface-is-ambient-intelligence/
- GitHub Docs — About GitHub Copilot cloud agent: https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent
- GitHub Blog — GitHub Copilot: Meet the new coding agent: https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/
- APF — README: https://github.com/chayobi03-cyber/agent-platform/blob/main/README.md
- APF — Constitution: https://github.com/chayobi03-cyber/agent-platform/blob/main/CONSTITUTION.md
- AgentFactory — README: https://github.com/chayobi03-cyber/agent-factory/blob/main/README.md
- AgentFactory — HOTL demo: https://github.com/chayobi03-cyber/agent-factory/blob/main/docs/FACTORY_HOTL_DEMO.md
- AgentFactory — CER Architecture Contract v1.0: https://github.com/chayobi03-cyber/agent-factory/blob/main/docs/governance/CER_ARCHITECTURE_CONTRACT_V1.md
