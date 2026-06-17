---
name: collector-architecture
description: "Multi-source data collector architecture with unified source_status, RSS-first + API optional graceful degradation, hash-diff change detection, auth/strategy tracking, and SPA site fetching rules. Use when building any system that collects data from multiple heterogeneous sources, or when fetching data from SPA sites."
version: "1.0.0"
tags: ["data-collection", "collector", "source-status", "rss", "api", "graceful-degradation"]
---

# Collector Architecture Pattern

Build robust multi-source data collectors that never crash the pipeline when a single source fails.

## Core Design: Unified source_status

Every collector returns `(items, source_status)` — a tuple of collected items and a standardized status dict.

### 9 Status Enums

| Status | Meaning |
|--------|---------|
| `success` | Data collected and keywords matched |
| `success_no_match` | Data collected but no keyword match |
| `checked_no_change` | Page checked, hash same as last time (docs only) |
| `skipped_disabled` | Source disabled in config |
| `skipped_missing_auth` | Required env vars missing |
| `failed_network` | Connection/timeout/HTTP 5xx |
| `failed_parse` | Response received but unparseable |
| `failed_auth` | Auth present but rejected (401/403) |
| `failed_rate_limited` | HTTP 429 |

### source_status Dict Structure

```python
{
    "source": "linuxdo",
    "enabled": True,
    "status": "success",          # one of 9 enums
    "auth": "ok",                 # "ok" | "missing" | "failed" | "n/a"
    "strategy_used": "rss",       # "api" | "rss" | "rss_fallback" | "hash_diff" | "scrape"
    "raw_count": 30,
    "matched_count": 14,
    "selected_count": 14,
    "items": [...],
    "errors": [],
    "warnings": []
}
```

### Factory Functions (source_status.py)

```python
from source_status import make_source_status, skipped_disabled, skipped_missing_auth, failed_network

# Full control
status = make_source_status(source="reddit", status="success", auth="ok", strategy_used="api",
                            raw_count=100, matched_count=20, selected_count=20, items=[...])

# Quick returns
return skipped_disabled("reddit")                    # ([], status)
return skipped_missing_auth("reddit", ["REDDIT_ID"]) # ([], status)
return failed_network("reddit", "timeout")           # ([], status)
```

## 3 Fallback Strategies

### 1. RSS-first + API optional (Reddit, Product Hunt)

```
has_auth?
  ├─ yes → try API
  │         ├─ API success → return
  │         ├─ API auth fail → set auth="failed", fall through to RSS
  │         └─ API 0 results → try RSS as supplement
  └─ no → skip API, go directly to RSS
           └─ RSS → return (strategy="rss" or "rss_fallback")
```

Key rule: `skipped_missing_auth` is ONLY for when the entire source has no fallback. If RSS exists, the source returns `success` or `success_no_match` regardless of auth status.

### 2. Hash-diff change detection (Model Docs)

```
for each page:
  fetch → extract text → compute sha256 hash
  compare with state/model_docs_state.json
  ├─ same hash → checked_no_change
  └─ different hash → keyword match on diff
                       ├─ matched → success
                       └─ no match → success_no_match
```

State file format:
```json
{
  "deepseek:https://api-docs.deepseek.com": {
    "last_hash": "abc123",
    "last_checked": "2026-06-01T09:00:00+00:00",
    "last_changed": "2026-05-30T09:00:00+00:00",
    "last_text_preview": "first 2000 chars..."
  }
}
```

### 3. RSS endpoint auto-discovery (NodeSeek)

```
check state/source_state.json for cached working endpoint
├─ cached → verify still works → use it
└─ no cache → iterate rss_endpoint_candidates
              ├─ first valid → save to state, use it
              └─ all fail → HTML fallback
```

## main.py Pattern

```python
def safe_collect(name, collect_fn, config, logger):
    """Never let one collector crash the pipeline."""
    try:
        items, source_status = collect_fn(config)
        return items, source_status
    except Exception as e:
        return [], make_source_status(
            source=name, status="failed_network",
            errors=[f"Collector exception: {e}"],
        )

# In main():
for name, fn in collectors:
    items, status = safe_collect(name, fn, config, logger)
    all_statuses[name] = status
    if status["status"] == "success":
        all_items.extend(items)

# Pass source_statuses to report generator
report = generate_report(all_items, config, date, source_statuses=all_statuses)
```

## Report Source Status Table

```markdown
## 0. 数据源状态 (Source Status)

| Source | Auth | Strategy Used | Status | Raw | Matched | Selected | Notes |
|---|---|---|---|---:|---:|---:|---|
| github | ok | api | ✅ success | 643 | 643 | 50 | Data collected successfully |
| reddit | missing | rss | ✅ success | 257 | 48 | 48 | OAuth missing, used RSS fallback |
| model_docs | n/a | hash_diff | 🟡 success_no_match | 8 | 0 | 0 | raw=8 but no keyword match |
```

## SPA Site Fetching Rules

SPA单页应用（React/Vue/Next.js）用 web_fetch 只拿到静态骨架/旧缓存，不是真实数据。

### 核心规则

| 场景 | 正确做法 | 错误做法 |
|------|---------|---------|
| SPA站点数据获取 | browser 完整渲染后提取 | web_fetch / curl（拿到静态骨架） |
| browser失败时 | 跳过该板块，标注"今日未能获取" | 用旧数据填充 |
| 用户提供截图 | 优先级最高，用 vision_analyze 读取 | 用旧缓存"纠正"用户信息 |

### 验证优先级

```
用户截图 > browser实时渲染 > web_fetch（SPA不可靠）> 子任务返回数据
```

### 已知 SPA 站点

| 站点 | 正确方式 | 备注 |
|------|---------|------|
| artificialanalysis.ai | browser | 15个benchmark综合排名 |
| lmarena.ai | browser | 用户投票ELO排名 |
| openrouter.ai | browser | 使用热度/价格 |
| GitHub API | curl ✅ | REST API，不是SPA |
| HN Algolia | curl ✅ | REST API，不是SPA |

### 判断 SPA 的方法

curl 返回的 HTML 中几乎没有目标数据内容 → 是 SPA。页面依赖 JavaScript 动态渲染 → 是 SPA。

### 程序化 SPA 抓取（Crawlee + Playwright）

```python
import asyncio
from crawlee.crawlers import PlaywrightCrawler

async def scrape_spa_site():
    crawler = PlaywrightCrawler(headless=True, browser_type='chromium')
    @crawler.router.default_handler
    async def request_handler(context):
        await context.page.wait_for_load_state('networkidle')
        content = await context.page.content()
        # 提取数据...
    await crawler.run(['https://target-spa-site.com'])
```

已验证: github.com/trending ✅, artificialanalysis.ai ⚠️ (Vercel安全检查需反检测)

### 子任务数据验证

delegate_task 子任务返回的数据可能完全编造（GitHub仓库404、Stars数捏造、排名无来源）。验证流程：
1. GitHub项目 → web_fetch 验证 URL 是否 404
2. Stars数 → GitHub API 确认
3. 模型版本 → browser 访问排行榜确认
4. **未验证数据不能写入报告**

### 终极方案：Python urllib

当 terminal/WSL 不可用时：
```python
import urllib.request, json
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode())
```
已验证: HN Algolia API ✅, GitHub REST API ✅。SPA站点仍需 browser。

See `references/spa-fetching-patterns.md` for 详细案例和 Crawlee 配置。

## Pitfalls

### PITFALL: Batch string replacement can corrupt code

When patching multiple files with string replacement, a short pattern like `STATUS_SUCCESS` will match INSIDE `STATUS_SUCCESS_NO_MATCH`, creating broken code like `status=STATUS_SUCCESS, auth="n/a", strategy_used="api", status=STATUS_SUCCESS_NO_MATCH`.

**Fix**: Always replace longer strings first. Use regex with word boundaries. Or rewrite the whole function rather than patching in place.

**Example of what goes wrong**:
```python
# This replacement:
content.replace('STATUS_SUCCESS,', 'STATUS_SUCCESS, auth="n/a",')
# Also corrupts STATUS_SUCCESS_NO_MATCH by matching the STATUS_SUCCESS prefix
```

### PITFALL: Function signature must match caller kwargs

When adding new fields (like `auth`, `strategy_used`) to `make_source_status`, update BOTH:
1. The function signature (parameters)
2. The return dict construction

Missing either causes `unexpected keyword argument` or fields stuck at defaults.

### PITFALL: Environment variable naming mismatch

`.env` may have `GITHUB_PERSONAL_ACCESS_TOKEN` while code expects `GITHUB_TOKEN`. Fix with fallback chain:
```python
self.token = os.environ.get(config.get("token_env", "GITHUB_TOKEN"), "")
if not self.token:
    self.token = os.environ.get("GITHUB_TOKEN", "") or os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN", "")
```

### PITFALL: Windows WSL relay breaks write_file

On Windows with WSL, the `write_file` tool may fail with WSL relay errors. Use `execute_code` with Python `open()` as fallback — it uses native Windows IO.

### PITFALL: RSS parsing without feedparser

When feedparser is not available, use regex to parse RSS/Atom:
```python
entries = re.findall(r"<entry>(.*?)</entry>", content, re.DOTALL)
# or for RSS 2.0:
items_xml = re.findall(r"<item>(.*?)</item>", content, re.DOTALL)
```
Always handle both `<entry>` (Atom) and `<item>` (RSS 2.0) formats.
