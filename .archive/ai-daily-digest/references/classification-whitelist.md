# 分类白名单 (2026-05-31更新)

## 概述

已知项目的正确分类，避免P24决策树误判。分类时先查白名单，再走决策树。

## 白名单

### Agent - 全能 (agent_allround)

| 项目 | Stars | 说明 |
|------|-------|------|
| anthropics/claude-code | 128K | Anthropic官方编码Agent |
| google-gemini/gemini-cli | 104K | Google官方CLI Agent |
| openai/codex | 87K | OpenAI编码Agent |
| anomalyco/opencode | 167K | 开源全能编码Agent |
| zhayujie/CowAgent | 44K | Agent Harness系统 |
| AstrBotDevs/AstrBot | 33K | 全能Agent平台 |

### Agent - 专精 (agent_specialized)

| 项目 | Stars | 说明 |
|------|-------|------|
| karpathy/autoresearch | 84K | 科研自动化Agent |
| FoundationAgents/MetaGPT | 68K | 多Agent协作框架 |
| msitarzewski/agency-agents | 106K | AI agency平台 |
| lobehub/lobehub | 77K | Agent operator平台 |

### Skills

| 项目 | Stars | 说明 |
|------|-------|------|
| obra/superpowers | 213K | Skills框架 |
| anthropics/skills | 144K | Anthropic官方Skills |
| addyosmani/agent-skills | 47K | Agent技能开发指南 |
| hesreallyhim/awesome-claude-code | 45K | Claude Code技能大全 |
| sickn33/antigravity-awesome-skills | 39K | Skills集合 |
| Shubhamsaboo/awesome-llm-apps | 112K | LLM应用案例集合 |
| VoltAgent/awesome-design-md | 85K | 设计文档资源 |
| dair-ai/Prompt-Engineering-Guide | 75K | 提示词工程指南 |
| github/awesome-copilot | 34K | Copilot技能集合 |

### Component (Agent组件)

| 项目 | Stars | 说明 |
|------|-------|------|
| affaan-m/ECC | 199K | Agent性能优化系统 |
| langflow-ai/langflow | 148K | LLM工作流编排 |
| x1xhlol/system-prompts-and-models-of-ai-tools | 138K | 系统提示词集合 |
| n8n-io/n8n | 190K | 工作流自动化平台 |
| browser-use/browser-use | 96K | 浏览器自动化组件 |
| microsoft/autogen | 58K | Agent框架 |
| crewAIInc/crewAI | 52K | Agent框架 |
| D4Vinci/Scrapling | - | 爬虫框架 |
| creativetimofficial/ui | 11K | UI组件库 |

### MCP

| 项目 | Stars | 说明 |
|------|-------|------|
| punkpeye/awesome-mcp-servers | 88K | MCP服务器集合 |
| microsoft/playwright-mcp | 33K | Playwright MCP |
| github/github-mcp-server | 30K | GitHub MCP Server |
| PrefectHQ/fastmcp | 25K | FastMCP框架 |
| modelcontextprotocol/servers | 86K | MCP官方服务器 |

## 使用方法

```python
KNOWN_PROJECTS = {
    # Agent - 全能
    "anthropics/claude-code": ("agent_allround", "Claude Code"),
    "google-gemini/gemini-cli": ("agent_allround", "Gemini CLI"),
    "openai/codex": ("agent_allround", "Codex"),
    "anomalyco/opencode": ("agent_allround", "OpenCode"),
    "zhayujie/CowAgent": ("agent_allround", "CowAgent"),
    "AstrBotDevs/AstrBot": ("agent_allround", "AstrBot"),
    
    # Agent - 专精
    "karpathy/autoresearch": ("agent_specialized", "AutoResearch"),
    "FoundationAgents/MetaGPT": ("agent_specialized", "MetaGPT"),
    "msitarzewski/agency-agents": ("agent_specialized", "agency-agents"),
    "lobehub/lobehub": ("agent_specialized", "lobehub"),
    
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
    "microsoft/autogen": ("component", "AutoGen"),
    "crewAIInc/crewAI": ("component", "CrewAI"),
    
    # MCP
    "punkpeye/awesome-mcp-servers": ("mcp", "Awesome MCP"),
    "microsoft/playwright-mcp": ("mcp", "Playwright MCP"),
    "github/github-mcp-server": ("mcp", "GitHub MCP"),
    "PrefectHQ/fastmcp": ("mcp", "FastMCP"),
    "modelcontextprotocol/servers": ("mcp", "MCP Servers"),
}

def classify(repo):
    name = repo.get("full_name", "")
    
    # 白名单优先
    if name in KNOWN_PROJECTS:
        return KNOWN_PROJECTS[name]
    
    # 继续P24决策树...
```

## 更新记录

- 2026-05-31: 添加MetaGPT/agency-agents/lobehub到agent_specialized
- 2026-05-31: 添加9个误判案例到白名单
