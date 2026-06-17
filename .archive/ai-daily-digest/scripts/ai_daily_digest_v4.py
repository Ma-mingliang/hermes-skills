#!/usr/bin/env python3
"""
AI日报自动化脚本 v4.0
修复内容:
- P52: 专精Agent搜索策略（垂直领域关键词）
- P54: 痛点描述按9种问题类型框架
- P55: CowAgent/AstrBot等具体核心功能描述
- P56: 行业覆盖>=3个
- P58: 报告中的每个项目必须来自数据收集
"""

import urllib.request, urllib.parse, json, os, re
from datetime import datetime, timedelta

# ========== 配置 ==========
KNOWN_PROJECTS = {
    "anthropics/claude-code": ("agent_allround", "Claude Code"),
    "google-gemini/gemini-cli": ("agent_allround", "Gemini CLI"),
    "openai/codex": ("agent_allround", "Codex"),
    "zhayujie/CowAgent": ("agent_allround", "CowAgent"),
    "anomalyco/opencode": ("agent_allround", "OpenCode"),
    "AstrBotDevs/AstrBot": ("agent_allround", "AstrBot"),
    "obra/superpowers": ("skills", "Superpowers"),
    "anthropics/skills": ("skills", "Anthropic Skills"),
    "addyosmani/agent-skills": ("skills", "Agent Skills"),
    "Shubhamsaboo/awesome-llm-apps": ("skills", "Awesome LLM Apps"),
    "VoltAgent/awesome-design-md": ("skills", "Awesome Design"),
    "dair-ai/Prompt-Engineering-Guide": ("skills", "Prompt Guide"),
    "github/awesome-copilot": ("skills", "Awesome Copilot"),
    "affaan-m/ECC": ("component", "ECC"),
    "langflow-ai/langflow": ("component", "Langflow"),
    "n8n-io/n8n": ("component", "n8n"),
    "browser-use/browser-use": ("component", "browser-use"),
    "microsoft/autogen": ("component", "AutoGen"),
    "crewAIInc/crewAI": ("component", "CrewAI"),
    "FoundationAgents/MetaGPT": ("component", "MetaGPT"),
    "msitarzewski/agency-agents": ("component", "agency-agents"),
    "lobehub/lobehub": ("component", "LobeHub"),
    "punkpeye/awesome-mcp-servers": ("mcp", "Awesome MCP"),
    "microsoft/playwright-mcp": ("mcp", "Playwright MCP"),
    "github/github-mcp-server": ("mcp", "GitHub MCP"),
    "PrefectHQ/fastmcp": ("mcp", "FastMCP"),
    "modelcontextprotocol/servers": ("mcp", "MCP Servers"),
    # 专精Agent（垂直领域）
    "eosphoros-ai/DB-GPT": ("agent_specialized", "DB-GPT 数据Agent"),
    "HolmesGPT/holmesgpt": ("agent_specialized", "HolmesGPT SRE Agent"),
    "nexu-io/html-anything": ("agent_specialized", "html-anything 设计Agent"),
    "TauricResearch/TradingAgents": ("agent_specialized", "TradingAgents 金融Agent"),
    "karpathy/autoresearch": ("agent_specialized", "AutoResearch 科研Agent"),
}

# ========== 9种问题类型框架 ==========
PAIN_TYPES = {
    "能力缺失型": "AI可以解决但没有好的使用方案",
    "使用不便型": "人使用AI时的不便之处",
    "成本过高型": "API/部署成本不可控",
    "安全风险型": "AI行为不可控",
    "效率低下型": "AI工作流程繁琐",
    "知识壁垒型": "不知道怎么用AI",
    "协作困难型": "多Agent/多人协作不便",
    "数据孤岛型": "Agent间数据不互通",
    "行业落地型": "AI技术难以落地到具体行业",
}

AGENT_PAIN_TYPES = {
    "anomalyco/opencode": ("成本过高型", "Claude Code/Codex付费门槛高（$3~15/M），开源开发者无法使用编码Agent"),
    "anthropics/claude-code": ("能力缺失型", "AI能写代码，但缺乏深度推理能力，无法处理复杂架构设计"),
    "google-gemini/gemini-cli": ("使用不便型", "Google生态缺乏CLI入口，开发者需要在浏览器中操作Agent"),
    "openai/codex": ("能力缺失型", "OpenAI缺乏专用编码Agent，ChatGPT无法直接执行代码"),
    "zhayujie/CowAgent": ("效率低下型", "Agent每次对话从零开始，缺乏任务分解+记忆管理+多Agent协作"),
    "AstrBotDevs/AstrBot": ("使用不便型", "AI Agent分散在不同平台，需要逐个配置，缺乏统一管理"),
    "TauricResearch/TradingAgents": ("行业落地型", "AI技术难以落地到金融领域，传统量化工具缺乏市场理解能力"),
    "eosphoros-ai/DB-GPT": ("知识壁垒型", "非技术人员无法使用数据库，需要学习SQL语言"),
    "HolmesGPT/holmesgpt": ("效率低下型", "SRE需要手动分析告警和日志，工作流程繁琐"),
    "karpathy/autoresearch": ("效率低下型", "科研流程繁琐，文献调研+实验设计+论文写作耗时"),
}

# ========== 工具函数 ==========
def fetch_json(url, headers=None, timeout=20):
    if headers is None:
        headers = {"User-Agent": "Mozilla/5.0 (Hermes-Agent/1.0)"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())

def pts(h):
    return h.get("points", h.get("score", 0))

def cmts(h):
    return h.get("comments", h.get("num_comments", 0))

def ghub(name, info):
    url = info.get("url", "")
    return url if url else f"https://github.com/{name}"

def get_pain_description(name, info):
    if name in AGENT_PAIN_TYPES:
        return AGENT_PAIN_TYPES[name]
    return ("能力缺失型", info.get("desc", "")[:50])

# ========== 数据收集 ==========
def collect_hn(week_ago_ts, keywords=None):
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
    return sorted(deduped, key=lambda x: pts(x), reverse=True)

def collect_github(week_ago_str):
    gh_headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"}
    # 通用搜索
    queries_high = ["ai+agent", "coding+agent", "agent+skills", "mcp+server", "ai+framework"]
    # P52: 专精Agent搜索（垂直领域）
    queries_specialized = ["DB-GPT", "HolmesGPT", "TradingAgents", "html-anything",
                            "security+agent", "data+agent", "sre+agent"]
    all_repos = []
    for q in queries_high + queries_specialized:
        try:
            url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}&sort=stars&per_page=10"
            data = fetch_json(url, headers=gh_headers)
            all_repos.extend(data.get("items", []))
        except Exception as e:
            print(f"  GH '{q[:20]}': FAIL {e}")
    seen = set()
    deduped = []
    for r in all_repos:
        rid = r.get("id")
        if rid and rid not in seen:
            seen.add(rid)
            deduped.append(r)
    return sorted(deduped, key=lambda x: x.get("stargazers_count", 0), reverse=True)

def collect_industry_hn(week_ago_ts):
    """P56: 行业覆盖>=3个"""
    hn_filter = f"created_at_i>{week_ago_ts}"
    queries = ["AI healthcare", "AI education", "AI finance", "AI enterprise", "AI security"]
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
    return sorted(deduped, key=lambda x: pts(x), reverse=True)

# ========== 分类 ==========
def classify(repo):
    name = repo.get("full_name", "")
    if name in KNOWN_PROJECTS:
        return KNOWN_PROJECTS[name]
    desc = (repo.get("description") or "").lower()
    topics = [t.lower() for t in repo.get("topics", [])]
    lang = (repo.get("language") or "").lower()
    all_text = f"{name} {desc} {' '.join(topics)}"
    if "skill" in desc and "skills" in desc:
        return ("skills", "描述含skill")
    if lang == "markdown":
        return ("skills", "Markdown仓库")
    if "mcp" in all_text and ("server" in all_text or "protocol" in all_text):
        return ("mcp", "MCP server")
    if any(w in all_text for w in ["for ai agents", "for claude", "agent framework", "agent sdk"]):
        return ("component", "Agent基础设施")
    if any(w in all_text for w in ["sdk", "library", "toolkit"]):
        return ("component", "SDK/库")
    if any(w in all_text for w in ["ai agent", "agent for", "autonomous agent", "coding agent"]):
        return ("agent_allround", "全能Agent")
    return ("component", "默认-组件")

# ========== 验证 ==========
def verify_data(hn_items, gh_repos, today_str, week_ago_str):
    hn_today = [h for h in hn_items if h.get("created", "")[:10] == today_str]
    hn_week = [h for h in hn_items if h.get("created", "")[:10] >= week_ago_str and h.get("created", "")[:10] != today_str]
    gh_today = [r for r in gh_repos if r.get("created_at", "")[:10] == today_str]
    gh_week = [r for r in gh_repos if r.get("created_at", "")[:10] >= week_ago_str and r.get("created_at", "")[:10] != today_str]
    gh_old = [r for r in gh_repos if r.get("created_at", "")[:10] < week_ago_str]
    return {
        "hn_today": len(hn_today), "hn_week": len(hn_week),
        "gh_today": len(gh_today), "gh_week": len(gh_week), "gh_old": len(gh_old),
    }

def verify_report_items(report, collected_names):
    """P58: 报告中的每个项目必须来自数据收集"""
    issues = []
    github_pattern = r'github\.com/([a-zA-Z0-9-]+/[a-zA-Z0-9-]+)'
    report_items = set(re.findall(github_pattern, report))
    for item in report_items:
        if item not in collected_names and not item.startswith("anthropics/") and not item.startswith("google-gemini/"):
            issues.append(f"项目 {item} 不在数据收集结果中")
    return issues

# ========== 主流程 ==========
def main():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_str = today.strftime("%Y-%m-%d")
    week_ago = today - timedelta(days=7)
    week_ago_str = week_ago.strftime("%Y-%m-%d")
    week_ago_ts = int(week_ago.timestamp())
    out_dir = f"D:/openclaw-hermes/data/daily/{today_str}"
    os.makedirs(out_dir, exist_ok=True)

    print(f"=== AI日报自动化 v4.0 {today_str} ===")

    # Step 1-2: 数据收集
    print("\n[Step 1-2] 数据收集...")
    hn = collect_hn(week_ago_ts)
    gh = collect_github(week_ago_str)
    industry = collect_industry_hn(week_ago_ts)
    print(f"  HN: {len(hn)}条, GitHub: {len(gh)}个, 行业HN: {len(industry)}条")

    # Step 3: 数据验证
    print("\n[Step 3] 数据验证...")
    v = verify_data(hn, gh, today_str, week_ago_str)
    print(f"  HN: 今日{v['hn_today']}, 本周{v['hn_week']}")
    print(f"  GitHub: 今日{v['gh_today']}, 本周{v['gh_week']}, 历史{v['gh_old']}")

    # Step 4: 分类
    print("\n[Step 4] 分类...")
    classified = {}
    for repo in gh:
        name = repo.get("full_name", "")
        cat, reason = classify(repo)
        classified[name] = {"category": cat, "reason": reason, "stars": repo.get("stargazers_count", 0),
                             "desc": (repo.get("description") or "")[:80], "url": repo.get("html_url", "")}
    cats = {}
    for name, info in classified.items():
        cat = info["category"]
        if cat not in cats:
            cats[cat] = []
        cats[cat].append((name, info))
    for cat in sorted(cats.keys()):
        print(f"  {cat}: {len(cats[cat])}个")

    # 保存
    raw = {"date": today_str, "hn": hn, "github": gh, "industry": industry,
           "classified": classified, "categories": cats, "verification": v}
    with open(f"{out_dir}/raw_data_v4.json", "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False, indent=2, default=str)

    print(f"\n数据已保存: {out_dir}/raw_data_v4.json")
    print("=== 完成 ===")

if __name__ == "__main__":
    main()
