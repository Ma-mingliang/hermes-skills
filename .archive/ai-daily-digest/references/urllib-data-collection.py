# Python urllib 数据收集模板（WSL/terminal不可用时使用）
# 直接在 execute_code 中运行，不依赖 shell/curl

import urllib.request
import json
from datetime import datetime

def fetch_hn(query, hits=10, days=3):
    """HN Algolia API — 最可靠的AI新闻源"""
    ts = int(datetime.now().timestamp()) - days * 86400
    url = f"https://hn.algolia.com/api/v1/search?query={query}&tags=story&hitsPerPage={hits}&numericFilters=created_at_i>{ts}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    return data.get("hits", [])

def fetch_github(query, per_page=10):
    """GitHub REST API — 项目搜索"""
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={per_page}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    return data.get("items", [])

def deduplicate(items, key_fn, sort_fn=None):
    """去重+排序"""
    seen = set()
    unique = []
    if sort_fn:
        items = sorted(items, key=sort_fn, reverse=True)
    for item in items:
        k = key_fn(item)
        if k not in seen:
            seen.add(k)
            unique.append(item)
    return unique

# === 示例用法 ===
# HN搜索
queries = ["AI+agent", "claude+code", "LLM+benchmark", "deepseek", "gemini", "openai+gpt", "skills+agent", "MCP+server"]
hn_hits = []
for q in queries:
    try:
        hits = fetch_hn(q, hits=10, days=3)
        hn_hits.extend(hits)
    except Exception as e:
        print(f"HN query '{q}' failed: {e}")

hn_unique = deduplicate(hn_hits, lambda h: h.get("title","")[:50], lambda h: h.get("points",0))
print(f"HN: {len(hn_unique)} unique stories")

# GitHub搜索
gh_queries = ["AI+agent+created:>2026-05-01", "LLM+skills+created:>2026-05-01", "claude+code+created:>2026-05-01"]
gh_repos = []
for q in gh_queries:
    try:
        items = fetch_github(q, per_page=10)
        gh_repos.extend(items)
    except Exception as e:
        print(f"GH query '{q}' failed: {e}")

gh_unique = deduplicate(gh_repos, lambda r: r["full_name"], lambda r: r["stargazers_count"])
print(f"GitHub: {len(gh_unique)} unique repos")
