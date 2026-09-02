"""Whether a benchmark measured what it declared — asserted, not grepped.

BENCH-0004 declared six primary measures and ran three rounds. A keyword search
for any of them across the execution records returns hits in all three, because
each record *says the metric was not measured*. A guard written the obvious way
reports full coverage on a benchmark that measured one of its six.

So the register carries a machine-readable measurement status per case, and a
measure may only be marked `measured` if a named key exists in committed raw
results. Prose cannot satisfy it; the key either is in the JSON or is not.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
REGISTER = REPO / "docs" / "research" / "BENCHMARK_REGISTER.md"
EXECUTIONS = REPO / "docs" / "research" / "executions"

CASE_RE = re.compile(r"^### (BENCH-\d{4}) —", re.M)
MEASURES_RE = re.compile(r"^\*\*(?:Primary m|M)easures:\*\*\s*(.+?)(?=\n\n)", re.M | re.S)
STATUS_BLOCK_RE = re.compile(
    r"^\*\*Measurement status:\*\*.*?\n```text\n(.*?)```", re.M | re.S)
STATUS_LINE_RE = re.compile(r"^\s*(.+?)\s*=\s*(measured:(\S+)|unmeasured)\s*$")


def cases() -> dict[str, str]:
    """BENCH id -> the text of its case block."""
    text = REGISTER.read_text(encoding="utf-8")
    marks = [(m.group(1), m.start()) for m in CASE_RE.finditer(text)]
    out = {}
    for i, (bench, start) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(text)
        out[bench] = text[start:end]
    return out


def declared_measures(block: str) -> list[str]:
    match = MEASURES_RE.search(block)
    if not match:
        return []
    raw = " ".join(match.group(1).split())
    return [m.strip() for m in raw.split(";") if m.strip()]


def measurement_status(block: str) -> dict[str, str | None] | None:
    """measure -> evidence key, or None for an explicitly unmeasured one.

    Returns None when the case declares no status block at all.
    """
    match = STATUS_BLOCK_RE.search(block)
    if not match:
        return None
    status: dict[str, str | None] = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        parsed = STATUS_LINE_RE.match(line)
        if not parsed:
            status[line.strip()] = "!unparseable"
            continue
        status[parsed.group(1)] = parsed.group(3)
    return status


def has_executions(block: str) -> bool:
    return "**Executions:**" in block


def evidence_keys() -> set[str]:
    """Every key present in committed raw-results JSON, dotted for nesting."""
    keys: set[str] = set()

    def walk(node, prefix=""):
        if isinstance(node, dict):
            for key, value in node.items():
                keys.add(f"{prefix}{key}")
                walk(value, f"{prefix}{key}.")
        elif isinstance(node, list) and node:
            walk(node[0], prefix)

    for path in sorted(EXECUTIONS.rglob("*.json")):
        try:
            walk(json.loads(path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
    return keys
