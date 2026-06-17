# SkillOpt Integration for agent-daily-report

## Overview

SkillOpt (Microsoft, ⭐4619) can optimize the natural-language prompts in `agent_prompts.py`.
It treats `SKILL.md` as the trainable state and iteratively improves it.

## Setup Location

- Environment: `D:\openclaw-hermes\SkillOpt\skillopt\envs\agent_daily_report\`
- Config: `D:\openclaw-hermes\SkillOpt\configs\agent-daily-report\default.yaml`
- Training data: `D:\openclaw-hermes\SkillOpt\data\agent-daily-report\`
- Output: `D:\openclaw-hermes\SkillOpt\outputs\agent-daily-report\`

## Critical: SkillOpt Edit Format

SkillOpt expects edits with **specific field names**. Wrong field names → `skipped_unknown_op`.

```python
# CORRECT format (SkillOpt expects):
{
    "op": "append" | "insert_after" | "replace" | "delete",
    "content": "new content to add/replace with",
    "target": "existing text to find (for replace/delete/insert_after)"
}

# WRONG format (common mistake):
{
    "operation": "add",     # WRONG field name
    "old_text": "",          # WRONG field name
    "new_text": "..."        # WRONG field name
}
```

Field mapping:
- `operation` → `op`
- `new_text` → `content`
- `old_text` → `target`
- `add` → `append`

## Critical: Python Module Naming

Python module names **cannot contain hyphens**. The directory must use underscores:
```
skillopt/envs/agent_daily_report/  ✅ correct
skillopt/envs/agent-daily-report/  ❌ will fail to import
```

The config YAML can still use hyphens: `name: agent-daily-report`

## Critical: MiMo v2.5 Pro Prompt Language

MiMo v2.5 Pro returns **empty content intermittently for complex English prompts**.

Evidence:
- Simple Chinese prompt → ✅ always works
- Simple English prompt → ❌ sometimes empty
- Complex English prompt (reflect system prompt) → ❌ often empty
- Chinese prompt with examples → ✅ always works

**Solution**: Use Chinese prompts for all SkillOpt LLM calls, add retry logic (3 retries, temperature 0.2/0.3/0.4).

## Required File Structure

```
skillopt/envs/agent_daily_report/
├── __init__.py          # Import adapter class
├── adapter.py           # EnvAdapter subclass (rollout, reflect, get_task_types)
├── dataloader.py        # SplitDataLoader subclass (load_split_items)
├── rollout.py           # run_rollout() + run_reflect() functions
├── evaluator.py         # evaluate_skill() function
└── skills/
    └── initial.md       # Seed skill document (all prompts)
```

## Registration

Must register in `scripts/train.py` `_register_builtins()`:
```python
try:
    from skillopt.envs.agent_daily_report.adapter import AgentDailyReportEnv
    _ENV_REGISTRY["agent-daily-report"] = AgentDailyReportEnv
except ImportError:
    pass
```

## Required Directories (Pre-create)

```python
for epoch in range(1, num_epochs+1):
    os.makedirs(f"{out_root}/slow_update/epoch_{epoch:02d}", exist_ok=True)
for step in range(1, total_steps+1):
    os.makedirs(f"{out_root}/steps/step_{step:04d}", exist_ok=True)
os.makedirs(f"{out_root}/skills", exist_ok=True)
os.makedirs(f"{out_root}/test_eval_baseline", exist_ok=True)
os.makedirs(f"{out_root}/meta_skill", exist_ok=True)
```

Without these, `FileNotFoundError` crashes the training mid-run.

## Config Template

```yaml
_base_: ../_base_/default.yaml
model:
  backend: azure_openai
  optimizer: mimo-v2.5-pro
  target: mimo-v2.5-pro
  optimizer_backend: openai_chat
  target_backend: openai_chat
train:
  num_epochs: 3
  train_size: N  # must match actual split size
  batch_size: 1
gradient:
  minibatch_size: 1
  merge_batch_size: 1
optimizer:
  learning_rate: 2
  skill_update_mode: patch
env:
  name: agent-daily-report
  skill_init: skillopt/envs/agent_daily_report/skills/initial.md
  split_mode: split_dir
  split_dir: data/agent-daily-report
  out_root: outputs/agent-daily-report
```

## Training Data Format

```json
[
  {
    "id": "scenario_name",
    "input": {
      "date": "2026-06-04",
      "task": "optimize_agent_prompts",
      "report_content": "...",
      "constraints": ["constraint1", "constraint2"]
    },
    "output": {
      "expected_quality": "high",
      "expected_improvements": ["improvement1"],
      "evaluation_criteria": {"relevance": 80, "completeness": 75, ...}
    }
  }
]
```

Must be split into `train/`, `val/`, `test/` directories with `items.json` in each.
