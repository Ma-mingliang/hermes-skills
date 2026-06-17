--- 
name: ai-daily-digest-full
description: "AI日报完整版备份 - 2026-05-31重构前的原始版本，包含101K字符的完整规则、60+条Pitfalls、详细分类标准等。仅供查阅，不再作为执行依据。"
version: "6.5.0-backup"
tags: ["archive", "backup"]
---

# ⚠️ 这是 ai-daily-digest v6.5.0 的完整备份

> 本文件是2026-05-31重构前的原始版本，仅供查阅历史规则和Pitfalls。
> 实际执行请使用 `ai-daily-digest`（重构版）。

**备份原因**：原始skill有101K字符，规则散落在各处，执行时容易跳步。
重构后采用方案D（脚本+agent协作），SKILL.md精简到10K以内。

**完整内容位置**：
- 原始SKILL.md：`C:\Users\lenovo_mml\.hermes\skills\news\ai-daily-digest\SKILL.md`
- Pitfalls集合：`references/pitfalls-complete.md`（待创建）
- 执行清单：`checklists/` 目录
- 自动化脚本：`scripts/ai_daily_digest_v3.py` / `v4.py`

**重构变更记录**：
- 2026-05-31：从101K精简到~8K，铁律前置，脚本化确定性工作
- 分离：规则(Skill) + 清单(checklists/) + 参考(references/) + 脚本(scripts/)
