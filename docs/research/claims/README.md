# APF Claim State Index

Single place to see what every claim's state actually is. `docs/research/CLAIM_INVENTORY.md` holds the claim statements and the record template; this file holds their current state and record status.

## States

`current_state` uses the CLAIM_INVENTORY section 4 enum only:

```text
DISCOVERED | FORMULATED | TESTABLE | UNDER_TEST | SUPPORTED | WEAKENED | CONTRADICTED | FALSIFIED | INCONCLUSIVE
```

`record_status` is separate and says whether a completed claim record exists:

- **COMPLETE** — a record file exists and passes the CLAIM_INVENTORY section 5 quality gate
- **PENDING** — no record yet; will be completed when its benchmark is prepared (DEC-0002 option C)
- **INSUFFICIENT** — no record, no benchmark queued, and evidence coverage is not sufficient to write one; tracked as a gap, not an oversight

## Index

| Claim | P0 | current_state | record_status | Benchmark | Record |
|---|:--:|---|---|---|---|
| CLM-0001 Work-centric generality | ● | **CONTRADICTED** (F4 fired) | COMPLETE | BENCH-0001 executed | [CLM-0001.md](CLM-0001.md) |
| CLM-0002 Capture value | ● | FORMULATED | PENDING | BENCH-0002 queued | — |
| CLM-0003 Progressive disclosure | | FORMULATED | **INSUFFICIENT** | none queued | — |
| CLM-0004 Structured retrieval (broad) | ● | WEAKENED / INCONCLUSIVE | PENDING | BENCH-0004 R1, R2 | — |
| CLM-0005 Failed attempts as evidence | | FORMULATED | **INSUFFICIENT** | none queued | — |
| CLM-0006 Provenance trust | ● | FORMULATED | PENDING | BENCH-0006, no execution record | — |
| CLM-0007 Human boundary value | ● | FORMULATED | PENDING | BENCH-0007 queued | — |
| CLM-0008 Primitives over framework copying | | FORMULATED | **INSUFFICIENT** | none queued | — |
| CLM-0009 Measured automation value | ● | FORMULATED | PENDING | BENCH-0009 queued | — |
| CLM-0010 Engineering augmentation thesis | | FORMULATED | **INSUFFICIENT** | none queued | — |
| CLM-0011 Cross-document chain recovery | | **SUPPORTED** (one corpus, k ≤ 5) | COMPLETE | BENCH-0004 R3 | [CLM-0011.md](CLM-0011.md) |

## The four INSUFFICIENT claims

CLM-0003, CLM-0005, CLM-0008, and CLM-0010 have no completed record and no queued benchmark. DEC-0002 section 5 accepts that, on the condition they carry the label rather than sitting blank — an incomplete record that is marked incomplete is a tracked gap; one that looks unstarted is indistinguishable from an oversight.

None of them may be cited as evidence for anything while in this state.

## Vocabulary correction

DEC-0002 section 5 says to mark these claims `INSUFFICIENT` "per the corpus map stop condition". `INSUFFICIENT` belongs to the corpus map's *asset* vocabulary and is not a member of the CLAIM_INVENTORY claim-state enum, so applying it to `current_state` would have made the enum meaningless.

It is applied here to `record_status` instead, which is what DEC-0002 was actually describing — whether a record exists and is adequate — while `current_state` keeps the enum it is defined over. DEC-0002's intent is unchanged; only the field it lands in is corrected. No decision record needs amending, since DEC-0002 does not turn on which field carries the label.

## Related

- Claim statements and record template: `../CLAIM_INVENTORY.md`
- Record completion timing: `../../decisions/DEC-0002-claim-record-completion-timing.md`
- Promotion gate: `../../decisions/DEC-0001-evidence-gate.md`
- Corpora: `../corpora/`

## Standing contradiction

CLM-0001 is `CONTRADICTED` as worded, and `CONSTITUTION.md` section 2 rests on it. The contradiction is recorded, not resolved: amending a Constitution invariant requires explicit review under its own section 9, and the decision belongs to a human under DEC-0001. Until then, section 2 should be read as carrying a known exception for agentic workloads rather than as an established generality.
