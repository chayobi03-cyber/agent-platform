# BENCH-0004-E2b fixture builder

Builds the E2b 96-context fixture from the APF repository's own committed history.

```bash
python3 tools/bench0004_e2b/build_fixture.py --out <dir> --at-commit <sha>
```

**Always pass `--at-commit`.** The corpus is built from committed history, so it changes as the
repository grows. Without a pin the fixture cannot be rebuilt identically after the next commit.
The committed fixture is pinned at `a0bc5a6`, recorded in its lock and bundle manifest.

Determinism is the point: rebuilding at the pinned commit reproduces byte-identical output, so
any reviewer can regenerate the fixture and recompute the Stage 1 result rather than taking it
on trust.

## Case set

`cases.json` holds twelve engineering-history questions with declared gold evidence and declared
scoring requirements, frozen before any context was built or scored. Editing it invalidates the
lock — rebuild and re-lock rather than editing in place.

## What the factors do

All three act on a shared TF-IDF cosine retriever, never inside it.

| | Off | On |
|---|---|---|
| **T** | every committed version competes | only the version current as of the question's date; context carries version currency |
| **R** | top-k only | top-k plus one-hop expansion along declared relations |
| **P** | bare text | commit, date, author, path |

T and P contribute independently. An earlier revision let P suppress what T contributed, which
collapsed six context pairs into identical bytes; the factors are not separable if one can mask
the other.

The rendered context carries its question. A context without its question is not an answerable
generator input, and the generator contract forbids supplying the question separately.

## Verification and running

The E2b fixture uses the same G2/G4/G7 tooling as E2:

```bash
python3 tools/bench0004_e2/verify_fixture.py \
  --bundle docs/research/benchmarks/BENCH-0004-E2b/fixture \
  --lock   docs/research/benchmarks/BENCH-0004-E2b/FIXTURE_LOCK.json
```

## E2b is not E2

E2b is a new benchmark, not a recovery of the BENCH-0004-E2 fixture, whose bytes were never in
this repository. E2b's hashes are its own and must never be compared against the E2 lock.
