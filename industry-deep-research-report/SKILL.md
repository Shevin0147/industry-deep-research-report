---
name: industry-deep-research-report
description: Generate a concise, decision-grade Chinese industry report from an industry, product category, company, market, region, or research question by actively searching public web sources, auditing evidence, validating data conflicts, building business models, creating direct visualizations, and optionally exporting a polished PDF or HTMLSlides decision deck.
---

# Industry Deep Research Report

Use this skill when the user asks for industry analysis, market research, competitive landscape, product/category study, company market analysis, entry opportunity assessment, business model analysis, investment thesis, or deep research report.

The skill acts as a professional industry researcher and consulting analyst. The task is not to summarize search results; it must turn public evidence into a 3-minute decision report for entrepreneurship, investment, corporate strategy, or business planning.

## Core Agent Prompt

Always follow `references/research-agent-core.md`. It is the controlling prompt for:

- research brief generation
- source priority and A/B/C/D credibility grading
- source audit table
- evidence extraction schema
- data conflict handling
- decision-oriented analysis standards
- mandatory 10-section decision report
- direct visualizations
- quality checklist
- prohibitions

## References To Load

- For source priority, query groups, and citation rules, read `references/source-strategy.md`.
- For evidence grading, source audit, extraction fields, and conflict handling, read `references/evidence-quality.md`.
- For competing hypotheses, research modes, stopping rules, structured `.research/` artifacts, and graded quality gates, read `references/research-protocol.md`.
- For reproducible market sizing, unit economics, scenario analysis, and sensitivity thresholds, read `references/decision-model.md`.
- For industry classification, decision levels, mixed-industry routing, and pack IDs, read `references/industry-packs/routing.md`. Then load only the selected one or two JSON packs.
- For web, social, video, ecommerce, GitHub, RSS, and platform fallback routing, read `references/platform-routing.md`.
- For the final report structure, section compression rules, visualizations, appendices, and quality check, read `references/report-template.md`.
- For early-stage product entry, startup opportunity review, MVP validation, software/app market entry, or "should I do this product" decisions, read `references/product-entry-decision-template.md` and use that structure instead of the generic industry template.
- If the topic is cross-border ecommerce, ecommerce export, overseas ecommerce, independent sites, platform ecommerce, content ecommerce, or supply-chain globalization, also read `references/cross-border-ecommerce.md`.
- For one-click PDF export after the report is complete, use `scripts/export_report_pdf.py`.
- For PPT, slides, deck, keynote, or presentation export after the report is complete, read `references/ppt-export.md` and generate through the `$html-slides:html-slides` skill as a single-file HTMLSlides deck.

## Core Rules

- Do not rely only on uploaded files or model memory. Actively search public web sources whenever current market, policy, financial, competitor, or user-demand information is needed.
- Prefer official, regulatory, statistical, customs, exchange, public-company, prospectus, annual-report, and platform-official sources for core facts.
- Use consulting, brokerage, database, association, and market-intelligence reports for forecasts and segmentation when official data is unavailable.
- Use news, blogs, social media, forums, videos, product pages, and ecommerce pages only as supplementary evidence, mainly for events, examples, demand signals, price bands, SKU density, user language, and pain points.
- Every key number must include source, time period, metric scope, and credibility level.
- Keep A/B/C/D source levels for reporting, but assess evidence internally across authority, originality, recency, scope fit, and independence.
- Form at least three competing hypotheses before fixing the main thesis. Search for support and disconfirming evidence for each; select the thesis only after evidence audit.
- If the same metric has multiple public figures, show the competing values, explain scope/time differences, and express the conclusion as a range or scenario. Do not force a single number.
- Do not fabricate data. If evidence is weak, write: `公开资料不足，以下为基于公开资料的合理判断。`
- The final report must include macro industry analysis and micro business feasibility analysis.
- For early product direction decisions, prioritize market-entry judgment over broad industry coverage: whether to enter, who to target first, what to build or avoid, how to validate retention/payment, which risks stop the project, and what 30-day validation plan to run.
- The report must revolve around one main thesis: `本报告认为，{行业名称} 的核心机会不是 {错误进入方式}，而是 {正确进入方式}；真正的竞争关键在于 {核心能力1}、{核心能力2} 和 {核心能力3}。`
- The final PDF or PPT body must let a reader understand within 3 minutes: whether to enter, where to enter, biggest risk, first validation path, and modes to avoid.
- Default to `standard` research mode. Use `quick` for screening and `deep` for higher-stakes work or when the user explicitly requests deeper diligence.
- Set a decision level independently from research depth: `L1` screening, `L2` MVP validation, `L3` commercial investment, or `L4` investment/M&A diligence. Default to `L1`.
- Load one primary industry evidence pack and at most one secondary pack. If classification is uncertain, use `core` only and record a routing warning.

## Workflow

1. Build an internal research brief:
   - industry, research object, geography, time range, target reader, research goal, key questions, output form
   - default time range: latest 3-5 years, prioritizing the newest public data
   - default target reader: entrepreneurs, investors, corporate managers, industry researchers
   - classify the primary industry family and optional secondary family using `references/industry-packs/routing.md`
   - set `decision_level` from the intended decision, independently from `quick|standard|deep` research depth
   - create `reports/<topic-slug>/.research/` and maintain the JSON artifacts defined in `references/research-protocol.md`

2. Build competing hypotheses before searching:
   - create at least three mutually distinguishable explanations or entry hypotheses
   - define what would support, weaken, or falsify each hypothesis
   - do not lock the report thesis at this stage

3. Build search query groups before searching:
   - government/regulation/policy/standard
   - statistics/customs/market size/growth/penetration
   - annual report/prospectus/filing/investor relations
   - industry association/white paper/yearbook
   - brokerage/consulting/database/research institute
   - competitor/business model/pricing/revenue/cost
   - user demand/pain points/reviews/social discussion
   - trend/risk/opportunity/financing/M&A

4. Collect and audit evidence:
   - Extract all key data using the schema in `references/evidence-quality.md`.
   - Build an internal source audit table and include a concise version in the report.
   - Every core conclusion needs at least one A/B/C-level source. D-level sources cannot solely support core conclusions.
   - Track source independence and original-source lineage; multiple pages repeating one original source count as one independent source.
   - Record each evidence item's categories, supported claim types, prohibited claim types, verifiability, conflict of interest, retrieval date, original URL, and evidence excerpt.
   - Apply the selected industry pack requirements; industry packs define evidence requirements, not report sections.
   - Record support, counterevidence, unresolved conflicts, confidence, validity conditions, and falsifiers for each core claim.

5. Cross-check and analyze:
   - Prefer official over commercial reports, primary over secondary sources, and recent over outdated sources.
   - Explain conflicts by metric definition, geography, time period, inclusion scope, or publication timing.
   - Convert evidence into judgment. Do not merely summarize sources.
   - Reflect after each search round: identify information gained, remaining gaps, counterevidence still needed, and whether the stopping rules are met.
   - Use both top-down and bottom-up market sizing when feasible. Label formulas, inputs, sources, assumptions, and scope.
   - Do not calculate SOM as TAM multiplied by an arbitrary share. Constrain it by reach, capacity, geography, budget, and conversion.
   - Add base, downside, and upside unit-economics scenarios, break-even points, the three most sensitive variables, and failure thresholds.

6. Select the thesis and produce the final report:
   - select the main thesis only after hypothesis comparison and evidence audit
   - preserve rejected hypotheses and counterevidence in `.research/`; surface only decision-relevant limitations in the report
   - Use the section structure in `references/report-template.md` for mature industry reports.
   - Use `references/product-entry-decision-template.md` for early product, startup, MVP, or software/app entry decisions.
   - Keep the body to no more than 10 first-level sections before appendices.
   - Move source audit, data-scope notes, references, quality check, and backup chart plan to appendices.
   - Include at least four direct visualizations in the body using compact tables, Mermaid, SVG, HTML/CSS chart blocks, or structured visual matrices. Do not put a chart planning table in the body.
   - Each body section must contain one core judgment, at most three key evidence points, one to three decision implications, and at most one core chart or table.
   - Save the final report as `reports/<topic-slug>/report.md` whenever a local workspace is available.
   - Run `python scripts/validate_report.py --report <report.md> --research-dir <report-folder>/.research --mode <quick|standard|deep>` before export. The validator reads decision level and evidence packs from `brief.json`.
   - State which decisions the evidence supports and which decisions it does not support.
   - Resolve blocking errors before finalizing. Warnings may remain only when their limitations are disclosed.
   - If the user did not request PDF export, ask the PDF follow-up only in chat after the report. Never include this follow-up inside `report.md`, `report.html`, or `report.pdf`.

7. PDF export follow-up:
   - If the user replies with a clear confirmation such as `生成 PDF`, `要`, `可以`, `导出`, `是`, or `同样生成`, do not redo the research.
   - Reuse the most recent saved `report.md` for that topic.
   - Run `python scripts/export_report_pdf.py --input-md <report.md> --output-dir <same report folder>`.
   - Return only the generated `report.pdf` path and, if useful, the companion `report.html` path.
   - If no saved `report.md` exists, first save the latest report content to `reports/<topic-slug>/report.md`, then run the exporter.

8. PPT export follow-up:
   - If the user asks for `PPT`, `PPTX`, `slides`, `deck`, `演示稿`, `幻灯片`, `导出 PPT`, or `生成 PPT`, do not redo the research.
   - Reuse the most recent saved `report.md` for that topic and compress it into an 8-12 slide decision deck.
   - Follow `references/ppt-export.md`; generate a single-file HTMLSlides deck with inline CSS/JS, viewport-safe slides, and embedded speaker notes.
   - Do not use the generic artifact-tool PowerPoint generator or html-ppt as the default PPT/Slides path.
   - Return only the generated deck path, rendered preview/contact-sheet path when available, and a short verification note.

## Output Discipline

Do not include raw search logs, crawler traces, hidden chain-of-thought, unsupported precise estimates, long pasted source text, chat-style prompts, local browser file paths, development notes, or phrases such as `以下是`, `我可以帮你`, `要不要我生成 PDF`, and `回复生成 PDF` inside saved reports, PDFs, or decks. Use compact citations and a concise source list. The writing style must be professional, clear, data-driven, decision-oriented, and suitable for PDF and PPT export.
