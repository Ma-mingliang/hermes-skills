# External Sources Reference (v2.0)

## 子源一览 (11 sources)

| 子源 | 类型 | 状态 | Items | 说明 |
|------|------|------|-------|------|
| agents-radar | github_issues | ✅ active | 5 | 780⭐, 10源日报, TypeScript |
| ai-news-agent | github_issues | ✅ active | 4 | 25 RSS源日报, candidate→decision |
| ai-news-radar | github_pages_json | ✅ active | 30 | 843⭐, latest-24h.json + raw fallback |
| awesome-mcp-servers | awesome_commits | ✅ active | 8 | 88k⭐, 新MCP server |
| awesome-ai-agents | awesome_commits | ✅ active | 8 | 16k⭐, 新AI agent |
| awesome-llm-apps | awesome_commits | ✅ active | 2 | 43k⭐, 新LLM app |
| official-mcp-registry | mcp_registry | ✅ active | 50 | 官方MCP Registry, cursor分页 |
| glama-mcp | mcp_registry | ✅ active | 10 | Glama MCP目录, 公开API |
| smithery | mcp_registry | ⏭ skipped | 0 | 需要SMITHERY_API_KEY |
| mcp-so | mcp_registry | ⏭ disabled | 0 | 无稳定公开JSON API |
| ai-tool-releases | github_releases | ✅ active | 17 | 13个AI工具/框架版本发布 |

**总计**: 134 items (10/11 sources active)

## v2.0 变更

- ai-news-radar: 修复端点 /data/latest-24h.json + raw.githubusercontent.com fallback
- glama-mcp: 新增，公开API /api/mcp/v1/servers
- smithery: 新增，需SMITHERY_API_KEY
- official-mcp-registry: 新增，cursor分页
- mcp.so: 降级为disabled
- source_status: 新增 skipped_no_stable_api, skipped_requires_api_key
- 日志格式: source | repo= | api= | items= | status=

## API 端点

| 子源 | API | 认证 |
|------|-----|------|
| agents-radar | api.github.com/repos/duanyytop/agents-radar/issues | token_optional |
| ai-news-agent | api.github.com/repos/nickzren/ai-news-agent/issues?labels=ai-digest | token_optional |
| ai-news-radar | learnprompt.github.io/ai-news-radar/data/latest-24h.json | 无 |
| awesome-* | api.github.com/repos/{repo}/commits | token_optional |
| official-mcp-registry | registry.modelcontextprotocol.io/v0.1/servers | 无 |
| glama-mcp | glama.ai/api/mcp/v1/servers | 无 |
| smithery | api.smithery.ai/servers | SMITHERY_API_KEY |
| ai-tool-releases | api.github.com/repos/{repo}/releases | token_optional |

## 字段映射 (ai-news-radar)

- title = title_bilingual → title_zh → title_en → title_original → title
- url = url
- source = source / site / feed_title
- published_at = published_at / first_seen_at / last_seen_at
- summary = summary / description / ai_relevance_reason
- category = ai_label
- score = ai_score (>= 0.5 保留)
- is_ai_related = ai_is_related (true 保留, false 丢弃)
