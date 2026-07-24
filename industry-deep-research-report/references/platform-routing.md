# Platform Routing

Use this reference when an industry report needs user-demand evidence, product evidence, social trend signals, video/transcript evidence, open-source ecosystem evidence, ecommerce signals, or when a website blocks direct crawling.

Core principle: do not get stuck on a single platform. Try the primary route first, then fall back to public search, alternative readers, official pages, news/research sources, and evidence limitations. Do not bypass paywalls, login walls, captcha, anti-crawling controls, or paid databases.

## General Fallback Ladder

1. Primary route: Firecrawl, platform CLI, MCP, API, or agent-reach route.
2. Reader route: Jina Reader, web-reader MCP, Exa crawling, or browser-rendered public page.
3. Search route: targeted web search with `site:` filters and Chinese/English keywords.
4. Alternative source route: official reports, company IR pages, industry media, research reports, public screenshots only if legally accessible.
5. Degrade gracefully: state that platform-native evidence was not accessible and use cautious language.

Never wait indefinitely. For each platform, cap retries, avoid deep pagination, and preserve the report workflow.

## Platform Map

| Evidence need | Primary route | Fallback route | Use in report |
|---|---|---|---|
| General webpages/articles | Firecrawl or Jina Reader | web-reader MCP, Exa crawling, standard web search | Policy, market, company, trend evidence |
| Search discovery | Exa/web search | standard web search, domain-specific search | Source discovery |
| WeChat public articles | Exa search/crawling on `mp.weixin.qq.com` | public reposts, publisher website, screenshots only if public | Trend and expert commentary |
| RSS/news feeds | feedparser | publisher website search | Recent news and trend monitoring |
| Xiaohongshu | `xhs search`, then `xhs read`, `xhs comments` | `site:xiaohongshu.com` search, public media summaries | User scenarios, pain points, word-of-mouth |
| Douyin | Douyin MCP for shared video links | web search, media summaries, creator pages, short-video articles | Trend, content angle, consumer language |
| Weibo | Jina Reader on public post URL | `site:weibo.com` search, news summaries | Public discussion and sentiment |
| Bilibili | `yt-dlp` metadata/subtitles, `bili search` | web search, public video page, article mirrors | Video evidence, creator analysis, comments if public |
| YouTube | `yt-dlp` search/metadata/subtitles | public transcript pages, channel pages, news summaries | Global trend and expert interviews |
| GitHub | `gh search repos/code` | GitHub web search, repository pages | Open-source ecosystem, developer adoption |
| Taobao/Tmall | public search/page scraping when accessible | search snippets, brand official stores, media/ecommerce reports | Price band, SKU, brand, review signals |
| JD | public search/page scraping when accessible | JD IR, search snippets, product pages, ecommerce reports | Price band, SKU, brand, review signals |
| Pinduoduo | public Yangkeduo/PDD pages when accessible | PDD IR, search snippets, ecommerce reports | Low-price competition and SKU signals |
| Reddit/V2EX/Zhihu | public CLI/API/Jina Reader | site search, thread summaries | Developer/user discussion, pain points |

## Agent-Reach Inspired Commands

Use available commands only when installed and configured.

### General Search

```bash
mcporter call 'exa.web_search_exa(query: "query", numResults: 5)'
```

### Web Reader

```bash
curl -s "https://r.jina.ai/https://example.com/article"
mcporter call 'web-reader.webReader(url: "https://example.com", return_format: "markdown")'
```

### WeChat Articles

```bash
mcporter call 'exa.web_search_exa(query: "关键词", numResults: 5, includeDomains: ["mp.weixin.qq.com"])'
mcporter call 'exa.crawling_exa(urls: ["https://mp.weixin.qq.com/s/ARTICLE_ID"], maxCharacters: 10000)'
```

### Xiaohongshu

```bash
xhs search "query"
xhs read NOTE_ID_OR_URL
xhs comments NOTE_ID_OR_URL
```

Important: first obtain a note URL or ID from `xhs search` or feed output. Do not construct bare note IDs. Add delay between requests and stop when captcha/risk control appears.

### Douyin

```bash
mcporter call 'douyin.parse_douyin_video_info(share_link: "https://v.douyin.com/xxx/")'
mcporter call 'douyin.extract_douyin_text(share_link: "https://v.douyin.com/xxx/")'
```

Douyin search may not be available. If no public share links are available, use targeted public web search and do not overstate Douyin-native evidence.

### Weibo

```bash
curl -s "https://r.jina.ai/https://weibo.com/USER_ID/POST_ID"
```

If direct post reading fails, use web search with `site:weibo.com` and cite only accessible public pages.

### Bilibili

```bash
yt-dlp --dump-json "https://www.bilibili.com/video/BVxxx"
yt-dlp --write-sub --write-auto-sub --sub-lang "zh-Hans,zh,en" --convert-subs vtt --skip-download -o "/tmp/%(id)s" "URL"
bili search "query" --type video -n 5
```

### YouTube

```bash
yt-dlp --dump-json "ytsearch5:query"
yt-dlp --write-sub --write-auto-sub --sub-lang "zh-Hans,zh,en" --skip-download -o "/tmp/%(id)s" "URL"
```

### GitHub

```bash
gh search repos "query" --sort stars --limit 10
gh search code "query" --language python
gh repo view owner/repo
```

### Reddit and V2EX

```bash
rdt search "query" --limit 10
rdt read POST_ID
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: industry-deep-research/1.0"
```

## Ecommerce Routing

Use ecommerce sources for price bands, SKU density, brand visibility, reviews, claims, and channel signals. Do not use product pages alone for market size or market share.

Primary public routes:

```text
Taobao: https://s.taobao.com/search?q={query}
Tmall: search via web `site:tmall.com {query}`
JD: https://search.jd.com/Search?keyword={query}
PDD/Yangkeduo: https://mobile.yangkeduo.com/search_result.html?search_key={query}
```

Fallback routes:

- Platform official reports or investor relations pages
- Brand official stores and brand websites
- Public ecommerce research reports
- Search snippets and news summaries
- Manual note: platform-native product evidence unavailable

## Anti-Blocking Rules

- Respect robots, login walls, paywalls, captcha, and platform terms.
- Do not automate write actions such as posting, liking, commenting, following, or purchasing.
- Use short runs, shallow pagination, and delays for social platforms.
- Prefer public, stable URLs over fragile dynamic endpoints.
- If a platform blocks access, record the limitation internally and continue with other sources.
- In the final report, cite platform evidence only when the public source is accessible and relevant.

## Evidence Interpretation

Platform data should map to report sections as follows:

- Xiaohongshu/Douyin/Weibo/Bilibili/YouTube: user demand, pain points, trends, consumer language, content themes.
- Ecommerce: price band, SKU structure, brand visibility, reviews, channel strategy.
- GitHub: technical ecosystem, open-source alternatives, developer adoption.
- RSS/news: latest events, financing, regulation updates.
- Official websites/IR/filings: core facts, market numbers, revenue, policy, and strategic claims.
