#!/bin/bash
# APF session-start gate.
#
# Every failure this repository has repeated was invisible at the moment a
# session started: SESSION_STATE two executions out of date, a benchmark listed
# as the next action that another branch had already run, three decisions
# numbered DEC-0001. Each was discoverable from git in under two seconds. None
# was discovered, because nothing looked.
#
# This runs the guard suite before the session reads anything, and prints the
# result into the session's context. It does not exit non-zero: blocking a
# session from starting on a repository that is *already* in violation would
# make the first task impossible to do. The hard gate is CI
# (.github/workflows/apf-guards.yml); this one exists so a session cannot begin
# by believing a stale document.
set -uo pipefail

cd "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}" || exit 0

# The cross-ref checks compare branches. Without this they compare one branch
# to itself and pass by seeing nothing.
git fetch --quiet origin '+refs/heads/*:refs/remotes/origin/*' 2>/dev/null || true

output=$(python3 -m unittest discover -s tools/tests 2>&1)
status=$?

if [ $status -eq 0 ]; then
  echo "APF guards: $(echo "$output" | grep -oE 'Ran [0-9]+ tests') passed."
  echo "Divergence ledger: $(python3 - <<'PY' 2>/dev/null || echo 'unreadable'
import sys
sys.path.insert(0, "tools")
from apfguard import ledger
d = ledger.load()
print(", ".join(f"{s.replace(chr(95), chr(32))}: {len(d.get(s, {}))}"
                for s in ledger.SECTIONS))
PY
)"
else
  echo "############################################################"
  echo "# APF GUARDS FAILED — do not plan against this repository"
  echo "# state until these are read. Each one is a defect this"
  echo "# project has already made once."
  echo "############################################################"
  echo "$output" | grep -vE '^\s*$' | tail -60
  echo "############################################################"
  echo "# Reproduce: python3 -m unittest discover -s tools/tests -v"
  echo "############################################################"
fi
exit 0
