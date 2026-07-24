# Decision Model

Use this reference for reproducible market sizing and commercial feasibility analysis. Keep detailed calculations in `.research/model.json`; show only decision-relevant results in the existing report format.

## Market Sizing

Use both methods when feasible:

- top-down: credible total market narrowed by geography, customer, channel, category, and eligibility
- bottom-up: reachable customers or units multiplied by frequency and price

If one method is unavailable, record the reason and lower confidence.

Never calculate SOM as `TAM × arbitrary market share`. Constrain SOM by reachable customers, channel capacity, geographic coverage, supply capacity, acquisition budget, and conversion.

## Model Artifact

```json
{
  "schema_version": "1.0",
  "market_sizing": {
    "top_down": {"formula": "", "inputs": [], "result": 0, "unit": "", "scope": "", "limitations": []},
    "bottom_up": {"formula": "", "inputs": [], "result": 0, "unit": "", "scope": "", "limitations": []},
    "reconciliation": "",
    "som_constraints": []
  },
  "scenarios": [],
  "calculations": [],
  "sensitivity": [],
  "break_even": {},
  "limitations": []
}
```

Each input must use:

```json
{
  "name": "",
  "value": 0,
  "unit": "",
  "kind": "external_fact|internal_assumption",
  "evidence_id": "E1",
  "reason": ""
}
```

`evidence_id` is required for `external_fact` and must be empty for `internal_assumption`.

## Scenarios

Create `downside`, `base`, and `upside` scenarios. Each scenario must contain named inputs, formulas, outputs, margin when relevant, constraints, and a decision implication.

## Calculations

Record arithmetic that the validator can recompute:

```json
{
  "id": "M1",
  "label": "monthly_revenue",
  "operation": "multiply",
  "operands": [1000, 0.05, 100],
  "reported_result": 5000,
  "tolerance": 0.01
}
```

Supported operations are `add`, `subtract`, `multiply`, and `divide`. For `subtract` and `divide`, operands are evaluated from left to right.

## Sensitivity And Failure Thresholds

Identify the three variables that most affect the decision. For each, record its base/downside/upside values, effect on the decision metric, break-even or failure threshold, and monitoring signal. State the condition under which the project should stop, adjust, or continue.