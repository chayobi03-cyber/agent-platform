"""BENCH-0001 — mechanical concept extraction from third-party workflow specs.

Extraction only. Produces no scores and takes no position on either
representation. Run before the binding tables are written, so the concept
vocabulary is fixed by the sources rather than chosen to suit a schema.

Sources are pinned public repositories; see CORPUS-0002.
"""

import ast
import json
import os
import re
import sys

SOURCES = {
    "peps": "/home/user/python/peps",
    "airflow": "/home/user/corpus/airflow",
    "temporal": "/home/user/corpus/samples-python",
    "langgraph": "/home/user/corpus/langgraph",
}

# 14 workflows, selected to cover the six classes BENCH-0001 requires.
# Selection is purposive by class and was fixed before any scoring existed.
WORKFLOWS = [
    ("W01", "C1_deterministic", "peps", ".github/workflows/render.yml", "gha"),
    ("W02", "C1_deterministic", "airflow", "airflow-core/src/airflow/example_dags/tutorial_dag.py", "airflow"),
    ("W03", "C2_agentic", "temporal", "bedrock/signals_and_queries/workflows.py", "temporal"),
    ("W04", "C2_agentic", "langgraph", "libs/cli/examples/graphs/storm.py", "langgraph"),
    ("W15", "C2_agentic", "langgraph", "libs/cli/examples/graphs/agent.py", "langgraph"),
    ("W16", "C2_agentic", "temporal", "openai_agents/customer_service/customer_service.py", "temporal"),
    ("W05", "C3_human_in_the_loop", "temporal", "hello/hello_signal.py", "temporal"),
    ("W06", "C3_human_in_the_loop", "temporal", "hello/hello_update.py", "temporal"),
    ("W07", "C3_human_in_the_loop", "airflow", ".github/workflows/ts-sdk-release.yml", "gha"),
    ("W08", "C4_scheduled", "temporal", "schedules/start_schedule.py", "temporal"),
    ("W09", "C4_scheduled", "airflow", ".github/workflows/ci-duration-monitor.yml", "gha"),
    ("W10", "C5_external_orchestration", "airflow", "airflow-core/src/airflow/example_dags/example_trigger_target_dag.py", "airflow"),
    ("W11", "C5_external_orchestration", "temporal", "polling/periodic_sequence/workflows.py", "temporal"),
    ("W12", "C6_validation", "peps", ".github/workflows/lint.yml", "gha"),
    ("W13", "C6_validation", "peps", ".github/workflows/test.yml", "gha"),
    ("W14", "C6_validation", "airflow", ".github/workflows/basic-tests.yml", "gha"),
]

# Normalized concept vocabulary. Each entry maps a surface form in a source
# ecosystem to one normalized concept. The vocabulary is the union of what the
# ecosystems declare; it is not derived from either representation under test.
GHA_MAP = {
    "on.schedule": "SCHEDULE", "on.workflow_dispatch": "MANUAL_INVOCATION",
    "on.push": "TRIGGER_EVENT", "on.pull_request": "TRIGGER_EVENT",
    "on.workflow_call": "TRIGGER_EVENT", "on.workflow_run": "TRIGGER_EVENT",
    "on.release": "TRIGGER_EVENT", "on.issues": "TRIGGER_EVENT",
    "on.pull_request_target": "TRIGGER_EVENT", "on.issue_comment": "TRIGGER_EVENT",
    "inputs": "INPUT_PARAMETER", "outputs": "ARTIFACT_OUTPUT",
    "env": "CONFIGURATION", "permissions": "PERMISSION_SCOPE",
    "secrets": "SECRET_ACCESS", "environment": "HUMAN_APPROVAL",
    "concurrency": "CONCURRENCY_CONTROL", "strategy": "DYNAMIC_FANOUT",
    "matrix": "DYNAMIC_FANOUT", "needs": "DEPENDENCY_RELATION",
    "if": "BRANCH_CONDITION", "steps": "STEP_SEQUENCE", "uses": "EXTERNAL_SYSTEM_CALL",
    "run": "STEP_SEQUENCE", "timeout-minutes": "TIMEOUT",
    "continue-on-error": "FAILURE_HANDLER", "runs-on": "EXECUTION_TARGET",
    "container": "EXECUTION_TARGET", "services": "EXTERNAL_SYSTEM_CALL",
    "defaults": "CONFIGURATION", "with": "INPUT_PARAMETER",
}
PY_MAP = {
    # Airflow
    "DAG": "WORKFLOW_DEFINITION", "dag": "WORKFLOW_DEFINITION",
    "schedule": "SCHEDULE", "start_date": "SCHEDULE", "catchup": "SCHEDULE",
    "retries": "RETRY_POLICY", "retry_delay": "RETRY_POLICY",
    "execution_timeout": "TIMEOUT", "trigger_rule": "BRANCH_CONDITION",
    "on_failure_callback": "FAILURE_HANDLER", "on_success_callback": "OBSERVABILITY_HOOK",
    "params": "INPUT_PARAMETER", "default_args": "CONFIGURATION",
    "BashOperator": "STEP_SEQUENCE", "PythonOperator": "STEP_SEQUENCE",
    "EmptyOperator": "STEP_SEQUENCE", "task": "STEP_SEQUENCE",
    "TriggerDagRunOperator": "EXTERNAL_SYSTEM_CALL", "expand": "DYNAMIC_FANOUT",
    "TaskGroup": "STEP_SEQUENCE", "Asset": "DATA_ASSET", "outlets": "DATA_ASSET",
    "doc_md": "DOCUMENTATION", "tags": "CLASSIFICATION", "owner": "ACTOR_OWNERSHIP",
    "max_active_runs": "CONCURRENCY_CONTROL", "depends_on_past": "DEPENDENCY_RELATION",
    # Temporal
    "workflow": "WORKFLOW_DEFINITION", "defn": "WORKFLOW_DEFINITION",
    "execute_activity": "STEP_SEQUENCE", "activity": "STEP_SEQUENCE",
    "signal": "EVENT_SIGNAL", "update": "EVENT_SIGNAL", "query": "STATE_INSPECTION",
    "wait_condition": "HUMAN_APPROVAL", "RetryPolicy": "RETRY_POLICY",
    "start_to_close_timeout": "TIMEOUT", "schedule_to_close_timeout": "TIMEOUT",
    "continue_as_new": "STATE_PERSISTENCE", "ScheduleSpec": "SCHEDULE",
    "ScheduleIntervalSpec": "SCHEDULE", "Schedule": "SCHEDULE",
    "task_queue": "EXECUTION_TARGET", "heartbeat": "OBSERVABILITY_HOOK",
    "sleep": "TIMEOUT", "start_child_workflow": "EXTERNAL_SYSTEM_CALL",
    "execute_child_workflow": "EXTERNAL_SYSTEM_CALL",
    # LangGraph / agent
    "StateGraph": "WORKFLOW_DEFINITION", "add_node": "STEP_SEQUENCE",
    "add_edge": "DEPENDENCY_RELATION", "add_conditional_edges": "BRANCH_CONDITION",
    "interrupt": "HUMAN_APPROVAL", "checkpointer": "STATE_PERSISTENCE",
    "bind_tools": "TOOL_BINDING", "ChatOpenAI": "LLM_INVOCATION",
    "ChatAnthropic": "LLM_INVOCATION", "invoke": "LLM_INVOCATION",
    "ainvoke": "LLM_INVOCATION", "with_structured_output": "LLM_INVOCATION",
    "SystemMessage": "PROMPT_CONTENT", "HumanMessage": "PROMPT_CONTENT",
    "AIMessage": "PROMPT_CONTENT", "TypedDict": "STATE_SCHEMA",
    "BaseModel": "STATE_SCHEMA", "memory": "AGENT_MEMORY",
    "tool": "TOOL_BINDING", "converse": "LLM_INVOCATION",
}


def walk_yaml_keys(node, prefix=""):
    """Key paths from a YAML document, list indices collapsed."""
    out = []
    if isinstance(node, dict):
        for k, v in node.items():
            key = str(k)
            path = f"{prefix}.{key}" if prefix else key
            out.append((key, path))
            out.extend(walk_yaml_keys(v, path))
    elif isinstance(node, list):
        for item in node:
            out.extend(walk_yaml_keys(item, prefix))
    return out


def extract_gha(path):
    import yaml
    doc = yaml.safe_load(open(path, encoding="utf-8"))
    concepts = set()
    for key, full in walk_yaml_keys(doc):
        for probe in (full, key):
            if probe in GHA_MAP:
                concepts.add(GHA_MAP[probe])
                break
        else:
            if full.startswith("on.") or full == "on" or full == "true":
                concepts.add("TRIGGER_EVENT")
    return sorted(concepts)


def extract_python(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Name):
                names.add(f.id)
            elif isinstance(f, ast.Attribute):
                names.add(f.attr)
            for kw in node.keywords:
                if kw.arg:
                    names.add(kw.arg)
        elif isinstance(node, ast.Attribute):
            names.add(node.attr)
        elif isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, (ast.AsyncWith, ast.With)):
            pass
    return sorted({PY_MAP[n] for n in names if n in PY_MAP})


def main():
    out = {"workflows": [], "vocabulary": {}}
    vocab = {}
    for wid, cls, src, rel, kind in WORKFLOWS:
        path = os.path.join(SOURCES[src], rel)
        if not os.path.exists(path):
            print(f"MISSING {wid} {path}", file=sys.stderr)
            continue
        concepts = extract_gha(path) if kind == "gha" else extract_python(path)
        out["workflows"].append({
            "id": wid, "class": cls, "source": src, "path": rel,
            "kind": kind, "concepts": concepts, "n_concepts": len(concepts),
        })
        for c in concepts:
            vocab[c] = vocab.get(c, 0) + 1
    out["vocabulary"] = dict(sorted(vocab.items(), key=lambda kv: (-kv[1], kv[0])))
    out["n_workflows"] = len(out["workflows"])
    out["n_distinct_concepts"] = len(vocab)

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "concepts.json"), "w") as f:
        json.dump(out, f, indent=2, sort_keys=True)
    for w in out["workflows"]:
        print(f"{w['id']} {w['class']:26s} {w['kind']:9s} {w['n_concepts']:2d}  {','.join(w['concepts'])}")
    print(f"\n{out['n_workflows']} workflows, {out['n_distinct_concepts']} distinct concepts")
    print(json.dumps(out["vocabulary"], indent=2))


if __name__ == "__main__":
    main()
