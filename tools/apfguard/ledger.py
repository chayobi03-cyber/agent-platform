"""The divergence ledger: what makes the guard green on arrival and unable to rot.

The repository already contains five unreconciled divergences. A guard that
simply failed on all of them would be red on its first run and stay red, and a
permanently red check is one people learn to ignore — the failure mode this
whole investigation is about.

So the guard fails on *unrecorded* divergence. Recording one costs a ref name, a
head SHA and a disposition, all of which git verifies. Three properties follow,
and they are the reason this is not "write a document saying you know":

  stale   a recorded head SHA that no longer matches means the branch moved
          after someone decided what to do about it; the decision was made
          against different content, so it fails again.
  orphan  a ledger entry with nothing left to describe fails. The ledger
          retires its own rows — which is exactly what the document set never
          did, 21 files added and 0 removed.
  blind   a recorded ref that this clone cannot resolve fails, because a guard
          that cannot see the refs it is supposed to compare is not passing,
          it is not looking.
"""

from __future__ import annotations

import json
from pathlib import Path

LEDGER = Path(__file__).resolve().parent / "divergence_ledger.json"

SECTIONS = (
    "decision_id_collisions",
    "untested_but_executed",
    "execution_collisions",
    "divergent_refs",
)


def load() -> dict:
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    for section in SECTIONS:
        data.setdefault(section, {})
    return data


def entry_refs(section: str, body: dict) -> dict[str, str]:
    """The ref -> head-sha map an entry pins itself to."""
    return dict(body.get("refs", {}))


def reconcile(section: str, observed: dict, recorded: dict) -> list[str]:
    """Compare what git shows against what the ledger claims. Returns problems."""
    problems = []
    for key in sorted(set(observed) - set(recorded)):
        problems.append(
            f"{section}: '{key}' is not in the divergence ledger. "
            f"Record it in {LEDGER.relative_to(LEDGER.parents[2])} with the refs "
            f"it spans, their current head SHAs, and a disposition.")
    for key in sorted(set(recorded) - set(observed)):
        problems.append(
            f"{section}: ledger entry '{key}' no longer describes anything "
            f"observable. Remove it — the ledger must retire its own rows.")
    for key in sorted(set(observed) & set(recorded)):
        was = list(recorded[key].get("claimants", []))
        now = list(observed[key].get("claimants", []))
        if was != now:
            problems.append(
                f"{section}: '{key}' changed who is in it. Recorded {was}, "
                f"found {now}. A row already marked known must not absorb new "
                f"divergence silently — re-decide and re-record.")
    return problems


def stale_pins(recorded: dict, current_heads: dict[str, str]) -> list[str]:
    """A pinned SHA that moved, or a ref this clone cannot see at all."""
    problems = []
    for section in SECTIONS:
        for key, body in sorted(recorded.get(section, {}).items()):
            for ref, sha in sorted(entry_refs(section, body).items()):
                if ref not in current_heads:
                    problems.append(
                        f"{section}/{key}: ref '{ref}' is not visible in this "
                        f"clone, so the guard cannot compare it. Run: "
                        f"git fetch origin '+refs/heads/*:refs/remotes/origin/*'")
                elif current_heads[ref] != sha:
                    problems.append(
                        f"{section}/{key}: ref '{ref}' moved "
                        f"{sha[:8]} -> {current_heads[ref][:8]} since this "
                        f"disposition was recorded. Re-decide and re-pin.")
    return problems
