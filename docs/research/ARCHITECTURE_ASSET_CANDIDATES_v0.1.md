# APF Architecture Asset Candidates v0.1

**Status:** CANDIDATE / HUMAN REVIEW REQUIRED  
**Scope:** Research synthesis only. No asset is accepted, no contract is changed, and no implementation is authorized by this document.

## 0. Normalization Rule

```text
Research Finding
→ Architectural Primitive
→ Cross-Source Pattern
→ Architecture Asset Candidate
→ Human Review
→ Decision
→ Contract Proposal
→ Human Approval
→ Implementation
```

A framework feature is not an APF asset. An external technology name is recorded as evidence or implementation reference only.

## 1. Candidate Summary

| ID | Architecture Asset Candidate | Type | Priority | Recommendation | Confidence |
|---|---|---|---|---|---|
| A01 | Work / Opportunity Model | Core | CORE | ADOPT | High |
| A02 | Automation Decision Model | Core | CORE | ADOPT | Medium |
| A03 | Stateful Durable Execution Model | Core | CORE | ADOPT | High |
| A04 | Human Control / Intervention Model | Core | CORE | ADOPT | High |
| A05 | Capability Boundary Model | Core | CORE | ADOPT | High |
| A06 | Identity / Delegation Model | Core | CORE | ADOPT | High |
| A07 | Authorization / Policy Decision Model | Core | CORE | ADOPT | High |
| A08 | Execution Evidence / Provenance Model | Core | CORE | ADOPT | High |
| A09 | Evaluation / Learning Loop Model | Supporting-to-Core | IMPORTANT | ADOPT | High |
| A10 | Business Outcome Linkage Model | Core | CORE | ADOPT | Medium |
| A11 | Work–Execution Identity / Correlation Model | Supporting | SUPPORTING | ADOPT | Medium-High |
| A12 | Context / Lineage Model | Supporting | SUPPORTING | DEFER | Medium |
| A13 | Agent–Workflow Composition Model | Supporting | SUPPORTING | ADOPT | Medium-High |

**Recommendation semantics:** `ADOPT` means "candidate direction to review," not human approval.

---

## A01 — Work / Opportunity Model

**asset_type:** Core Domain / Architecture Asset Candidate  
**status:** HUMAN_REVIEW  
**research_basis:** Backstage entity/relation/ownership/lifecycle patterns; APF work-centric constitution. Backstage explicitly emphasizes entities, relations, ownership, and lifecycle while warning that catalog ownership is not itself runtime authorization.  
**source_evidence:** Backstage Catalog Graph; Backstage well-known relations.

**problem:** APF needs a canonical business-domain object representing work and the opportunity to automate or improve it without making Agent the root object.

**scope:** Model the work being performed, its business context, ownership, opportunity/rationale, and lifecycle.

**primitive:** Entity + relation + ownership + lifecycle + business purpose.

**entities:** Work, Opportunity, Owner, Business Context, Candidate Automation.

**relationships:** Work HAS_OPPORTUNITY Opportunity; Work OWNED_BY Owner; Opportunity TARGETS Work; Work RELATED_TO System/Resource/Policy.

**lifecycle:** Discovered → Analyzed → Candidate → Accepted/Rejected → Automated → Measured → Retired.

**control:** Human ownership of business acceptance and automation approval.

**execution:** Does not execute; provides the business anchor for downstream execution.

**evidence:** Origin, owner, rationale, analysis, decision, and resulting outcome references.

**ownership:** Business/domain owner; platform preserves technical traceability.

**security_boundary:** Business/data classification and ownership; not equivalent to runtime authorization.

**failure_mode:** Work is underspecified, duplicated, orphaned, or incorrectly mapped to an automation opportunity.

**recovery:** Reclassify, merge, retire, or return to analysis without corrupting execution history.

**dependencies:** Identity, correlation, outcome model.

**trade_offs:** Rich work modeling improves governance but can become catalog bureaucracy if over-modeled.

**cross_source_support:** Backstage provides reusable entity/relation/ownership semantics; A2A reinforces task/context/artifact identity patterns; APF Constitution provides the work-centric anchor.

**contradictions:** Backstage's catalog is not a runtime source of truth; APF must not use a catalog model as runtime state.

**counter_evidence:** Some automations may be initiated directly by events without a long-lived business Work object.

**apf_relevance:** Very high; differentiates APF from agent/runtime frameworks.

**architectural_impact:** Establishes business-domain anchor candidate.

**security_impact:** Defines ownership context but does not authorize actions.

**operational_impact:** Enables portfolio discovery and lifecycle reporting.

**migration_impact:** Existing automation records may need linkage to Work identifiers later.

**lock_in_risk:** Low if expressed as semantic model, not Backstage schema.

**recommendation:** ADOPT  
**recommendation_rationale:** Central to APF mission and strongly aligned with existing constitution, but canonical Work/Opportunity boundaries require human/domain validation.

**decision_dependency:** Human agreement on canonical Work/Opportunity semantics.

**confidence:** HIGH

**open_questions:** Is Work always persistent? Can an Opportunity exist before Work is formalized? What is the minimum required owner/business context?

**related_architecture_assets:** A02, A10, A11, A12.

---

## A02 — Automation Decision Model

**asset_type:** Core Decision Asset Candidate  
**status:** HUMAN_REVIEW  
**research_basis:** APF work-centric flow; cross-source observation that workflows, agents, scripts, and human intervention are different mechanisms rather than interchangeable architecture roots.

**problem:** APF must explain why a work item is automated by rule, script, workflow, agentic mechanism, human-assisted mode, or left manual.

**scope:** Strategy selection and decision rationale; not runtime implementation.

**primitive:** Candidate strategy + constraints + risk + expected value + rationale + decision.

**entities:** Work, Opportunity, Automation Strategy, Decision, Risk, Constraint.

**relationships:** Opportunity EVALUATED_BY Decision; Decision SELECTS Strategy; Strategy CONSTRAINED_BY Policy/Risk.

**lifecycle:** Candidate → Analyzed → Proposed → Human Review → Decided → Implemented → Verified.

**control:** Consequential strategy selection remains human-owned where APF governance requires it.

**execution:** Produces an implementation direction, not an execution instance.

**evidence:** Alternatives considered, evidence used, rationale, assumptions, expected outcome.

**ownership:** Domain + architecture owner.

**security_boundary:** Strategy cannot escalate authority by itself.

**failure_mode:** Wrong mechanism selected; agent overused for deterministic work; durable execution applied where unnecessary; human work automated without adequate controls.

**recovery:** Reopen decision, compare alternative strategies, revise or retire automation.

**dependencies:** A01, A04, A05, A07, A10.

**trade_offs:** Explicit decisioning improves auditability but adds engineering overhead.

**cross_source_support:** Temporal/LangGraph show differentiated execution semantics; Backstage demonstrates entity-based contextualization; APF governance requires alternatives and human decision.

**contradictions:** No universal evidence supports a single default between workflow-centric and agent-centric automation.

**counter_evidence:** Low-risk repetitive tasks may not justify explicit strategy records.

**apf_relevance:** Very high.

**architectural_impact:** Provides a control point between work discovery and execution mechanism.

**security_impact:** Can encode risk tier and required control level without becoming the authorization engine.

**operational_impact:** Enables automation portfolio governance.

**migration_impact:** Existing automations will require retrospective classification only if useful.

**lock_in_risk:** Low.

**recommendation:** ADOPT  
**recommendation_rationale:** APF-specific value is strong because it owns the "why this automation mechanism" decision.

**decision_dependency:** Human approval of decision semantics and mandatory decision conditions.

**confidence:** MEDIUM

**open_questions:** Which decisions require a record? How should strategy confidence/risk be represented? Can the choice be revised after production evidence?

**related_architecture_assets:** A01, A03, A04, A05, A10, A09.

---

## A03 — Stateful Durable Execution Model

**asset_type:** Core Execution Asset Candidate  
**status:** HUMAN_REVIEW  
**research_basis:** Temporal durable execution; LangGraph checkpointed persistence, interrupts, resume, fault tolerance.

**problem:** Long-running or consequential automation requires explicit state, recovery, retry, and continuity semantics.

**scope:** Runtime-independent execution contract semantics; not a specific workflow engine.

**primitive:** State + checkpoint + persistence + retry + resume + interrupt + history.

**entities:** Execution, Step, State, Checkpoint, Attempt, Signal/Event, Failure, Recovery.

**relationships:** Execution HAS_STATE; Execution HAS_CHECKPOINT; Step PRODUCES_STATE; Failure TRIGGERS_RECOVERY; Human Control MAY_INTERRUPT/RESUME.

**lifecycle:** Created → Running → Waiting/Interrupted → Resumed → Completed/Failed/Cancelled.

**control:** Policy and human control can pause, reject, or redirect execution.

**execution:** Deterministic workflow and agentic steps may both participate.

**evidence:** State transitions, attempts, checkpoint identifiers, execution history, terminal reason.

**ownership:** Runtime owns mechanics; APF owns semantics.

**security_boundary:** Execution state may contain sensitive context and must obey data classification.

**failure_mode:** Crash, network failure, duplicate side effects, lost state, non-idempotent retry.

**recovery:** Retry, resume from checkpoint, compensate, or escalate to human.

**dependencies:** A04, A05, A07, A08, A11.

**trade_offs:** Durability improves recoverability but costs storage, complexity, and latency.

**cross_source_support:** Temporal emphasizes crash-proof resumable execution; LangGraph uses checkpoint persistence for human-in-the-loop and fault tolerance.

**contradictions:** Not every execution needs durable guarantees; lightweight work may be sufficient.

**counter_evidence:** Over-applying durable execution can create unnecessary complexity.

**apf_relevance:** Very high.

**architectural_impact:** Strong candidate for runtime-independent Execution Contract.

**security_impact:** Requires state/data protection and side-effect controls.

**operational_impact:** Drives recovery, replay, incident response, and capacity requirements.

**migration_impact:** Existing runtimes would be adapters to the semantic contract.

**lock_in_risk:** Low if contract is semantic; high if APF directly exposes vendor workflow primitives.

**recommendation:** ADOPT  
**recommendation_rationale:** Strong convergence across independent execution systems, with an explicit durability-tier question remaining.

**decision_dependency:** Human decision on minimum guarantees and durability tiers.

**confidence:** HIGH

**open_questions:** What is the minimum durable guarantee? Which execution classes may remain ephemeral? What is the APF idempotency model?

**related_architecture_assets:** A04, A05, A08, A11, A13.

---

## A04 — Human Control / Intervention Model

**asset_type:** Core Control Asset Candidate  
**status:** HUMAN_REVIEW  
**research_basis:** LangChain/LangGraph interrupt-based HITL patterns; APF HoTL governance; agent safety guidance.

**problem:** Consequential automation needs explicit human control that can interrupt, inspect, approve, edit, reject, escalate, resume, or abort.

**scope:** Human control semantics coupled to execution, not UI.

**primitive:** Intervention point + pending action + decision + actor + resume/termination semantics.

**entities:** Human Actor, Control Request, Pending Action, Approval, Rejection, Edit, Escalation, Resume.

**relationships:** Execution REQUIRES_CONTROL; Human MAKES_DECISION; Decision CHANGES_EXECUTION.

**lifecycle:** Requested → Presented → Approved/Edited/Rejected/Delegated → Applied → Recorded.

**control:** Explicit and auditable.

**execution:** May interrupt and later resume a stateful execution.

**evidence:** Who decided, what was presented, what changed, timestamp, authority basis.

**ownership:** Human decision owner; platform records and enforces workflow.

**security_boundary:** Human approval is not authorization by itself; it is one control input.

**failure_mode:** Approval bypass, stale approval, ambiguous action scope, human fatigue, queue deadlock.

**recovery:** Reconfirm, expire, escalate, or abort.

**dependencies:** A03, A06, A07, A08.

**trade_offs:** Stronger oversight can reduce throughput; too little oversight increases risk.

**cross_source_support:** LangGraph documents pause/resume and approve/edit/reject decisions; APF governance requires human ownership of consequential decisions.

**contradictions:** Continuous approval is not appropriate for every low-risk action.

**counter_evidence:** Excessive intervention can make automation economically unattractive.

**apf_relevance:** Very high.

**architectural_impact:** Establishes control boundary between proposed action and execution.

**security_impact:** Critical for privilege escalation and irreversible actions.

**operational_impact:** Adds approval queues, SLAs, escalation, and operator workload.

**migration_impact:** Existing automation must identify high-risk actions and control points.

**lock_in_risk:** Low.

**recommendation:** ADOPT  
**recommendation_rationale:** Human accountability is already a platform invariant; research supplies concrete execution semantics.

**decision_dependency:** Human definition of control levels and mandatory intervention classes.

**confidence:** HIGH

**open_questions:** What risk tiers require intervention? What constitutes a valid approval scope? How does approval expire?

**related_architecture_assets:** A03, A05, A06, A07, A08.

---

## A05 — Capability Boundary Model

**asset_type:** Core Security / Architecture Asset Candidate  
**status:** HUMAN_REVIEW  
**research_basis:** MCP tool safety and authorization; OpenHands sandbox boundaries; OWASP agentic security.

**problem:** Agents and workflows need a stable description of what actions/tools/capabilities are available and what side effects they may cause.

**scope:** Capability semantics and boundary; not a specific tool protocol.

**primitive:** Capability + resource scope + action + side effect + constraints + isolation.

**entities:** Capability, Tool, Resource, Action, Parameter, Side Effect, Sandbox.

**relationships:** Agent/Execution USES Capability; Capability TARGETS Resource; Capability PERFORMS Action; Capability CONSTRAINED_BY Policy.

**lifecycle:** Registered → Validated → Enabled → Used → Deprecated/Revoked.

**control:** Capability availability and invocation constraints are policy-controlled.

**execution:** Capability invocation is an execution step with declared side effects.

**evidence:** Capability identity/version, parameters, invocation result, authorization decision reference.

**ownership:** Capability provider/system owner; APF owns boundary semantics.

**security_boundary:** Trust, data, privilege, and side-effect boundary.

**failure_mode:** Tool misuse, parameter injection, excessive capability, confused deputy, untrusted tool metadata.

**recovery:** Reject, constrain, revoke, isolate, or route to human control.

**dependencies:** A06, A07, A08, A03.

**trade_offs:** Fine-grained capability modeling increases safety but increases administration burden.

**cross_source_support:** MCP treats tools as potentially powerful operations and calls for consent/authorization; sandbox systems isolate execution.

**contradictions:** Different environments may expose capabilities as APIs, commands, workflows, or agents.

**counter_evidence:** Over-modeling every low-risk read operation can create excessive catalog overhead.

**apf_relevance:** Very high.

**architectural_impact:** Separates "what can be done" from "who may do it" and "whether it is currently allowed".

**security_impact:** Critical.

**operational_impact:** Requires capability registry/lifecycle management later.

**migration_impact:** Existing tools will need semantic wrappers/adapters.

**lock_in_risk:** Low if protocol-neutral.

**recommendation:** ADOPT  
**recommendation_rationale:** Strong security convergence and clear APF boundary.

**decision_dependency:** Human approval of capability vocabulary and risk classification.

**confidence:** HIGH

**open_questions:** What is the minimum capability descriptor? How are side effects classified? Where is sandbox ownership represented?

**related_architecture_assets:** A04, A06, A07, A08.

---

## A06 — Identity / Delegation Model

**asset_type:** Core Security Asset Candidate  
**status:** HUMAN_REVIEW  
**research_basis:** NIST 2026 agent identity/authority work; MCP OAuth authorization patterns; APF identity/authorization boundary.

**problem:** APF needs to represent who/what is acting and whether an agent is acting for itself, a service, or a human principal.

**scope:** Identity, principal, delegation, authority provenance; not policy evaluation itself.

**primitive:** Principal + identity + delegation + credential/reference + authority context.

**entities:** Human Principal, Service Principal, Agent, Identity, Delegation, Credential, Session.

**relationships:** Agent ACTS_AS Principal; Principal DELEGATES_TO Agent; Identity IDENTIFIES Actor.

**lifecycle:** Established → Delegated → Active → Expired/Revoked.

**control:** Delegation scope and duration must be explicit.

**execution:** Every consequential execution should be attributable to an acting principal/identity context.

**evidence:** Identity and delegation references associated with execution and decision records.

**ownership:** Identity system / organization governance.

**security_boundary:** Identity is the attribution/trust boundary, not authorization.

**failure_mode:** Spoofing, stale credentials, confused deputy, privilege laundering, ambiguous principal.

**recovery:** Re-authenticate, revoke delegation, fail closed, escalate.

**dependencies:** A05, A07, A08, A11.

**trade_offs:** Rich delegation improves accountability but adds lifecycle and credential complexity.

**cross_source_support:** NIST explicitly highlights identification, authorization, auditing, and non-repudiation for software agents; MCP defines client/resource-owner/authorization-server roles.

**contradictions:** Human identity, workload identity, and agent identity may have different operational mechanisms.

**counter_evidence:** Some internal automation may run under a stable service identity with no user delegation.

**apf_relevance:** Very high.

**architectural_impact:** Establishes principal/authority semantics independent of auth engine.

**security_impact:** Critical.

**operational_impact:** Requires lifecycle, rotation, and delegation observability.

**migration_impact:** Existing tools will need principal propagation.

**lock_in_risk:** Low if identity references are abstract.

**recommendation:** ADOPT  
**recommendation_rationale:** Current standards work explicitly treats agent identity and authority as a first-class architectural concern.

**decision_dependency:** Human/enterprise IAM model and delegation policy.

**confidence:** HIGH

**open_questions:** What is the canonical APF principal? How is delegation scoped and represented? How are non-human principals audited?

**related_architecture_assets:** A05, A07, A08, A11.

---

## A07 — Authorization / Policy Decision Model

**asset_type:** Core Security / Control Asset Candidate  
**status:** HUMAN_REVIEW  
**research_basis:** OpenFGA relationship-based authorization; OPA policy decision point and policy/enforcement separation.

**problem:** APF must decide whether an actor may perform a capability/action on a resource under contextual policy.

**scope:** Relationship, policy evaluation, decision, enforcement reference; separate from identity and approval.

**primitive:** Actor + relation + resource + action + policy + context → decision.

**entities:** Principal, Relation, Resource, Action, Policy, Policy Version, Authorization Decision, Enforcement Point.

**relationships:** Principal HAS_RELATION_TO Resource; Policy CONSTRAINS Action; PDP RETURNS Decision; PEP ENFORCES Decision.

**lifecycle:** Requested → Evaluated → Allowed/Denied/Conditional → Enforced → Logged.

**control:** Policy version, decision constraints, and enforcement behavior are governed.

**execution:** Authorization decision precedes or constrains capability execution.

**evidence:** Decision id, policy/version, relevant input, outcome, enforcement reference.

**ownership:** Security/policy owner; resource owner may define relations.

**security_boundary:** Principal, resource, action, relation, policy, and enforcement boundary.

**failure_mode:** Default-allow, stale policy, relation drift, policy mismatch, PDP failure, enforcement bypass.

**recovery:** Fail closed where risk requires; retry decision; use cached decision only within explicit validity.

**dependencies:** A05, A06, A08.

**trade_offs:** Fine-grained policy improves control but adds latency, complexity, and policy lifecycle burden.

**cross_source_support:** OpenFGA answers relation-based authorization checks; OPA separates policy decision-making from enforcement and supports decision logs.

**contradictions:** ReBAC and rule/policy evaluation are complementary, not mutually exclusive; APF should not collapse them.

**counter_evidence:** Simple applications may use coarse RBAC and not need rich relationship semantics.

**apf_relevance:** Very high.

**architectural_impact:** Strong candidate for explicit authorization boundary.

**security_impact:** Critical.

**operational_impact:** Requires policy lifecycle, decision observability, failure semantics.

**migration_impact:** Existing role checks may require abstraction wrappers.

**lock_in_risk:** Low if APF owns the decision semantics, not OPA/OpenFGA schemas.

**recommendation:** ADOPT  
**recommendation_rationale:** Strong evidence for separating relationship reasoning, policy decision, and enforcement.

**decision_dependency:** Security governance on policy semantics and fail-open/fail-closed tiers.

**confidence:** HIGH

**open_questions:** Is APF authorization one combined contract or separate Relation and Policy contracts? What is minimum context for a decision?

**related_architecture_assets:** A05, A06, A08, A04.

---

## A08 — Execution Evidence / Provenance Model

**asset_type:** Core Evidence Asset Candidate  
**status:** HUMAN_REVIEW  
**research_basis:** OpenTelemetry semantic conventions/events; OPA decision logs; A2A task/artifact/history; W3C PROV conceptual model.

**problem:** APF must distinguish telemetry from durable evidence proving what execution, decision, approval, and outcome actually occurred.

**scope:** Provenance and evidence semantics; telemetry is a contributing signal, not the whole model.

**primitive:** Evidence item + subject + event/activity + actor + timestamp + source + provenance link.

**entities:** Execution Evidence, Decision Evidence, Approval Evidence, Policy Decision, Artifact, Outcome Evidence, Telemetry Observation.

**relationships:** Evidence DESCRIBES Activity; Evidence ATTRIBUTED_TO Actor; Evidence DERIVED_FROM Evidence/Artifact; Evidence SUPPORTS Evaluation.

**lifecycle:** Created → Linked → Retained → Queried → Archived/Deleted according to policy.

**control:** Evidence retention, access, masking, integrity, and classification are governed.

**execution:** Execution emits records sufficient to reconstruct or substantiate required facts.

**evidence:** Evidence itself is the artifact; telemetry may provide supporting observations.

**ownership:** Platform evidence service + source system ownership.

**security_boundary:** Sensitive data, retention, access, redaction, integrity.

**failure_mode:** Missing evidence, insufficient correlation, sensitive data leakage, non-reconstructable action, tampering.

**recovery:** Backfill where possible, annotate evidence gap, fail high-risk actions if required evidence cannot be produced.

**dependencies:** A06, A07, A11, A09, A10.

**trade_offs:** Strong evidence improves auditability but creates storage/privacy/cost burdens.

**cross_source_support:** OTel defines standardized telemetry semantics; OPA decision logs provide policy decision audit data; A2A models task history/artifacts; W3C PROV formalizes provenance relationships.

**contradictions:** Telemetry standards intentionally optimize observability, not legal-grade proof or business evidence.

**counter_evidence:** Some low-risk ephemeral actions may only need lightweight telemetry.

**apf_relevance:** Very high.

**architectural_impact:** Candidate for Evidence Contract and provenance graph.

**security_impact:** Critical due to sensitive execution content.

**operational_impact:** Drives retention, indexing, masking, storage, and audit capabilities.

**migration_impact:** Existing traces/logs may need semantic linkage.

**lock_in_risk:** Low if APF evidence semantics are distinct from OTel data model.

**recommendation:** ADOPT  
**recommendation_rationale:** Strong convergence and directly supports APF's auditable execution mandate.

**decision_dependency:** Human definition of evidence sufficiency, retention, integrity, and sensitive-data handling.

**confidence:** HIGH

**open_questions:** What makes evidence durable enough? Which fields are mandatory? How is tamper evidence achieved?

**related_architecture_assets:** A03, A04, A06, A07, A09, A10, A11.

---

## A09 — Evaluation / Learning Loop Model

**asset_type:** Supporting-to-Core Learning Asset Candidate  
**status:** HUMAN_REVIEW  
**research_basis:** Phoenix dataset/evaluation/experiment workflows; APF learning loop; distinction between evaluation and outcome.

**problem:** Production executions should produce reusable cases and evidence that can be evaluated and fed into improvement cycles.

**scope:** Evaluation datasets, evaluators, experiments, findings, and promotion back to automation decisions.

**primitive:** Case → Dataset → Evaluation → Experiment → Improvement Proposal.

**entities:** Execution Case, Dataset, Evaluator, Evaluation Result, Experiment, Variant, Improvement Proposal.

**relationships:** Evidence FEEDS Dataset; Dataset USED_BY Evaluation; Evaluation PRODUCES Finding; Experiment TESTS Variant; Finding FEEDS Decision.

**lifecycle:** Captured → Curated → Evaluated → Experimented → Validated → Promoted/Rejected.

**control:** Dataset selection, evaluator definition, experiment acceptance, and production promotion are governed.

**execution:** Evaluation itself is a controlled workload, separate from production execution.

**evidence:** Test inputs, evaluator versions, scores, explanations, experiment metadata, promotion decision.

**ownership:** Engineering/evaluation owner with business outcome owner.

**security_boundary:** Dataset confidentiality and evaluator access.

**failure_mode:** Biased datasets, evaluator drift, proxy metrics, contamination, overfitting to benchmark.

**recovery:** Re-curate dataset, revise evaluator, rerun experiment, reject promotion.

**dependencies:** A08, A10, A02.

**trade_offs:** Strong evaluation improves quality but can become disconnected from actual business outcomes.

**cross_source_support:** Phoenix connects production traces to datasets, evaluations, and experiments; APF learning loop requires feedback into future automation.

**contradictions:** Evaluation score is not equivalent to business value.

**counter_evidence:** Some deterministic automations may need only operational assertions rather than sophisticated datasets/experiments.

**apf_relevance:** High.

**architectural_impact:** Candidate for Evaluation Contract and learning loop semantics.

**security_impact:** Dataset access and experiment controls.

**operational_impact:** Requires evaluation storage and reproducibility.

**migration_impact:** Existing logs may not be evaluation-ready.

**lock_in_risk:** Low.

**recommendation:** ADOPT  
**recommendation_rationale:** Strong cross-source pattern, but APF must keep Evaluation distinct from Outcome.

**decision_dependency:** Human definition of evaluability and production promotion policy.

**confidence:** HIGH

**open_questions:** What constitutes an evaluation case? How are evaluators versioned? Which findings can change an automation decision?

**related_architecture_assets:** A08, A10, A02, A03.

---

## A10 — Business Outcome Linkage Model

**asset_type:** Core Business Semantics Asset Candidate  
**status:** HUMAN_REVIEW  
**research_basis:** APF mission and work-centric flow; indirect support from Backstage domain/metric/KPI modeling and evaluation systems.

**problem:** APF must connect execution and evaluation to the business result the automation was intended to improve.

**scope:** Outcome definition, measurement linkage, attribution metadata, and acceptance.

**primitive:** Intended outcome + metric/KPI + observation + attribution confidence + business acceptance.

**entities:** Outcome, KPI/Metric, Baseline, Observation, Attribution, Business Owner, Acceptance.

**relationships:** Work TARGETS Outcome; Execution CONTRIBUTES_TO Outcome; Evaluation INFORMS Outcome; Owner ACCEPTS Outcome.

**lifecycle:** Intended → Measured → Attributed/Uncertain → Accepted/Rejected → Reassessed.

**control:** Business owner validates outcome interpretation and acceptance.

**execution:** Execution emits outcome references; outcome measurement may occur outside execution lifecycle.

**evidence:** Baseline, measurement period, source, attribution notes, acceptance record.

**ownership:** Business/domain owner.

**security_boundary:** Business-sensitive metrics and decision records.

**failure_mode:** False attribution, proxy KPI, incomplete baseline, delayed outcome, mixed causal factors.

**recovery:** Rebaseline, annotate uncertainty, refine metric, re-evaluate attribution.

**dependencies:** A01, A02, A08, A09, A11.

**trade_offs:** Strong outcome linkage improves portfolio decisions but is costly for indirect/long-cycle benefits.

**cross_source_support:** APF constitution requires Outcome; Backstage models domain/KPI/business purpose at catalog level; evaluation systems provide measurement mechanisms but not business truth.

**contradictions:** Many automation outputs lack immediate measurable business outcomes.

**counter_evidence:** Technical outcomes may be the only feasible early-stage measure.

**apf_relevance:** Very high and APF-specific.

**architectural_impact:** Prevents APF from optimizing only agent quality or task completion.

**security_impact:** Usually lower than authorization, but business-sensitive.

**operational_impact:** Requires outcome data integration.

**migration_impact:** Outcome linkage may initially be optional.

**lock_in_risk:** Very low.

**recommendation:** ADOPT  
**recommendation_rationale:** Core to APF differentiation, but precise outcome attribution remains a domain research problem.

**decision_dependency:** Business governance and metric ownership.

**confidence:** MEDIUM

**open_questions:** What is the minimum outcome representation? How is causality/attribution expressed? Can an outcome be provisional?

**related_architecture_assets:** A01, A02, A08, A09, A11.

---

## A11 — Work–Execution Identity / Correlation Model

**asset_type:** Supporting Identity / Lineage Asset Candidate  
**status:** HUMAN_REVIEW  
**research_basis:** Temporal workflow identifiers/history; A2A Task/contextId/artifacts/history; OTel correlation semantics.

**problem:** APF must reliably connect Work, Decision, Execution, Evidence, Evaluation, and Outcome without conflating them.

**scope:** Stable identifiers and explicit correlation relationships.

**primitive:** Entity IDs + parent/causal/correlation links + context identifiers.

**entities:** Work ID, Opportunity ID, Decision ID, Execution ID, Evidence ID, Evaluation ID, Outcome ID, Context ID.

**relationships:** DERIVES_FROM, CORRELATES_WITH, CAUSED_BY, REFERENCES, PRODUCED_BY.

**lifecycle:** Created → Propagated → Resolved → Retained.

**control:** Correlation identifiers are immutable or versioned when semantics change.

**execution:** Execution carries references, not giant embedded objects.

**evidence:** Correlation chain is itself evidence metadata.

**ownership:** Platform semantic ownership.

**security_boundary:** Identifier leakage and cross-domain correlation must be controlled.

**failure_mode:** Broken links, reused identifiers, ambiguous parentage, cross-tenant collisions.

**recovery:** Reconcile through immutable source records; never silently rewrite history.

**dependencies:** Nearly all other assets.

**trade_offs:** More explicit lineage improves auditability but increases schema and propagation work.

**cross_source_support:** A2A has task/context/artifact/history identifiers; Temporal has execution identity/history; OTel emphasizes correlation across telemetry.

**contradictions:** Correlation ID and causal provenance are not identical concepts.

**counter_evidence:** Small isolated automations may need minimal identifiers only.

**apf_relevance:** High.

**architectural_impact:** Supporting layer for all major assets.

**security_impact:** High in multi-domain environments.

**operational_impact:** Important for debugging and portfolio reporting.

**migration_impact:** Existing identifiers need mapping.

**lock_in_risk:** Low.

**recommendation:** ADOPT  
**recommendation_rationale:** Required to connect otherwise separate APF asset semantics without creating one giant object.

**decision_dependency:** Human agreement on identifier classes and relationship vocabulary.

**confidence:** MEDIUM-HIGH

**open_questions:** Which links are causal versus merely correlational? What is the canonical context boundary?

**related_architecture_assets:** A01–A10, A12, A13.

---

## A12 — Context / Lineage Model

**asset_type:** Supporting Context Asset Candidate  
**status:** HUMAN_REVIEW  
**research_basis:** LangGraph checkpoints/threads; A2A contextId/history; OTel semantic context propagation; provenance concepts.

**problem:** Execution and decision systems need enough contextual state to reproduce, explain, or continue work without making context an unbounded blob.

**scope:** Context references, versioning, provenance, selected state snapshots, and lineage.

**primitive:** Context reference + version + scope + source + validity.

**entities:** Context, Snapshot, Message/Artifact, Source, Version, Validity Window.

**relationships:** Execution USES Context; Context DERIVED_FROM Source; Context VERSION_OF Context; Evidence REFERENCES Context.

**lifecycle:** Created → Updated/Versioned → Consumed → Expired/Archived.

**control:** Access, retention, mutation, and sensitivity are governed.

**execution:** Context is an input/supporting state, not necessarily the authoritative execution state.

**evidence:** Context version and provenance reference.

**ownership:** Depends on context domain; platform owns linkage semantics.

**security_boundary:** Data access and leakage boundary.

**failure_mode:** Stale context, hidden mutation, context explosion, provenance loss.

**recovery:** Re-resolve authoritative source, invalidate stale version, rebuild context.

**dependencies:** A03, A08, A11.

**trade_offs:** Rich context increases continuity but increases privacy/storage cost.

**cross_source_support:** LangGraph threads/checkpoints and A2A contextId/history show explicit contextual continuity; OTel supports propagation for correlated telemetry.

**contradictions:** Context is not identical to durable execution state or conversation history.

**counter_evidence:** Some workflows are stateless or receive complete inputs each time.

**apf_relevance:** Medium-high.

**architectural_impact:** Likely important but may be decomposed into smaller primitives.

**security_impact:** Potentially critical due to data exposure.

**operational_impact:** Significant storage/indexing implications.

**migration_impact:** Must avoid imposing an enterprise context store prematurely.

**lock_in_risk:** Medium if merged with a specific memory/context framework.

**recommendation:** DEFER  
**recommendation_rationale:** Evidence supports the need for context semantics, but the correct APF boundary is not yet sufficiently stable.

**decision_dependency:** Further research on context versus state versus provenance.

**confidence:** MEDIUM

**open_questions:** Is Context a first-class asset or a supporting attribute? What is authoritative state? How should memory be separated from execution state?

**related_architecture_assets:** A03, A08, A11.

---

## A13 — Agent–Workflow Composition Model

**asset_type:** Supporting Composition Asset Candidate  
**status:** HUMAN_REVIEW  
**research_basis:** Temporal workflow model; LangGraph graph/agent model; A2A agent task interoperability.

**problem:** APF needs a neutral way to combine deterministic orchestration, agentic reasoning, and human-controlled steps without making any one mechanism the platform root.

**scope:** Composition semantics between control flow, agentic steps, capability invocations, and human interventions.

**primitive:** Control node + decision/agent node + capability node + human control point.

**entities:** Workflow, Agent, Step, Capability, Human Control Point, Subtask.

**relationships:** Workflow CONTAINS Agent Step; Agent USES Capability; Workflow REQUIRES Human Control; Agent MAY DELEGATE Task.

**lifecycle:** Planned → Executed → Interrupted/Delegated → Completed/Failed.

**control:** Composition is bounded by authorization and execution policy.

**execution:** Agentic and deterministic steps share the same execution envelope where appropriate.

**evidence:** Step-level records show which mechanism performed each action.

**ownership:** APF owns composition semantics; runtime owns implementation.

**security_boundary:** Agent autonomy and delegation boundaries.

**failure_mode:** Agent runaway, hidden orchestration, uncontrolled recursion, duplicated work, state mismatch.

**recovery:** Limit depth/budget, interrupt, checkpoint, delegate, or abort.

**dependencies:** A03, A04, A05, A06, A07.

**trade_offs:** Flexible composition increases capability but complicates reasoning, testing, and governance.

**cross_source_support:** Temporal provides durable workflow orchestration; LangGraph supports graph/agent execution and interrupts; A2A supports opaque agent-to-agent task collaboration.

**contradictions:** Central orchestration and agent autonomy represent different control preferences.

**counter_evidence:** Some organizations may intentionally standardize on one execution paradigm.

**apf_relevance:** High.

**architectural_impact:** Prevents premature Agent-vs-Workflow architecture lock-in.

**security_impact:** High because composition changes autonomy surface.

**operational_impact:** Requires limits, tracing, and failure semantics.

**migration_impact:** Enables multiple runtimes behind a stable execution boundary.

**lock_in_risk:** Low if composition is expressed semantically.

**recommendation:** ADOPT  
**recommendation_rationale:** The research conflict is better resolved as composition/layering than as a binary framework choice.

**decision_dependency:** Human decision on autonomy boundaries and composition constraints.

**confidence:** MEDIUM-HIGH

**open_questions:** Is workflow the control plane? Can an agent create or modify workflow structure? What limits recursive delegation?

**related_architecture_assets:** A03, A04, A05, A06, A07, A11.

---

## 2. Cross-Candidate Invariants

These are synthesis hypotheses, not approved principles:

1. **Agent is a mechanism, not the APF root abstraction.**
2. **Execution is a lifecycle, not merely a function call.**
3. **Capability, Identity, Authorization, Policy, Approval, Execution, and Evidence are separate boundaries.**
4. **Telemetry is supporting observation; Evidence is an explicit semantic object.**
5. **Evaluation is not Business Outcome.**
6. **Work-to-Execution and Execution-to-Outcome continuity require explicit identity/correlation.**
7. **Runtime implementations should sit behind APF-owned semantic boundaries.**

## 3. Explicit Non-Assets

The following remain technology/reference categories, not APF-owned assets by themselves:

- Temporal
- LangGraph
- OpenFGA
- OPA
- MCP
- OpenTelemetry
- Phoenix
- A2A
- Backstage
- OpenHands

These may become implementation dependencies only after a separate human technology decision.

## 4. Proposed Asset Relationship Summary

```text
A01 Work / Opportunity
  ↓
A02 Automation Decision
  ↓
A03 Controlled Stateful Execution
  ├── A04 Human Control
  ├── A05 Capability Boundary
  └── A13 Agent–Workflow Composition
          ↓
      A06 Identity / Delegation
          ↓
      A07 Authorization / Policy
          ↓
      Execution
          ↓
      A08 Evidence / Provenance
       ├──→ A09 Evaluation / Learning
       └──→ A10 Business Outcome
                  ↓
              Learning
                  ↓
              A02 re-evaluation

A11 Correlation and A12 Context/Lineage span the graph.
```

**Status:** PROPOSED / NOT APPROVED
