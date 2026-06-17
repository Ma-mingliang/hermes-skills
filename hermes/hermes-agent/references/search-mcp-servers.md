# 搜索相关MCP服务器（2026-05-30）

## 高Star候选

| MCP | Stars | 功能 | 语言 | API Key |
|-----|-------|------|------|---------|
| hangwin/mcp-chrome | ⭐11756 | Chrome浏览器MCP | JS | 无 |
| firecrawl/firecrawl-mcp-server | ⭐6433 | Web抓取+搜索+内容提取 | JS | FIRECRAWL_API_KEY |
| exa-labs/exa-mcp-server | ⭐4496 | 神经搜索+Web爬取 | TS | EXA_API_KEY |
| taylorwilsdon/google_workspace_mcp | ⭐2515 | Gmail/Calendar/Docs/Sheets | TS | Google OAuth |
| tavily-ai/tavily-mcp | ⭐2038 | 实时搜索+提取+爬取 | JS | TAVILY_API_KEY |
| Aas-ee/open-webSearch | ⭐1328 | 多引擎Web搜索 | TS | 无 |
| nickclyde/duckduckgo-mcp-server | ⭐1193 | DuckDuckGo搜索 | Python | 无 |
| jerry-ai-dev/MODULAR-RAG-MCP-SERVER | ⭐937 | RAG系统+MCP | Python | 无 |
| mrkrsl/web-search-mcp | ⭐904 | 本地Web搜索 | TS | 无 |

## 与Hermes已有能力对比

| 功能 | Hermes已有 | MCP替代 | 差距 |
|------|-----------|---------|------|
| DuckDuckGo搜索 | ✅ skill | DuckDuckGo MCP | 无差距 |
| Exa神经搜索 | ✅ skill | Exa MCP | 无差距 |
| 深度研究 | ✅ deep-research | - | 无差距 |
| Web抓取 | ✅ scrapling | Firecrawl MCP | Firecrawl更强（JS渲染） |
| 实时搜索 | ⚠️ 有限 | Tavily MCP | Tavily更强（生产级） |
| RAG检索 | ❌ 无 | MODULAR RAG MCP | 缺失 |

## 安装推荐

### 建议安装
- **Tavily MCP** ⭐2038：生产级实时搜索，比DuckDuckGo更稳定
- **Firecrawl MCP** ⭐6433：JS渲染页面抓取，解决SPA站点数据获取

### 不需要安装
- DuckDuckGo MCP（已有skill）
- Exa MCP（已有skill）
- MCP Chrome（已有browser工具）

## 安装步骤

```bash
# 1. 安装MCP server
npm install -g tavily-mcp
npm install -g firecrawl-mcp

# 2. 添加API Key到.env
# TAVILY_API_KEY=tvly-xxxxx
# FIRECRAWL_API_KEY=fc-xxxxx

# 3. config.yaml添加mcp_servers
# tavily:
#   command: tavily-mcp
#   args: ['-y']
#   env:
#     TAVILY_API_KEY: ${TAVILY_API_KEY}
# firecrawl:
#   command: firecrawl-mcp
#   args: ['-y']
#   env:
#     FIRECRAWL_API_KEY: ${FIRECRAWL_API_KEY}

# 4. 重启Gateway
```

## API Key获取

- Tavily: https://tavily.com （免费1000次/月）
- Firecrawl: https://firecrawl.dev （免费500次/月）
