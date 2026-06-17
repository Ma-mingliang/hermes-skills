---
name: mimocode-setup
description: Install, configure, and troubleshoot MiMoCode (Xiaomi's AI coding agent). Covers npm install, token plan config, provider setup, model selection.
version: 1.0.0
triggers:
  - User asks about MiMoCode installation, configuration, or usage
  - User mentions "mimo code", "mimocode", "@mimo-ai/cli"
  - User needs to configure MiMo token plan or API key
---

# MiMoCode Setup & Configuration

## What is MiMoCode

Xiaomi's open-source terminal-native AI coding agent (fork of OpenCode). Features: persistent cross-session memory (SQLite FTS5), multiple agents (build/plan/compose), subagent orchestration, voice input, dream/distill self-improvement.

GitHub: https://github.com/XiaomiMiMo/MiMo-Code
Website: https://mimo.xiaomi.com/en/mimocode

## Installation

```bash
npm install -g @mimo-ai/cli
```

Verify: `mimo --version` (current: 0.1.0)
Binary location (Windows): `C:\Users\<user>\AppData\Roaming\npm\mimo.cmd`

## Configuration

### Config file locations
- **Global**: `~/.config/mimocode/mimocode.json`
- **Project**: `.mimocode/mimocode.json` (in project root)

### View current config
```bash
mimo debug config
```

### Provider setup

MiMoCode supports multiple providers. On Windows, config is typically at:
`C:\Users\<user>\.config\mimocode\mimocode.json`

#### Free channel (MiMo Auto) — zero config
Built-in, no API key needed (limited time free):
```json
{
  "provider": {
    "mimo": {
      "name": "MiMo Auto (free)",
      "api": "https://api.xiaomimimo.com/api/free-ai/openai"
    }
  }
}
```

#### Token Plan provider
```json
{
  "provider": {
    "xiaomi": {
      "name": "MiMo Token Plan",
      "api": "https://token-plan-cn.xiaomimimo.com/v1",
      "apiKey": "YOUR_API_KEY"
    }
  }
}
```

Get API key: https://platform.xiaomimimo.com (login → API Keys page)

#### Custom provider (OpenAI-compatible)
```json
{
  "provider": {
    "custom": {
      "name": "Custom",
      "api": "https://your-endpoint.com/v1",
      "apiKey": "YOUR_KEY"
    }
  }
}
```

### First-run setup
Run `mimo` — TUI guides through:
1. MiMo Auto (free, zero config)
2. Xiaomi MiMo Platform (OAuth login)
3. Import from Claude Code
4. Custom Provider

## Available Models

List all: `mimo models`

| Model | Notes |
|-------|-------|
| `mimo/mimo-auto` | Free channel, auto-routes |
| `xiaomi/mimo-v2-flash` | |
| `xiaomi/mimo-v2-omni` | Multimodal |
| `xiaomi/mimo-v2-pro` | |
| `xiaomi/mimo-v2.5` | |
| `xiaomi/mimo-v2.5-pro` | |
| `xiaomi/mimo-v2.5-pro-ultraspeed` | Fastest |

Use specific model: `mimo -m xiaomi/mimo-v2.5-pro`

## Key Commands

| Command | Purpose |
|---------|---------|
| `mimo` | Start TUI (default) |
| `mimo models` | List available models |
| `mimo stats` | Token usage statistics |
| `mimo providers` | Manage providers/auth |
| `mimo debug config` | Show full config JSON |
| `mimo upgrade` | Update to latest |
| `mimo web` | Start web interface |
| `mimo serve` | Headless server mode |

## Pitfalls

- **Config file may not exist yet**: If `~/.config/mimocode/mimocode.json` doesn't exist, run `mimo` once to trigger first-run setup, or create it manually.
- **Token Plan URL differs**: The token plan endpoint is `token-plan-cn.xiaomimimo.com`, NOT `api.xiaomimimo.com`. Using the wrong URL will give auth errors.
- **Windows path**: Config goes under `C:\Users\<user>\.config\mimocode\`, not AppData.
- **npm global install on Windows**: Binary lands in `AppData\Roaming\npm\`, ensure this is on PATH.
