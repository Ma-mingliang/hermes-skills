# Anthropic Prompt Caching Rules & Hermes Optimization

## Core Principle: Prefix Matching

LLM prompt caching works by **prefix matching**. Any change to the prefix invalidates everything after it.

```
System Prompt → Skills List → Tool Definitions → Memory → User Messages → History
←─────────── Cacheable Prefix ───────────→
```

## Anthropic's 6 Rules (from cache-audit)

| Rule | What Breaks Cache | Hermes Status |
|------|-------------------|---------------|
| 1. Ordering | Dynamic data in system prompt (timestamps, git status) | ❌ Host has timestamps |
| 2. Message injection | Editing system prompt mid-session | ⚠️ memory tool modifies |
| 3. Tool stability | Adding/removing tools mid-conversation | ⚠️ Dynamic skill loading |
| 4. Model switching | Switching models in same thread | ✅ Only MiMo v2.5 Pro |
| 5. Dynamic content size | Injecting thousands of tokens per session | ❌ MEMORY+USER change |
| 6. Fork safety | Compaction/subagent calls not sharing parent prefix | ⚠️ delegate_task triggers |

## Hermes System Prompt Structure

Current order (UNSTABLE):
```
Base Instructions → Host(DYNAMIC) → MEMORY(DYNAMIC) → USER(DYNAMIC) → Skills(SEMI) → Tools(FIXED) → Messages
                    ↑ Changes every session, invalidates all cache ↑
```

Recommended order (STABLE):
```
Base Instructions → Tools(FIXED) → Skills(FIXED) → Host → MEMORY → USER → Messages
←─────── Stable prefix, cacheable ───────→
```

## Available Tools

| Tool | Stars | Function | Recommendation |
|------|-------|----------|----------------|
| cache-audit | ⭐53 | Audit cache config, return score report | ✅ Install |
| prompt-cache-skills | ⭐69 | 13 drop-in cache optimization skills | ✅ Install |
| prompt-caching | ⭐120 | MCP plugin, inject cache_control breakpoints | ⚠️ Needs MCP |
| token-optimizer-mcp | ⭐399 | MCP server, 95%+ token reduction | ⚠️ Needs MCP |

## Optimization Recommendations

### 1. Extend cache_ttl (MOST CRITICAL)
```yaml
# Current
prompt_caching:
  cache_ttl: 5m

# Recommended
prompt_caching:
  cache_ttl: 1h  # or longer
```

### 2. Optimize System Prompt Order
- Put stable content (base instructions, tool definitions, skills list) FIRST
- Put dynamic content (MEMORY, USER, Host) LAST

### 3. Reduce MEMORY Change Frequency
- Batch memory updates, don't modify every conversation
- Or put memory at the END of system prompt

### 4. Stabilize Skills List
- Batch install skills, avoid frequent add/remove
- Skills list changes invalidate entire prefix cache

## Expected Impact

| Metric | Before | After |
|--------|--------|-------|
| Cache hit rate | ~20% | ~60-80% |
| Long session hit rate | ~30% | ~80%+ |
| Cache token price | 0.1× | 0.1× |
| Monthly savings | — | 60-80% |

## References
- [Anthropic Prompt Caching Docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [cache-audit GitHub](https://github.com/ussumant/cache-audit)
- [prompt-cache-skills GitHub](https://github.com/OnlyTerp/prompt-cache-skills)
- Thariq Shihipar's thread: "Lessons from Building Claude Code: Prompt Caching Is Everything"
