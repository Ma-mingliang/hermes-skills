# Cache Optimization Tools Research (2026-05-29)

## Context-Mode (⭐15,940) — MCP Server
- **URL**: https://github.com/mksglu/context-mode
- **Effect**: 98% tool output reduction (315KB → 5.4KB)
- **Mechanism**: Sandboxes tool output, indexes in SQLite/FTS5, retrieves via BM25
- **Install**: `npm install -g context-mode` (installed at `%APPDATA%\npm\context-mode.cmd`)
- **Used by**: Microsoft, Google, Meta, Amazon, Stripe, NVIDIA, ByteDance
- **Platforms**: 15 platforms including Claude Code, Codex, Cursor, OpenClaw

## Cache-Audit (⭐53)
- **URL**: https://github.com/ussumant/cache-audit
- **Function**: Audits setup against Anthropic's 6 prompt caching rules
- **Install**: Skill installed at `~/.hermes/skills\cache-audit\SKILL.md`

## Token-Saver (⭐5)
- **URL**: https://github.com/SiruGao/token-saver
- **Effect**: 50-80% cost reduction through intelligent model routing
- **Features**: Model routing, context compression, reply efficiency, tool optimization
- **Install**: Skill installed at `~/.hermes\skills\token-saver\SKILL.md`

## Prompt-Cache-Skills (⭐69)
- **URL**: https://github.com/OnlyTerp/prompt-cache-skills
- **Function**: 14 platform-specific caching fixes
- **Install**: Skills installed at `~/.hermes\skills\prompt-cache-*\SKILL.md`

## Anthropic's 6 Prompt Caching Rules

1. **Ordering**: Dynamic data in system prompt breaks cache
2. **Message injection**: Editing system prompt mid-session
3. **Tool stability**: Adding/removing tools mid-conversation
4. **Model switching**: Switching models in same thread
5. **Dynamic content size**: Injecting thousands of tokens per session
6. **Fork safety**: Subagent calls must share parent prefix

## Hermes Current Config

```yaml
prompt_caching:
  cache_ttl: 5m  # Should be 1h for better cache hits

compression:
  enabled: true
  threshold: 0.5
  target_ratio: 0.2
  protect_last_n: 20
  protect_first_n: 3
```

## Optimization Recommendations

1. Extend `cache_ttl` from 5m to 1h (most impactful)
2. Batch memory updates (each update breaks prefix)
3. Stable skills list (frequent changes break cache)
4. Remove timestamps from Host info