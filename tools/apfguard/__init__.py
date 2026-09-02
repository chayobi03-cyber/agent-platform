"""apfguard — repository guards whose observation scope is the whole repository.

`tools/tests/test_docs_integrity.py` guards defects *within* a working tree.
Every check it makes reads `HEAD`. That is the right scope for the defects it
was written for and the wrong scope for the ones that followed: three documents
numbered `DEC-0001` on three refs, two different `BENCH-0004 Round 3`
executions reaching opposite conclusions, a benchmark recorded `UNTESTED` in
the register that another ref had already executed.

None of those defects exist inside any single working tree. Each one is a
disagreement *between* trees, so no check that reads one tree can see it, and
no amount of care inside one session can prevent it.

    apfbench/   how a benchmark is measured
    apfguard/   what the repository as a whole must not contradict

The split from `test_docs_integrity.py` is the scope, not the subject: these
checks read every ref, so they must talk to git rather than the filesystem.

Standard library only, matching `apfbench` — a guard that needs an install step
is one that will not run in the hook that is supposed to make it unskippable.
"""

from __future__ import annotations

__all__ = ["ledger", "refs", "divergence"]
