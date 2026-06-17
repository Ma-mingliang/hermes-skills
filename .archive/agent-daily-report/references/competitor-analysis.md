# Competitor Analysis — Agent Ecosystem Tracking Projects

## 对比项目

| 项目 | Stars | 语言 | 信源数 | LLM介入 | 输出 |
|------|-------|------|--------|---------|------|
| duanyytop/agents-radar | 780 | TypeScript | 10 | 过滤+分类+趋势 | Issues+Web+RSS+MCP+Telegram |
| nickzren/ai-news-agent | 2 | Python | ~25 RSS | 去重+分组+分类 | Issues |
| LearnPrompt/ai-news-radar | 843 | Python | 20+ | 无(纯规则) | GitHub Pages |

## agents-radar (780⭐)

**核心**: GitHub Actions 每天 08:00 CST，聚合 10 源，发布中英双语日报。

**信源**: GitHub API (17+ tracked repos), GitHub Trending, HN Algolia, PH GraphQL, ArXiv, HuggingFace, Dev.to, Lobste.rs, Anthropic/OpenAI sitemap, Claude Code Skills。

**LLM**: DeepSeek (fallback on 403) 过滤非 AI 项目、分类、提取趋势信号。

**亮点**: MCP Server (Cloudflare Worker), Telegram/飞书推送, RSS feed, 月度合订本。

**可参考**: MCP Server 设计, 10源架构, GitHub Trending HTML 解析。

## ai-news-agent (2⭐)

**核心**: RSS 收集 → 去重 → LLM 分组分类 → GitHub Issues。

**信源**: ~25 RSS (TechCrunch, Wired, Ars Technica, The Verge, OpenAI, Anthropic 等)。

**LLM**: OpenAI API / Codex / Claude Code 两种模式:
- GitHub Actions 模式: OpenAI API 做去重+分类
- Agent 模式: 输出 candidates.json → Agent 写 decisions.json → 应用决策

**亮点**: candidate→decision JSON 模式, AGENTS.md (Codex runbook), 源级过滤规则。

**可参考**: candidate→decision JSON 架构, Agent 介入点设计, feed health 检查。

## ai-news-radar (843⭐)

**核心**: 伯乐Skill 判断信源质量，纯规则 pipeline，GitHub Pages 静态站。

**信源**: 官方 RSS, OPML 导入, 公开 feed, 静态页面, AgentMail 邮箱。

**LLM**: 无。核心是"不需要 LLM API Key 就能跑"。

**亮点**: 伯乐Skill (信源评估), 源健康统计, AI强相关过滤, OPML 批量导入, 两层模型 (Signal层+Advanced层)。

**可参考**: 信源评估方法论, 源健康追踪, OPML 导入, 静态站发布。

## 我们的优势

1. **GitHub 追踪最深** — 4池架构 + 7状态 lifecycle + 实时 stargazers
2. **评分系统最完整** — 5维度100分 + 13类 + actionability + cost_signal
3. **中文社区覆盖** — LinuxDo/V2EX/NodeSeek
4. **Lifecycle 管理** — discovered→spike_hold→probation_7d→candidate_30d→watchlist
5. **External Digests** — 10 个外部子源

## 我们的劣势

1. **没有 Agent 介入** — 全脚本，无 LLM 判断力
2. **没有外部输出** — 只输出本地 Markdown，无 Issues/Web/RSS/MCP
3. **RSS 覆盖面窄** — 无 TechCrunch/Wired 等主流媒体
4. **没有源健康长期追踪** — source_status 只记录当天 (已部分修复)
5. **没有 OPML 导入** — (已添加 opml_import.py)

## Agent 架构规划 (待实现)

参考 ai-news-agent 的 candidate→decision 模式:

1. **GitHub Trust Agent**: score 后、select 前。判断 GitHub 项目真实价值。输出 keep/demote/drop。
2. **Item Enrichment Agent**: select 后。中文描述、工程价值总结。
3. **Editor Agent**: Markdown 初稿后。风格统一、低信号日措辞。
