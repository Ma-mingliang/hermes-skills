# Cache Optimization Components (2026-05-29 Research)

## High-Star Cache/Token Optimization Tools

| Component | Stars | Function | Effect | GitHub |
|-----------|-------|----------|--------|--------|
| context-mode | ⭐15,940 | Context window optimization, sandbox tool output | **98% reduction** | [GitHub](https://github.com/mksglu/context-mode) |
| Context-Engine | ⭐392 | Semantic code search + memory + symbol intelligence | — | [GitHub](https://github.com/Context-Engine-AI/Context-Engine) |
| distill | ⭐169 | Persistent memory + write-time dedup + hierarchical decay | ~12ms overhead | [GitHub](https://github.com/Siddhant-K-code/distill) |
| acon | ⭐80 | Microsoft's context compression for long-horizon agents | Academic | [GitHub](https://github.com/microsoft/acon) |
| token-saver | ⭐5 | Intelligent model routing + context compression | **50-80% reduction** | [GitHub](https://github.com/SiruGao/token-saver) |
| laconic | ⭐15 | Token compression skill (caveman adaptation) | — | [GitHub](https://github.com/GabrielBarberini/laconic) |
| ctxsift | ⭐5 | Local-first token saving skill | — | [GitHub](https://github.com/aakashH242/ctxsift) |

## Recommended for Hermes

### context-mode (⭐15,940) — Strongly Recommended
- **Principle**: MCP tool calls dump raw data into context (Playwright snapshot 56KB, 20 GitHub issues 59KB). context-mode sandboxes tool output, only puts summary into context.
- **Effect**: 98% tool output reduction
- **Adoption**: Used by Microsoft, Google, Meta, Amazon, Stripe, NVIDIA, ByteDance
- **HN**: #1 with 570+ points
- **Compatibility**: 15 platforms including Claude Code, Codex, Cursor, OpenClaw, Hermes

### token-saver (⭐5) — Recommended
- **Principle**:
  - Intelligent model routing: classify question complexity, switch to cost-effective model
  - Context compression: auto-summarize after 8+ turns
  - Reply efficiency: match response length to question complexity
  - Tool call optimization: combine commands, eliminate redundant operations
- **Effect**: 50-80% monthly API cost reduction
- **Detail**: 70% of daily messages are simple/medium → saves 60-80% vs always using strongest model

### distill (⭐169) — Optional
- **Principle**:
  - Write-time dedup: auto-identify and merge semantically similar content
  - Sensitivity tagging: distinguish important/unimportant memory
  - Conflict detection: find contradictory information
  - Hierarchical decay: old info gradually loses weight
  - Cache annotation: mark stable prefixes for prompt caching
- **Effect**: ~12ms overhead, no LLM calls, fully deterministic
- **Note**: Requires independent Go service deployment

## Hermes Built-in Cache Capabilities
- context-compression skill ✅
- context-budget skill ✅
- Compression engine ✅ (threshold: 0.5, target: 0.2)
- Prompt caching ✅ (5min TTL)

## Excluded Components
- Browser-use (⭐96K): Hermes built-in browser sufficient
- Mem0 (⭐57K): Current memory system sufficient, may reconsider later
