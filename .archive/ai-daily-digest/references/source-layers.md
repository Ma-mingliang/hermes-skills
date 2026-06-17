# AI Daily News — Source Layers Reference

> Condensed knowledge bank: which sources to hit, how to access them, and what to expect.

## Layer 1: Hacker News (Primary Community Signal)

- **API**: `https://hn.algolia.com/api/v1/search_by_date?query=KEYWORD&tags=story&hitsPerPage=10&numericFilters=points>5`
- **Why**: Community-voted, provides points/comments as importance signal
- **Queries to use**: "AI", "OpenAI", "Claude", "GPT", "Gemini", "LLM", "agent", "DeepSeek"
- **Filter**: Last 3 days, deduplicate by URL
- **Output**: title, url, points, num_comments, created_at

## Layer 2: HuggingFace Daily Papers

- **URL**: `https://huggingface.co/papers`
- **Method**: GET with standard headers, extract `<h3>` titles with regex
- **Why**: Curated paper selection, often surfaces model releases before news outlets
- **Limitation**: Paper titles only, no abstracts in HTML scrape

## Layer 3: GitHub Aggregator Repos

### ai-daily-digest (Jimmuji) — ⭐ BASELINE, FETCH FIRST
- **Raw**: `https://raw.githubusercontent.com/Jimmuji/ai-daily-digest/main/daily/YYYY-MM-DD.md`
- **Note**: Dated one day ahead (May 28 report covers May 27 events). Try both dates.
- **Format**: Structured with importance stars (★), source links, sectioned by 行业新闻/重要论文/开源项目
- **Why baseline**: Already cross-referenced, rated by importance, bilingual. Counting Jimmuji as a source plus any other source that independently reports the same event = ≥2 sources.
- **Fallback**: If the target date returns 404, try the next day's date.

### Horizon (Thysrael) and follow-news (tangwz) — ⚠️ NOT PRACTICAL FOR CRON
- These repos require full clone + local processing. No easily fetchable daily raw report.
- SKIP for automated daily collection. Use Jimmuji instead.

## Source Reliability Quick-Reference

| Source | Reliability | Notes |
|--------|------------|-------|
| **Jimmuji/ai-daily-digest** | ⭐⭐⭐⭐⭐ | FETCH FIRST. Pre-curated, cross-referenced, Chinese+English, importance stars. Single most valuable source. |
| **HN Algolia API** | ⭐⭐⭐⭐⭐ | Always works. Community-validated. |
| **HuggingFace Papers** | ⭐⭐⭐⭐ | Always works. Titles only without LLM-based extraction. |
| **Reddit (json API)** | ⭐⭐⭐⭐ | Works with User-Agent header, no auth needed. r/singularity and r/LocalLLaMA best for AI news. |
| **量子位 RSS** | ⭐⭐⭐⭐ | RSS works, article bodies are JS-rendered. See RSS parsing notes below. |
| **36氪 RSS** | ⭐⭐⭐ | RSS works, but only ~10% of items are AI-related. Filter by keyword. |
| **arXiv cs.AI** | ⭐⭐⭐ | HTML scrape fragile — regex `Title:</span>` works but page layout changes. Prefer HF Papers. |
| **Horizon/Thysrael** | ⭐⭐ | No structured daily report — requires full clone + local processing. Impractical for cron. |
| **follow-news/tangwz** | ⭐⭐ | Same — no easily fetchable daily output. |
| **ProductHunt AI** | ❌ | 404. URL may have changed. |
| **Ben's Bites** | ❌ | 404. beehiiv URL changed. |
| **极客公园** | ❌ | 403. Blocks automated access. |
| **机器之心** | ❌ | JS-rendered. HTML scrape returns 0 titles. |
| **TLDR AI** | ❌ | JS-rendered. No scrapable article content. |

## Layer 4: Chinese Sources (RSS Parsing — Critical Nuance)

### ⚠️ RSS CDATA Handling (MUST GET RIGHT)

Chinese RSS feeds use INCONSISTENT CDATA wrapping. This is the #1 cause of 0-result collections:

**量子位 (QbitAI)**: 
- `<title>plain text</title>` — **NO CDATA** for title
- `<description><![CDATA[...]]></description>` — **WITH CDATA** for description
- Correct title regex: `r'<title>(.*?)</title>'`
- Correct desc regex: `r'<description>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</description>'`

**36氪**:
- `<title><![CDATA[...]]></title>` — **WITH CDATA** for title
- `<link><![CDATA[...]]></link>` — **WITH CDATA** for link
- Correct title regex: `r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>'`

**Universal safe pattern** (works for both CDATA and plain text):
```python
# For any field that might or might not use CDATA
title_m = re.search(r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', item, re.DOTALL)
link_m = re.search(r'<link>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</link>', item)
pubdate_m = re.search(r'<pubDate>(.*?)</pubDate>', item)
```

### 量子位 (QbitAI) — Primary Chinese Source
- **RSS**: `https://www.qbitai.com/feed`
- **Method**: Parse `<item>` elements with universal CDATA-safe regex above
- **Filter by date**: Look for `pubDate` containing the target date (format: `Wed, 27 May 2026`)
- **⚠️ Article bodies**: JS-rendered, HTML only has title + meta. Accept title-only summaries from RSS.
- **Priority**: High (1.3 weight in source_registry)

### 36氪 AI
- **RSS**: `https://36kr.com/feed`
- **Method**: Same universal CDATA-safe regex. Filter items by AI keywords.
- **AI keyword filter**: `['ai', '人工智能', '大模型', 'gpt', 'openai', 'deepseek', 'agent', '智能', 'Claude', 'Gemini']`
- **Content**: Mix of AI industry + startup funding news. Only ~10% of items pass keyword filter.

### 机器之心 (jiqizhixin)
- **URL**: `https://www.jiqizhixin.com`
- **Method**: Direct HTML scrape of `<h2>/<h3>` titles
- **⚠️**: May also use JS rendering

## Layer 5: Direct Article Fetching

For top items (HN ≥50pts or multi-source), fetch full text:
```python
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
r = requests.get(url, headers=headers, timeout=15)
```

Extract with regex (try in order):
1. `<article>...</article>`
2. `<main>...</main>`
3. `<div class="article-content">...</div>`
4. `<div class="post-content">...</div>`

## Layer 6: Reddit (Community Signal)

Reddit provides a reliable JSON API with no auth required:
```python
# Standard headers are sufficient
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
r = requests.get(f'https://www.reddit.com/r/{sub}/new.json?limit=25', headers=headers, timeout=20)
data = r.json()
for post in data['data']['children']:
    d = post['data']
    created_dt = datetime.utcfromtimestamp(d['created_utc'])
    # Filter to Beijing-date window (UTC+8)
```

**Most AI-news-rich subreddits** (in priority order):
1. `r/singularity` — Broad AI/tech news, high engagement (often 300-700 pts for big stories)
2. `r/LocalLLaMA` — Open-source models, local deployment, model releases
3. `r/MachineLearning` — Research-focused, lower volume
4. `r/OpenAI` — OpenAI-specific, occasionally has general AI job-displacement discussion
5. `r/ClaudeAI` — Claude-specific, lower volume

**Date filtering**: Convert `created_utc` to datetime and check against Beijing date window (UTC+8):
```python
from datetime import datetime
target_day_start = datetime(2026, 5, 27, 0, 0)  # Beijing midnight
utc_start = target_day_start - timedelta(hours=8)  # 2026-05-26T16:00:00Z
utc_end = utc_start + timedelta(hours=24)          # 2026-05-27T16:00:00Z
```

## Layer 6: DuckDuckGo (⚠️ LAST RESORT — severely rate-limited)

**2026-05-31 实测结论**: DDG 在本机几乎不可用于批量采集，不应作为主要数据源。

- `ddgs.news()`: 403 Ratelimit 在第2个查询就开始触发（1.2s间隔也挡不住），15个查询中仅1个成功
- `ddgs.text()`: 同session内返回全0结果（无报错但无数据），IP被标记后连text search也废了
- **DDG skill本身推荐DDG作为搜索工具，但对日报批量采集场景完全不适用**

正确策略：把DDG放在采集流程最前面（趁IP还没被标记），只跑1-2个最重要的查询，然后立即切换到HN Algolia + GitHub API。不要把DDG当作可靠的降级方案。

```python
# DDG采集模式（最小化限流风险）
from duckduckgo_search import DDGS
import time

with DDGS() as ddgs:
    # 只跑1个最关键的查询
    results = list(ddgs.news("AI agent new release", region='wt-wt', timelimit='d', max_results=15))
    print(f"Got {len(results)} results")
    # 立即切换到API采集，不要再调DDG
```

- ⚠️ **绝对不要**在DDG失败后重试——只会加深限流
- ⚠️ **绝对不要**在同一session内混合news+text search——两者共享限流桶

## Cross-Reference Scoring

Count distinct independent sources per event:
- HN story + ai-daily-digest mention + 量子位 article = 3 sources → 🟡 重要
- HN story + HF paper + ai-daily-digest + 量子位 + TechCrunch = 5 sources → 🔴 极高重要
- Single source only → ⚪ 低置信观察

Note: Same event appearing under different HN search queries only counts as 1 source. Deduplicate by URL.
