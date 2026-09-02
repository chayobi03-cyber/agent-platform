"""Frozen-corpus loading and mechanically derived corpus features.

Every function here takes its corpus map explicitly rather than reading a
module global, so a second benchmark can use a different document set without
touching this file.
"""

from __future__ import annotations

import re
import subprocess
from collections import defaultdict
from pathlib import Path

META_FIELD_RE = re.compile(
    r"^\*\*(?:Status|Date|Scope|Purpose|Target claim|Session):\*\*.*$", re.MULTILINE)
VERSION_RE = re.compile(r"v\d+\.\d+")
H1_RE = re.compile(r"^#\s+(.*)$", re.MULTILINE)
IDENT_RE = re.compile(
    r"\b(?:CLM-\d+[a-c]?|BENCH-\d+|FB-\d+|ASSET-[A-Z0-9*]+|HP-\d+)\b")


def load_frozen_corpus(repo: Path, commit: str,
                       paths: dict[str, str]) -> dict[str, str]:
    """Read each document at `commit` rather than from the working tree.

    Corpus documents are ordinary repository files and keep changing after a
    benchmark runs. Reading them from the frozen commit is what makes recorded
    results replayable at any later HEAD.
    """
    out = {}
    for doc_id, path in paths.items():
        out[doc_id] = subprocess.run(
            ["git", "show", f"{commit}:{path}"],
            cwd=repo, capture_output=True, text=True, check=True,
        ).stdout
    return out


def git_commit_order(repo: Path, commit: str,
                     paths: dict[str, str]) -> dict[str, tuple[int, int]]:
    """(first_commit_index, last_commit_index) per document, oldest commit = 0."""
    out = subprocess.run(
        ["git", "log", "--reverse", "--format=@%H", "--name-only", commit],
        cwd=repo, capture_output=True, text=True, check=True,
    ).stdout
    path_to_id = {p: d for d, p in paths.items()}
    first: dict[str, int] = {}
    last: dict[str, int] = {}
    idx = -1
    for line in out.splitlines():
        if line.startswith("@"):
            idx += 1
        elif line.strip() in path_to_id:
            doc = path_to_id[line.strip()]
            first.setdefault(doc, idx)
            last[doc] = idx
    return {d: (first.get(d, 0), last.get(d, 0)) for d in paths}


def extract_metadata_text(body: str, path: str) -> str:
    """Title, bolded field lines and path segments — the 'better indexing' control."""
    parts = []
    h1 = H1_RE.search(body)
    if h1:
        parts.append(h1.group(1))
    parts.extend(META_FIELD_RE.findall(body))
    parts.append(" ".join(re.split(r"[/_\-.]", path.replace(".md", ""))))
    return "\n".join(parts)


def extract_provenance_text(body: str) -> str:
    """Status/date/scope/purpose field lines plus version tokens."""
    parts = list(META_FIELD_RE.findall(body))
    parts.extend(VERSION_RE.findall(body))
    return "\n".join(parts)


def derive_relationship_graph(bodies: dict[str, str],
                              paths: dict[str, str]) -> dict[str, dict[str, float]]:
    """Edges from filename mentions and shared identifiers, row-normalised.

    Derivation is fully mechanical: no operator discretion decides which
    documents are related. That is the point — a hand-drawn graph lets whoever
    knows the questions produce the ranking they expect, which is exactly the
    bias BENCH-0004 Round 3 was built to expose in Round 2.
    """
    ids = list(bodies)

    # A bare basename is only usable when it is unambiguous across the corpus
    # (README.md can appear several times, so those documents match on full path).
    basename_counts: dict[str, int] = defaultdict(int)
    for d in ids:
        basename_counts[Path(paths[d]).stem] += 1

    mention_keys: dict[str, list[str]] = {}
    for d in ids:
        path = paths[d]
        keys = [path, Path(path).name]
        stem = Path(path).stem
        if basename_counts[stem] == 1:
            keys.append(stem)
        mention_keys[d] = keys

    idents = {d: set(IDENT_RE.findall(bodies[d])) for d in ids}

    graph: dict[str, dict[str, float]] = {d: {} for d in ids}
    for a in ids:
        for b in ids:
            if a == b:
                continue
            w = 0.0
            if any(k in bodies[a] for k in mention_keys[b]):
                w += 1.0
            union = idents[a] | idents[b]
            if union:
                w += len(idents[a] & idents[b]) / len(union)
            if w > 0:
                graph[a][b] = w

    for a in ids:
        total = sum(graph[a].values())
        if total > 0:
            for b in graph[a]:
                graph[a][b] /= total
    return graph
