# Product Entry Decision Report Template

Use this template when the user is evaluating an early product direction, startup idea, software/app opportunity, MVP, productized service, or "should I enter this niche" question.

The output must be a decision-grade market entry report, not a broad industry encyclopedia. It should answer:

- Is this worth entering?
- Under what conditions is it worth entering?
- Who should be targeted first?
- What should the first product boundary be?
- What should not be built yet?
- How should retention/payment be validated?
- What evidence would stop the project?

Write in Chinese unless the user requests another language.

## Core Writing Rules

- Be direct, specific, and judgment-heavy.
- Do not write academic prose or generic market background.
- Do not use broad market size as proof that the startup/product will work.
- Separate confirmed external evidence from internal assumptions.
- If data is unavailable, write `待验证假设` instead of inventing numbers.
- Every section should end with a short `小结判断`.
- Use tables heavily. Prefer decision tables, validation tables, risk tables, and competitive matrices.
- Keep the body to 10 first-level sections plus optional appendices.
- The conclusion must state: `建议小成本验证，不建议一开始重投入` unless evidence strongly supports another decision.
- Treat the first stage as a validation project, not a full product launch.

## Required 10-Section Structure

### 1. 执行摘要

300-500 Chinese characters.

Must include:

- whether the product/market is worth entering
- why it may work now
- biggest risk
- first-stage validation path
- clear conclusion: small-cost validation vs. heavy investment

Avoid vague optimism. Say exactly when to continue and when to stop.

### 2. 行业边界与产品定义

Define the product precisely.

Must include:

- which adjacent markets it crosses
- what it is
- what it is not
- one-sentence product definition

Use a boundary table:

| 属于什么 | 与本项目的关系 | 应吸收什么 |
|---|---|---|

And an exclusion table:

| 不是 | 原因 |
|---|---|

### 3. 目标用户与核心场景

Segment users. Do not say "all users".

Use this table:

| 用户群体 | 核心痛点 | 高频使用场景 | 被产品打动的理由 | 可能付费的内容 | 第一阶段是否优先切入 |
|---|---|---|---|---|---|

End with a specific first-entry user recommendation.

### 4. 市场机会与为什么现在做

Separate:

- 大趋势证据
- 小切口机会
- 待验证假设

Do not let macro market size replace product-market fit validation.

Use:

| 趋势 | 证据 | 对项目的意义 |
|---|---|---|

If figures are used, include source, year, scope, and credibility level.

### 5. 竞品分析与差异化定位

Build a competitor matrix. Include direct, indirect, and substitute competitors.

Use:

| 产品 | 定位 | 核心功能 | 优势 | 可能短板 | 对本项目的启发 | 本项目如何避开正面竞争 |
|---|---|---|---|---|---|---|

End with:

- what competitors already prove
- what not to compete on
- what to compete on first

### 6. MVP 功能边界

Use three columns:

| 模块 | 必须做 | 可以延后 | 坚决不做 |
|---|---|---|---|

This section must prevent scope creep.

The first MVP should validate the key business loop, not showcase technical ambition.

### 7. 留存机制设计

This is mandatory for consumer software, apps, AI companion, content, social, community, and digital consumption products.

Answer: how to avoid "interesting for two days, then churn"?

Use:

| 留存问题 | 用户表现 | 产品机制 | 对应指标 |
|---|---|---|---|

Emphasize concrete retention loops:

- daily small events
- streaks
- relationship/affinity
- branching personality or progress
- hidden rewards
- seasonal/holiday content
- user-initiated recall
- low-interruption mode

### 8. 商业模式与简单测算

Use a simple internal assumption model. Label it clearly as `内部假设模型`.

Required formulas when applicable:

```text
月收入 = MAU × 付费转化率 × ARPPU
AI 成本 = MAU × 日均 AI 调用次数 × 单次调用成本 × 30
毛利 = 月收入 - AI 调用成本 - 服务器成本 - 内容制作成本
```

Use three scenarios:

| 情况 | MAU | 付费转化率 | ARPPU | 月收入 | 关键成本 | 估算毛利 | 判断 |
|---|---:|---:|---:|---:|---:|---:|---|

Never present internal assumptions as external market facts.

### 9. 风险、反向判断与合规边界

Use:

| 风险 | 风险表现 | 为什么重要 | 早期怎么验证 | 应对策略 | 不成立怎么办 |
|---|---|---|---|---|---|

Must include:

- retention risk
- aesthetics/product appeal risk
- commoditization risk
- cost risk
- privacy/data risk
- interruption/annoyance risk
- minor-user risk when relevant
- emotional dependence / mental-health boundary when relevant
- platform compatibility risk when relevant
- content-update pressure when relevant

Clearly state stop-or-adjust criteria.

### 10. 30 天验证计划

For early-stage product decisions, always include a 30-day validation plan unless the user asks for a different horizon.

Break into 4 weeks:

| 周期 | 目标 | 具体动作 | 产出物 | 核心指标 | 通过标准 | 不通过怎么办 |
|---|---|---|---|---|---|---|

The goal is to decide whether to continue, not to launch a complete product.

Include metrics such as:

-预约/下载意愿
- installation rate
- D1/D3/D7 retention
- active interaction
- payment intent or fake-door click
- willingness to pay
- sharing behavior
- uninstall reasons

## Optional Final Section

If rewriting or improving a previous report, add:

### 本次重写相比原报告的增强点

| 原报告问题 | 修改后如何解决 | 对商业判断的帮助 |
|---|---|---|

## Example Decision Thesis Pattern

Use a concrete thesis sentence:

`本报告认为，{项目} 可以小成本验证，但不应一开始重投入。第一阶段的核心不是 {错误竞争点}，而是 {正确切入点}；只有当 {关键验证指标1}、{关键验证指标2} 和 {关键验证指标3} 成立时，才值得继续开发和放大。`

## Quality Checklist

Before finalizing, verify:

- Does the report state enter / do not enter / validate first?
- Does it define first target users?
- Does it define what not to build?
- Does it include competitor differentiation?
- Does it include retention/payment validation?
- Does it include a simple business model or unit-economics assumption?
- Does it include stop criteria?
- Does it include a 30-day validation plan?
- Are all uncertain numbers labeled as assumptions?
- Are external sources linked?
