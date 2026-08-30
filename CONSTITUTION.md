# APF Constitution v0.1

**Status:** Foundation / Candidate

## 1. Purpose

APF — Internal Agent Platform exists to make organizational automation engineering repeatable, auditable, governable, and outcome-oriented.

The platform connects:

```text
Work → Opportunity → Automation Decision → Engineering → Control → Execution → Evidence → Evaluation → Outcome → Learning
```

## 2. Work-Centric Boundary

APF is not primarily an Agent Builder, generic Agent Framework, LLM Router, Multi-Agent Framework, MCP Gateway, or Observability Dashboard.

An Agent is one possible automation mechanism. The platform's primary abstraction is the relationship between work, automation decisions, execution, evidence, and outcomes.

## 3. Human Accountability

Human accountability is a platform invariant.

Agents may research, analyze, draft, generate code, test, evaluate, monitor, and propose. Consequential decisions remain subject to human ownership and approval.

Human decision boundaries include, at minimum:

- architecture and contract changes
- adoption of external assets as APF design primitives
- identity or permission escalation
- sensitive-data access
- production release
- business acceptance
- policy exceptions
- high-risk actions

## 4. State Separation

APF distinguishes:

```text
DISCOVERED
CANDIDATE
REVIEWED
ACCEPTED
DECIDED
IMPLEMENTED
VERIFIED
```

No state is implicitly equivalent to another.

In particular:

```text
Research finding != APF rule
Accepted asset != implementation authorization
Commit != human decision
Implementation != verification
```

## 5. Evidence Before Architecture

Architecture conclusions require evidence. External research, repository state, runtime behavior, evaluation results, and human decisions are distinct evidence classes.

Contradictory evidence must be surfaced rather than suppressed.

## 6. Framework Neutrality

Frameworks and vendors are references and implementation candidates. APF should extract reusable primitives and contracts rather than copy framework-specific abstractions into the core model without analysis.

## 7. Change Governance

The default consequential change sequence is:

```text
Evidence
→ Analysis
→ Alternatives
→ Risk
→ Recommendation
→ Human Decision
→ Implementation
→ Verification
```

## 8. Repository Boundary

APF is independent from `chayobi03-cyber/agent-factory`.

AgentFactory artifacts may be referenced as external implementation assets, but its architecture, governance, code, or assumptions are not inherited automatically.

## 9. Evolution

This Constitution is versioned. Changes to its invariants require explicit review and a decision record.
