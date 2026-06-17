# 分类Python函数（改进版）

> 用于 execute_code 中的自动分类逻辑
> 改进日期：2026-05-30
> 改进原因：原版函数按关键词匹配将 ECC/Dify/Gemini CLI 误判为 MCP

## 改进后的分类函数

```python
def classify_repo(repo):
    """改进版分类函数，解决 ECC→MCP、Dify→MCP 误判问题"""
    desc = (repo.get("description") or "").lower()
    topics = [t.lower() for t in repo.get("topics", [])]
    lang = (repo.get("language") or "").lower()
    full_name = (repo.get("full_name") or "").lower()
    
    # === Step 1: Skills 检测 ===
    skill_signals = [
        "markdown-only skills",
        "skills for claude",
        "skills for coding",
        "collection of skills",
        "set of skills",
        "library of skills",
        "agent skills",  # 注意：如果后面跟"framework"则不是
        "skill.md",
        "claude.md skills",
    ]
    # "skill" 在描述中 + 不含 "framework"/"platform"/"system"
    has_skill = any(s in desc for s in skill_signals)
    has_skill_word = "skill" in desc
    is_framework = any(w in desc for w in ["framework", "platform", "system", "sdk", "toolkit"])
    if has_skill or (has_skill_word and not is_framework):
        return "skill"
    
    # === Step 3: MCP 检测（最高优先级，但需排除误判） ===
    # ⚠️ 关键：必须显式提及 "mcp server" 或 "model context protocol"
    mcp_signals = [
        "mcp server",
        "model context protocol",
        "mcp tool",
        "mcp for",
        "mcp client",
    ]
    mcp_topics = ["mcp", "mcp-server", "model-context-protocol"]
    
    is_explicit_mcp = any(s in desc for s in mcp_signals)
    has_mcp_topic = any(t in topics for t in mcp_topics)
    
    # 排除误判：如果描述中有 "agent harness" 或 "workflow" 但不是 MCP
    mcp_false_positives = [
        "agent harness",    # ECC
        "workflow",         # Dify
        "gemini",           # Gemini CLI（是Agent不是MCP）
        "coding agent",     # 编码Agent
        "open-source ai agent",  # Agent
    ]
    is_false_mcp = any(w in desc for w in mcp_false_positives)
    
    if (is_explicit_mcp or has_mcp_topic) and not is_false_mcp:
        return "mcp"
    
    # === Step 4: Agent组件检测 ===
    component_signals = [
        "for ai agent",
        "for claude code",
        "for coding agent",
        "for cursor",
        "for windsurf",
        "let ai agent",
        "agent framework",
        "agent sdk",
        "agent harness",       # ECC 类型
        "agent performance",   # ECC 类型
    ]
    component_topics = [
        "agent-framework",
        "ai-agents",
        "agent-sdk",
        "agent-skills",
    ]
    
    if any(s in desc for s in component_signals) or any(t in topics for t in component_topics):
        return "component"
    
    # === Step 5: Agent 检测 ===
    agent_signals = [
        "ai agent",
        "agent for",
        "autonomous agent",
        "coding agent",
        "agent that",
        "agent platform",
        "agent system",
        "open-source ai agent",  # Gemini CLI
        "agentic",               # Dify
    ]
    agent_topics = ["agent", "llm-agent", "ai-agent", "agents"]
    
    has_agent_desc = any(s in desc for s in agent_signals)
    has_agent_topic = any(t in topics for t in agent_topics)
    
    # 排除：描述说 "for agents" 的实际上是组件
    if "for agent" in desc or "for ai agent" in desc:
        return "component"
    
    if has_agent_desc or has_agent_topic:
        return "agent"
    
    # === Step 6: Fallback → 组件 ===
    return "component"


# 子分类：全能Agent vs 专精Agent
def classify_agent_type(repo):
    """判断Agent是全能的还是专精的"""
    desc = (repo.get("description") or "").lower()
    topics = [t.lower() for t in repo.get("topics", [])]
    
    # 全能信号（通用型）
    general_signals = [
        "general-purpose",
        "general purpose",
        "universal",
        "multi-purpose",
        "multi purpose",
        "coding agent",
        "terminal agent",
        "cli agent",
        "workflow",
        "platform",
    ]
    
    # 专精信号（垂直领域）
    specialized_signals = [
        "database", "sql", "data",
        "security", "sre", "devops", "monitoring",
        "trading", "finance", "stock",
        "design", "html", "css", "ui",
        "research", "paper", "academic",
        "medical", "health", "clinical",
    ]
    
    has_general = any(s in desc for s in general_signals)
    has_specialized = any(s in desc for s in specialized_signals)
    
    if has_specialized and not has_general:
        return "specialized"
    return "general"
```

## 误判案例与修正

| 仓库 | 原分类 | 修正后 | 原因 |
|------|--------|--------|------|
| affaan-m/ECC | mcp | component | 描述含"agent harness"，不含"mcp server" |
| langgenius/dify | mcp | agent | 描述含"agentic workflow"，不含"mcp" |
| google-gemini/gemini-cli | mcp | agent | 描述含"open-source AI agent" |
| anthropics/skills | agent | skill | 描述含"Agent Skills" |
| obra/superpowers | agent | component | 描述含"agentic skills framework" |

## 已知项目速查表（2026-05-30新增）

> **为什么需要**：启发式分类必然会误判高星项目。在调用 classify_repo() 之前，先查此表。这是P0级步骤——跳过它会导致 hermes-agent 被归为"component"。

```python
KNOWN_CLASSIFICATIONS = {
    # Agent — 全能型
    "NousResearch/hermes-agent": ("agent", "general"),
    "anomalyco/opencode": ("agent", "general"),
    "google-gemini/gemini-cli": ("agent", "general"),
    "ruvnet/ruflo": ("agent", "general"),
    "CherryHQ/cherry-studio": ("agent", "general"),
    "HKUDS/nanobot": ("agent", "general"),
    
    # Agent — 专精型
    "eosphoros-ai/DB-GPT": ("agent", "specialized"),
    "robusta-dev/holmesgpt": ("agent", "specialized"),
    "TauricResearch/TradingAgents": ("agent", "specialized"),
    "ai-soc/aisoc": ("agent", "specialized"),
    
    # Skills
    "obra/superpowers": ("skill", None),         # "agentic skills framework" = skills仓库
    "anthropics/skills": ("skill", None),         # 官方Agent Skills
    "wanshuiyin/Auto-claude-code-research-in-sleep": ("skill", None),  # ARIS, Markdown-only
    
    # Components
    "affaan-m/ECC": ("component", None),          # agent harness, 非agent
    "langflow-ai/langflow": ("component", None),   # agent框架, 非独立agent
    "langgenius/dify": ("component", None),        # workflow平台
    "langchain-ai/langchain": ("component", None),  # agent engineering platform
    
    # MCP
    "microsoft/playwright-mcp": ("mcp", None),
    "github/github-mcp-server": ("mcp", None),
    "PrefectHQ/fastmcp": ("mcp", None),
    "googleapis/mcp-toolbox": ("mcp", None),
    "GLips/Figma-Context-MCP": ("mcp", None),
    "punkpeye/awesome-mcp-servers": ("mcp", None),
    
    # Resource（不是Agent/Skills/组件，只是资源合集）
    "Shubhamsaboo/awesome-llm-apps": ("resource", None),
    "Snailclimb/JavaGuide": ("resource", None),
    "x1xhlol/system-prompts-and-models-of-ai-tools": ("resource", None),
}
```

## 使用方式（必须先用速查表！）

```python
# Step 0: 先查已知项目表
full_name = repo.get("full_name", "")
if full_name in KNOWN_CLASSIFICATIONS:
    cat, subcat = KNOWN_CLASSIFICATIONS[full_name]
    return cat, subcat

# Step 1-6: 启发式分类
cat = classify_repo(repo)
if cat == "agent":
    subcat = classify_agent_type(repo)
```

## 36kr RSS 解析修复（2026-05-30新增）

**问题**：正则 `r'<item>.*?<title><!\[CDATA\[(.*?)\]\]></title>.*?<link>(.*?)</link>'` 返回0条，因为36kr RSS的`<link>`不在`<item>`内。

**正确方式**：先用 `re.findall(r'<item>(.*?)</item>', data, re.DOTALL)` 拆出每个item，再逐个提取`<title>`和`<link>`。

```python
items = re.findall(r'<item>(.*?)</item>', data, re.DOTALL)
kr_items = []
for item in items:
    title_m = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
    link_m = re.search(r'<link>(.*?)</link>', item)
    if title_m and link_m:
        kr_items.append({"title": title_m.group(1), "url": link_m.group(1)})
```
