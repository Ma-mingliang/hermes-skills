#!/usr/bin/env python3
"""
AI日报数据收集脚本
解决的问题：
1. 分类误判 → 已知项目白名单
2. GitHub日期过滤返回0条 → 两遍策略
3. 36kr RSS解析 → 正则+CDATA处理
用法: python ai_daily_digest.py
输出: D:/openclaw-hermes/data/daily/YYYY-MM-DD/raw_data.json
"""

import urllib.request, urllib.parse, json, os, re
from datetime import datetime, timedelta

# ========== 白名单 ==========
KNOWN_PROJECTS = {
    "anthropics/claude-code": "agent_allround",
    "google-gemini/gemini-cli": "agent_allround",
    "openai/codex": "agent_allround",
    "zhayujie/CowAgent": "agent_allround",
    "anomalyco/opencode": "agent_specialized",
    "karpathy/autoresearch": "agent_specialized",
    "obra/superpowers": "skills",
    "anthropics/skills": "skills",
    "addyosmani/agent-skills": "skills",
    "affaan-m/ECC": "component",
    "langflow-ai/langflow": "component",
    "punkpeye/awesome-mcp-servers": "mcp",
    "microsoft/playwright-mcp": "mcp",
    "github/github-mcp-server": "mcp",
    "PrefectHQ/fastmcp": "mcp",
}

# ========== 工具函数 ==========
def fetch_json(url, headers=None, timeout=15):
    if headers is None:
        headers = {"User-Agent": "Mozilla/5.0 (Hermes-Agent/1.0)"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())

def fetch_text(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")

# ========== 数据收集 ==========
def collect_hn(week_ago_ts, keywords=None):
    """收集HN数据"""
    if keywords is None:
        keywords = ["AI agent", "Claude", "ChatGPT", "Gemini", "open source AI",
                    "MCP model context protocol", "coding agent", "AI safety", "LLM", "DeepSeek"]
    
    hn_filter = f"created_at_i>{week_ago_ts}"
    all_items = []
    
    for kw in keywords:
        try:
            enc = urllib.parse.quote(kw)
            url = f"https://hn.algolia.com/api/v1/search?query={enc}&tags=story&hitsPerPage=15&numericFilters={hn_filter}"
            data = fetch_json(url)
            all_items.extend(data.get("hits", []))
            print(f"  HN '{kw}': {len(data.get('hits', []))}")
        except Exception as e:
            print(f"  HN '{kw}': FAIL {e}")
    
    # 去重
    seen = set()
    deduped = []
    for h in all_items:
        oid = h.get("objectID")
        if oid and oid not in seen:
            seen.add(oid)
            deduped.append(h)
    
    return sorted(deduped, key=lambda x: x.get("points", 0), reverse=True)

def collect_github(week_ago_str):
    """收集GitHub数据 - 两遍策略（日期过滤 + 无过滤高星搜索）"""
    gh_headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"}
    
    # 第一遍: 日期过滤（找本周新增，结果少正常）
    queries_new = [
        f"ai+agent+created:>={week_ago_str}",
        f"ai+tool+created:>={week_ago_str}",
        f"mcp+server+created:>={week_ago_str}",
    ]
    
    # 第二遍: 无过滤（找高星项目）
    queries_high = [
        "ai+agent", "coding+agent", "agent+skills",
        "mcp+server", "ai+framework", "llm+agent"
    ]
    
    all_repos = []
    
    for q in queries_new + queries_high:
        try:
            url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}&sort=stars&per_page=10"
            data = fetch_json(url, headers=gh_headers)
            all_repos.extend(data.get("items", []))
            print(f"  GH '{q[:30]}': {len(data.get('items', []))}")
        except Exception as e:
            print(f"  GH '{q[:30]}': FAIL {e}")
    
    # 去重
    seen = set()
    deduped = []
    for r in all_repos:
        rid = r.get("id")
        if rid and rid not in seen:
            seen.add(rid)
            deduped.append(r)
    
    return sorted(deduped, key=lambda x: x.get("stargazers_count", 0), reverse=True)

def collect_openrouter():
    """收集OpenRouter模型数据"""
    try:
        data = fetch_json("https://openrouter.ai/api/v1/models")
        models = data.get("data", [])
        print(f"  OpenRouter: {len(models)} models")
        return models
    except Exception as e:
        print(f"  OpenRouter: FAIL {e}")
        return []

def collect_36kr():
    """收集36kr RSS（CDATA格式处理）"""
    try:
        text = fetch_text("https://36kr.com/feed")
        items = re.findall(r'<item>(.*?)</item>', text, re.DOTALL)
        news = []
        for item in items:
            # 处理CDATA和非CDATA两种格式
            tm = re.search(r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', item)
            lm = re.search(r'<link>(.*?)</link>', item)
            if tm and lm:
                news.append({"title": tm.group(1).strip(), "link": lm.group(1).strip()})
        print(f"  36kr: {len(news)} articles")
        return news
    except Exception as e:
        print(f"  36kr: FAIL {e}")
        return []

# ========== 分类 ==========
def classify_project(repo):
    """P24分类决策树 + 白名单修正"""
    name = repo.get("full_name", repo.get("name", ""))
    
    # 白名单优先
    if name in KNOWN_PROJECTS:
        return KNOWN_PROJECTS[name], "白名单"
    
    desc = (repo.get("description") or "").lower()
    topics = [t.lower() for t in repo.get("topics", [])]
    lang = (repo.get("language") or "").lower()
    all_text = f"{name} {desc} {' '.join(topics)}"
    
    # P24决策树
    if "skill" in desc or "skills" in desc:
        if any(w in desc for w in ["framework", "system", "platform", "engine", "cli"]):
            return "component", "含skills但实际是系统"
        return "skills", "描述含skill"
    
    if lang == "markdown":
        return "skills", "Markdown仓库"
    
    if "mcp" in all_text and ("server" in all_text or "protocol" in all_text):
        return "mcp", "MCP server"
    
    if any(w in all_text for w in ["for ai agents", "for claude", "agent framework", "agent sdk"]):
        return "component", "Agent基础设施"
    if any(w in all_text for w in ["sdk", "library", "toolkit", "gateway", "proxy"]):
        return "component", "SDK/库"
    
    if any(w in all_text for w in ["ai agent", "agent for", "autonomous agent", "coding agent"]):
        if any(w in all_text for w in ["general", "universal", "all-in-one"]):
            return "agent_allround", "全能Agent"
        return "agent_specialized", "专精Agent"
    
    return "component", "默认-组件"

# ========== 主流程 ==========
def main():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_str = today.strftime("%Y-%m-%d")
    week_ago = today - timedelta(days=7)
    week_ago_str = week_ago.strftime("%Y-%m-%d")
    week_ago_ts = int(week_ago.timestamp())
    
    out_dir = f"D:/openclaw-hermes/data/daily/{today_str}"
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"=== AI日报数据收集 {today_str} ===")
    print(f"7天窗口: {week_ago_str} ~ {today_str}")
    
    # 1. 数据收集
    print("\n[1/4] HN Algolia...")
    hn = collect_hn(week_ago_ts)
    
    print("\n[2/4] GitHub API (两遍策略)...")
    gh = collect_github(week_ago_str)
    
    print("\n[3/4] OpenRouter + 36kr...")
    models = collect_openrouter()
    kr = collect_36kr()
    
    # 2. 分类
    print("\n[4/4] 分类...")
    classified = {}
    for repo in gh:
        name = repo.get("full_name", "")
        cat, reason = classify_project(repo)
        classified[name] = {
            "category": cat,
            "reason": reason,
            "stars": repo.get("stargazers_count", 0),
            "desc": (repo.get("description") or "")[:100]
        }
    
    cats = {}
    for name, info in classified.items():
        cat = info["category"]
        if cat not in cats:
            cats[cat] = []
        cats[cat].append(name)
    
    for cat in sorted(cats.keys()):
        print(f"  {cat}: {len(cats[cat])}个")
    
    # 3. 保存
    raw = {
        "date": today_str,
        "hn": {
            "total": len(hn),
            "items": [{"title": h.get("title",""), "url": h.get("url",""),
                       "points": h.get("points",0), "comments": h.get("num_comments",0)}
                      for h in hn[:50]]
        },
        "github": {
            "total": len(gh),
            "repos": [{"name": r["full_name"], "stars": r.get("stargazers_count",0),
                       "desc": r.get("description",""), "lang": r.get("language",""),
                       "url": r.get("html_url",""), "topics": r.get("topics",[]),
                       "created": r.get("created_at","")}
                      for r in gh[:50]]
        },
        "openrouter": {"count": len(models)},
        "36kr": kr[:20],
        "classification": classified,
    }
    
    with open(f"{out_dir}/raw_data.json", "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n=== 完成 ===")
    print(f"HN: {len(hn)}条, GitHub: {len(gh)}个, OpenRouter: {len(models)}模型, 36kr: {len(kr)}篇")
    print(f"保存: {out_dir}/raw_data.json")

if __name__ == "__main__":
    main()
