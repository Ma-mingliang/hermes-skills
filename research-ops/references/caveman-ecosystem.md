# Caveman Ecosystem Analysis

**Date**: 2026-05-29
**GitHub**: [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) (66k⭐)
**License**: MIT

## Ecosystem Components

| Repo | Stars | Function | Description |
|------|-------|----------|-------------|
| [caveman](https://github.com/JuliusBrussee/caveman) | 66k | Output compression skill | ~75% fewer output tokens, keeps technical accuracy |
| [cavemem](https://github.com/JuliusBrussee/cavemem) | 465 | Persistent memory | SQLite + MCP, cross-agent memory |
| [cavekit](https://github.com/JuliusBrussee/cavekit) | - | Spec-driven build | Natural language → kits → parallel build |
| [cavegemma](https://github.com/JuliusBrussee/finetune-caveman) | - | Fine-tuned model | Gemma 4 31B with compression baked in |

## Architecture

### caveman (output compression)
- **Type**: .md skill file
- **Mechanism**: Grammar-based compression (drop filler, keep technical terms)
- **Levels**: lite / full / ultra / wenyan (classical Chinese)
- **Supported**: Claude Code, Cursor, Gemini CLI, OpenCode, Codex, 30+ more
- **Key**: Only compresses OUTPUT, not INPUT/CONTEXT

### cavemem (persistent memory)
- **Type**: npm package + hooks + MCP
- **Storage**: Local SQLite + FTS5 + vector index
- **Compression**: Caveman grammar (~75% fewer prose tokens)
- **Retrieval**: MCP tools (search, timeline, get_observations)
- **Supported**: Claude Code, Cursor, Gemini CLI, OpenCode, Codex
- **Privacy**: `<private>...</private>` tags stripped at write boundary

## Known Issues (as of 2026-05-29)

### Windows Problems
- **#43**: Windows path backslashes break under bash -c
- **#44**: Claude Code hook commands path normalization
- **#45**: Not working on Windows with OpenCode Desktop

### General
- Designed for **coding assistants** with hooks, not general-purpose AI
- Requires npm install + MCP configuration
- Hooks fire at session boundaries (not continuous)

## Integration Assessment for Hermes

### ❌ Why NOT suitable for Hermes

1. **Architecture mismatch**
   - cavemem designed for coding assistants (Claude Code, Cursor)
   - Uses hooks mechanism at session boundaries
   - Hermes is general-purpose AI, doesn't use hooks

2. **Windows issues**
   - Known bugs #43, #44, #45 all affect Windows
   - Path handling problems with bash compatibility

3. **Different problem domain**
   - caveman: reduces OUTPUT tokens (not INPUT/CONTEXT)
   - Hermes memory problem: INPUT context limit (2,200 chars)
   - cavemem: session-boundary capture (not continuous memory)

4. **Integration complexity**
   - npm install + MCP config + hooks setup
   - Conflicts with Hermes native memory system
   - High migration cost, uncertain benefit

### ✅ Current Hermes solution (already works)

| Component | Purpose | Status |
|-----------|---------|--------|
| memory tool | Internal indexes (2,200 chars) | ✅ Working |
| memory-archive.md | External detailed rules | ✅ Working |
| session_search | Cross-session recall | ✅ Working |
| skills/*.md | Procedural memory | ✅ Working |
| SKILL compression | Core (1,952) vs Full (40,984) | ✅ Working |

## Key Takeaway

caveman/cavemem is a well-designed ecosystem for **coding assistants** with hooks-based architecture. For **general-purpose AI** like Hermes, the native memory system (memory tool + external files + session_search + skills) is more appropriate and already solves the core problems.
