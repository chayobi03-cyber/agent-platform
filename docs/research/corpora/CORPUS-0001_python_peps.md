# CORPUS-0001 — Python Enhancement Proposals

**Status:** Frozen / available for benchmark execution
**Role:** First independent engineering corpus, satisfying DEC-0001 exit criterion 1

## 1. Why an independent corpus was required

Every APF benchmark executed so far ran on APF's own repository. BENCH-0004 Round 2 lists this as its first limitation, and DEC-0001 makes it exit criterion 1: no claim leaves the evidence gate on a corpus that is APF's own development history.

The reason is not procedural. A corpus written by the same project that is testing a retrieval hypothesis contains relations that were authored with that hypothesis in mind. Round 2's relationship graph was hand-specified by the same author as the corpus — its own limitation 2. Any result from that arrangement measures the author's consistency, not the mechanism.

## 2. Source

| Field | Value |
|---|---|
| Source | `github.com/python/peps` |
| Frozen commit | `a4f4971816e2edf74ce90672df91f01e87df0ce5` |
| Documents | 737 PEPs with parseable headers (`peps/pep-*.rst`) |
| License | PEPs are public domain or CC0 per PEP 1 |
| Access | Anonymous public git read |
| Local checkout used | `/home/user/python/peps` (not vendored into this repository) |

The corpus is not committed here. It is a public repository at a pinned commit; the commit SHA is the provenance record, and re-running the benchmark requires a fresh clone at that SHA.

## 3. Why this corpus fits the claim under test

The claim under test concerns recovery of multi-document evidence chains where the answer depends on history, version transitions, or causal relations. PEPs supply that structure natively, and — critically — supply it from third parties.

| Requirement | How CORPUS-0001 satisfies it | Coverage |
|---|---|---|
| Independent of APF | Authored by the Python community since 2000; no relationship to this project | Complete |
| Revision transitions | `Post-History` records real revision dates | 633 / 737 documents |
| Evidence transitions | `Status` transitions (Draft → Accepted → Final → Superseded / Rejected / Withdrawn) | 737 / 737 |
| Causal / supersession relations | `Superseded-By` (31), `Replaces` (36), `Requires` (27) | 94 declared relations |
| Decision provenance | `Resolution` links to the message where the decision was made | 257 / 737 |
| Configuration transitions | `Python-Version` targets | 522 / 737 |
| Authorship provenance | `Author` | 737 / 737 |

## 4. The property that matters most

Ground truth and the mechanism under test come from **different channels**:

```text
ground truth      ←  header-declared relations (Superseded-By / Replaces / Requires)
                     written by PEP authors, years before this benchmark existed

mechanism under   ←  PEP-to-PEP references extracted from document bodies
test (condition D2)  by the benchmark, never given the header relations
```

This is what Round 2 could not do. There, the relation graph and the corpus had the same author, so traversal success was partly guaranteed by construction. Here the benchmark must rediscover, from body text, relations that someone else declared in headers — and it can fail.

The overlap between the two channels is itself measured and reported (`graph_ground_truth_edge_overlap`) rather than assumed.

## 5. Known limitations — recorded before execution

1. **Domain mismatch.** PEPs are software-process decision records. APF's target workload is EMC/PCB engineering. A result here is evidence about the retrieval mechanism, not about transfer to the target domain. Under DEC-0001 exit criterion 3, any promotion must be worded to the mechanism, not the domain.
2. **Configuration transitions are weak.** `Python-Version` is a coarse target-version field, not the revision/configuration/tool/setup provenance CLM-0006 concerns. This corpus does not discharge BENCH-0006.
3. **Structured by construction.** PEPs are unusually well-structured for engineering documents. Real engineering history is messier, so this corpus likely flatters any structure-exploiting condition. That biases toward the claim, which is the wrong direction for a falsification attempt, and must be stated in any result.
4. **Relation sparsity.** 94 declared relations across 737 documents. The chain task set is therefore small relative to the corpus, and dominated by supersession rather than by other relation types.
5. **Single corpus.** One corpus is not independent replication (benchmark rule B6). A second corpus in a different domain is required before the mechanism claim generalizes.

## 6. What this corpus can and cannot settle

**Can:** whether relationship, temporal, or provenance structure recovers cross-document evidence chains better than a semantic baseline, and which of the three mechanisms carries any advantage.

**Cannot:** whether that advantage survives in EMC/PCB engineering history; whether it survives on unstructured or noisy corpora; anything about CLM-0006 provenance trust; anything about end-user engineering productivity.

## 7. Related

- Decisions: DEC-0001 (exit criterion 1)
- Claims: CLM-0011, CLM-0004
- Benchmarks: BENCH-0004 Round 3
- Prior executions: `docs/research/executions/BENCH-0004_RUN_2026-08-31.md`, `docs/research/executions/BENCH-0004_R2_2026-08-31.md`
