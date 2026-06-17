# SkillOpt Prompt Optimization Workflow

## Overview

SkillOpt optimizes natural-language skill documents (SKILL.md) through iterative training. It does NOT optimize code.

## Quick Start

```bash
cd D:\openclaw-hermes\SkillOpt

# 1. Load environment
set -a; source .env; set +a

# 2. Run training
python scripts/train.py --config configs/agent-daily-report/default.yaml

# 3. Check results
type outputs\agent-daily-report\best_skill.md
type outputs\agent-daily-report\history.json
```

## Environment Setup

### Required Files
- `configs/agent-daily-report/default.yaml` - Training config
- `skillopt/envs/agent_daily_report/adapter.py` - Environment adapter
- `skillopt/envs/agent_daily_report/dataloader.py` - Data loader
- `skillopt/envs/agent_daily_report/rollout.py` - Rollout & reflection logic
- `skillopt/envs/agent_daily_report/evaluator.py` - Evaluation logic
- `data/agent-daily-report/training_data.json` - Training data

### Environment Registration
Add to `scripts/train.py` `_register_builtins()`:
```python
try:
    from skillopt.envs.agent_daily_report.adapter import AgentDailyReportEnv
    _ENV_REGISTRY["agent-daily-report"] = AgentDailyReportEnv
except ImportError:
    pass
```

## Training Data Format

```json
[
  {
    "id": "scenario_name",
    "input": {
      "date": "2026-06-04",
      "task": "optimize_agent_prompts",
      "report_content": "Report content...",
      "constraints": ["constraint1", "constraint2"]
    },
    "output": {
      "expected_quality": "high",
      "expected_improvements": ["improvement1", "improvement2"],
      "evaluation_criteria": {
        "relevance": 90,
        "completeness": 85,
        "accuracy": 90,
        "actionability": 85,
        "specificity": 95,
        "consistency": 80,
        "coverage": 90,
        "clarity": 85,
        "dedup_effectiveness": 80,
        "scoring_accuracy": 85,
        "mcp_validation": 95,
        "source_filtering": 80
      }
    }
  }
]
```

## Evaluation Dimensions (12)

| Dimension | Weight | Description |
|-----------|--------|-------------|
| relevance | 10% | Agent ecosystem relevance |
| completeness | 10% | Output completeness |
| accuracy | 10% | Information accuracy |
| actionability | 10% | Actionability |
| specificity | 15% | Specific values vs vague descriptions |
| consistency | 10% | No contradictions between rules |
| coverage | 15% | All necessary rules covered |
| clarity | 10% | Clear instructions |
| dedup_effectiveness | 10% | Dedup rules effective |
| scoring_accuracy | 10% | Scoring criteria reasonable |
| mcp_validation | 10% | MCP validation rules完善 |
| source_filtering | 10% | Source filtering effective |

## Common Issues

### 1. API 401 Unauthorized
- Check `.env` file: remove `export` prefix from env vars
- Verify API key is correct
- Test with: `python -c "import urllib.request; ..."`

### 2. No Patches Generated
- Check reflect function returns valid JSON
- Add fallback mechanism for JSON parse failures
- Lower soft threshold (currently 0.3)

### 3. Training Timeout
- Use `subprocess.Popen` with background mode
- Set `timeout_seconds: 0` in config for no limit
- Use `execute_code` with longer timeout

### 4. Directory Not Found
- Create `slow_update/epoch_XX/` directories before training
- Create `outputs/agent-daily-report/` directory

### 5. Environment Name Mismatch
- Python modules can't have hyphens: use `agent_daily_report` not `agent-daily-report`
- Registry key can have hyphens: `agent-daily-report`

## Output Files

- `best_skill.md` - Optimized skill document
- `history.json` - Training history (per-step scores)
- `config.json` - Training configuration
- `runtime_state.json` - Current state
- `skills/` - Per-step skill snapshots
- `slow_update/` - Epoch comparison data

## Integration with agent-daily-report

After training, apply optimized skill:
```bash
python configs/agent-daily-report/update_prompts.py \
  --skill outputs/agent-daily-report/best_skill.md \
  --output D:/openclaw-hermes/agent-daily-report-skill/scripts/agent_prompts.py
```

Then restart Hermes Gateway for changes to take effect.
