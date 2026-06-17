# SKILL.md Compression Pattern for ai-daily-digest

## Problem
SKILL.md grew to 71,189 characters, consuming excessive tokens on every cron job load. But the compressed 4K version lacked critical examples and format specifications, causing agent to produce low-quality reports.

## Solution: Three-Tier Compression
| Version | Size | Contents | Use Case |
|---------|------|----------|----------|
| **SKILL.md** (core) | ~4K | Core rules only | Token-sensitive cron |
| **SKILL-balanced.md** | ~5-10K | Core + key examples + key pitfalls | Quality-first cron |
| **SKILL-full.md** | ~71K | Everything | First run / training / debug |

## Compression Ratios
- Core: 5.7% (4K / 71K)
- Balanced: 13.3% (9.4K / 71K)

## What Goes in Core (~4K)
1. Classification judgment flow (6 steps)
2. Description principles (9 problem types)
3. Report structure outline
4. Predecessor comparison requirement
5. Workflow summary
6. Key pitfalls (abbreviated)
7. Reference pointers

## What Gets Added in Balanced (~9.4K)
1. **Key examples** (Nanobot description) — without examples, agent writes one-line descriptions
2. **Critical format specs** (WeChat push segmentation [1/8]...[8/8]) — without specs, agent scrambles section order
3. **Detailed Pitfalls with explanations** (12 items) — without details, agent repeats mistakes
4. **Phased data collection strategy** — avoids 5-minute execute_code timeout
5. **Expanded reference file list** — agent knows where to find detailed rules

## What Gets Cut from Full
- Full 102 source list (→ source_registry.yaml)
- Duplicate sections (MCP/数据面板/核心信号 appeared twice in full)
- Verbose workflow details
- Website weight system table
- Installed skills inventory
- Execution logs

## Why Balanced Was Needed (2026-05-30 Lesson)
Comparing core vs full output revealed core version caused:
- **Agent descriptions**: One-line敷衍 (e.g., "超轻量级AI Agent") instead of detailed multi-section descriptions
- **Report structure**: Scrambled section order, missing subsections
- **Classification errors**: Misclassified projects without following decision tree
- **Missing pitfalls**: Repeated known mistakes (bytes in access_log, hardcoded model versions)

## Cron Job Configuration
| Task | Time | SKILL Version | Output |
|------|------|---------------|--------|
| 压缩版测试 | 00:00 | SKILL.md | report-core.md |
| 折中版测试 | 00:30 | SKILL-balanced.md | report-balanced.md |
| 完整版对比 | 01:00 | SKILL-full.md | report-full.md |

## Verification Method
Run all three tasks same day, compare:
1. Agent描述质量 — does it include application domains, core features, technical principles, predecessor comparison?
2. 报告结构一致性 — does it follow the [1/8]...[8/8] segmentation?
3. 分类准确率 — does it verify each project through the decision tree?
4. 微信推送格式 — correct section order?
5. Token消耗 — input tokens
6. 执行时间 — wall clock time

## Generalization
This three-tier pattern applies to any skill that's too large for efficient cron execution:
- **Tier 1 (Core)**: Rules only, no examples → for experienced agents or token-sensitive runs
- **Tier 2 (Balanced)**: Rules + critical examples + critical pitfalls → recommended default
- **Tier 3 (Full)**: Everything → for first run, training, or debugging

## Date
Created: 2026-05-29 (two-tier)
Updated: 2026-05-30 (three-tier with balanced version)
