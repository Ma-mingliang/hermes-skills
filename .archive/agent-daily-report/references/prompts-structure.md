# Prompts Directory Structure

## Overview

Agent prompts extracted from `scripts/agent_prompts.py` into individual files for SkillOpt optimization.

Location: `D:\openclaw-hermes\agent-daily-report-skill\prompts\`

## Files

| File | Size | Description |
|------|------|-------------|
| trust_agent_system.txt | 961 bytes | Trust Agent system prompt |
| trust_agent_user_template.txt | 673 bytes | Trust Agent user input template |
| trust_verify_system.txt | 23 bytes | Trust Agent verifier |
| enrichment_agent_system.txt | 805 bytes | Enrichment Agent system prompt |
| enrichment_agent_user_template.txt | 582 bytes | Enrichment Agent user input template |
| enrichment_verify_system.txt | 543 bytes | Enrichment Agent verifier |
| editor_agent_system.txt | 1321 bytes | Editor Agent system prompt |
| editor_agent_user_template.txt | 134 bytes | Editor Agent user input template |
| editor_verify_system.txt | 753 bytes | Editor Agent verifier |
| README.md | 3594 bytes | Usage instructions |

## Agent Roles

### Trust Agent
- Evaluates GitHub project credibility (0-100 trust_score)
- Decision: keep (>=60) / demote (30-60) / drop (<30)
- Output: JSON with repo, trust_score, decision, reason

### Enrichment Agent
- Generates Chinese summaries and engineering value
- Output fields: title_zh, description_zh, engineering_value, integration_suggestion, key_insight
- Must not fabricate data

### Editor Agent
- Final polish of daily report
- Checks: section order, dedup, style, links, data sources
- Prohibited: add unverified info, modify scores, delete Source Status table

## Modification Workflow

1. Edit `.txt` file in prompts/
2. Test with `python main.py --dry-run`
3. Update `scripts/agent_prompts.py` with changes
4. Commit changes

## SkillOpt Integration

Prompts are combined into `skillopt/envs/agent_daily_report/skills/initial.md` for optimization. See `references/skillopt-integration.md` for details.
