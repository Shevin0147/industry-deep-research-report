# Evidence Quality And Source Audit

## Source Audit Table

Build an internal source audit table for every report. Include a concise version in the final report.

Required fields:

| 来源名称 | 来源类型 | 可信度等级 | 使用内容 | 数据时间 | 是否支撑核心结论 |
|---|---|---|---|---|---|

Credibility levels:

- A: official, regulatory, statistical, government, exchange
- B: listed-company financial report, prospectus, platform official material
- C: brokerage, consulting company, industry association, database, professional research institution
- D: news, blog, ordinary webpage, self-media, forum, social content

Rules:

- Every key data point must map to at least one source.
- Every core conclusion must have at least one A/B/C-level source.
- D-level sources can only support cases, sentiment, examples, user language, and trend signals.
- If sources conflict, explain the reason and avoid false precision.
- If public evidence is missing, write `公开资料不足`, not invented data.

## Five-Dimensional Evidence Assessment

Keep A/B/C/D levels for report readability. Internally score each evidence item from 0 to 4 on:

- authority
- originality
- recency
- scope fit
- independence

Track `original_source_id`. Multiple pages repeating the same original source count as one independent source. Do not mechanically convert the five scores into A/B/C/D.

Build an internal claim-evidence matrix containing support, counterevidence, unresolved conflicts, confidence, validity conditions, falsifiers, and gaps. Every core claim must have qualifying A/B/C evidence and a documented counterevidence search.

For social, ecommerce, forum, and review samples, record date range, queries, sample size, deduplicated size, exclusion rules, and sample bias. Discussion volume is not proof of market size or willingness to pay.

## Universal Claim Types And Source Boundaries

Classify each claim as one of:

- `policy_regulation`
- `market_size`
- `demand`
- `product_effectiveness`
- `commercialization`
- `competition`
- `business_model`
- `unit_economics`
- `technical_feasibility`
- `operational_feasibility`
- `risk`

Each evidence item must declare `evidence_categories`, `supports_claim_types`, and `cannot_support_claim_types`. Never use evidence for a prohibited claim type.

Default boundaries:

- policy and industrial plans support policy direction, not market demand or commercial success
- regulatory approval supports market-access status, not clinical superiority, revenue, or adoption
- trial registration supports trial existence and design, not positive outcomes
- company disclosures support company claims and strategy, not independently verified market share or product effectiveness
- social and search signals support language, awareness, and hypotheses, not willingness to pay or market size
- broad population or disease burden supports need context, not addressable market without eligibility, access, payment, and capacity filters

For schema 1.1, also record `verifiability`, `conflict_of_interest`, `retrieved_at`, `original_source_url`, `evidence_excerpt`, and optional `content_hash`. Evidence for a core claim must contain a concise excerpt or structured data note showing what the source actually supports.

## Data Extraction Schema

For every important data point, extract:

```json
{
  "indicator": "指标名称",
  "value": "数值",
  "unit": "单位",
  "year_or_period": "年份或时间段",
  "region": "地区",
  "source": "来源",
  "source_level": "A/B/C/D",
  "note": "口径说明"
}
```

## Required Data Types

Extract when relevant:

- market size
- growth rate
- user scale
- penetration rate
- import/export value
- transaction value / GMV
- revenue
- profit
- price range
- cost structure
- industry concentration
- market share
- policy timeline
- regulatory change
- financing
- IPO or M&A information

## Conflict Handling

When one indicator has multiple public values:

1. List multiple sources and values.
2. Identify differences in time, geography, metric definition, statistical scope, or publication timing.
3. Keep conflicting values visible instead of silently deleting them.
4. Use a range, scenario, or scope-specific conclusion.
5. Explain the discrepancy in concise language.

Preferred wording:

`关于该指标，公开资料存在不同口径。A 来源披露为 xxx，B 来源披露为 xxx，差异可能来自统计范围、披露时间或是否包含某类业务。因此，本报告将其理解为 xxx-xxx 区间。`

## Quality Gates

Before finalizing:

- Key market-size numbers have A/B/C sources.
- Company financial figures use B-level sources where possible.
- Forecasts are marked as C-level estimates unless official.
- News and social sources are not used as sole evidence for core data.
- Unsupported exact numbers are removed or converted into assumptions.
- Assumption-based calculations are labeled as scenario analysis.
- Each major section contains analysis, not only extracted facts.
