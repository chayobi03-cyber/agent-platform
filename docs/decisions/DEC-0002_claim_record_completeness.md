# DEC-0002 — Resolve the gap between the claim quality gate and inventory practice

**Status:** `PROPOSED — awaiting human decision`
**Raised:** 2026-09-02
**Raised by:** `APF_PROJECT_AUDIT_2026-09-02.md` finding F3
**Decision owner:** Project owner (human). **This record must not be self-approved.**
**Constitution basis:** §4 state separation, §5 evidence before architecture

## 1. The gap

`CLAIM_INVENTORY.md` §5 states a claim is `TESTABLE` only when six elements are present.
Measured across the inventory on 2026-09-02:

| Element | Claims having it |
|---|---:|
| bounded statement | 13/13 |
| falsifier | 13/13 |
| explicit scope | 3/13 |
| explicit non-scope | 3/13 |
| observable prediction | 3/13 |
| minimum evidence | 3/13 |

The three are `CLM-0004a/b/c`, entered 2026-09-02. The §4 record template defines 23 fields and
is populated for none.

BENCH-0004 was nonetheless executed against `CLM-0004`, which does not meet the gate. The runs
were not invalid — R1 and R2 both predeclared falsifiers, which is the operative protection —
but the document's stated rule and the project's actual practice disagree, and one of them is
wrong.

## 2. Options

**Option A — complete the records for the P0 claims.**
Fill scope, non-scope, observable prediction and minimum evidence for `CLM-0001`, `CLM-0002`,
`CLM-0006`, `CLM-0007`, `CLM-0009`.

*Cost:* these fields are claim **definitions**, not descriptions. For five claims with no
executed evidence, writing them means deciding now what each claim will and will not assert.
That is owner work; done speculatively it puts untested assertions into the inventory wearing
the appearance of rigour.

**Option B — amend §5 to state the minimum actually in use.**
Declare that `statement + falsifier` makes a claim executable, and that the full six-element
form is required only before a claim may transition out of `UNDER_TEST`.

*Cost:* weakens the stated gate. Requires this decision record as the justification trail
(§5 itself and `FALSIFICATION_BENCHMARK.md` both warn against changing rules after seeing
results).

**Option C — A for P0 claims as each is scheduled, B as the standing rule.**
Keep `statement + falsifier` as the bar for executing a benchmark; require the full six elements
before the claim's first execution, produced as part of preparing that benchmark rather than in
bulk now.

## 3. Recommendation

**Option C.** It matches what actually happened with `CLM-0004a/b/c`: those three could be
completed only because an executed factorial had already defined what was measured. Writing the
same fields for claims with no evidence inverts that order. Option C also keeps the queue
moving — `BENCH-0006` is next, so `CLM-0006` would be completed as part of preparing it, not as
a documentation exercise detached from the experiment.

## 4. Scope

This decision governs record completeness only. It does not change any claim's state, does not
promote anything, and does not alter the falsifier requirement, which stays mandatory before
execution under all three options.

## 5. Human decision

```text
Decision:        [ ] OPTION A   [ ] OPTION B   [ ] OPTION C   [ ] REVISE
Decided by:
Date:
Notes:
```
