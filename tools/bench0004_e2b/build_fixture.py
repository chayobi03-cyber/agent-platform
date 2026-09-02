#!/usr/bin/env python3
"""BENCH-0004-E2b -- build the 96-context fixture from the APF repository.

E2b is a NEW benchmark, not a recovery of the BENCH-0004-E2 fixture. Its
contexts are built from real repository history: 25 commits, six versions of
SESSION_STATE.md, and four genuine supersession events. The temporal,
relationship and provenance structure is authentic rather than planted; the
declared limitation is that the corpus domain is APF itself.

Deterministic: identical repository state produces identical bytes, which is
what makes the emitted lock meaningful.

Emits, into --out:
  contexts_96.jsonl              the frozen fixture
  canonical_context_manifest.json
  bundle_manifest.json
  generator_contract.json
  stage1_context_scores.json     E2b's own context-sufficiency factorial
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
from collections import defaultdict
from pathlib import Path

CELLS = [(t, r, p) for t in (0, 1) for r in (0, 1) for p in (0, 1)]
TOP_K = 3
TOKEN = re.compile(r"[a-z0-9]{2,}")


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def tokenize(s: str) -> list[str]:
    return TOKEN.findall(s.lower())


def build_corpus(paths: set[str], at_commit: str) -> list[dict]:
    """Every committed version of every gold-reachable document, with real commit
    metadata. Multiple versions of one path are distinct corpus entries -- that is
    what makes temporal filtering a real operation rather than a label."""
    corpus = []
    for path in sorted(paths):
        log = git("log", "--reverse", "--format=%H|%aI|%an|%s", at_commit, "--", path).strip()
        if not log:
            continue
        for n, line in enumerate(log.splitlines(), 1):
            sha, iso, author, subject = line.split("|", 3)
            try:
                text = git("show", f"{sha}:{path}")
            except subprocess.CalledProcessError:
                continue
            corpus.append({
                "doc_id": f"{path}@v{n}",
                "path": path,
                "version": n,
                "commit": sha[:12],
                "committed_at": iso,
                "author": author,
                "subject": subject,
                "text": text,
            })
    return corpus


def current_version(corpus: list[dict], path: str, as_of: str) -> int | None:
    """Version of `path` current as of a date -- the temporal ground truth."""
    versions = [c for c in corpus if c["path"] == path and c["committed_at"][:10] <= as_of]
    return max((c["version"] for c in versions), default=None)


def tfidf_rank(query: str, corpus: list[dict], allowed: list[int]) -> list[int]:
    """Plain TF-IDF cosine. This is the baseline retriever every cell shares;
    T/R/P act on top of it, never inside it."""
    docs = [tokenize(corpus[i]["text"]) for i in allowed]
    df: dict[str, int] = defaultdict(int)
    for d in docs:
        for term in set(d):
            df[term] += 1
    n = len(docs) or 1
    idf = {t: math.log(n / (1 + c)) + 1.0 for t, c in df.items()}

    def vec(tokens):
        tf: dict[str, int] = defaultdict(int)
        for t in tokens:
            tf[t] += 1
        v = {t: (1 + math.log(c)) * idf.get(t, 0.0) for t, c in tf.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {t: x / norm for t, x in v.items()}

    q = vec(tokenize(query))
    scored = []
    for pos, i in enumerate(allowed):
        d = vec(docs[pos])
        sim = sum(q[t] * d.get(t, 0.0) for t in q)
        scored.append((-sim, corpus[i]["doc_id"], i))
    scored.sort()
    return [i for _, _, i in scored]


def expand(selected: list[int], corpus: list[dict], relations: list[list[str]],
           allowed: set[int]) -> list[int]:
    """One-hop expansion along declared relations, newest allowed version per path."""
    neigh: dict[str, set[str]] = defaultdict(set)
    for a, b in relations:
        neigh[a].add(b)
        neigh[b].add(a)
    out = list(selected)
    seen_paths = {corpus[i]["path"] for i in selected}
    for i in selected:
        for target in sorted(neigh.get(corpus[i]["path"], ())):
            if target in seen_paths:
                continue
            cands = [j for j in allowed if corpus[j]["path"] == target]
            if cands:
                out.append(max(cands, key=lambda j: corpus[j]["version"]))
                seen_paths.add(target)
    return out


def render(indices: list[int], corpus: list[dict], t: int, p: int, as_of: str,
           question: str) -> str:
    """The rendered context is the complete generator input: it carries the
    question and the retrieved evidence. A context without its question is not
    answerable, and the generator contract forbids supplying the question
    separately.

    T and P contribute independently. T supplies version currency, P supplies
    attribution; setting P must not suppress what T contributes, or the two
    factors stop being separable."""
    parts = [f"QUESTION: {question}", "EVIDENCE:"]
    for i in indices:
        c = corpus[i]
        fields = [f"source: {c['path']}"]
        if t:
            fields.append(f"version {c['version']}, valid as of {as_of}")
        if p:
            fields.append(f"commit {c['commit']}")
            fields.append(f"committed {c['committed_at']}")
            fields.append(f"author {c['author']}")
        parts.append(f"[{' | '.join(fields)}]\n{c['text'].rstrip()}")
    return parts[0] + "\n\n" + parts[1] + "\n\n" + "\n\n---\n\n".join(parts[2:])


def score(indices: list[int], corpus: list[dict], case: dict, t: int, p: int) -> float:
    """Fraction of declared gold evidence present in a form that can actually
    answer the question. Requirements are declared per case in cases.json before
    any context was built, not inferred from the result."""
    gold = case["gold"]
    dep = set(case["depends_on"])
    hits = 0.0
    for path in gold:
        picked = [i for i in indices if corpus[i]["path"] == path]
        if not picked:
            continue
        credit = 1.0
        if "T" in dep:
            want = current_version(corpus, path, case["as_of"])
            if want is not None and not any(corpus[i]["version"] == want for i in picked):
                credit = 0.0          # a stale version cannot answer a temporal question
        if "P" in dep and not p:
            credit = 0.0              # the answer requires attribution the context lacks
        hits += credit
    return hits / len(gold)


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the BENCH-0004-E2b fixture")
    ap.add_argument("--cases", type=Path, default=Path("tools/bench0004_e2b/cases.json"))
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--at-commit", default="HEAD",
                    help="pin the corpus to this commit. The corpus is built from committed "
                         "history, so it changes as the repository grows; without a pin the "
                         "fixture cannot be rebuilt identically after the next commit.")
    args = ap.parse_args()
    at = git("rev-parse", args.at_commit).strip()

    spec = json.loads(args.cases.read_text())
    cases, relations = spec["cases"], spec["relations"]

    paths = {g for c in cases for g in c["gold"]}
    for a, b in relations:
        paths.add(a)
        paths.add(b)
    corpus = build_corpus(paths, at)
    print(f"corpus pinned at {at[:12]}")
    print(f"corpus: {len(corpus)} document versions across {len(paths)} paths")
    multi = sorted({c['path'] for c in corpus if c['version'] > 1})
    print(f"  paths with real revision history: {len(multi)}")

    args.out.mkdir(parents=True, exist_ok=True)
    records, stage1 = [], []

    for t, r, p in CELLS:
        cell = f"T{t}R{r}P{p}"
        for case in cases:
            if t:  # temporal filtering: only versions current as of the question's date
                allowed = [i for i, c in enumerate(corpus)
                           if c["version"] == current_version(corpus, c["path"], case["as_of"])]
            else:  # no temporal awareness: every version competes
                allowed = list(range(len(corpus)))

            ranked = tfidf_rank(case["question"], corpus, allowed)
            selected = ranked[:TOP_K]
            if r:
                selected = expand(selected, corpus, relations, set(allowed))

            text = render(selected, corpus, t, p, case["as_of"], case["question"])
            s = score(selected, corpus, case, t, p)
            cid = f"{cell}-{case['case_id']}"
            records.append({
                "context_id": cid,
                "cell": cell,
                "case_id": case["case_id"],
                "T": t, "R": r, "P": p,
                "question": case["question"],
                "retrieved": [corpus[i]["doc_id"] for i in selected],
                "context": text,
                "context_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            })
            stage1.append({"context_id": cid, "cell": cell, "case_id": case["case_id"],
                           "T": t, "R": r, "P": p, "context_score": round(s, 4)})

    # ---- emit ------------------------------------------------------------
    contexts = args.out / "contexts_96.jsonl"
    contexts.write_text("".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n"
                                for x in records), encoding="utf-8")

    rows = sorted(({"context_id": x["context_id"], "context_sha256": x["context_sha256"],
                    "cell": x["cell"]} for x in records), key=lambda x: x["context_id"])
    manifest = args.out / "canonical_context_manifest.json"
    manifest.write_text(json.dumps(rows, sort_keys=True, separators=(",", ":"),
                                   ensure_ascii=False) + "\n", encoding="utf-8")

    contract = {
        "benchmark": "BENCH-0004-E2b",
        "generation_policy": {
            "one_pass_only": True, "one_frozen_context_per_request": True,
            "no_external_information": True, "no_hidden_gold_access": True,
            "no_regeneration_after_first_answer": True, "no_posthoc_mutation": True,
            "tools_enabled": False, "answer_sha256_required": True,
            "response_id_required_when_available": True,
        },
        "prompt_construction": {
            "system_prompt": "supplied at run time as a file; its SHA-256 is recorded per answer",
            "user_template": "supplied at run time; must contain the {context} placeholder",
            "context_field": "context",
            "note": "The context is passed verbatim. The question is embedded in the context "
                    "record and must not be re-supplied separately.",
        },
        "required_record_fields": [
            "context_id", "context_sha256", "model_provider", "model_version",
            "system_prompt_sha256", "user_prompt_template_sha256", "temperature",
            "top_p", "max_tokens", "seed", "tools_enabled", "generated_at_utc",
            "response_id", "answer_sha256", "answer"],
    }
    contract_p = args.out / "generator_contract.json"
    contract_p.write_text(json.dumps(contract, indent=2, sort_keys=True,
                                     ensure_ascii=False) + "\n", encoding="utf-8")

    def sh(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    bundle = {
        "benchmark": "BENCH-0004-E2b",
        "context_count": len(records),
        "cells": {f"T{t}R{r}P{p}": sum(1 for x in records if x["cell"] == f"T{t}R{r}P{p}")
                  for t, r, p in CELLS},
        "corpus_versions": len(corpus),
        "corpus_pinned_at_commit": at,
        "case_set_version": spec["case_set_version"],
        "contents": {"contexts_96.jsonl": sh(contexts),
                     "canonical_context_manifest.json": sh(manifest),
                     "generator_contract.json": sh(contract_p)},
    }
    bundle_p = args.out / "bundle_manifest.json"
    bundle_p.write_text(json.dumps(bundle, indent=2, sort_keys=True,
                                   ensure_ascii=False) + "\n", encoding="utf-8")
    (args.out / "stage1_context_scores.json").write_text(
        json.dumps(stage1, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"\ncontexts: {len(records)}  "
          f"unique ids: {len({x['context_id'] for x in records})}  "
          f"unique sha: {len({x['context_sha256'] for x in records})}")
    print("\nexpected_sha256 for the lock:")
    for k, v in [("contexts_jsonl", sh(contexts)),
                 ("canonical_context_manifest", sh(manifest)),
                 ("declared_bundle_manifest", sh(bundle_p)),
                 ("generator_contract", sh(contract_p))]:
        print(f"  {k:28} {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
