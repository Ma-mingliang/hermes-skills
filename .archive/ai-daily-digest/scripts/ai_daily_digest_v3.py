#!/usr/bin/env python3
"""
AI日报自动化脚本 v3.0
修复：数据验证时间戳逻辑（区分今日/本周/历史）
"""

import urllib.request, urllib.parse, json, os, re
from datetime import datetime, timedelta

# ========== 配置 ==========
KNOWN_PROJECTS = {
    # Agent - 全能
    "anthropics/claude-code": ("agent_allround", "Claude Code"),
    "google-gemini/gemini-cli": ("agent_allround", "Gemini CLI"),
    "openai/codex": ("agent_allround", "Codex"),
    "zhayujie/CowAgent": ("agent_allround", "CowAgent"),
    "anomalyco/opencode": ("agent_allround", "OpenCode"),
    "AstrBotDevs/AstrBot": ("agent_allround", "AstrBot"),
    # Skills
    "obra/superpowers": ("skills", "Superpowers"),
    "anthropics/skills": ("skills", "Anthropic Skills"),
    "addyosmani/agent-skills": ("skills", "Agent Skills"),
    "Shubhamsaboo/awesome-llm-apps": ("skills", "Awesome LLM Apps"),
    # Component
    "affaan-m/ECC": ("component", "ECC"),
    "langflow-ai/langflow": ("component", "Langflow"),
    "n8n-io/n8n": ("component", "n8n"),
    "browser-use/browser-use": ("component", "browser-use"),
    # MCP
    "punkpeye/awesome-mcp-servers": ("mcp", "Awesome MCP"),
    "microsoft/playwright-mcp": ("mcp", "Playwright MCP"),
    "github/github-mcp-server": ("mcp", "GitHub MCP"),
    "PrefectHQ/fastmcp": ("mcp", "FastMCP"),
}

# ========== 工具函数 ==========
def fetch_json(url, headers=None, timeout=20):
    if headers is None:
        headers = {"User-Agent": "Mozilla/5.0 (Hermes-Agent/1.0)"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())

def fetch_text(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")

# ========== Step 1: 数据收集 ==========
def collect_hn(week_ago_ts, keywords=None):
    """收集HN数据"""
    if keywords is None:
        keywords = ["AI agent", "Claude Code", "ChatGPT", "Gemini",
                    "open source AI", "MCP server", "coding agent",
                    "AI safety", "LLM", "DeepSeek"]
    
    hn_filter = f"created_at_i>{week_ago_ts}"
    all_items = []
    
    for kw in keywords:
        try:
            enc = urllib.parse.quote(kw)
            url = f"https://hn.algolia.com/api/v1/search?query={enc}&tags=story&hitsPerPage=20&numericFilters={hn_filter}"
            data = fetch_json(url)
            all_items.extend(data.get("hits", []))
        except Exception as e:
            print(f"  HN '{kw}': FAIL {e}")
    
    seen = set()
    deduped = []
    for h in all_items:
        oid = h.get("objectID")
        if oid and oid not in seen:
            seen.add(oid)
            deduped.append(h)
    
    return sorted(deduped, key=lambda x: x.get("points",0), reverse=True)

def collect_github(week_ago_str):
    """收集GitHub数据 - 两遍策略"""
    gh_headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"}
    
    queries_new = [
        f"ai+agent+created:>={week_ago_str}",
        f"coding+agent+created:>={week_ago_str}",
        f"mcp+server+created:>={week_ago_str}",
    ]
    
    queries_high = [
        "ai+agent", "coding+agent", "agent+skills",
        "mcp+server", "ai+framework"
    ]
    
    all_repos = []
    
    for q in queries_new + queries_high:
        try:
            url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}&sort=stars&per_page=10"
            data = fetch_json(url, headers=gh_headers)
            all_repos.extend(data.get("items", []))
        except Exception as e:
            print(f"  GH '{q[:30]}': FAIL {e}")
    
    seen = set()
    deduped = []
    for r in all_repos:
        rid = r.get("id")
        if rid and rid not in seen:
            seen.add(rid)
            deduped.append(r)
    
    return sorted(deduped, key=lambda x: x.get("stargazers_count",0), reverse=True)

# ========== Step 2: 数据验证（修复版） ==========
def verify_data(hn_items, gh_repos, today_str, week_ago_str):
    """验证数据时间戳，区分今日/本周/历史"""
    
    print("=" * 60)
    print("Step 2: 数据验证（时间戳）")
    print("=" * 60)
    
    hn_today = [h for h in hn_items if h.get("created","")[:10] == today_str]
    hn_week = [h for h in hn_items if h.get("created","")[:10] >= week_ago_str and h.get("created","")[:10] != today_str]
    hn_old = [h for h in hn_items if h.get("created","")[:10] < week_ago_str]
    
    print(f"\n[HN数据]")
    print(f"  总条数: {len(hn_items)}")
    print(f"  今日({today_str}): {len(hn_today)}条")
    print(f"  本周({week_ago_str}~{today_str}): {len(hn_week)}条")
    print(f"  更早: {len(hn_old)}条")
    
    gh_today = [r for r in gh_repos if r.get("created","")[:10] == today_str]
    gh_week = [r for r in gh_repos if r.get("created","")[:10] >= week_ago_str and r.get("created","")[:10] != today_str]
    gh_old = [r for r in gh_repos if r.get("created","")[:10] < week_ago_str]
    
    print(f"\n[GitHub数据]")
    print(f"  总项目: {len(gh_repos)}")
    print(f"  今日创建: {len(gh_today)}个")
    print(f"  本周创建: {len(gh_week)}个")
    print(f"  历史高星: {len(gh_old)}个")
    
    return {
        "hn": {"today": hn_today, "week": hn_week, "old": hn_old},
        "github": {"today": gh_today, "week": gh_week, "old": gh_old}
    }

# ========== Step 3: 分类 ==========
def classify_project(repo):
    """P24分类决策树 + 白名单"""
    name = repo.get("name", repo.get("full_name", ""))
    
    if name in KNOWN_PROJECTS:
        return KNOWN_PROJECTS[name]
    
    desc = (repo.get("desc") or repo.get("description") or "").lower()
    topics = [t.lower() for t in repo.get("topics", [])]
    lang = (repo.get("lang") or repo.get("language") or "").lower()
    all_text = f"{name} {desc} {' '.join(topics)}"
    
    if "skill" in desc or "skills" in desc:
        if any(w in desc for w in ["framework", "system", "platform", "engine", "cli", "harness"]):
            return ("component", "含skills但实际是系统")
        return ("skills", "描述含skill")
    
    if lang == "markdown":
        return ("skills", "Markdown仓库")
    
    if "mcp" in all_text and ("server" in all_text or "protocol" in all_text or "model context" in all_text):
        return ("mcp", "MCP server")
    
    if any(w in all_text for w in ["for ai agents", "for claude", "for agents", "agent framework", "agent sdk"]):
        return ("component", "Agent基础设施")
    if any(w in all_text for w in ["sdk", "library", "toolkit", "gateway", "proxy"]):
        return ("component", "SDK/库/工具包")
    
    if any(w in all_text for w in ["ai agent", "agent for", "autonomous agent", "coding agent"]):
        if any(w in all_text for w in ["general", "universal", "all-in-one"]):
            return ("agent_allround", "全能Agent")
        return ("agent_specialized", "专精Agent")
    
    return ("component", "默认-组件")

# ========== 主流程 ==========
def main():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_str = today.strftime("%Y-%m-%d")
    week_ago = today - timedelta(days=7)
    week_ago_str = week_ago.strftime("%Y-%m-%d")
    week_ago_ts = int(week_ago.timestamp())
    
    out_dir = f"D:/openclaw-hermes/data/daily/{today_str}"
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"=== AI日报自动化 v3.0 {today_str} ===")
    print(f"时间窗口: {week_ago_str} ~ {today_str}")
    
    print("\n[1/3] 数据收集...")
    hn = collect_hn(week_ago_ts)
    gh = collect_github(week_ago_str)
    
    print(f"  HN: {len(hn)}条")
    print(f"  GitHub: {len(gh)}个")
    
    print("\n[2/3] 数据验证...")
    verification = verify_data(hn, gh, today_str, week_ago_str)
    
    print("\n[3/3] 分类...")
    classified = {}
    for repo in gh:
        name = repo.get("full_name", "")
        cat, reason = classify_project(repo)
        classified[name] = {"category": cat, "reason": reason, "stars": repo.get("stargazers_count",0)}
    
    cats = {}
    for name, info in classified.items():
        cat = info["category"]
        if cat not in cats:
            cats[cat] = []
        cats[cat].append(name)
    
    for cat in sorted(cats.keys()):
        print(f"  {cat}: {len(cats[cat])}个")
    
    raw = {
        "date": today_str,
        "verification": verification,
        "hn": hn,
        "github": gh,
        "classified": classified,
    }
    
    with open(f"{out_dir}/raw_data_v3.json", "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n数据已保存: {out_dir}/raw_data_v3.json")

if __name__ == "__main__":
    main()
