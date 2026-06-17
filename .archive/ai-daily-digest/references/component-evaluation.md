# Component Evaluation Framework for Hermes

## When User Asks "Should I Add X to Hermes?"

Use this framework to evaluate external components.

### Step 1: Understand What It Does

| Question | Why It Matters |
|----------|---------------|
| What problem does it solve? | Must address a real gap in Hermes |
| How does it work technically? | Architecture determines integration cost |
| Is it standalone or library? | Standalone = separate process; library = code integration |

### Step 2: Compare with Hermes Built-in

Check these Hermes capabilities first:

| Capability | Hermes Built-in | Notes |
|------------|----------------|-------|
| Memory | memory tool + MEMORY.md | Persistent across sessions |
| Skills | skill_manage + skill_view | 47 installed |
| Delegation | delegate_task | Parallel subagents |
| Cron | cronjob | Scheduled tasks |
| Web | web search + firecrawl | Information gathering |
| Browser | browser tool | Playwright/CDP |
| Terminal | terminal | Shell commands |
| File ops | read/write/patch/search | File management |
| TTS | text_to_speech | Voice output |
| Vision | vision_analyze | Image understanding |
| Platforms | WeChat/Telegram/Discord/etc | Multi-platform |
| Model routing | Multi-provider + fallback | Flexible |
| Compression | Context compression | Token savings |

### Step 3: Evaluate Integration Cost

| Factor | Low Cost | High Cost |
|--------|----------|-----------|
| Installation | npm/pip install | Complex setup |
| Token impact | <1K tokens/call | >5K tokens/call |
| Dependencies | None | Vector DB, external services |
| Maintenance | Self-contained | Needs updates |

### Step 4: Decision Matrix

| Scenario | Recommendation |
|----------|---------------|
| Hermes already does it well | ❌ Don't add |
| Similar but slightly better | ⚠️ Probably not worth it |
| Fills a real gap | ✅ Add selectively |
| Requires major changes | ❌ Wait until needed |

### Step 5: Installation Strategy

If adding:
1. **Selective install** - only relevant parts, not everything
2. **Measure impact** - check token consumption before/after
3. **Test thoroughly** - verify it works with existing setup
4. **Document** - add reference file explaining what was added and why

## Case Studies

### Browser-use (⭐96K) - REJECTED
- **What**: LLM-driven browser automation
- **Why not**: Hermes already has browser tool; Browser-use's advantage (auto-planning) is redundant when Hermes Agent can plan itself
- **When to reconsider**: If need complex multi-step web automation

### Mem0 (⭐57K) - DEFERRED
- **What**: Universal memory layer with semantic search
- **Why not now**: Hermes memory is sufficient; Mem0 needs vector DB (extra complexity)
- **When to add**: When memory grows large enough that semantic search > full-text search

### ECC (⭐197K) - SELECTIVE INSTALL
- **What**: Agent optimization system (348 skills)
- **Why selective**: Full install adds 4,890 tokens/call; many skills irrelevant
- **What was added**: 25 most relevant skills (security, content, research, audit)
- **Result**: +1,500 tokens/call, +¥4.5/month cost
