# PPT / Slides Export With HTMLSlides

Use this reference when the user asks to export an already generated industry report as PPT, slides, deck, keynote, presentation, 演示稿, or 幻灯片.

## Principle

Do not redo the industry research. Reuse the latest `reports/<topic-slug>/report.md` and convert the decision logic into a concise visual deck.

Generate through `$html-slides:html-slides` by default. The output should be a single self-contained HTMLSlides file with inline CSS, inline JS, embedded speaker notes, and no build step. Do not use the generic artifact-tool PowerPoint generator or html-ppt as the default path.

## Output Format

Default output:

- `reports/<topic-slug>/html-slides/<topic-slug>.html`

The file must be portable and directly openable in the user's local HTMLSlides viewer or browser. Use external links only for fonts; keep all other CSS and JS inline unless the user explicitly asks for another format.

If the user explicitly asks for `.pptx`, first generate the HTMLSlides file as the source of truth. Convert or export to `.pptx` only when a reliable local conversion path is available; otherwise return the HTMLSlides file and clearly state the produced format.

## Required HTMLSlides Spec

Every generated deck must pass these checks:

- `<div class="deck" id="deck">` wraps all slides.
- Slides are `<div class="slide">` elements, not `<section>`.
- First slide has `class="slide active"` and no other slide has `active`.
- Slides have sequential `data-slide="0"` through `data-slide="N"`.
- Global `goTo(index)`, `next()`, and `prev()` functions exist.
- CSS is inline except font imports.
- JS is inline except explicitly required CDN libraries.
- `<meta name="generator" content="html-slides v0.9.4">` exists in `<head>`.
- Every slide includes a hidden `<script type="application/json" class="slide-notes">` block.

## Deck Structure

Keep the deck to 8-12 slides. Recommended structure:

1. Cover: industry name, date, main thesis, 3-4 key numbers
2. 3-minute decision: enter or not, who fits, who does not, biggest risk
3. Market proof: market size, growth, data口径, key caveat
4. Demand/segment heatmap: hot categories, user scenarios, or region segments
5. Value chain: who controls traffic, product, fulfillment, compliance, profit
6. Competitive map: player positioning and new entrant gap
7. Business model: revenue, cost, unit economics or profit waterfall
8. Risks and no-go modes: regulatory, platform, cost, supply, brand risks
9. First-stage validation path: target user, MVP, metrics, gate to scale
10. Action recommendation and sources

Adapt the structure to the topic, but keep the reader able to answer in 3 minutes:

- 是否值得进入
- 从哪里切入
- 最大风险是什么
- 第一阶段怎么验证
- 哪些模式不建议做

## Slide Design Rules

- One slide, one decision point.
- Use visual hierarchy, not dense tables.
- Use at least four direct visuals across the deck: market chart, segment heatmap, value-chain flow, competition matrix, profit waterfall, roadmap, or risk map.
- Keep sources on-slide as compact labels, and put longer references on the final slide or speaker notes.
- Use fonts that support Chinese well; prefer `Noto Sans SC` plus one professional Latin companion font.
- All typography and slide spacing should use `clamp(...)` and the `viewport-base.css` rules from `$html-slides:html-slides`.
- Do not put presenter-only explanations on visible slides.
- Do not include chat-style wording, local browser paths, development logs, or phrases such as `我可以帮你`.

## Validation

Before returning:

- Count slides by checking `<div class="slide"`.
- Confirm slide numbers are sequential.
- Confirm every slide has a `data-slide` and a hidden `slide-notes` JSON block.
- Confirm the first slide is active and only one slide has `active`.
- Confirm required global navigation functions exist.
- Confirm no visible text contains chat-style wording, local file paths, or development logs.
- Render or preview when feasible. If the user says they have local viewer software, static validation is enough.

## Final Response

Return only:

- HTMLSlides file path
- optional preview path if generated
- short verification note with slide count and validation status
