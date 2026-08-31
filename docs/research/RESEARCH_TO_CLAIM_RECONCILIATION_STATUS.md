# APF Research → Claim Reconciliation Status v0.1

**Status:** Working inventory; not complete

## What is known

The APF repository currently contains a Research Asset Ledger and a separate Claim/Falsification layer. The Ledger explicitly keeps findings from becoming APF rules without evidence and human decision. The current phase therefore treats the Claim Inventory as a verification index, not as an architecture specification.

## Current reconciliation coverage

### Repository-native research assets

| Source family | Current handling | Confidence |
|---|---|---:|
| Research Asset Ledger | canonical intake/index | High |
| Engineering Work Augmentation lessons | converted into candidate product/engineering claims | Medium |
| Capture-first UX lessons | mapped primarily to CLM-0002 and related claims | Medium |
| History / retrieval lessons | mapped primarily to CLM-0004 | Medium |
| Provenance / trust lessons | mapped primarily to CLM-0006 | Medium |
| Human accountability / HoTL governance | mapped primarily to CLM-0007 | High |
| Automation value thesis | mapped primarily to CLM-0009 | Medium |

## Known limitation

The repository contains the formalized foundation and recent research artifacts, but this does **not** prove that every research finding from prior conversational sessions has been recovered. Conversation-derived assets that were never persisted to the repository remain a reconciliation gap.

Therefore the phase is explicitly marked:

```text
CORPUS_RECONCILIATION = PARTIAL
```

and not `COMPLETE`.

## Required next reconciliation pass

1. Recover every persisted research asset and source note available to the project.
2. Extract atomic claims rather than importing conclusions wholesale.
3. Link each claim to support and counter-evidence.
4. Identify duplicate and contradictory claims.
5. Mark missing source provenance as a gap; do not silently fill it.
6. Give every P0 claim a benchmark or an explicit `INSUFFICIENT` status.

## Important negative finding

The current repository structure is not yet sufficient to claim that APF's architectural thesis has been empirically validated. The evidence base is still primarily research, governance, and candidate-hypothesis material. This is expected at this phase and should remain visible.

## Exit criterion

Do not move from `CORPUS_RECONCILIATION = PARTIAL` to `COMPLETE` until the provenance gap above has been addressed with a recorded inventory or an explicit statement of inaccessible source history.
