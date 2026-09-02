#!/usr/bin/env python3
"""apf — a capture-and-find tool for engineering work.

Trial instrument, not APF implementation. It commits to no architecture and
carries no claim. Its only job is to be used or not used for two weeks.

Design constraints it is built against:
  * Zero ceremony. Capture takes no required fields and no schema choice.
  * Plain files. If this tool is abandoned, the notes stay readable and
    greppable. Nothing is locked in a database.
  * Stdlib only. No install step, no API key, no network, no service.
  * Summary first. Results are one line each until asked for more.

Usage:
    apf c "trace impedance came out 8 ohms low on rev C"
    apf c                      # reads stdin, or opens $EDITOR on a terminal
    cat notes.txt | apf c
    apf c -f sim/result.png "post-layout, 3.2GHz peak"
    apf f impedance rev c
    apf f "8 ohms" --full
    apf recent
    apf stats

Storage: $APF_HOME (default ~/.apf)
    entries/YYYY/MM/<id>.md   one file per capture, YAML-ish front matter
    usage.jsonl               one line per invocation
"""

import argparse
import datetime as dt
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from collections import defaultdict

HOME = os.environ.get("APF_HOME") or os.path.expanduser("~/.apf")
ENTRIES = os.path.join(HOME, "entries")
USAGE = os.path.join(HOME, "usage.jsonl")

TOKEN_RE = re.compile(r"[a-z0-9]+")
ID_REF_RE = re.compile(r"#(\d{8}T\d{6}Z-[0-9a-f]{4})")
PATH_RE = re.compile(r"(?:^|\s)((?:~|\.{0,2}/)[^\s,;]+)")
URL_RE = re.compile(r"https?://[^\s,;\"'<>]+")
# Relation propagation weight. 0.5 is the value BENCH-0004 round 3 measured on
# an independent corpus; it is not tuned here and is not load-bearing at small N.
BETA = 0.5


# ---------------------------------------------------------------- utilities

def now():
    return dt.datetime.now(dt.timezone.utc)


def new_id(when, body):
    h = hashlib.sha1(f"{when.isoformat()}{body}".encode()).hexdigest()[:4]
    return f"{when.strftime('%Y%m%dT%H%M%SZ')}-{h}"


def tokenize(s):
    return TOKEN_RE.findall(s.lower())


def git_context(cwd):
    def run(*args):
        try:
            out = subprocess.run(["git", "-C", cwd, *args], capture_output=True,
                                 text=True, timeout=3)
            return out.stdout.strip() if out.returncode == 0 else ""
        except Exception:
            return ""
    top = run("rev-parse", "--show-toplevel")
    if not top:
        return {}
    return {k: v for k, v in (
        ("repo", os.path.basename(top)),
        ("branch", run("rev-parse", "--abbrev-ref", "HEAD")),
        ("commit", run("rev-parse", "--short", "HEAD")),
    ) if v}


def infer_project(cwd, git):
    """Project is inferred, never asked for. Explicit --project overrides."""
    if git.get("repo"):
        return git["repo"]
    return os.path.basename(os.path.abspath(cwd)) or "unfiled"


def log_usage(cmd, **extra):
    os.makedirs(HOME, exist_ok=True)
    rec = {"ts": now().isoformat(), "cmd": cmd, **extra}
    with open(USAGE, "a") as f:
        f.write(json.dumps(rec) + "\n")


# ------------------------------------------------------------- entry format

def write_entry(entry):
    when = dt.datetime.fromisoformat(entry["created"])
    d = os.path.join(ENTRIES, when.strftime("%Y"), when.strftime("%m"))
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, entry["id"] + ".md")
    meta = {k: v for k, v in entry.items() if k != "body"}
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(json.dumps(meta, indent=2, sort_keys=True))
        f.write("\n---\n")
        f.write(entry["body"].rstrip() + "\n")
    return path


def read_entry(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    if raw.startswith("---\n"):
        _, meta, body = raw.split("---\n", 2)
        try:
            entry = json.loads(meta)
        except json.JSONDecodeError:
            entry = {}
    else:
        entry, body = {}, raw
    entry["body"] = body.strip()
    entry.setdefault("id", os.path.splitext(os.path.basename(path))[0])
    entry["path"] = path
    return entry


def load_all():
    out = []
    for root, _, files in os.walk(ENTRIES):
        for fn in files:
            if fn.endswith(".md"):
                out.append(read_entry(os.path.join(root, fn)))
    out.sort(key=lambda e: e.get("created", ""))
    return out


# ------------------------------------------------------------------ capture

def read_body(args):
    if args.text:
        return " ".join(args.text)
    if not sys.stdin.isatty():
        return sys.stdin.read()
    editor = os.environ.get("EDITOR")
    if editor:
        import tempfile
        with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False) as tf:
            tmp = tf.name
        subprocess.call([editor, tmp])
        body = open(tmp, encoding="utf-8").read()
        os.unlink(tmp)
        return body
    print("reading until EOF (ctrl-D to finish):", file=sys.stderr)
    return sys.stdin.read()


def extract_refs(body, extra_files):
    """Links are extracted, never entered. Only paths that exist are kept."""
    refs = []
    for m in ID_REF_RE.findall(body):
        refs.append({"kind": "entry", "value": m})
    for u in URL_RE.findall(body):
        refs.append({"kind": "url", "value": u})
    for p in PATH_RE.findall(body):
        full = os.path.abspath(os.path.expanduser(p))
        if os.path.exists(full):
            refs.append({"kind": "file", "value": full})
    for p in extra_files or []:
        full = os.path.abspath(os.path.expanduser(p))
        ref = {"kind": "file", "value": full, "exists": os.path.exists(full)}
        if ref["exists"]:
            try:
                with open(full, "rb") as f:
                    ref["sha1"] = hashlib.sha1(f.read()).hexdigest()[:12]
                ref["bytes"] = os.path.getsize(full)
            except OSError:
                pass
        refs.append(ref)
    seen, uniq = set(), []
    for r in refs:
        key = (r["kind"], r["value"])
        if key not in seen:
            seen.add(key)
            uniq.append(r)
    return uniq


def cmd_capture(args):
    body = read_body(args).strip()
    if not body and not args.file:
        print("nothing captured (empty input)", file=sys.stderr)
        return 1
    when = now()
    cwd = os.getcwd()
    git = git_context(cwd)
    entry = {
        "id": new_id(when, body),
        "created": when.isoformat(),
        "project": args.project or infer_project(cwd, git),
        "tags": args.tag or [],
        "refs": extract_refs(body, args.file),
        "cwd": cwd,
        "source": "cli",
    }
    if git:
        entry["git"] = git
    entry["body"] = body or f"(files only: {', '.join(args.file or [])})"
    path = write_entry(entry)
    log_usage("capture", id=entry["id"], project=entry["project"],
              chars=len(entry["body"]), refs=len(entry["refs"]))
    print(f"{entry['id']}  {entry['project']}"
          + (f"  {len(entry['refs'])} ref(s)" if entry["refs"] else ""))
    if args.verbose:
        print(path)
    return 0


# ---------------------------------------------------------------- retrieval

def build_index(entries):
    df, tfs = defaultdict(int), []
    for e in entries:
        text = f"{e.get('project','')} {' '.join(e.get('tags',[]))} {e['body']}"
        counts = defaultdict(int)
        for t in tokenize(text):
            counts[t] += 1
        tfs.append(counts)
        for t in counts:
            df[t] += 1
    n = max(len(entries), 1)
    idf = {t: math.log(1 + n / c) for t, c in df.items()}
    vecs = []
    for counts in tfs:
        v = {t: (1 + math.log(c)) * idf.get(t, 0.0) for t, c in counts.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vecs.append({t: x / norm for t, x in v.items()})
    return vecs, idf


def neighbours(entries):
    """One-hop edges: explicit entry refs and shared file or URL refs.

    Shared project is deliberately NOT an edge. Everything in a project shares
    it, so using it makes the graph near-complete and propagation lifts the
    whole project instead of the related entries — the same collapse BENCH-0004
    round 3 measured when the propagation weight was pushed too high. Project is
    a filter (see find -p), not a relation.
    """
    by_id = {e["id"]: i for i, e in enumerate(entries)}
    shared = defaultdict(list)
    edges = defaultdict(set)
    for i, e in enumerate(entries):
        for r in e.get("refs", []):
            if r["kind"] in ("file", "url"):
                shared[r["value"]].append(i)
            elif r["kind"] == "entry" and r["value"] in by_id:
                j = by_id[r["value"]]
                edges[i].add(j)
                edges[j].add(i)
    for group in shared.values():
        if 1 < len(group) <= 12:   # a file touched by everything relates nothing
            for i in group:
                for j in group:
                    if i != j:
                        edges[i].add(j)
    return edges


def search(entries, query, limit, recency_days=180, project=None):
    if project:
        entries = [e for e in entries if e.get("project") == project]
    if not entries:
        return []
    vecs, idf = build_index(entries)
    counts = defaultdict(int)
    for t in tokenize(query):
        counts[t] += 1
    q = {t: (1 + math.log(c)) * idf.get(t, 0.0) for t, c in counts.items()}
    norm = math.sqrt(sum(x * x for x in q.values())) or 1.0
    q = {t: x / norm for t, x in q.items()}

    phrase = query.strip().lower()
    ref = now()
    base = []
    for i, e in enumerate(entries):
        s = sum(x * vecs[i].get(t, 0.0) for t, x in q.items())
        if len(phrase) > 2 and phrase in e["body"].lower():
            s += 0.35                      # exact phrase beats topical match
        try:
            age = (ref - dt.datetime.fromisoformat(e["created"])).days
            s *= 1 + 0.15 * math.exp(-max(age, 0) / recency_days)
        except (ValueError, KeyError):
            pass
        base.append(s)

    edges = neighbours(entries)
    scored = list(base)
    for i in range(len(entries)):
        nb = edges.get(i)
        if nb:
            scored[i] = base[i] + BETA * max(base[j] for j in nb)

    ranked = sorted(range(len(entries)), key=lambda i: -scored[i])
    return [(entries[i], scored[i], base[i]) for i in ranked[:limit]
            if scored[i] > 1e-9]


def summarize(body, width=88):
    line = next((l.strip() for l in body.splitlines() if l.strip()), "")
    return line[:width] + ("…" if len(line) > width else "")


def show(hits, full):
    if not hits:
        print("no matches")
        return
    for e, score, base in hits:
        day = e.get("created", "")[:10]
        via = " ↗" if score - base > 1e-9 else "  "   # surfaced via a relation
        print(f"{day} {e.get('project','?'):16.16s}{via} {summarize(e['body'])}")
        if full:
            for line in e["body"].splitlines():
                print(f"    {line}")
            for r in e.get("refs", []):
                print(f"    · {r['kind']}: {r['value']}")
            print(f"    · id {e['id']}  {e.get('path','')}")
            print()


def cmd_find(args):
    entries = load_all()
    hits = search(entries, " ".join(args.query), args.limit, project=args.project)
    log_usage("find", query_len=len(" ".join(args.query)), n_results=len(hits),
              corpus=len(entries), scoped=bool(args.project))
    show(hits, args.full)
    return 0


def cmd_recent(args):
    entries = load_all()[-args.limit:][::-1]
    log_usage("recent", n_results=len(entries))
    show([(e, 0.0, 0.0) for e in entries], args.full)
    return 0


# -------------------------------------------------------------------- stats

def cmd_stats(args):
    entries = load_all()
    if not entries:
        print("no entries yet")
        return 0
    days = defaultdict(int)
    projects = defaultdict(int)
    for e in entries:
        days[e.get("created", "")[:10]] += 1
        projects[e.get("project", "?")] += 1

    first = min(days)
    last = max(days)
    span = (dt.date.fromisoformat(last) - dt.date.fromisoformat(first)).days + 1
    active = len(days)

    gaps, prev = [], None
    for d in sorted(days):
        cur = dt.date.fromisoformat(d)
        if prev:
            gaps.append((cur - prev).days - 1)
        prev = cur
    today = now().date()
    since_last = (today - dt.date.fromisoformat(last)).days

    print(f"entries        {len(entries)}")
    print(f"span           {first} → {last}  ({span} days)")
    print(f"active days    {active} of {span}  ({active / span:.0%})")
    print(f"per active day {len(entries) / active:.1f}")
    print(f"longest gap    {max(gaps) if gaps else 0} days")
    print(f"last capture   {since_last} day(s) ago")
    print("\nprojects")
    for p, c in sorted(projects.items(), key=lambda kv: -kv[1])[:8]:
        print(f"  {c:4d}  {p}")

    print("\nlast 14 days")
    for i in range(13, -1, -1):
        d = (today - dt.timedelta(days=i)).isoformat()
        n = days.get(d, 0)
        print(f"  {d}  {'█' * min(n, 30)}{'' if n else '·'} {n or ''}")

    finds = 0
    if os.path.exists(USAGE):
        for line in open(USAGE):
            try:
                if json.loads(line).get("cmd") == "find":
                    finds += 1
            except json.JSONDecodeError:
                pass
    print(f"\nsearches run   {finds}")
    print("\nThe trial question is whether you reach for this unprompted.")
    print("Active-day rate and searches run are the evidence; the rest is texture.")
    log_usage("stats", entries=len(entries), active_days=active)
    return 0


# --------------------------------------------------------------------- main

def main(argv=None):
    p = argparse.ArgumentParser(prog="apf", description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("capture", aliases=["c"], help="capture something")
    c.add_argument("text", nargs="*", help="text; omit to read stdin or $EDITOR")
    c.add_argument("-f", "--file", action="append", help="attach a file path")
    c.add_argument("-t", "--tag", action="append", help="optional tag")
    c.add_argument("-p", "--project", help="override the inferred project")
    c.add_argument("-v", "--verbose", action="store_true")
    c.set_defaults(func=cmd_capture)

    f = sub.add_parser("find", aliases=["f"], help="find something")
    f.add_argument("query", nargs="+")
    f.add_argument("-n", "--limit", type=int, default=10)
    f.add_argument("--full", action="store_true", help="show bodies and refs")
    f.add_argument("-p", "--project", help="restrict to one project")
    f.set_defaults(func=cmd_find)

    r = sub.add_parser("recent", help="most recent captures")
    r.add_argument("-n", "--limit", type=int, default=10)
    r.add_argument("--full", action="store_true")
    r.set_defaults(func=cmd_recent)

    s = sub.add_parser("stats", help="usage, for the two-week verdict")
    s.set_defaults(func=cmd_stats)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
