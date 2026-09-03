"""The cross-ref disagreements this repository has actually produced.

Each function below corresponds to a defect verified in git history, not a
hypothetical one. None of them is visible from a single working tree, which is
why they survived a session that was auditing document integrity at the time.
"""

from __future__ import annotations

import re
from collections import defaultdict

from . import refs, subjects

MAIN = "refs/remotes/origin/main"
DECISIONS = "docs/decisions/"
EXECUTIONS = "docs/research/executions/"
REGISTER = "docs/research/BENCHMARK_REGISTER.md"

DEC_ID_RE = re.compile(r"^\s*id:\s*(DEC-\d{4})\s*$", re.M)
DEC_TITLE_RE = re.compile(r"^\s*title:\s*(.+?)\s*$", re.M)
DEC_HEADING_RE = re.compile(r"^#\s*(?:DEC-\d{4}\s*[—-]\s*)?(.+?)\s*$", re.M)
DEC_FILE_ID_RE = re.compile(r"(DEC-\d{4})")
BENCH_RE = re.compile(r"BENCH-\d{4}")
ROUND_RE = re.compile(r"BENCH-(\d{4})[_-]((?:R|E)\d+[a-z]?)")
REGISTER_ROW_RE = re.compile(r"^\|\s*(BENCH-\d{4})\s*\|.*\|\s*(?:\*\*)?([A-Za-z][A-Za-z ]*?)(?:\*\*)?\s*\|\s*$", re.M)


def main_ref() -> str:
    return MAIN if refs.exists(MAIN) else "refs/heads/main"


# --- 1. one identifier, several decisions -----------------------------------

def decision_records() -> dict[str, list[tuple[str, str, str]]]:
    """DEC id -> [(ref, path, title)] across every ref."""
    found: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for ref in refs.branch_refs():
        for path in refs.files(ref, DECISIONS):
            if not path.endswith(".md"):
                continue
            text = refs.read(ref, path) or ""
            match = DEC_ID_RE.search(text) or DEC_FILE_ID_RE.search(path)
            if not match:
                continue
            dec_id = match.group(1)
            title = DEC_TITLE_RE.search(text) or DEC_HEADING_RE.search(text)
            found[dec_id].append(
                (refs.short(ref), path, title.group(1) if title else path))
    return found


def decision_id_collisions() -> dict[str, list[tuple[str, str, str]]]:
    """An id claimed by two decisions is not a merge conflict — it is two
    decisions that can never both be cited."""
    collisions = {}
    for dec_id, records in decision_records().items():
        if len({title for _, _, title in records}) > 1:
            collisions[dec_id] = sorted(records)
    return collisions


# --- 2. a state on main that another ref has already disproved --------------

def register_states(ref: str) -> dict[str, str]:
    text = refs.read(ref, REGISTER) or ""
    return {bench: state.strip() for bench, state in REGISTER_ROW_RE.findall(text)}


def execution_records() -> dict[str, list[tuple[str, str]]]:
    """BENCH id -> [(ref, path)] for every execution record on every ref."""
    found: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for ref in refs.branch_refs():
        for path in refs.files(ref, EXECUTIONS):
            if not path.endswith(".md"):
                continue
            tail = path[len(EXECUTIONS):]
            if "PREDECLARATION" in tail.upper():
                continue
            for bench in set(BENCH_RE.findall(tail)):
                found[bench].append((refs.short(ref), path))
    return found


def untested_but_executed() -> dict[str, list[tuple[str, str]]]:
    """The register calls a benchmark UNTESTED; some ref holds its execution."""
    states = register_states(main_ref())
    executed = execution_records()
    return {
        bench: sorted(where)
        for bench, state in states.items()
        if state.upper().startswith("UNTESTED") and (where := executed.get(bench))
    }


# --- 3. one execution identity, two executions ------------------------------

def execution_collisions() -> dict[str, list[tuple[str, str, str]]]:
    """`BENCH-0004 R3` names one experiment. Two refs ran different ones."""
    by_id: dict[str, dict[str, tuple[str, str]]] = defaultdict(dict)
    for ref in refs.branch_refs():
        for path in refs.files(ref, EXECUTIONS):
            if not path.endswith(".md") or "PREDECLARATION" in path.upper():
                continue
            match = ROUND_RE.search(path[len(EXECUTIONS):])
            if not match:
                continue
            key = f"BENCH-{match.group(1)} {match.group(2)}"
            text = refs.read(ref, path) or ""
            # Same content on two refs is one execution, not two.
            by_id[key][refs.short(ref)] = (path, _fingerprint(text))
    collisions = {}
    for key, per_ref in by_id.items():
        if len({fp for _, fp in per_ref.values()}) > 1:
            collisions[key] = sorted(
                (ref, path, fp) for ref, (path, fp) in per_ref.items())
    return collisions


def _fingerprint(text: str) -> str:
    import hashlib
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


# --- 4. work that never came back -------------------------------------------

def divergent_refs() -> dict[str, tuple[str, int, str]]:
    """ref -> (head sha, commits not on main, last commit date)."""
    base = main_ref()
    here = refs.current()
    out = {}
    for ref in refs.branch_refs():
        if refs.head(ref) == refs.head(base) or refs.short(ref) == here:
            continue
        ahead = refs.commits_not_in(ref, base)
        if ahead:
            out[refs.short(ref)] = (refs.head(ref), ahead, refs.committed_at(ref))
    return out


# --- what the guard compares against the ledger -----------------------------

def observed() -> dict[str, dict]:
    """Every cross-ref disagreement git currently shows, keyed for the ledger.

    Each entry carries two different things, and the distinction is the whole
    point of the guard:

      refs        head SHAs, for staleness. The checked-out branch is excluded:
                  its head moves with every commit, and a pin that goes stale on
                  every commit trains people to re-pin without reading.
      claimants   *who* is in the disagreement — the distinct decision titles,
                  the distinct execution contents, the refs holding a result.
                  The checked-out branch is included, because a session adding a
                  fourth DEC-0001 is exactly the event this guard exists for.

    Recording only the key would let a ledger row absorb new divergence
    silently: the id was already known to collide, so a fourth claimant would
    change nothing the guard looks at. It was written that way first, and a
    negative test caught it.
    """
    here = refs.current()
    heads = {refs.short(r): refs.head(r) for r in refs.branch_refs()}

    def pin(names) -> dict[str, str]:
        return {n: heads[n] for n in sorted(set(names))
                if n in heads and n != here}

    out: dict[str, dict] = {s: {} for s in (
        "decision_id_collisions", "untested_but_executed",
        "execution_collisions", "divergent_refs", "subject_ownership")}
    for key, rows in decision_id_collisions().items():
        out["decision_id_collisions"][key] = {
            "refs": pin(r for r, _, _ in rows),
            "claimants": sorted({title for _, _, title in rows})}
    for key, rows in untested_but_executed().items():
        out["untested_but_executed"][key] = {
            "refs": pin(r for r, _ in rows),
            "claimants": sorted({f"{r}:{p}" for r, p in rows})}
    for key, rows in execution_collisions().items():
        out["execution_collisions"][key] = {
            "refs": pin(r for r, _, _ in rows),
            "claimants": sorted({fp for _, _, fp in rows})}
    for key, (sha, ahead, when) in divergent_refs().items():
        out["divergent_refs"][key] = {
            "refs": pin([key]), "claimants": [key],
            "commits_ahead": ahead, "last_commit": when}
    for ref in refs.branch_refs():
        found = subjects.violations(ref)
        if not found:
            continue
        name = refs.short(ref)
        out["subject_ownership"][name] = {
            "refs": pin([name]),
            "claimants": sorted(f"{subject} <- {path}"
                                for subject, paths in found.items()
                                for path in paths)}
    return out
