#!/usr/bin/env python3
"""
AI日报自动化脚本 v2.0
完整工作流: 数据收集→验证→分类→报告生成→质量检查
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
    "hesreallyhim/awesome-claude-code": ("skills", "Awesome Claude Code"),
    "sickn33/antigravity-awesome-skills": ("skills", "Antigravity Skills"),
    "Shubhamsaboo/awesome-llm-apps": ("skills", "Awesome LLM Apps"),
    "VoltAgent/awesome-design-md": ("skills", "Awesome Design"),
    "dair-ai/Prompt-Engineering-Guide": ("skills", "Prompt Guide"),
    "github/awesome-copilot": ("skills", "Awesome Copilot"),
    # Component
    "affaan-m/ECC": ("component", "ECC"),
    "langflow-ai/langflow": ("component", "Langflow"),
    "x1xhlol/system-prompts-and-models-of-ai-tools": ("component", "System Prompts"),
    "n8n-io/n8n": ("component", "n8n"),
    "browser-use/browser-use": ("component", "browser-use"),
    "microsoft/autogen": ("component", "AutoGen"),
    "crewAIInc/crewAI": ("component", "CrewAI"),
    "D4Vinci/Scrapling": ("component", "Scrapling"),
    "creativetimofficial/ui": ("component", "UI Kit"),
    # MCP
    "punkpeye/awesome-mcp-servers": ("mcp", "Awesome MCP"),
    "microsoft/playwright-mcp": ("mcp", "Playwright MCP"),
    "github/github-mcp-server": ("mcp", "GitHub MCP"),
    "PrefectHQ/fastmcp": ("mcp", "FastMCP"),
    "modelcontextprotocol/servers": ("mcp", "MCP Servers"),
    "ChromeDevTools/chrome-devtools-mcp": ("mcp", "Chrome MCP"),
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
    if keywords is None:
        keywords = ["AI agent", "Claude Code", "ChatGPT", "Gemini",
                    "open source AI", "MCP server", "coding agent",
                    "AI safety", "LLM", "DeepSeek", "OpenAI Codex",
                    "Cursor AI", "Hermes agent", "MCP protocol"]
    
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
    gh_headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"}
    
    queries = [
        f"ai+agent+created:>={week_ago_str}",
        f"coding+agent+created:>={week_ago_str}",
        f"mcp+server+created:>={week_ago_str}",
        "ai+agent", "coding+agent", "agent+skills",
        "mcp+server", "ai+framework"
    ]
    
    all_repos = []
    for q in queries:
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

def collect_openrouter():
    try:
        data = fetch_json("https://openrouter.ai/api/v1/models")
        return data.get("data", [])
    except Exception as e:
        print(f"  OpenRouter: FAIL {e}")
        return []

def collect_36kr():
    try:
        text = fetch_text("https://36kr.com/feed")
        items = re.findall(r'<item>(.*?)</item>', text, re.DOTALL)
        news = []
        for item in items:
            tm = re.search(r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', item)
            lm = re.search(r'<link>(.*?)</link>', item)
            if tm and lm:
                news.append({"title": tm.group(1).strip(), "link": lm.group(1).strip()})
        return news
    except Exception as e:
        print(f"  36kr: FAIL {e}")
        return []

def collect_industry_hn(week_ago_ts):
    hn_filter = f"created_at_i>{week_ago_ts}"
    queries = ["AI healthcare", "AI education", "AI finance",
               "AI enterprise", "AI security", "AI robotics"]
    all_items = []
    for q in queries:
        try:
            enc = urllib.parse.quote(q)
            url = f"https://hn.algolia.com/api/v1/search?query={enc}&tags=story&hitsPerPage=5&numericFilters={hn_filter}"
            data = fetch_json(url)
            all_items.extend(data.get("hits", []))
        except:
            pass
    seen = set()
    deduped = []
    for h in all_items:
        oid = h.get("objectID")
        if oid and oid not in seen:
            seen.add(oid)
            deduped.append(h)
    return sorted(deduped, key=lambda x: x.get("points",0), reverse=True)

# ========== Step 2: 分类 ==========
def classify_project(repo):
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
    
    if any(w in all_text for w in ["for ai agents", "for claude", "for agents", "agent framework", "agent sdk", "agent harness"]):
        return ("component", "Agent基础设施")
    if any(w in all_text for w in ["sdk", "library", "toolkit", "gateway", "proxy"]):
        return ("component", "SDK/库/工具包")
    
    if any(w in all_text for w in ["ai agent", "agent for", "autonomous agent", "coding agent", "llm agent"]):
        if any(w in all_text for w in ["general", "universal", "all-in-one", "everything"]):
            return ("agent_allround", "全能Agent")
        return ("agent_specialized", "专精Agent")
    
    return ("component", "默认-组件")

# ========== Step 3: 质量检查 ==========
def validate_report(report):
    checks = []
    def check(name, cond):
        checks.append({"name": name, "pass": cond})
    
    check("Agent定义", "Agent定义" in report)
    check("全能Agent", "全能型Agent" in report)
    check("专精Agent", "专精型Agent" in report)
    check("Agent组件", "Agent组件" in report)
    check("使用指南", "使用指南" in report)
    check("高星Agent", "高星" in report)
    check("对比表", "| Agent" in report)
    check("拆分分析", "拆分分析" in report)
    check("归纳", "归纳" in report)
    check("GitHub链接", report.count("github.com") >= 10)
    check("Skills定义", "Skills定义" in report)
    check("6类emoji", all(c in report for c in ["📉", "🔒", "⚡", "🔬", "🔍", "📦"]))
    check("痛点", "痛点" in report)
    check("原理", "原理" in report)
    check("模型动态", "模型动态" in report)
    check("行业热点", "行业热点" in report)
    check("MCP动态", "MCP动态" in report)
    check("数据面板", "数据面板" in report)
    check("核心信号", "核心信号" in report)
    check("AI基础", "AI基础" in report or "Day" in report)
    check("今日目标", "今日目标" in report)
    check("小测验", "小测验" in report)
    check("无第X类", "第一类：" not in report and "第二类：" not in report)
    
    passed = sum(1 for c in checks if c["pass"])
    total = len(checks)
    failed = [c["name"] for c in checks if not c["pass"]]
    
    return {"passed": passed, "total": total, "failed": failed}

# ========== 主流程 ==========
def main():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_str = today.strftime("%Y-%m-%d")
    week_ago = today - timedelta(days=7)
    week_ago_str = week_ago.strftime("%Y-%m-%d")
    week_ago_ts = int(week_ago.timestamp())
    
    out_dir = f"D:/openclaw-hermes/data/daily/{today_str}"
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"=== AI日报自动化 {today_str} ===")
    
    # 1. 数据收集
    print("\n[1/4] 数据收集...")
    hn = collect_hn(week_ago_ts)
    gh = collect_github(week_ago_str)
    models = collect_openrouter()
    kr = collect_36kr()
    industry = collect_industry_hn(week_ago_ts)
    
    print(f"  HN: {len(hn)}条")
    print(f"  GitHub: {len(gh)}个")
    print(f"  OpenRouter: {len(models)}模型")
    print(f"  36kr: {len(kr)}篇")
    print(f"  行业HN: {len(industry)}条")
    
    # 2. 分类
    print("\n[2/4] 分类...")
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
    
    # 3. 保存数据
    print("\n[3/4] 保存数据...")
    raw = {
        "date": today_str,
        "hn": hn,
        "github": gh,
        "openrouter": {"count": len(models), "models": models[:50]},
        "36kr": kr,
        "industry": industry,
        "classified": classified,
    }
    
    with open(f"{out_dir}/raw_data.json", "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n数据已保存: {out_dir}/raw_data.json")
    print("=== 完成 ===")

if __name__ == "__main__":
    main()
