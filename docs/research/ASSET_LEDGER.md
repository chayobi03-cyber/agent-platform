# APF Research Asset Ledger

**Status:** Initial foundation; no asset is accepted by default.

## State Model

```text
RAW_FINDING → ASSET_CANDIDATE → REVIEWED → ACCEPTED_ASSET
```

A research finding is not an APF rule. Adoption requires evidence, analysis, and an explicit human decision where consequential.

## Asset Record Template

```yaml
asset_id:
title:
status:
source:
source_type:
primitive:
entities:
relationships:
lifecycle:
control:
execution:
evidence:
ownership:
failure_mode:
security_boundary:
finding:
counter_evidence:
apf_relevance:
architectural_impact:
recommendation:
adoption: ADOPT | REFERENCE | DEFER | REJECT
confidence:
related_assets:
related_decisions:
evidence_links:
```

## Evidence Classes

- EXTERNAL_EVIDENCE
- REPOSITORY_EVIDENCE
- RUNTIME_EVIDENCE
- EVALUATION_EVIDENCE
- HUMAN_DECISION_EVIDENCE

## Initial Research Tracks

### P0

- Work / Opportunity
- Backstage
- Temporal
- LangGraph
- OpenFGA
- OPA
- MCP
- OpenTelemetry
- Phoenix / Evaluation
- Identity / Authorization

### P1

- A2A
- OpenHands / Sandbox
- Agent Security
- FinOps
- Agent Governance
- Operational Knowledge

## Research Rule

For every external source, extract architectural primitives rather than copying its framework-specific model. Cross-source agreement increases confidence; contradictions must be recorded explicitly.

## Asset Records

Records are appended here as research produces them. The template above is
authoritative; a record that omits a field omits it because the field is not yet
known, and says so.

### ASSET-0001

```yaml
asset_id: ASSET-0001
title: ODB++ as a net-resolved geometry source
status: ASSET_CANDIDATE
source: ODB++ Design Format Specification (rel. 8.1); ulikoehler/ODBPy; sjgallagher2/ODBplusplus-Parser; nam20485/OdbDesign
source_type: format specification (unread this session) + two independent implementations
primitive: a fabrication data package that carries geometry and connectivity in one model
entities: job, step, layer, feature (line/arc/pad/surface/text/barcode), symbol, net, subnet, package, component, drill
relationships: feature -> net and subnet via steps/<step>/eda/data; layer -> type/polarity via matrix/matrix; symbol table scoped to one feature file
lifecycle: authored in ECAD, exported per release, consumed by CAM/DFM; the archive is a snapshot, not a live model
control: none - the format is inert data; control belongs to whatever reads it
execution: parse -> unit normalisation -> polarity-ordered fold -> geometry per layer per net
evidence: record syntax verified by reading two independent parser implementations that agree (surface S/SE, contour OB/OS/OC/OE, unit record U)
ownership: Siemens EDA publishes the format; the job file is owned by whoever produced the design
failure_mode: polarity mishandled inverts every derived result; missing eda/data removes net attribution entirely; per-file symbol scope violated silently corrupts pad geometry
security_boundary: a job file is design IP; parsing is local and read-only, and no part of this method requires transmitting it
finding: connectivity, not geometry, is what makes ODB++ more useful than an image or a Gerber set for this class of check
counter_evidence: net attribution is optional in practice; features can be absent from eda/data or carry $NONE$, in which case the advantage disappears for those features
apf_relevance: an instance of a work input that carries its own semantics - relevant to whether the work-centric abstraction holds outside APF's own corpus
architectural_impact: none yet
recommendation: verify section 3 of the methodology document against the specification before any adoption
adoption: DEFER
confidence: medium for the data model, low for exact record syntax beyond what the two parsers implement
related_assets: ASSET-0002
related_decisions: none
evidence_links: docs/research/PCB_ODB_SHIELDING_INSPECTION_METHODOLOGY.md
```

### ASSET-0002

```yaml
asset_id: ASSET-0002
title: Vector-verdict / rendered-evidence inspection pattern
status: ASSET_CANDIDATE
source: analysis in docs/research/PCB_ODB_SHIELDING_INSPECTION_METHODOLOGY.md; corroborated by how Allegro, HyperLynx DRC and Valor NPI structure equivalent checks
source_type: derived analysis + secondary vendor material
primitive: compute the verdict in the exact representation; render only to evidence a verdict already reached
entities: source model, derived exact geometry, check, finding, evidence artefact, validation raster
relationships: finding -> coordinates -> evidence crop; independent raster XOR derived raster -> parse-gap report
lifecycle: parse -> normalise -> check -> finding -> evidence; evidence is downstream of the verdict, never upstream
control: check parameters are design intent and must be supplied, not inferred
execution: exact geometry for verdicts; raster for human review and for self-validation
evidence: resolution budget in tools/research/pcb_shield_budget.py - a whole-board raster able to measure a 50um gap to +/-5um costs ~9GB per copper stack, while a cheap raster is provably blind to a 25um gap
ownership: whoever owns the check parameters owns the verdict
failure_mode: rendering becomes the substrate and the verdict inherits quantization error and loses semantics; or evidence is generated independently of findings and stops corresponding to them
security_boundary: evidence artefacts embed design coordinates and net names and inherit the source data's confidentiality
finding: an image is the right output of an inspection and the wrong input to one
counter_evidence: raster is representation-agnostic and still shows copper a parser failed to understand; the pattern only holds because that virtue is preserved as the XOR cross-check
apf_relevance: generalises beyond PCB - any check where a human-readable artefact is confused with the measurement substrate
architectural_impact: none yet
recommendation: hold as a candidate pattern; a prototype now executes it end to end on synthetic jobs, but not against a real job or a second renderer
adoption: DEFER
confidence: medium - arithmetic reproducible and the pattern runs; the XOR self-validation half is still unexecuted
related_assets: ASSET-0001, ASSET-0003
related_decisions: none
evidence_links: docs/research/PCB_ODB_SHIELDING_INSPECTION_METHODOLOGY.md, tools/research/pcb_shield_budget.py, tools/pcbshield/
```

### ASSET-0003

```yaml
asset_id: ASSET-0003
title: Injected-defect validation pattern for geometric checkers
status: ASSET_CANDIDATE
source: analysis in docs/research/PCB_ODB_SHIELDING_INSPECTION_METHODOLOGY.md section 10
source_type: derived analysis
primitive: construct ground truth by injection so that detection rate, localisation error and size error are all measurable without an oracle
entities: clean corpus, injected defect (class, position, size), detection, null control, agreement matrix
relationships: injected defect -> expected finding; clean board -> expected silence
lifecycle: predeclare measures and falsifier -> inject -> run -> score -> record raw results
control: the injection specification is the ground truth and must be frozen before the run
execution: paired runs over injected and clean corpora
evidence: executed once - tools/tests/test_pcbshield.py injects five defect classes at known coordinates; all five detected and located, clean-board null control silent. The null control failed on the first run and caught two real defects in the checker plus one physically invalid fixture
ownership: whoever predeclares the falsifier
failure_mode: injected defects drawn from the same assumptions as the checker, so the test confirms the implementation rather than testing it; recall reported without a false-positive rate; and - observed on the first run - a fixture that is physically invalid, so the checker's correct answer looks like a false positive
security_boundary: none beyond the source data
finding: the null control, not the detection rate, is what makes this a falsification test
counter_evidence: injection cannot produce the defect classes nobody thought to inject, so a passing score bounds nothing about unknown classes
apf_relevance: same shape as the falsification-benchmark protocol already used in this repository, applied to a geometric rather than a retrieval checker
architectural_impact: none
recommendation: predeclare before executing, using docs/research/executions/BENCH-0004_R3_PREDECLARATION.md as the template. This run was not predeclared, so it demonstrates the pattern rather than testing a claim with it
adoption: DEFER
confidence: medium - executed once, on a fixture whose writer shares assumptions with the reader under test
related_assets: ASSET-0002
related_decisions: none
evidence_links: docs/research/PCB_ODB_SHIELDING_INSPECTION_METHODOLOGY.md
```
