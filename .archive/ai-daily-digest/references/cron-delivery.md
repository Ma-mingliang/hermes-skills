# Cron Delivery Pipeline

## Two-Phase Architecture

The AI daily report uses two separate cron jobs:

| Job | Schedule | Deliver | Purpose |
|-----|----------|---------|---------|
| AI日报-搜集生成 | `0 7 * * *` | `local` | Runs `daily_report_v2.py`, writes all files |
| AI日报-微信推送 | `0 10 * * *` (configurable) | `weixin` | Reads `push_payload.json`, outputs messages |

## How `--deliver weixin` Works

When a cron job has `--deliver weixin`:
- The agent's final response text is automatically routed to the WeChat gateway
- The gateway uses the connected `weixin` platform (configured via `WEIXIN_*` env vars)
- **No direct WeChat API calls needed** — the framework handles everything

## Push Job Prompt Template

```
读取 D:/openclaw-hermes/data/daily/昨天日期YYYY-MM-DD/push_payload.json。
将其中的所有消息逐条通过微信推送给用户。
如果文件不存在或内容为空, 推送通知: '日报生成中, 请稍候'。
```

## push_payload.json Format

```json
{
  "date": "YYYY-MM-DD",
  "generated_at": "ISO timestamp",
  "phase": "backfill|normal",
  "messages": [
    {
      "index": 1,
      "title": "🤖 AI日报 YYYY/MM/DD · 主题",
      "content": "格式化消息正文"
    }
  ],
  "full_report_path": "D:/openclaw-hermes/data/daily/YYYY-MM-DD/report.md",
  "stats": {
    "hn_stories": N,
    "hf_papers": N,
    "github_trending": N,
    "critical_events": N,
    "important_events": N,
    "watch_events": N,
    "sources_covered": ["HN", "HuggingFace", ...]
  }
}
```

Each message's `content` field is already formatted for WeChat display. The push job just reads and relays.

## WeChat Gateway Configuration

Active platform in `channel_directory.json`:
```json
{
  "weixin": [
    {
      "id": "o9cq803R0Y4HMdI1VnJApgMyYGbo@im.wechat",
      "type": "dm"
    }
  ]
}
```

Key env vars (in `~/.hermes/.env`):
- `WEIXIN_ACCOUNT_ID` — bot account ID
- `WEIXIN_TOKEN` — iLink bearer token
- `WEIXIN_BASE_URL` — `https://ilinkai.weixin.qq.com`
- `WEIXIN_HOME_CHANNEL` — target user ID for delivery
- `WEIXIN_DM_POLICY=open` — allows push delivery

## Manual Test

```bash
# Test push job manually
hermes cron run 51caabc11179

# Check gateway status
hermes gateway status

# Verify WeChat connection
hermes status
```

## Single-Response Fallback (when send_message unavailable)

**Scenario**: The cron push job runs in a session where the `send_message` tool is NOT loaded (common when the job's `enabled_toolsets` doesn't include the messaging toolset, or the provider session restricts tool access).

**Discovery** (2026-05-30 session): Instead of calling `send_message` 8 times with 15s intervals, the agent can output the **full segmented report as a single final response**, and the framework auto-routes it to the WeChat home channel.

**Implementation pattern**:
1. Read `report-full.md` (or `report.md`) directly via `execute_code` + Python `open()`
2. Format content into 8 segments with `[1/8]` through `[8/8]` headers
3. Include API call statistics as the final segment
4. Output as final response — **DO NOT** call `send_message`

**Format template**:
```
[1/8] 🤖 Agent生态 — 全能Agent
...
[2/8] 🤖 Agent生态续 — 专精Agent
...
[3/8] 🛠️ Skills市场（上）
...
[4/8] 🛠️ Skills市场（下）
...
[5/8] 🧩 Agent组件
...
[6/8] 📊 模型动态
...
[7/8] 🔌 MCP + 📰 行业热点 + 🏭 行业应用
...
[8/8] 📊 数据面板 + 🔮 核心信号
...

📊 API调用统计: 总33次 | ✅成功30次 | ❌失败3次 | 成功率90.9%
```

**Why this works**: Cron jobs configured with `--deliver weixin` auto-route the agent's final response to the WeChat gateway. The gateway uses `channel_directory.json` to find the home channel (`o9cq803R0Y4HMdI1VnJApgMyYGbo@im.wechat` → "AI日报" chat).

**Known limitation**: Single message delivery (no 15s spacing between segments). This is acceptable when the report fits within WeChat's message length limit (~4000 chars per message — system may chunk automatically).
