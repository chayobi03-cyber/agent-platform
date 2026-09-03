"""Which document owns which subject, checked on every ref.

`DEC-0001` established one-subject-one-document by editing the documents. That
holds on `main` and on no other ref: `claude/handover-eu02yk` has three
documents declaring the execution order and `claude/session-governance-
decisions-6fi9vf` has four declaring the claim state vocabulary. The convention
was restored, not enforced, so it was restored on one branch.

The detectors look for a *declaration*, never a mention. "Execution order" as a
phrase appears in documents that only cite the register; what identifies a
declaration is a fenced block enumerating four or more benchmark ids. The same
distinction the measurement guard needs, for the same reason.
"""

from __future__ import annotations

import fnmatch
import json
import re
from pathlib import Path

from . import refs

MANIFEST = Path(__file__).resolve().parent / "subject_manifest.json"
FENCED = re.compile(r"```.*?```", re.S)


def load() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def _fenced_distinct_matches(text: str, spec: dict) -> bool:
    pattern = re.compile(spec["pattern"])
    return any(len(set(pattern.findall(block))) >= spec["minimum"]
               for block in FENCED.findall(text))


def _fenced_token_set(text: str, spec: dict) -> bool:
    tokens = spec["tokens"]
    return any(sum(token in block for token in tokens) >= spec["minimum"]
               for block in FENCED.findall(text))


def _line_pattern(text: str, spec: dict) -> bool:
    return bool(re.search(spec["pattern"], text, re.M))


KINDS = {
    "fenced_distinct_matches": _fenced_distinct_matches,
    "fenced_token_set": _fenced_token_set,
    "line_pattern": _line_pattern,
}


def declares(text: str, detector: dict) -> bool:
    return KINDS[detector["kind"]](text, detector)


def exempt(path: str, globs) -> bool:
    return any(fnmatch.fnmatch(path, g) for g in globs)


def declarers(ref: str) -> dict[str, list[str]]:
    """subject -> the documents on `ref` that declare it."""
    manifest = load()
    globs = manifest["exempt_globs"]
    out: dict[str, list[str]] = {name: [] for name in manifest["subjects"]}
    for path in refs.files(ref, "docs/"):
        if not path.endswith(".md") or exempt(path, globs):
            continue
        text = refs.read(ref, path) or ""
        for name, subject in manifest["subjects"].items():
            if declares(text, subject["detector"]):
                out[name].append(path)
    return {name: sorted(paths) for name, paths in out.items()}


def violations(ref: str) -> dict[str, list[str]]:
    """subject -> documents on `ref` that declare a subject they do not own."""
    manifest = load()
    found = {}
    for name, paths in declarers(ref).items():
        owner = manifest["subjects"][name]["owner"]
        trespassers = [p for p in paths if p != owner]
        if trespassers:
            found[name] = trespassers
    return found


def declarers_worktree() -> dict[str, list[str]]:
    """Same question, asked of the files on disk rather than of git.

    The distinction is not pedantry. Reading the ref means an edit is only
    checked once it is committed, which is one commit later than §4 of the
    root-cause brief requires — the defect surfaces after it is in history
    rather than before. The first version of this guard read the ref, and an
    equivalence test against the older hardcoded check caught it: the old check
    read the filesystem and failed, the new one read git and passed.
    """
    manifest = load()
    globs = manifest["exempt_globs"]
    out: dict[str, list[str]] = {name: [] for name in manifest["subjects"]}
    docs = Path(refs.REPO) / "docs"
    for path in sorted(docs.rglob("*.md")):
        rel = path.relative_to(refs.REPO).as_posix()
        if exempt(rel, globs):
            continue
        text = path.read_text(encoding="utf-8")
        for name, subject in manifest["subjects"].items():
            if declares(text, subject["detector"]):
                out[name].append(rel)
    return {name: sorted(paths) for name, paths in out.items()}


def violations_worktree() -> dict[str, list[str]]:
    manifest = load()
    found = {}
    for name, paths in declarers_worktree().items():
        owner = manifest["subjects"][name]["owner"]
        trespassers = [p for p in paths if p != owner]
        if trespassers:
            found[name] = trespassers
    return found
