# Classification Rules Reference (v2.1 — Content Entity Priority)

## Core Principle

**内容实体优先，不按 source 简单分类。**

- source == producthunt ≠ Product（PH 上的 AI IDE 归 Coding Agent）
- source in [hackernews, linuxdo, v2ex, nodeseek, reddit] ≠ Community（MCP 讨论归 MCP）
- secondary_categories 记录来源属性（Community/Product）

## Priority Order (first match wins)

1. source == arxiv → **Research**
2. title 含 "mcp" / "model context protocol" → **MCP**（任何 source）
3. title 含 "coding agent" / "claude code" / "cursor" / "aider" / "copilot" / "codex" / "ai ide" → **Coding Agent**（任何 source）
4. title 含 "openhands" / "browser agent" / "computer-use agent" / "openclaw" / "hermes" → **General Agent**（任何 source）
5. title 含 "db-gpt" / "sre agent" / "finance agent" / "research agent" → **Specialized Agent**
6. title 含 "langgraph" / "autogen" / "crewai" / "pydantic-ai" / "mastra" / "agents sdk" → **Agent Framework**
7. source_group == model_docs → **Model**
8. source == huggingface AND type == model → **Model**
9. source_group == framework_docs → **Agent Framework**
10. title 含 "firecrawl" / "browser-use" / "tavily" / "exa" / "connector" / "plugin" → **Tool / Plugin / Connector**
11. title 含 "workflow" / "pipeline" / "dag" / "orchestration" → **Workflow**
12. title 含 "skill" / "prompt template" → **Skill**
13. source == producthunt AND 无强内容信号 → **Product**
14. title 含 "funding" / "raises" / "acquisition" → **Business**
15. source in [hackernews, linuxdo, v2ex, nodeseek, reddit] AND 无强内容信号 → **Community**
16. Default → **Community**

## Secondary Categories

- source in [hackernews, linuxdo, v2ex, nodeseek, reddit] 且 primary ≠ Community → secondary 含 Community
- source == producthunt 且 primary ≠ Product → secondary 含 Product

## Examples

| 标题 | source | primary | secondary |
|------|--------|---------|-----------|
| "MCP Server for PostgreSQL" | hackernews | MCP | Community |
| "Claude Code now supports MCP" | reddit | MCP | Community |
| "New AI IDE: CodePilot" | producthunt | Coding Agent | Product |
| "LangGraph 0.3 released" | hackernews | Agent Framework | Community |
| "Best local LLM for coding?" | linuxdo | Community | — |
| "DeepSeek API pricing update" | reddit | Community | — |

## Actionability Assessment

- **high**: title 含 hermes/openclaw/skill/mcp/workflow/claude code
- **medium**: category in [MCP, Tool, Workflow, Skill, Coding Agent]
- **low**: everything else

## Tag Generation

Based on category:
- MCP → [mcp, tool-use]
- Model → [model, llm]
- Coding Agent → [coding-agent, agent]
- General Agent → [agent, autonomous]
- Agent Framework → [framework, sdk]
- Tool / Plugin / Connector → [tool, plugin]
- Workflow → [workflow, automation]
- Skill → [skill, prompt]
- Research → [research, paper]
- Product → [product]
- Business → [business]
- Community → [community]

Content-based:
- "open-source" in title → add "open-source"
- "github" in url → add "github"
- "browser" in title → add "browser-agent"
- "gui" or "computer" in title → add "gui-agent"
