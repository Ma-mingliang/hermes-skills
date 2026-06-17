# SkillOpt Custom Benchmark Setup

## When to Use
When user wants to optimize prompts/skills using SkillOpt for a custom task.

## Required Files
Create directory: `skillopt/envs/<name>/` (use underscores, NOT hyphens)

| File | Purpose | Key Method Signatures |
|------|---------|----------------------|
| `__init__.py` | Export adapter class | `from skillopt.envs.<name>.adapter import <Name>Env` |
| `adapter.py` | Environment adapter (subclass `EnvAdapter`) | `rollout(self, env_manager, skill_content: str, out_dir: str, **kwargs)` / `reflect(self, results: list[dict], skill_content: str, out_dir: str, **kwargs)` / `get_task_types(self) -> list[str]` |
| `dataloader.py` | Data loader (subclass `SplitDataLoader`) | `load_split_items(self, split_path: str) -> list[dict]` / `load_raw_items(self, data_path: str) -> list[dict]` |
| `rollout.py` | LLM calls for rollout + reflection | `run_rollout(skill_md, env_items, **kwargs) -> list[dict]` / `run_reflect(rollout_results, skill_md, **kwargs) -> list[dict]` |
| `evaluator.py` | Evaluation logic | `evaluate_skill(skill_md, eval_items) -> dict` |
| `skills/initial.md` | Initial skill document | Plain markdown with prompts |

## Registration
In `scripts/train.py` `_register_builtins()`:
```python
try:
    from skillopt.envs.<name>.adapter import <Name>Env
    _ENV_REGISTRY["<name-with-hyphens>"] = <Name>Env
except ImportError:
    pass
```

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
  num_epochs: 2
  train_size: <N>  # Must match actual split size
  batch_size: 1
env:
  name: <name-with-hyphens>
  skill_init: skillopt/envs/<name>/skills/initial.md
  split_mode: split_dir
  split_dir: data/<name>
  out_root: outputs/<name>
```

## Data Directory Structure
```
data/<name>/
├── train/items.json
├── val/items.json
└── test/items.json
```

## Critical Pitfalls

| Pitfall | Fix |
|---------|-----|
| Directory name with hyphens → `ModuleNotFoundError` | Use underscores: `agent_daily_report` not `agent-daily-report` |
| `train_size` mismatch → `ValueError` | Must match actual train split count |
| Missing `get_task_types` → `TypeError: Can't instantiate abstract class` | Must implement all 5 abstract methods |
| `rollout()` wrong signature → `TypeError: takes 3 positional but 4 given` | Signature: `rollout(self, env_manager, skill_content: str, out_dir: str, **kwargs)` |
| `reflect()` wrong signature → `TypeError: takes 3 positional but 4 given` | Signature: `reflect(self, results: list[dict], skill_content: str, out_dir: str, **kwargs)` |
| `skill_init` path uses hyphens | Use underscores in path |
| Training timeout | Use `subprocess.Popen` background with log file, not `subprocess.run` |

## Execution
```python
# Background training (avoid 300s timeout)
with open(log_path, 'w') as log_file:
    proc = subprocess.Popen(
        ["python", "scripts/train.py", "--config", "configs/<name>/default.yaml"],
        stdout=log_file, stderr=subprocess.STDOUT,
        cwd=skill_opt_dir, env={**os.environ, **env_vars}
    )
```

## Env Variables Required
- `AZURE_OPENAI_ENDPOINT` or `MIMO_BASE_URL`
- `AZURE_OPENAI_API_KEY` or `MIMO_API_KEY`
- `AZURE_OPENAI_AUTH_MODE=openai_compatible`
