# Research Protocol

Use this protocol for every research run. It strengthens the research process without changing the final 10-section report format.

## Research Modes

| Mode | Purpose | Independent support per core claim | Hypotheses | Search reflection |
|---|---|---:|---:|---|
| `quick` | Screen whether deeper work is justified | 1 A/B/C source | 3 | after major query groups |
| `standard` | Default decision report | 2 independent sources, including 1 A/B/C | 3 | after each search round |
| `deep` | Higher-stakes diligence | 3 independent sources, including 2 A/B/C where public evidence permits | 3 or more | after each search round |

If the evidence threshold cannot be met, do not manufacture coverage. Record the limitation, lower confidence, and identify the primary research or paid data needed.

## Industry Routing And Decision Levels

Keep research depth (`quick|standard|deep`) separate from decision level:

- `L1`: whether to continue research
- `L2`: whether to run an MVP or low-cost validation
- `L3`: whether to commit a team and commercial budget
- `L4`: whether to invest, acquire, or scale materially

For schema 1.1, `brief.json` must include `industry_family`, optional `secondary_industry_family`, `evidence_packs`, and `decision_level`. Load one primary pack and at most one secondary pack. Use `core` only when classification is uncertain and record a routing warning.

The validator computes the highest supported decision level. Missing pack evidence produces warnings at L1. If requested L2-L4 evidence is insufficient, block finalization and report the highest supported level.

Schema 1.0 remains readable and defaults to L1 with compatibility warnings; it must not be subjected to new blocking pack requirements.

## Competing Hypotheses

Before selecting a thesis:

1. Define at least three mutually distinguishable hypotheses.
2. For each, define expected evidence, disconfirming evidence, open questions, and a falsifier.
3. Search for both support and counterevidence.
4. Compare hypotheses only after evidence audit.
5. Select the thesis with the best evidence fit, not the most attractive narrative.

Every final core claim must record validity conditions, falsification conditions, confidence (`high`, `medium`, or `low`), support evidence IDs, counterevidence IDs, and unresolved gaps.

## Search Reflection And Stopping

After each search round record new decision-relevant information, source independence and lineage, remaining gaps, counterevidence still needed, next queries, and whether stopping conditions are met.

Stop when all are true:

- the five decision questions can be answered
- mode-specific evidence coverage is met or limitations are explicit
- major conflicts have been reconciled or retained visibly
- another search round is unlikely to change the decision

Also stop after two consecutive search rounds produce no material new evidence. Do not pad the source list with low-quality repetitions.

## Structured Research Artifacts

Store internal artifacts under `reports/<topic-slug>/.research/`. These files are not report chapters.

### `brief.json`

```json
{
  "schema_version": "1.0",
  "mode": "standard",
  "topic": "",
  "scope": "",
  "geography": "",
  "time_range": "",
  "target_reader": "",
  "research_goal": "",
  "decision_questions": [],
  "limitations": []
}
```

### `hypotheses.json`

```json
{
  "schema_version": "1.0",
  "hypotheses": [
    {
      "id": "H1",
      "statement": "",
      "expected_evidence": [],
      "support_evidence_ids": [],
      "counterevidence_ids": [],
      "falsifier": "",
      "gaps": [],
      "status": "selected|rejected|unresolved"
    }
  ]
}
```

### `evidence.json`

```json
{
  "schema_version": "1.0",
  "evidence": [
    {
      "id": "E1",
      "indicator": "",
      "value": "",
      "unit": "",
      "period": "",
      "region": "",
      "scope": "",
      "source_title": "",
      "url": "",
      "source_level": "A|B|C|D",
      "published_at": "",
      "original_source_id": "E1",
      "is_external_fact": true,
      "scores": {"authority": 0, "originality": 0, "recency": 0, "scope_fit": 0, "independence": 0},
      "notes": ""
    }
  ],
  "platform_samples": [
    {"platform": "", "date_range": "", "queries": [], "sample_size": 0, "deduplicated_size": 0, "exclusion_rules": [], "biases": []}
  ]
}
```

Scores use integers from 0 to 4. Source level and dimensional scores serve different purposes; do not convert one mechanically into the other. Items sharing `original_source_id` count as one independent source.

### `claims.json`

```json
{
  "schema_version": "1.0",
  "claims": [
    {
      "id": "C1",
      "statement": "",
      "core": true,
      "support_evidence_ids": [],
      "counterevidence_ids": [],
      "confidence": "high|medium|low",
      "valid_if": [],
      "falsified_if": [],
      "gaps": [],
      "report_section": ""
    }
  ]
}
```

### `model.json`

Follow `references/decision-model.md`.

### `validation.json`

Generated by `scripts/validate_report.py`. Do not edit it manually.

## Graded Quality Gates

Blocking errors:

- missing required artifact or invalid JSON shape
- fewer than three competing hypotheses
- no selected hypothesis
- core claim without qualifying evidence
- external fact or key number missing source, period, or scope
- report URL not represented in the evidence register
- missing entry judgment, biggest risk, or validation path
- inconsistent arithmetic in a declared model calculation

Warnings:

- low-confidence core claim
- mode-specific independent-source target not met
- old evidence
- incomplete counterevidence search
- weak platform sample
- limited sensitivity coverage

Warnings do not block output, but decision-relevant limitations must be disclosed.