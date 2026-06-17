# Proven Source Access Patterns — Cron Environment

> Last verified: 2026-05-30 (cron run on xiaomi provider)
> Context: execute_code + Python urllib (terminal/WSL unavailable on this host)
> ⚠️ Primary execution vehicle: `execute_code` with Python `urllib` — see `references/python-collection-pattern.md`

## Strategy: Python urllib via execute_code (DEFAULT PATH)

All data collection runs through `execute_code` with Python `urllib.request`. Terminal/bash is NOT available on this Windows host (WSL not installed). The `read_file` tool has Windows path issues with `\.` sequences — use `execute_code` + `open()` instead.

### Multi-Phase Pattern (respect 5-min execute_code timeout)
1. **Phase 1** (~3 min): Non-GitHub sources (community, media, newsletters, papers, pricing)
2. **Phase 2** (~3 min): GitHub aggregator READMEs via raw.githubusercontent.com (no API quota) + trending/topics pages
3. **Phase 3** (~2 min): GitHub API search queries (5-6 calls, max 60/hr unauthenticated) + model monitoring
4. **Phase 4** (~4 min): Parse, classify, generate report

## ⭐ Premier Single Source: awesome-ai-agents-2026

`Zijian-Ni/awesome-ai-agents-2026` — comprehensive model+agent timeline updated through May 2026.
- Covers ALL major model releases with dates, versions, and links
- Categorized: Foundation Models, Multimodal, Image/Video/Audio, Agent Projects
- Access via raw.githubusercontent.com (no API quota): `https://raw.githubusercontent.com/Zijian-Ni/awesome-ai-agents-2026/main/README.md`
- **Priority**: Check this BEFORE individual model official pages — it's faster and more complete

## Reliable Sources (Python urllib, 200 OK)

### HN Algolia API — Primary
```python
url = 'https://hn.algolia.com/api/v1/search?query=AI+agent+LLM&tags=story&hitsPerPage=15&numericFilters=created_at_i>2026-05-28'
```
- HN frontpage: `tags=front_page&hitsPerPage=20` (no date filter needed)
- Returns JSON, parse with `json.loads()`

### GitHub API Search — New Agents/Skills
```python
url = 'https://api.github.com/search/repositories?q=ai+agent+created:>2026-05-23&sort=stars&order=desc&per_page=15'
```
- 60 req/hr unauthenticated, sleep 2s between calls
- Key queries: `ai agent`, `agent skills`, `mcp server`, `coding agent`, `llm framework`

### GitHub raw READMEs — No API Quota
```python
url = 'https://raw.githubusercontent.com/OWNER/REPO/main/README.md'
```
- No rate limit, reliable HTML-free markdown content
- Works for: aggregator repos, official cookbooks, awesome-lists, education repos

### 36kr RSS — Chinese Primary
```python
url = 'https://36kr.com/feed'
# ⚠️ 2026-05-30 fix: 单步正则 r'<item>.*?<title>...' 会返回0条（跨行匹配失败）
# 正确做法：先拆item再逐条解析
resp = fetch(url)
items = re.findall(r'<item>(.*?)</item>', resp["data"], re.DOTALL)
for item in items:
    title_m = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
    link_m = re.search(r'<link>(.*?)</link>', item)
    if title_m and link_m:
        kr_items.append({"title": title_m.group(1), "url": link_m.group(1)})
```

### OpenRouter API — 数据截断处理（2026-05-30 verified）
```python
url = 'https://openrouter.ai/api/v1/models'
# execute_code 有50KB stdout硬限制，OpenRouter返回可能 >50KB
resp = fetch(url)
data_str = resp["data"][:30000]  # 截断到30KB确保可解析
try:
    models = json.loads(data_str)
    if isinstance(models, dict) and "data" in models:
        top = sorted(models["data"], key=lambda x: x.get("id",""))[:10]
except json.JSONDecodeError:
    # 截断后仍是坏JSON → 跳过，标注"未获取"
    print("OpenRouter: truncated JSON, skipping")
```
- GitHub Trending pages (github.com/trending) — HTML, parse with regex
- GitHub Topics (github.com/topics/ai-agent, /topics/agent-skills) — HTML
- HuggingFace Papers (huggingface.co/papers) — HTML
- Papers With Code (paperswithcode.com) — HTML
- OpenRouter API — see dedicated section above for truncation handling
- Semantic Scholar API (api.semanticscholar.org) — JSON
- DeepSeek pricing/docs (api-docs.deepseek.com) — HTML
- Anthropic docs (docs.anthropic.com) — HTML
- Google AI docs (ai.google.dev) — HTML
- MiniMax platform (platform.minimaxi.com) — HTML
- 智谱 docs (open.bigmodel.cn) — HTML
- Qwen GitHub README (raw.githubusercontent.com/QwenLM) — Markdown
- 量子位 RSS (qbitai.com/feed) — XML (small response, headlines only)
- 雷锋网 (leiphone.com) — HTML
- CSDN AI (csdn.net/nav/ai) — HTML
- V2EX AI (v2ex.com/go/ai) — HTML
- lobste.rs — HTML
- The Rundown AI (therundown.ai) — HTML (~1MB)
- Import AI / Jack Clark (jack-clark.net) — HTML
- Latent Space (latent.space) — HTML
- Ahead of AI / Raschka (magazine.sebastianraschka.com) — HTML
- Last Week in AI (lastweekin.ai) — HTML
- Alpha Signal (alphasignal.ai) — HTML
- TheSequence (thesequence.substack.com) — HTML
- Prompt Engineering Daily (promptengineeringdaily.com) — HTML
- Practical AI / Changelog (changelog.com/practicalai) — HTML
- Together AI Pricing (together.ai/pricing) — HTML

## Unreliable in This Environment (verified 2026-05-30)

| Source | Attempt | Result |
|--------|---------|--------|
| Reddit ALL (r/ML, r/LocalLLaMA, r/ClaudeAI, r/OpenAI, r/singularity, r/artificial, r/AIdev) | `.json`, `old.reddit.com/.json` | **HTTP 403 Blocked** — definitive, no workaround |
| artificialanalysis.ai | urllib GET | HTTP 403 Forbidden |
| OpenAI official (platform.openai.com/docs, openai.com/api/pricing) | urllib GET | HTTP 403 Forbidden |
| smol.ai | urllib GET | HTTP 403 Forbidden |
| TLDR AI (tldr.tech/ai) | urllib GET | HTTP 403 Forbidden |
| clawhub.ai | urllib GET | HTTP 403 Forbidden |
| LobeHub (lobehub.com) | urllib GET | HTTP 403 Forbidden |
| Groq pricing (console.groq.com) | urllib GET | HTTP 403 Forbidden |
| geekpark.net | urllib GET | HTTP 403 Forbidden |
| zhihu.com | urllib GET | HTTP 403 Forbidden |
| linux.do | urllib GET | HTTP 403 Forbidden |
| DL.AI The Batch | urllib GET | HTTP 403 Forbidden |
| infoq.cn | urllib GET | HTTP 500 Server Error |
| 机器之心 (jiqizhixin.com) | urllib GET | Redirects to data service page, no article content |
| arxiv-sanity-lite.com | urllib GET | SSL UNEXPECTED_EOF |
| Product Hunt AI (producthunt.com/topics/ai) | urllib GET | HTTP 404 |
| Ben's Bites (bensbites.beehiiv.com) | urllib GET | HTTP 404 |
| oschina.net/ai | urllib GET | HTTP 404 |
| Several stale GH READMEs | raw.githubusercontent.com | HTTP 404 (gh_agents_radar, gh_llm_daily, gh_agentic_atlas, gh_chart_lore, gh_aigc_nav, gh_best_ai_papers, gh_llm_lifestyle, gh_ai_weekly, gh_openai_agents_cookbook, anthropic_courses, hf_papers_cn, gh_openai_codex) |

## Paywalled / JS-Rendered (headlines only via HN)
- WSJ (wsj.com), Bloomberg (bloomberg.com), Financial Times (ft.com)
- Most newsletters are JS-rendered SPA — HTML titles extractable but article bodies are not

## Effective Multi-Source Strategy for Cron
1. **Phase 1** (execute_code): HN frontpage + HN AI search + 36kr RSS + Chinese media → headlines
2. **Phase 2** (execute_code): GitHub raw READMEs (20+ aggregator repos) + GitHub Trending/Topics → agent/skill landscape
3. **Phase 3** (execute_code): GitHub API (5 search queries) + model official pages + OpenRouter → new repos + models
4. **Phase 4** (execute_code): Parse all saved raw data, classify, generate report
5. **Do NOT use delegate_task** for data collection — subagents fabricate data
