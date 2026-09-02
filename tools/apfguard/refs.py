"""Reading the repository at every ref, not just the one checked out.

A guard that calls `Path.read_text()` can only ever see the working tree. These
helpers read blobs out of git objects instead, so a check can ask what a
document says on a branch nobody has checked out for three days.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

FETCH_HINT = (
    "git fetch origin '+refs/heads/*:refs/remotes/origin/*'"
)


def _git(*args: str) -> str:
    return subprocess.run(
        ("git", *args), cwd=REPO, check=True,
        capture_output=True, text=True,
    ).stdout


def _is_ancestor(a: str, b: str) -> bool:
    return subprocess.run(("git", "merge-base", "--is-ancestor", a, b),
                          cwd=REPO, capture_output=True).returncode == 0


def branch_refs() -> list[str]:
    """One ref per line of work: the most advanced state of each branch name.

    A branch usually exists twice, as `refs/heads/x` and `refs/remotes/origin/x`,
    and picking the wrong copy makes the guard lie in both directions. Taking the
    remote copy hides the session in progress — the local branch has the new
    commit and the guard reports the repository clean. Taking the local copy
    reads a `main` that is twelve commits stale.

    So each name resolves to whichever copy is not an ancestor of the other. If
    they have genuinely diverged, both are kept: that is not bookkeeping noise,
    it is two states of one branch and the guard should say so.
    """
    out = _git("for-each-ref", "--format=%(refname)", "refs/heads", "refs/remotes")
    all_refs = [r.strip() for r in out.splitlines()
                if r.strip() and not r.strip().endswith("/HEAD")]
    local = {r[len("refs/heads/"):]: r for r in all_refs
             if r.startswith("refs/heads/")}
    remote = {r.split("/", 3)[-1]: r for r in all_refs
              if r.startswith("refs/remotes/")}

    chosen: list[str] = []
    for name in sorted(set(local) | set(remote)):
        l, r = local.get(name), remote.get(name)
        if l and r:
            if _is_ancestor(l, r):
                chosen.append(r)
            elif _is_ancestor(r, l):
                chosen.append(l)
            else:
                chosen.extend((l, r))
        else:
            chosen.append(l or r)
    return chosen


def short(ref: str) -> str:
    for prefix in ("refs/remotes/origin/", "refs/remotes/", "refs/heads/"):
        if ref.startswith(prefix):
            return ref[len(prefix):]
    return ref


def exists(ref: str) -> bool:
    try:
        _git("rev-parse", "--verify", "--quiet", ref + "^{commit}")
        return True
    except subprocess.CalledProcessError:
        return False


def head(ref: str) -> str:
    return _git("rev-parse", ref).strip()


def files(ref: str, prefix: str = "") -> list[str]:
    out = _git("ls-tree", "-r", "--name-only", ref)
    paths = [p for p in out.splitlines() if p]
    return [p for p in paths if p.startswith(prefix)] if prefix else paths


def read(ref: str, path: str) -> str | None:
    try:
        return _git("show", f"{ref}:{path}")
    except subprocess.CalledProcessError:
        return None


def current() -> str | None:
    """The checked-out branch, if any. Work in progress is not stranded work."""
    name = _git("rev-parse", "--abbrev-ref", "HEAD").strip()
    return None if name == "HEAD" else name


def commits_not_in(ref: str, base: str) -> int:
    return len([c for c in _git("rev-list", f"{base}..{ref}").splitlines() if c])


def committed_at(ref: str) -> str:
    return _git("log", "-1", "--format=%cI", ref).strip()
