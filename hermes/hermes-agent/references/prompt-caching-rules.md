# Prompt Caching Reference

## How It Works

LLM prompt caching uses **prefix matching**. The provider stores stable content server-side.
Cache reads cost **0.1×** instead of **1×** (90% reduction for Anthropic).
Default TTL: 5 minutes (configurable to 1 hour).

## Anthropic's 6 Rules (from cache-audit skill)

| # | Rule | What Breaks It | Hermes Status |
|---|------|---------------|---------------|
| 1 | Ordering | Dynamic data (timestamps) in system prompt | ❌ Host has timestamp |
| 2 | Message injection | Editing system prompt mid-session | ⚠️ memory tool modifies MEMORY |
| 3 | Tool stability | Adding/removing tools mid-conversation | ⚠️ Dynamic skill loading |
| 4 | Model switching | Same thread, different model | ✅ Single model (MiMo) |
| 5 | Dynamic content size | Thousands of tokens of dynamic data per session | ❌ MEMORY+USER change |
| 6 | Fork safety | Subagent calls without shared prefix | ⚠️ delegate_task triggers |

## Hermes System Prompt Order

```
[STABLE PREFIX - cacheable]
  1. Basic instructions (fixed)
  2. Tool definitions (fixed)
  3. Skills list (semi-fixed)

[DYNAMIC SUFFIX - breaks cache]
  4. Host info (timestamp per session)
  5. MEMORY (changes with memory tool)
  6. USER profile (changes with memory tool)
  7. User messages
  8. Conversation history
```

## Installed Tools

| Tool | Type | Stars | Effect |
|------|------|-------|--------|
| cache-audit | Skill | ⭐53 | Diagnoses cache issues |
| context-mode | MCP+Skill | ⭐15,940 | 98% tool output reduction |
| token-saver | Skill | ⭐5 | 50-80% cost via model routing |
| prompt-cache-* | Skills | ⭐69 | 14 platform-specific fixes |

## Key Config

```yaml
# Current (hermes config.yaml)
prompt_caching:
  cache_ttl: 5m  # TOO SHORT — change to 1h

compression:
  enabled: true
  threshold: 0.5
  target_ratio: 0.2
  protect_last_n: 20
  protect_first_n: 3
```

## Sources

- Anthropic docs: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- cache-audit: https://github.com/ussumant/cache-audit
- prompt-cache-skills: https://github.com/OnlyTerp/prompt-cache-skills
- context-mode: https://github.com/mksglu/context-mode
