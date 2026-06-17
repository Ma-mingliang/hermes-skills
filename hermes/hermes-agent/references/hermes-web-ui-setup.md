# Hermes Web UI Setup Guide

## Project Info
- **Repo**: https://github.com/EKKOLearnAI/hermes-web-ui
- **Stars**: 7224
- **Version**: 0.6.10
- **Stack**: Vue 3 + Vite (frontend), Koa + Socket.IO (backend), TypeScript

## Installation

### Download (China — use mirror)
```bash
# Direct git clone is slow/unreliable from China
curl -L -o hermes-web-ui.zip "https://ghfast.top/https://github.com/EKKOLearnAI/hermes-web-ui/archive/refs/heads/main.zip"
unzip hermes-web-ui.zip
mv hermes-web-ui-main hermes-web-ui
```

### Install Dependencies
```bash
cd D:\openclaw-hermes\hermes-web-ui
npm ci --ignore-scripts   # ~35s, 779 packages
```

## Running

### Development Mode (recommended)
```bash
npm run dev
# Server (Koa API): http://127.0.0.1:8647
# Client (Vite):    http://127.0.0.1:8649
```

### Frontend Only (no backend — login will fail)
```bash
npm run start
# Vite on port 8648 — but no backend, login returns "Failed to fetch"
```

### Production Build
```bash
npm run build
npm run preview
```

## Login
- **Username**: `admin`
- **Password**: `123456`
- First login shows security popup asking to change credentials

## Features (Sidebar Navigation)
| Page | Route | Description |
|------|-------|-------------|
| 对话 | `/#/` | AI chat interface |
| 历史 | `/#/history` | Chat history |
| 群聊 (beta) | `/#/group` | Group chat |
| 中转站 | `/#/relay` | Transfer hub |
| 任务 | `/#/hermes/tasks` | Task management |
| **看板** | **`/#/hermes/kanban`** | **Kanban board** |
| 频道 | `/#/channels` | Channels |
| 技能 | `/#/hermes/skills` | Skills management |
| 插件 | `/#/hermes/plugins` | Plugins |
| MCP | `/#/hermes/mcp` | MCP servers |
| 记忆 | `/#/hermes/memory` | Memory management |
| 模型 | `/#/hermes/models` | Model selection |
| 日志 | `/#/hermes/logs` | Logs |
| 用量 | `/#/hermes/usage` | Usage stats |
| 用户 | `/#/system/users` | User management |
| 设置 | `/#/system/settings` | Settings |

## Kanban Integration
- Kanban page at `/#/hermes/kanban`
- Board selector dropdown (default board: "Default")
- Status columns: 待分拣/待办/就绪/进行中/阻塞/已完成/已归档
- Create tasks, assign, block/unblock, complete
- Real-time event stream via WebSocket
- Status summary bar with clickable chips
- Filter by status and assignee

## Architecture
- `packages/client/` — Vue 3 SPA (Vite, Naive UI components)
- `packages/server/` — Koa API server (proxies to Hermes Gateway)
- `packages/desktop/` — Electron wrapper
- `packages/skills/` — Built-in skill templates
- `packages/website/` — Marketing site

## Pitfalls
1. `npm run start` = frontend only, no backend → login "Failed to fetch"
2. Kanban route is `/hermes/kanban` NOT `/kanban` (Vue Router 404)
3. Vite proxies API to `HERMES_WEB_UI_BACKEND_PORT` (default 8647)
4. WSL terminal broken → use Python `subprocess` with `cmd /c` for npm/node commands
5. Large repo (73MB) → use ghfast.top proxy mirror for download in China
