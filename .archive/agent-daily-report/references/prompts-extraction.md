# Agent Prompts Extraction

## Overview

The 9 agent prompts in `scripts/agent_prompts.py` can be extracted to individual files for easier editing and SkillOpt optimization.

## Extracted Prompts Location

`D:\openclaw-hermes\agent-daily-report-skill\prompts\`

| File | Agent | Purpose |
|------|-------|---------|
| trust_agent_system.txt | Trust | System prompt for GitHub project trust evaluation |
| trust_agent_user_template.txt | Trust | User prompt template |
| trust_verify_system.txt | Trust | Verification prompt |
| enrichment_agent_system.txt | Enrichment | System prompt for Chinese summary generation |
| enrichment_agent_user_template.txt | Enrichment | User prompt template |
| enrichment_verify_system.txt | Enrichment | Verification prompt |
| editor_agent_system.txt | Editor | System prompt for report polishing |
| editor_agent_user_template.txt | Editor | User prompt template |
| editor_verify_system.txt | Editor | Verification prompt |

## Usage

### Reading Prompts
```python
with open("prompts/trust_agent_system.txt", "r", encoding="utf-8") as f:
    prompt = f.read()
```

### Updating agent_prompts.py
After modifying prompts, update the corresponding constants in `scripts/agent_prompts.py`.

### SkillOpt Optimization
Prompts are bundled into `skillopt/envs/agent_daily_report/skills/initial.md` for SkillOpt training.

## Key Constraints

### Trust Agent
- trust_score >= 60 → keep
- 30 <= trust_score < 60 → demote
- trust_score < 30 → drop

### Enrichment Agent
- title_zh must be Chinese
- description_zh must be Chinese, 2-3 sentences
- Cannot fabricate version numbers, stars, features
- If data insufficient, mark "⚠️ 信息不足"

### Editor Agent
- Cannot add unverified information
- Cannot modify stars/scores
- Cannot delete Source Status table
- Cannot delete "数据来源", "上榜原因", "页面确认", etc.
