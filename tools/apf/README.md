# apf — capture and find

A trial instrument, not APF implementation. It commits to no architecture and carries no claim. Its job is to be used or not used for two weeks.

## Run it

No install, no dependencies, no API key, no network. Python 3.8+.

```sh
alias apf='python3 /path/to/agent-platform/tools/apf/apf.py'
```

## Four commands

```sh
apf c "rev C diff pair came out 8 ohms low on TDR, suspect the prepreg swap"
apf c                       # stdin, or $EDITOR on a terminal
cat notes.txt | apf c
apf c -f sim/rev_c_tdr.csv "TDR trace, 100ps rise"

apf f impedance             # one line per hit
apf f prepreg --full        # bodies and refs
apf f "acid trap" -p boardX # scoped to one project

apf recent
apf stats                   # the two-week verdict
```

Capture takes no required fields. Project, timestamp, working directory, and git repo/branch/commit are inferred. Tags exist and are optional; you never have to pick a type, a category, or a place to put something.

## What it links, and what it does not

Two entries are related if one references the other by `#<id>`, or if they reference the same file or URL. That is all.

Shared project is deliberately **not** a relation. Everything in a project shares it, so treating it as one makes the graph near-complete and drags the whole project into every result — the same collapse BENCH-0004 round 3 measured when propagation was pushed too hard. Project is a filter.

A `↗` in the output means the entry surfaced through a relation rather than its own words. That is the one retrieval mechanism this project has independent evidence for, and it is bounded: it only helps where a link actually exists. Writing `#<id>` when you resolve something is what makes the history navigable later.

## Storage

`$APF_HOME`, default `~/.apf`:

```
entries/YYYY/MM/<id>.md    one file per capture, JSON front matter, plain body
usage.jsonl                one line per invocation
```

Readable, greppable, git-able. If this tool is abandoned the notes survive it, which is the point — a trial instrument must not be able to take your notes down with it.

## What it deliberately does not do

No server, no database, no sync, no LLM, no embeddings, no UI, no schema, no tagging discipline, no capture template. Retrieval is lexical plus one-hop relation propagation. Every one of those is a thing to add only if two weeks of use produces a reason.

## The trial

The question is not whether it is good. It is whether you reach for it unprompted.

`apf stats` reports active-day rate and searches run. After two weeks, if you did not reach for it without being reminded, the honest move is to stop — the project's own standard, applied to the project.
