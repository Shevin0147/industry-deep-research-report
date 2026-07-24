# Decision Report Template

Write in Chinese unless the user requests another language. The final report must be concise, professional, decision-oriented, and PDF-ready. It should feel like a consulting brief, brokerage research summary, or business-plan market section, not a research notebook.

# [行业名称]行业决策型研究报告

Immediately below the title, write the main thesis:

`本报告认为，{行业名称} 的核心机会不是 {错误进入方式}，而是 {正确进入方式}；真正的竞争关键在于 {核心能力1}、{核心能力2} 和 {核心能力3}。`

## Body Structure Rules

- Body has no more than 10 first-level sections before appendices.
- Do not use source audit, chart planning, quality check, or reference lists as body chapters.
- Each body section must contain:
  - one sentence core judgment
  - at most three key evidence points
  - one to three decision implications
  - at most one core visualization or table
- Large tables, long source lists, data-scope details, and quality check go to appendices.
- Body must include at least four direct visualizations. Use compact Markdown tables, Mermaid, SVG, HTML/CSS chart blocks, or structured visual matrices. Do not only list chart plans.
- The report must not contain chat-style text, PDF follow-up prompts, local file paths, or development logs.

## Recommended Body: Max 10 Sections

## 1. 执行摘要

One page maximum. No background essay.

Must include:

- 一句话核心判断
- 是否建议进入
- 适合谁进入
- 不适合谁进入
- 3 个主要机会
- 3 个主要风险
- 3 条行动建议

Suggested compact table:

| 决策问题 | 结论 |
|---|---|
| 是否建议进入 |  |
| 推荐切入点 |  |
| 最大风险 |  |
| 第一阶段验证 |  |
| 不建议模式 |  |

Forbidden vague wording: `前景广阔`, `潜力巨大`, `快速发展` unless immediately supported by data and action judgment.

## 2. 行业边界与定义

Core judgment: define what is in scope and what is out of scope.

Must include:

- industry boundary
- target customer / participant
- value-chain roles
- business-model types
- what this report excludes

Use one compact table only.

## 3. 政策/监管/宏观环境

Core judgment: explain whether the external environment creates entry opportunity or entry constraint.

Must include:

- policy/regulation boundary
- economic or demographic driver
- social/technology change if relevant
- implications for entry strategy

Use one PEST-lite table:

| 维度 | 关键变化 | 证据 | 决策含义 |
|---|---|---|---|

## 4. 市场规模与增长空间

Core judgment: state the usable market opportunity, not just the largest number.

Must include:

- key market size data
- conflicting data scopes if any
- TAM/SAM/SOM or scenario logic
- what can realistically be captured first

Direct visualization required: market size / scope comparison chart. A compact table or bar-style table is acceptable.

Example:

| 口径 | 数值 | 来源等级 | 如何使用 |
|---|---:|---|---|

If data is insufficient:

`由于公开数据不足，本报告不直接给出精确 SOM，而采用情景假设法。`

## 5. 用户需求与场景变化

Core judgment: identify the demand shift that creates a real entry window.

Must include:

- target users
- specific pain points
- high-frequency scenarios
- unmet needs

Use one user-scenario table:

| 用户/客户 | 场景 | 痛点 | 可切入产品/服务 |
|---|---|---|---|

## 6. 产业链与价值分布

Core judgment: show where value and risk sit.

Must answer:

- 谁掌握流量？
- 谁掌握产品？
- 谁承担库存/履约/合规风险？
- 利润更可能流向哪里？

Direct visualization required: value distribution table or value-chain map.

| 环节 | 掌握资源 | 价值来源 | 主要风险 | 进入机会 |
|---|---|---|---|---|

## 7. 竞争格局与玩家定位

Core judgment: show which players dominate and where gaps remain.

Must include:

- main players
- their positioning
- concentration or fragmentation judgment
- competitive matrix

Direct visualization required: competitive matrix.

Matrix choices:

- Platform industry: x-axis `低价/效率驱动 -> 品牌/内容/信任驱动`; y-axis `平台中心化强 -> 商家自主经营强`
- Technology industry: x-axis `技术壁垒低 -> 技术壁垒高`; y-axis `商业化早期 -> 商业化成熟`
- Consumer goods: x-axis `低价格带 -> 高价格带`; y-axis `低品牌溢价 -> 高品牌溢价`

## 8. 商业模式与盈利模型

Core judgment: explain how money is made and where profit leaks.

Choose by industry:

- Consumer goods / retail / restaurant: single-product profit model
- Ecommerce / platform: take rate, ad revenue, fulfillment/service revenue, merchant ecosystem
- SaaS / software / AI: ARR, ARPU, CAC, LTV, retention, gross margin
- Manufacturing / supply chain: unit cost, yield, capacity utilization, inventory turnover, capex
- Local service: ticket size, labor efficiency, store economics, repurchase frequency

Direct visualization required: profit waterfall or unit-economics model.

## 9. 机会、风险与进入路径

Core judgment: convert analysis into a concrete entry route.

Must include:

- 3 opportunities
- 3 risks
- recommended entry scenario
- first-stage validation path
- validation metrics
- modes not recommended

Use one decision table:

| 项目 | 建议 |
|---|---|
| 目标用户 |  |
| 具体痛点 |  |
| 切入场景 |  |
| 第一批产品/服务 |  |
| 验证指标 |  |
| 不建议方向 |  |

## 10. 结论与行动建议

Core judgment: state the final decision.

Must include recommendations for:

- new entrants
- existing companies
- service providers
- investors

End with:

`本报告认为，该行业...`

## Appendices

Appendices do not count as body chapters. Keep them concise.

### 附录 A：来源审计表

| 来源名称 | 来源类型 | 可信度等级 | 使用内容 | 数据时间 | 是否支撑核心结论 |
|---|---|---|---|---|---|

### 附录 B：数据口径说明

Include only data conflicts, assumptions, and scope limitations that affect interpretation.

### 附录 C：参考来源

Group by:

- 官方/监管/统计来源
- 上市公司财报/公告
- 行业协会/咨询/数据库
- 新闻与补充资料

Each source must include:

- source name
- publication time
- content used
- URL
- credibility level

### 附录 D：质量检查结果

Use a short checklist table:

| 检查项 | 结果 | 说明 |
|---|---|---|

### 附录 E：备用图表规划

Only include optional charts not already directly shown in the body. Do not duplicate body visualizations.

## PDF Rules

- Cover page required.
- Table of contents required.
- Page header/footer and page numbers must be correct.
- Hide browser URL, timestamp, and local file path.
- Do not show `Confidential draft for decision support` unless explicitly requested.
- Avoid dense tables. Keep body tables to 7 rows or fewer when possible.
- Use deep blue, gray-blue, light cyan, and small orange accents.
- Keep the style closer to a consulting brief, brokerage summary, or business-plan market analysis than a web printout.
