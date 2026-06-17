# MCP Registry API 详情

## Official MCP Registry

- 端点: `https://registry.modelcontextprotocol.io/v0.1/servers`
- 认证: 无（公开API）
- 分页: cursor-based
- 响应结构:
```json
{
  "servers": [
    {
      "server": {
        "name": "ai.xxx/mcp",
        "description": "...",
        "repository": {"url": "https://github.com/...", "source": "github"}
      },
      "_meta": {
        "io.modelcontextprotocol.registry/official": {
          "status": "active",
          "statusChangedAt": "2026-04-13T17:32:20Z",
          "publishedAt": "2026-04-13T17:32:20Z"
        }
      }
    }
  ],
  "metadata": {...}
}
```

- 可用字段: name, description, repository.url, status, publishedAt
- 缺失字段: stars, downloads, forks, last_commit
- `status` 可用于判断维护状态（active/inactive）

## Glama MCP Registry

- 端点: `https://glama.ai/api/mcp/v1/servers`
- 认证: 无（公开API）
- 分页: pageInfo-based
- 响应结构:
```json
{
  "pageInfo": {...},
  "servers": [
    {
      "id": "xxx",
      "name": "server-name",
      "slug": "server-name",
      "namespace": "username",
      "description": "...",
      "repository": {"url": "https://github.com/..."},
      "tools": [...],
      "spdxLicense": {"name": "MIT License"},
      "attributes": ["hosting:local-only"],
      "url": "https://glama.ai/mcp/servers/xxx"
    }
  ]
}
```

- 可用字段: name, description, repository.url, tools（工具列表）, license, attributes
- 缺失字段: stars, downloads, forks, last_commit
- `tools` 数量可用于评估成熟度

## 获取热度数据的方法

两个 Registry 都不提供 star 数据。如需热度信息：

1. 从 `repository.url` 提取 GitHub owner/repo
2. 调用 GitHub API `GET /repos/{owner}/{repo}` 获取 stars, forks, pushed_at
3. 将 stars 写入 item 的 `metrics.stars` 字段
4. 基于 stars 重新计算 Popularity 评分

## Smithery MCP Registry

- 需要 `SMITHERY_API_KEY`
- 缺 key 时返回 `skipped_requires_api_key`
- 2026-06-02 状态: 未启用

## mcp.so

- 无稳定公开 JSON API
- 已禁用（enabled=false）
- 返回 `skipped_disabled`
