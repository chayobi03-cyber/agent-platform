# CORPUS-0002 — Third-party automation workflow specifications

**Status:** Frozen / available for benchmark execution
**Role:** Independent corpus for BENCH-0001, satisfying DEC-0001 exit criterion 1

## 1. Sources

| Source | Frozen commit | Ecosystem |
|---|---|---|
| `python/peps` | `a4f4971` | GitHub Actions |
| `apache/airflow` | `bf976c8` | GitHub Actions, Airflow DAGs |
| `temporalio/samples-python` | `a9cb676` | Temporal workflows |
| `langchain-ai/langgraph` | `c0a13bb` | LangGraph agent graphs |

Four ecosystems, three of which have an explicit stake in an agent- or
task-centric model. None has any relationship to APF. Not vendored here; the
commit SHAs are the provenance record.

## 2. Selection

16 workflows, purposively selected to cover the six classes BENCH-0001
requires, and fixed before any scoring instrument existed.

| Class | n | Workflows |
|---|--:|---|
| C1 deterministic automation | 2 | W01, W02 |
| C2 agentic workflow | 4 | W03, W04, W15, W16 |
| C3 human-in-the-loop | 3 | W05, W06, W07 |
| C4 scheduled | 2 | W08, W09 |
| C5 external-system orchestration | 2 | W10, W11 |
| C6 validation / checking | 3 | W12, W13, W14 |

The agentic class is deliberately the largest. It is the class where the
work-centric schema is most likely to lose, and falsifier F4 turns on it.

Exact paths are in `extract.py`.

## 3. Concept extraction

Each workflow's concept set is extracted mechanically — YAML key paths for
GitHub Actions, Python AST for Airflow, Temporal, and LangGraph — then mapped to
a normalized vocabulary through a fixed per-ecosystem surface-form map.

16 workflows yielded 26 distinct concepts. Extraction ran before either binding
table was written and produced no scores.

## 4. Limitations — recorded before execution

1. **The surface-form map is hand-written.** Concepts it does not name are
   invisible to both conditions. It is applied identically to both, so it should
   not favour either, but it bounds what the benchmark can see.
2. **Code and configuration, not engineering work.** These are automation
   specifications from software ecosystems, not EMC/PCB engineering workloads.
   A result speaks to representational generality over automation specs.
3. **Concept counts are not importance weights.** A workflow declaring nine
   concepts is not necessarily richer than one declaring four; `score.py`
   therefore weights workflows equally and does not weight concepts at all.
4. **Ecosystem skew.** Eight of sixteen workflows are GitHub Actions, because
   that ecosystem's declarative surface extracts most reliably. GitHub Actions
   has no agent concepts, which if anything favours the work-centric schema on
   the non-agentic classes — the per-class breakdown is what guards against
   reading the overall average as the result.
