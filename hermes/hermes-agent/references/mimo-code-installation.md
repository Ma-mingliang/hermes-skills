# MiMoCode Installation & Configuration

## Installation

```bash
npm install -g @mimo-ai/cli
```

Verify: `mimo --version` → 0.1.0

Location: `C:\Users\<user>\AppData\Roaming\npm\mimo.cmd`

## Available Models

```
mimo/mimo-auto
xiaomi/mimo-v2-flash
xiaomi/mimo-v2-omni
xiaomi/mimo-v2-pro
xiaomi/mimo-v2.5
xiaomi/mimo-v2.5-pro
xiaomi/mimo-v2.5-pro-ultraspeed
```

## Token Plan Configuration

Platform: https://platform.xiaomimimo.com

Token Plan API endpoint: `https://token-plan-cn.xiaomimimo.com/v1`

Config file: `.mimocode/mimocode.json` (project) or `~/.config/mimocode/mimocode.json` (global)

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

## First Run

First launch of `mimo` guides through configuration:
- MiMo Auto (free, zero config)
- Xiaomi MiMo Platform (OAuth)
- Import from Claude Code
- Custom Provider (OpenAI-compatible)

## Key Commands

| Command | Purpose |
|---------|---------|
| `mimo` | Start TUI |
| `mimo models` | List available models |
| `mimo stats` | Token usage statistics |
| `mimo providers` | Manage providers |
| `mimo upgrade` | Update to latest version |
| `mimo run "message"` | One-shot mode |
