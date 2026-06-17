# Search Strategy Reference (v2.1)

## Source Weights (content value, not request count)

| Source | Weight | Role |
|--------|--------|------|
| GitHub | 35% | Discover projects, track growth, find releases/issues/PRs (token_optional) |
| LinuxDo/V2EX/NodeSeek | 20% | Chinese dev real experience, deployment, cost, API routing |
| Hacker News | 15% | Early signal from international dev community (72h Algolia limit) |
| Model Docs | 10% | API changes, pricing, context, tool calling, compatibility (hash_diff + baseline) |
| Reddit | 8% | Real user feedback, comparisons, migration trends (RSS first) |
| Product Hunt | 5% | New Agent/AI IDE/automation product launches (RSS first) |
| Hugging Face | 4% | Open models, demos, tool-use/code models |
| Framework Docs | 3% | MCP/LangGraph/OpenHands/CrewAI/AutoGen infrastructure changes (hash_diff) |
| arXiv | Weekly | Research trends, not daily priority |

## GitHub (35%) — What to Collect

### Token Strategy
- 有 GITHUB_TOKEN 或 GITHUB_PERSONAL_ACCESS_TOKEN → 认证 API，正常 rate limit
- 无 token → 未认证 API 降级采集，减少请求量（max_results_no_token: 20）
- 只有 API 访问失败或限流时才返回 failed_network / failed_rate_limited

### A. New/High-Growth Repos
- Search by keywords: agent, ai-agent, mcp, workflow, coding-agent, tool-use, browser-agent, computer-use
- Track: stars, forks, star_delta_24h, topics, language

### B. Releases
- From watch_repos: OpenHands, LangGraph, AutoGen, CrewAI, PydanticAI, Mastra, MCP servers, browser-use, aider, SWE-agent
- Focus: new Agent capabilities, MCP support, tool calling, runtime/sandbox, breaking changes

### C. Issues
- High-comment issues = user pain points, feature requests, roadmap signals

### D. Pull Requests
- PRs often reflect trends before releases

## Chinese Developer Communities (20%)

### LinuxDo
- Focus: Claude Code, Codex, Cursor, OpenClaw, Hermes, DeepSeek, Kimi, GLM, Mimo, MCP, API routing, LiteLLM, deployment, cost optimization
- Value: real testing, configuration methods, pitfall experiences

### V2EX
- Nodes: program, share, qa, ai, dev
- Focus: Claude Code, Codex, Cursor, AI IDE, MCP, Agent, automation scripts

### NodeSeek
- Focus: Agent deployment, API gateway, LiteLLM, model relay, server config

## Hacker News (15%)

- Sources: top/new/best stories + Algolia keyword search
- **Algolia 限最近 72 小时**
- **默认只抓 story**，comment 在 story 入选后补充
- **合并 Firebase + Algolia 后先去重再过滤**
- Focus: points, comments depth, GitHub project links

## Model Official Docs (10%)

- **hash_diff 变更检测**，不是新闻源
- **首次运行只保存 baseline，不进入日报**
- Providers: Anthropic, OpenAI, DeepSeek, Kimi, GLM, Mimo

## Reddit (8%)

- **RSS first + API optional**
- 缺 token → RSS fallback → success（不返回 skipped_missing_auth）
- Subreddits: r/ClaudeAI, r/OpenAI, r/LocalLLaMA, r/ChatGPTCoding, r/selfhosted

## Product Hunt (5%)

- **RSS first + GraphQL API optional**
- 缺 token → RSS fallback → success（不返回 skipped_missing_auth）
- Focus: AI agent, AI IDE, coding assistant, workflow, automation

## Hugging Face (4%)

- Focus: agent, tool-use, function-calling, code, reasoning, computer-use

## Agent Framework Docs (3%)

- **hash_diff 变更检测**（与 model_docs 同逻辑）
- Providers: MCP, LangGraph, OpenHands, CrewAI, AutoGen

## Data Volume Targets

| Stage | Count |
|-------|-------|
| Raw collected | 300-800 |
| After normalization + negative_keywords | 150-400 |
| After scoring (candidates) | 60-120 |
| Selected for report | 25-45 |

## Deduplication & Merging

Same event from multiple sources should merge:
- GitHub repo + HN discussion + Reddit feedback → merged item with related_items
- Merged items get score boost (+3 per related source)
- Event-level: normalized_entity + event_type + date_bucket

## Negative Keywords

非 AI Agent 内容过滤：
real estate agent, travel agent, insurance agent, sales agent, hiring, job, recruiting, coupon, giveaway, scholarship

## 中文关键词

智能体、代码智能体、编程智能体、工具调用、函数调用、工作流、自动化、上下文、长上下文、提示词、记忆、多智能体、浏览器控制、电脑控制
