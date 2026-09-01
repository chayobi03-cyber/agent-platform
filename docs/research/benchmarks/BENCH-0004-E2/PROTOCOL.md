# BENCH-0004-E2 — Frozen-Answer Evaluator Swap Protocol

**Status:** Protocol frozen / generation not executed
**Target claim:** CLM-0004 (downstream causal transfer)
**Does not adjudicate:** H07, H11 — see `docs/research/CLAIM_HYPOTHESIS_MAP.md`

## 1. Purpose

BENCH-0004 R1/R2 established retrieval/context-level effects only. E2 tests whether those
effects transfer to real LLM answer quality, and whether the mechanism ranking survives
evaluator replacement.

```text
R1/R2 + factorial audit          E2
(retrieval / context-level)  →   (answer-quality / causal transfer)
      PRIOR EVIDENCE                 THIS BENCHMARK
```

## 2. Execution gates

Gates are ordered. A gate may not be skipped or reordered.

```text
G1  bundle source bytes present
G2  byte-level fixture verification PASS      (tools/bench0004_e2/verify_fixture.py)
G3  generator model + version pinned, immutable
G4  single 1-pass generation over 96 contexts (tools/bench0004_e2/run_generator.py)
G5  answer set frozen + manifest emitted
G6  evaluators A/B/C score the identical frozen set
G7  variance decomposition                    (tools/bench0004_e2/analyze_e2.py)
G8  CLM-0004 verdict
```

Current position: **blocked at G1**.

## 3. Generation policy

- one pass only
- one frozen context per request
- no external information
- no hidden gold access
- no regeneration after first answer
- no post-hoc mutation of prompt, model, decoding, or context
- tools disabled
- answer SHA-256 required
- response ID required when available

## 4. Required answer record

`context_id`, `context_sha256`, `model_provider`, `model_version`,
`system_prompt_sha256`, `user_prompt_template_sha256`, `temperature`, `top_p`,
`max_tokens`, `seed`, `tools_enabled`, `generated_at_utc`, `response_id`,
`answer_sha256`, `answer`

### 4.1 Timestamp rule

`generated_at_utc` MUST be true UTC with a `Z` suffix (`2026-09-01T04:12:33Z`).
An offset-bearing local timestamp is rejected by the runner. This rule exists because
fixture lock v1 recorded a `+09:00` value in a field named `_utc`; that class of error
must not propagate into the answer set.

### 4.2 Seed rule

`seed` is recorded as declared, but is **best-effort on hosted APIs**. It MUST NOT be
described as guaranteeing reproducibility. Where the provider returns a system
fingerprint or equivalent, record it alongside. Absence of determinism is a limitation
to report, not a reason to re-run.

## 5. Partial-failure recovery

The original handoff stated "do not treat partial output as frozen" but defined no
recovery path. This section closes that gap.

A run is **atomic**. There are exactly two terminal outcomes.

```text
all 96 calls succeed   →  journal promoted to answers_96.jsonl  →  FROZEN
any call fails         →  run ABORTED, journal never promoted
```

On abort:

1. The runner stops immediately. It does not continue past a failed context.
2. The partial journal is moved to `runs/aborted/<utc-timestamp>/` together with an
   `ABORT_REASON.json` recording the failing `context_id`, the error, and how many
   contexts had completed.
3. Aborted journals are **retained as audit evidence** and are never deleted, never
   promoted, and never scored.
4. A new run starts from context 1 with the same fixture and the same pinned
   configuration. Resuming mid-run is prohibited: a resumed run would mix two
   generation sessions into one nominally single-pass answer set.

Retrying after a transport-level failure (timeout, 5xx, rate limit) is permitted
**within** the runner for the same context, up to a declared retry budget recorded in
the run configuration, because that does not change the generated answer set semantics.
A retry that produces a *completed* answer which is then discarded is prohibited —
the first completed answer for a context is the answer.

## 6. Prohibitions

- Do not regenerate answers when switching evaluators.
- Do not change model, prompt, decoding, or context after the first generation.
- Do not fill missing answers manually.
- Do not evaluate partial output as a frozen set.
- Do not fabricate answers or substitute a synthetic/rule-generated set.

## 7. Evaluator stage

Evaluators A, B, and C receive the byte-identical frozen answer set. Response variables:

- factual correctness
- evidence grounding
- temporal correctness
- relationship correctness
- provenance/citation correctness
- overall rubric score

## 8. Analysis model

```text
score ~ C(case) + T * R * P * evaluator
```

Reported terms: mechanism main effects, evaluator main effect, mechanism x evaluator
interaction, case block, residual.

Primary question: **does the mechanism ranking survive evaluator replacement?**

- Mechanism effects material across evaluators → confidence increases that the
  retrieval/context effect propagates to answer quality.
- Evaluator effect or mechanism x evaluator interaction dominates → the advantage is
  evaluator-sensitive and must not be promoted as an architecture invariant.
- Context-score gains that do not translate → CLM-0004 is weakened.
