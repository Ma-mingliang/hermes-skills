# 分类修正记录 - 2026-05-31

## 已知误判案例（按P24决策树分类后需人工修正）

| 项目 | 错误分类 | 正确分类 | 根因 |
|------|---------|---------|------|
| n8n-io/n8n | mcp | component | n8n是工作流平台，描述含"mcp server"但本质是工作流自动化 |
| Shubhamsaboo/awesome-llm-apps | agent_specialized | skills | 资源集合，不是Agent |
| VoltAgent/awesome-design-md | agent_specialized | skills | 设计资源集合 |
| dair-ai/Prompt-Engineering-Guide | agent_specialized | skills | 提示词工程指南文档 |
| D4Vinci/Scrapling | mcp | component | 爬虫框架，topics含"mcp"但不是MCP server |
| microsoft/autogen | agent_specialized | component | Agent框架，需要集成到其他系统 |
| crewAIInc/crewAI | agent_specialized | component | Agent框架，不是独立Agent |
| AstrBotDevs/AstrBot | agent_specialized | agent_allround | 全能Agent平台（多渠道+插件） |
| creativetimofficial/ui | agent_specialized | component | UI组件库 |

## 修正规则

1. **awesome-* 系列** → 大概率是skills（资源集合），不是agent
2. ***-guide / *-guide** → 大概率是skills（指南文档）
3. **n8n / langflow / flowise** → component（工作流平台），不是mcp
4. **autogen / crewai / langchain** → component（Agent框架），不是agent
5. **astrbot / openclaw** → agent_allround（全能Agent平台）
6. **scrapling / playwright / selenium** → component（工具框架），即使topics含"mcp"

## 白名单（已验证的正确分类）

```python
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
    "VoltAgent/awesome-design-md": ("skills", "Awesome Design"),
    "dair-ai/Prompt-Engineering-Guide": ("skills", "Prompt Guide"),
    # Component
    "affaan-m/ECC": ("component", "ECC"),
    "langflow-ai/langflow": ("component", "Langflow"),
    "n8n-io/n8n": ("component", "n8n"),
    "microsoft/autogen": ("component", "AutoGen"),
    "crewAIInc/crewAI": ("component", "CrewAI"),
    # MCP
    "punkpeye/awesome-mcp-servers": ("mcp", "Awesome MCP"),
    "microsoft/playwright-mcp": ("mcp", "Playwright MCP"),
    "github/github-mcp-server": ("mcp", "GitHub MCP"),
    "PrefectHQ/fastmcp": ("mcp", "FastMCP"),
}
```
