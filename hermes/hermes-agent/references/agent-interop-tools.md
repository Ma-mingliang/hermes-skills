# Agent Interop & Monitoring Tools (2026-06-06)

## Installed Tools

### Claude Code Agent Monitor
- **Location**: `D:\openclaw-hermes\claude-code-monitor`
- **Source**: https://github.com/hoangsonww/Claude-Code-Agent-Monitor
- **Port**: http://localhost:4820
- **Start**: `npm start` (after `npm run setup` + `npm run build`)
- **Features**: Real-time session monitoring, tool usage tracking, subagent orchestration, Kanban, WebSocket updates, SQLite persistence, REST API
- **Integration**: Uses Claude Code's native hook system (PreToolUse, PostToolUse, Stop, SubagentStop, Notification, SessionStart, SessionEnd, UserPromptSubmit)
- **Hooks install**: `npm run install-hooks` (auto-installed on startup)

### agents-chat (ACP Multi-Agent Chat UI)
- **Location**: `D:\openclaw-hermes\agents-chat`
- **Source**: https://github.com/huanyingtianhe/agents-chat
- **Port**: https://localhost:3010
- **Start**: `npm run dev`
- **Features**: Multi-agent chat with @mention routing, ACP protocol support, auto/pipeline/discussion orchestration, file attachments, per-agent model selection
- **Supported agents**: Claude Code, Copilot CLI, Gemini CLI, Codex CLI, OpenClaw, Hermes Agent, any ACP-compliant agent
- **Prereqs**: Node.js >= 20, `.env.local` from `.env.example`

### hermes-CCC — NOT RECOMMENDED
- **Location**: `D:\openclaw-hermes\hermes-CCC`
- **Source**: https://github.com/Arseni6361/hermes-CCC
- **Status**: DO NOT USE — contains `compiler.exe` (unsigned Windows binary) + highly obfuscated Lua script (309KB cp.txt). README is empty (just title). Cannot audit code safety.
- **Action**: Delete if present

## Claude Code Session File Locations

| File | Content |
|------|---------|
| `~/.claude/history.jsonl` | All user input history (display text, timestamp, project, sessionId) |
| `~/.claude/projects/<project>/<session-id>.jsonl` | Full conversation log (human/assistant/tool messages) |
| `~/.claude/sessions/` | Active session metadata (pid, sessionId, cwd, startedAt) |
| `~/.claude/.credentials.json` | OAuth credentials (shared with Hermes) |

**Project directory naming**: Path separators replaced with hyphens (e.g., `D--openclaw-hermes` for `D:\openclaw-hermes`).

## Key GitHub Projects for Agent Interop

| Category | Project | Stars | URL |
|----------|---------|-------|-----|
| Hermes↔CC integration | hermes-CCC | — | ⚠️ Unsafe (see above) |
| ACP multi-agent chat | agents-chat | — | github.com/huanyingtianhe/agents-chat |
| CC monitoring dashboard | Claude-Code-Agent-Monitor | — | github.com/hoangsonww/Claude-Code-Agent-Monitor |
| Multi-agent orchestration | golutra | — | github.com/golutra/golutra |
| CC session monitor (macOS) | c9watch | — | github.com/minchenlee/c9watch |
| Token tracking | token-tracker | — | github.com/stormzhang/token-tracker |
| ACP protocol impl | go-acp-server | — | github.com/xinjiyuan97/go-acp-server |

## Pitfalls

- `better-sqlite3` npm package requires native compilation. On Windows without Visual Studio Build Tools, use `npm install --build-from-source=false` to skip native build and use prebuilt binaries.
- Claude Code project dirs use `--` not `\` or `/` in directory names under `~/.claude/projects/`.
