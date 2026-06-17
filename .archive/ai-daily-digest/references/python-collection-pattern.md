# Python urllib 数据采集模式 — 核心版

> 适用场景：WSL/bash 不可用时，使用 execute_code + Python urllib 进行数据采集
> 验证日期：2026-05-30（xiaomi provider, Windows 11 host）

## 核心函数模板

```python
import urllib.request
import urllib.parse
import json
import time
import re
from datetime import datetime, timedelta

def fetch_url(url, headers=None, timeout=30, source_id="unknown"):
    """Fetch URL with urllib. Returns dict with success/status/data or error."""
    result = {"url": url, "source_id": source_id, "success": False, 
              "status": None, "size": 0, "time": datetime.now().isoformat()}
    try:
        req = urllib.request.Request(url, headers=headers or {})
        req.add_header('User-Agent', 'AI-Daily-Digest/5.2 (research-bot)')
        if 'github.com' in url or 'api.github.com' in url:
            req.add_header('Accept', 'application/vnd.github.v3+json')
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            result["success"] = True
            result["status"] = resp.status
            result["size"] = len(data)
            # ⚠️ NEVER store data in access_log — bytes can't be JSON-serialized
            result["text"] = data.decode('utf-8', errors='replace')
    except Exception as e:
        result["error"] = str(e)[:200]
    return result

def fetch_json(url, headers=None, source_id="unknown"):
    """Fetch and parse JSON, returns dict/list or None."""
    result = fetch_url(url, headers=headers, source_id=source_id)
    if result.get("success") and result.get("text"):
        try:
            return json.loads(result["text"])
        except:
            pass
    return None
```

## 分阶段执行策略（避免5分钟超时）

### Phase 1: 批量采集（≤4分钟）
- GitHub API repos（限≤15次调用/阶段）
- GitHub Trending topics（3个topic搜索）
- GitHub Trending HTML页面
- HN Algolia API（5-7个查询词）
- 保存到 `raw_data.json`

### Phase 2: 补充采集（≤4分钟）
- Reddit JSON feeds（旧版API）
- 中文源（36kr RSS, jiqizhixin, sspai）
- News站点（tldr, therundown, modelwatch）
- 论文源（arXiv, HuggingFace, Semantic Scholar）
- 保存到 `raw_data_v2.json`

### Phase 3: 解析+报告生成（≤2分钟）
- 解析RSS/HTML提取文章
- 聚合器输出分析
- 行业搜索（DuckDuckGo HTML）
- 生成最终报告
- 保存 `report-core.md` + `access-log-core.json`

## GitHub API 限额控制

```python
github_calls = 0
MAX_GITHUB_CALLS = 50  # 留10次余量给后续阶段

def track_github_call():
    global github_calls
    github_calls += 1
    return github_calls <= MAX_GITHUB_CALLS

# 每次调用后 sleep(1.2) 确保不触发瞬时限流
```

## 已验证可访问的源（核心版urllib）

| 源 | 方式 | 状态 |
|----|------|------|
| GitHub API (repo info) | `api.github.com/repos/{owner}/{repo}` | ✅ |
| GitHub API (search) | `api.github.com/search/repositories?q=...` | ✅ |
| GitHub Trending HTML | `github.com/trending?since=daily` | ✅ |
| HN Algolia | `hn.algolia.com/api/v1/search_by_date?query=...` | ✅ |
| 36kr RSS | `36kr.com/feed` | ✅ (XML) |
| OpenRouter API | `openrouter.ai/api/v1/models` | ✅ |
| Semantic Scholar API | `api.semanticscholar.org/graph/v1/paper/search` | ✅ |
| Thysrael/Horizon README | raw.githubusercontent.com | ✅ |
| arXiv HTML | `arxiv.org/list/cs.AI/recent` | ✅ (HTML parse) |
| PapersWithCode HTML | `paperswithcode.com` | ✅ |
| Reddit (old.) | `old.reddit.com/r/{sub}/.json` | ❌ 被阻止 |
| Reddit (www.) | `reddit.com/r/{sub}/hot.json` | ❌ 被阻止 |
| ProductHunt | `producthunt.com/topics/ai` | ❌ JS渲染 |
| TLDR AI | `tldr.tech/ai` | ❌ JS渲染 |
| Ben's Bites | `bensbites.beehiiv.com` | ❌ 被阻止 |
| ClawHub | `clawhub.ai` | ❌ 无法连接 |
| 机器之心 | `jiqizhixin.com` | ⚠️ 返回页面但提取失败 |
| linux.do | `linux.do/tag/ai.json` | ❌ 需要认证 |
| 量子位RSS | `qbitai.com/feed` | ⚠️ 解析错误 |

## JSON序列化陷阱（P18详解）

```python
# ❌ 错误：access_log保留bytes的data字段
access_log = {"fetches": []}
result = fetch_url(...)
access_log["fetches"].append(result)  # result包含bytes的"data"键！
json.dump(access_log, f)  # TypeError: Object of type bytes is not JSON serializable

# ✅ 正确：fetch_url只保留text（str），不保留data（bytes）
# 或者保存access_log时排除data字段
log_safe = [{k: v for k, v in r.items() if k != 'data'} for r in access_log["fetches"]]
```

## 文件保存路径约定

```
D:/openclaw-hermes/data/daily/YYYY-MM-DD/
├── raw_data.json          # Phase 1 原始数据
├── raw_data_v2.json       # Phase 2 补充数据
├── parsed_data.json       # Phase 3 解析结果
├── report-core.md         # 最终报告（核心版）
└── access-log-core.json   # 访问日志（无bytes对象）
```
