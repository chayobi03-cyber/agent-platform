#!/usr/bin/env python3
"""BENCH-0004-E2 gate G4 -- atomic one-pass generation over the 96 frozen contexts.

Enforces PROTOCOL.md: one pass, one frozen context per request, tools disabled,
no regeneration, no post-hoc mutation. A run is atomic -- either all 96 calls
succeed and the journal is promoted to answers_96.jsonl, or the run aborts and
the journal is retained under runs/aborted/ as audit evidence, never scored.

Standard library only; no provider SDK required.

Exit codes
  0  all 96 answers generated and frozen
  1  run aborted (a context failed) -- journal retained, nothing promoted
  2  precondition failure (gate not satisfied, config invalid, output exists)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_TOTAL = 96
TRANSPORT_ERRORS = (urllib.error.URLError, TimeoutError, ConnectionError)


def utc_now() -> str:
    """True UTC with a Z suffix. PROTOCOL 4.1 -- offset-bearing local time is rejected."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def precondition_failed(msg: str) -> "SystemExit":
    """Exit code 2 -- a gate or config precondition was not satisfied."""
    print(f"PRECONDITION FAILED: {msg}", file=sys.stderr)
    return SystemExit(2)


class Abort(Exception):
    def __init__(self, context_id: str, reason: str, completed: int):
        super().__init__(reason)
        self.context_id = context_id
        self.reason = reason
        self.completed = completed


# --------------------------------------------------------------------------
# provider adapters
# --------------------------------------------------------------------------
def _post(url: str, payload: dict, headers: dict, timeout: int) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **headers}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def call_openai(cfg: dict, system: str, user: str, timeout: int) -> tuple[str, str | None]:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    base = cfg.get("base_url", "https://api.openai.com/v1")
    payload = {
        "model": cfg["model_version"],
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "temperature": cfg["temperature"],
        "top_p": cfg["top_p"],
        "max_tokens": cfg["max_tokens"],
    }
    if cfg.get("seed") is not None:
        payload["seed"] = cfg["seed"]
    data = _post(f"{base}/chat/completions", payload, {"Authorization": f"Bearer {key}"}, timeout)
    return data["choices"][0]["message"]["content"], data.get("id")


def call_anthropic(cfg: dict, system: str, user: str, timeout: int) -> tuple[str, str | None]:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set")
    base = cfg.get("base_url", "https://api.anthropic.com/v1")
    payload = {
        "model": cfg["model_version"],
        "system": system,
        "messages": [{"role": "user", "content": user}],
        "temperature": cfg["temperature"],
        "top_p": cfg["top_p"],
        "max_tokens": cfg["max_tokens"],
    }
    data = _post(f"{base}/messages", payload,
                 {"x-api-key": key, "anthropic-version": "2023-06-01"}, timeout)
    return "".join(b.get("text", "") for b in data["content"]), data.get("id")


PROVIDERS = {"openai": call_openai, "anthropic": call_anthropic}


# --------------------------------------------------------------------------
def preflight(args, cfg: dict) -> tuple[list[dict], str, str]:
    """Verify every precondition before a single model call is made."""
    stamp_path = args.bundle / "VERIFICATION.json"
    if not stamp_path.is_file():
        raise precondition_failed(f"gate G2 not satisfied: {stamp_path} absent. Run verify_fixture.py first.")
    stamp = json.loads(stamp_path.read_text())
    if not stamp.get("all_pass"):
        raise precondition_failed(f"gate G2 FAILED in {stamp_path}: {stamp.get('failures')}")

    out = args.out_dir / "answers_96.jsonl"
    if out.exists():
        raise precondition_failed(
            f"refusing to overwrite an existing answer set: {out}\n"
            "PROTOCOL: no regeneration after first answer, no post-hoc mutation.")

    if cfg["model_version"] in ("", "UNSET", None):
        raise precondition_failed("model_version is UNSET -- gate G3 requires an immutable pinned version.")
    if cfg["provider"] not in PROVIDERS:
        raise precondition_failed(f"unknown provider {cfg['provider']!r}; known: {sorted(PROVIDERS)}")
    if cfg.get("tools_enabled"):
        raise precondition_failed("tools_enabled must be false -- PROTOCOL section 3.")

    contexts_path = args.bundle / "contexts_96.jsonl"
    records = [json.loads(l) for l in contexts_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    if len(records) != EXPECTED_TOTAL:
        raise precondition_failed(f"expected {EXPECTED_TOTAL} contexts, found {len(records)}")
    if sha256_file(contexts_path) != stamp["contexts_jsonl_sha256"]:
        raise precondition_failed("contexts_96.jsonl changed since verification -- re-run verify_fixture.py.")

    system = args.system_prompt.read_text(encoding="utf-8")
    template = args.user_template.read_text(encoding="utf-8")
    if "{context}" not in template:
        raise precondition_failed("user prompt template must contain the {context} placeholder.")
    return records, system, template


def generate(args, cfg, records, system, template, fields) -> list[dict]:
    journal = args.out_dir / "answers_96.partial.jsonl"
    journal.parent.mkdir(parents=True, exist_ok=True)
    if journal.exists():
        journal.unlink()

    fn = PROVIDERS[cfg["provider"]]
    sys_sha, tpl_sha = sha256_text(system), sha256_text(template)
    written: list[dict] = []

    with journal.open("w", encoding="utf-8") as jf:
        for n, rec in enumerate(records, 1):
            cid = rec[fields["id"]]
            user = template.replace("{context}", str(rec[fields["text"]]))
            answer = response_id = None
            last = ""
            # Retries cover transport failures only. A completed answer is never
            # discarded and re-requested -- PROTOCOL section 5.
            for attempt in range(1, args.retry_budget + 1):
                try:
                    answer, response_id = fn(cfg, system, user, args.timeout)
                    break
                except TRANSPORT_ERRORS as e:
                    last = f"transport: {e}"
                except urllib.error.HTTPError as e:
                    last = f"http {e.code}: {e.read()[:200]!r}"
                    if e.code not in (408, 429, 500, 502, 503, 504):
                        break
                except Exception as e:  # noqa: BLE001 -- recorded verbatim in the abort record
                    last = f"{type(e).__name__}: {e}"
                    break
                if attempt < args.retry_budget:
                    time.sleep(min(2 ** attempt, 30))
            if answer is None:
                raise Abort(cid, last or "unknown failure", len(written))

            row = {
                "context_id": cid,
                "context_sha256": rec[fields["sha"]],
                "model_provider": cfg["provider"],
                "model_version": cfg["model_version"],
                "system_prompt_sha256": sys_sha,
                "user_prompt_template_sha256": tpl_sha,
                "temperature": cfg["temperature"],
                "top_p": cfg["top_p"],
                "max_tokens": cfg["max_tokens"],
                "seed": cfg.get("seed"),
                "tools_enabled": False,
                "generated_at_utc": utc_now(),
                "response_id": response_id,
                "answer_sha256": sha256_text(answer),
                "answer": answer,
            }
            jf.write(json.dumps(row, ensure_ascii=False) + "\n")
            jf.flush()
            os.fsync(jf.fileno())
            written.append(row)
            print(f"  [{n:3d}/{EXPECTED_TOTAL}] {cid}  {row['answer_sha256'][:12]}")
    return written


def abort(args, exc: Abort) -> int:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = args.out_dir / "runs" / "aborted" / ts
    dest.mkdir(parents=True, exist_ok=True)
    journal = args.out_dir / "answers_96.partial.jsonl"
    if journal.exists():
        shutil.move(str(journal), str(dest / "answers.partial.jsonl"))
    (dest / "ABORT_REASON.json").write_text(json.dumps({
        "aborted_at_utc": utc_now(),
        "failing_context_id": exc.context_id,
        "error": exc.reason,
        "contexts_completed": exc.completed,
        "contexts_expected": EXPECTED_TOTAL,
        "promoted": False,
        "note": "Partial output is not a frozen set. Retained as audit evidence; never "
                "scored, never resumed. A new run restarts from context 1 with the same "
                "fixture and configuration (PROTOCOL section 5).",
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nRUN ABORTED at {exc.context_id} after {exc.completed}/{EXPECTED_TOTAL}", file=sys.stderr)
    print(f"  reason:  {exc.reason}", file=sys.stderr)
    print(f"  journal: {dest}", file=sys.stderr)
    print("  nothing was promoted. Resuming mid-run is prohibited.", file=sys.stderr)
    return 1


def freeze(args, cfg, rows) -> None:
    journal = args.out_dir / "answers_96.partial.jsonl"
    final = args.out_dir / "answers_96.jsonl"
    journal.replace(final)
    manifest = {
        "benchmark": "BENCH-0004-E2",
        "gate": "G5",
        "frozen_at_utc": utc_now(),
        "answer_count": len(rows),
        "answers_jsonl_sha256": sha256_file(final),
        "unique_answer_sha256": len({r["answer_sha256"] for r in rows}),
        "generator": {k: cfg.get(k) for k in
                      ("provider", "model_version", "temperature", "top_p", "max_tokens", "seed")},
        "tools_enabled": False,
        "system_prompt_sha256": rows[0]["system_prompt_sha256"],
        "user_prompt_template_sha256": rows[0]["user_prompt_template_sha256"],
        "response_ids_present": sum(1 for r in rows if r["response_id"]),
        "answer_sha256_by_context": {r["context_id"]: r["answer_sha256"] for r in rows},
        "policy": "one pass, one frozen context per request, tools disabled, no regeneration, "
                  "no post-hoc mutation. Evaluators A/B/C score this exact set.",
    }
    path = args.out_dir / "ANSWER_MANIFEST.json"
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\n{'=' * 60}")
    print(f"FROZEN  {len(rows)}/{EXPECTED_TOTAL} answers -> {final}")
    print(f"        answers_jsonl_sha256 {manifest['answers_jsonl_sha256']}")
    print(f"        manifest -> {path}")
    print("\nNext: submit this exact set to evaluators A, B and C. Do not regenerate.")


def main() -> int:
    ap = argparse.ArgumentParser(description="BENCH-0004-E2 one-pass generator (gate G4)")
    ap.add_argument("--bundle", required=True, type=Path)
    ap.add_argument("--out-dir", required=True, type=Path)
    ap.add_argument("--config", required=True, type=Path, help="JSON: provider, model_version, decoding")
    ap.add_argument("--system-prompt", required=True, type=Path)
    ap.add_argument("--user-template", required=True, type=Path)
    ap.add_argument("--retry-budget", type=int, default=3, help="transport-level retries per context")
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--dry-run", action="store_true", help="run every precondition, make no model call")
    args = ap.parse_args()

    cfg = json.loads(args.config.read_text())
    cfg.setdefault("temperature", 0.0)
    cfg.setdefault("top_p", 1.0)
    cfg.setdefault("max_tokens", 2048)
    cfg.setdefault("seed", None)

    records, system, template = preflight(args, cfg)
    stamp = json.loads((args.bundle / "VERIFICATION.json").read_text())
    fields = stamp["field_mapping"]

    print(f"BENCH-0004-E2 generation -- {cfg['provider']} / {cfg['model_version']}")
    print(f"  temperature={cfg['temperature']} top_p={cfg['top_p']} "
          f"max_tokens={cfg['max_tokens']} seed={cfg['seed']} tools=disabled")
    print(f"  contexts: {len(records)}  retry budget: {args.retry_budget} (transport only)\n")

    if args.dry_run:
        print("DRY RUN -- all preconditions satisfied, no model call made.")
        print("Remove --dry-run to execute the single generation pass.")
        return 0

    try:
        rows = generate(args, cfg, records, system, template, fields)
    except Abort as e:
        return abort(args, e)

    if len(rows) != EXPECTED_TOTAL:
        return abort(args, Abort("<final>", f"only {len(rows)} rows produced", len(rows)))
    freeze(args, cfg, rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
