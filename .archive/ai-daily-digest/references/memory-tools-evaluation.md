# Caveman/Cavemem Evaluation for Hermes Memory

## Question
Can caveman ecosystem (caveman 66k⭐, cavemem 465⭐) solve Hermes's memory limitations?

## Caveman Ecosystem Overview
| Project | Stars | Function |
|---------|-------|----------|
| [caveman](https://github.com/JuliusBrussee/caveman) | 66k | Output compression skill (~75% fewer output tokens) |
| [cavemem](https://github.com/JuliusBrussee/cavemem) | 465 | Persistent memory (SQLite + MCP) |
| [cavekit](https://github.com/JuliusBrussee/cavekit) | - | Spec-driven build loop |
| [cavegemma](https://github.com/JuliusBrussee/finetune-caveman) | - | Fine-tuned model with compression built-in |

## Verdict: NOT suitable for Hermes

### caveman (output compression)
- **Problem**: Only compresses OUTPUT tokens, not INPUT/context
- **Hermes's memory problem**: INPUT context (2,200 char limit for memory injection)
- **Conclusion**: Doesn't solve the core problem

### cavemem (persistent memory)
- **Architecture mismatch**: Designed for coding assistants (Claude Code, Cursor) with hooks
- **Windows issues**: #43 (paths), #44 (hook commands), #45 (not working)
- **Integration complexity**: Requires npm + hooks + MCP setup
- **Hermes already has**: memory tool + memory-archive.md + session_search + skills

## What Actually Works for Hermes
1. **Internal memory** (2,200 chars): Key indexes only
2. **External file** (memory-archive.md): Detailed rules, accessed via read_file
3. **session_search**: Cross-session recall
4. **Skills**: Procedural memory (.md files)
5. **Three-tier SKILL compression**: Core/Balanced/Full for different contexts

## Date
2026-05-30
