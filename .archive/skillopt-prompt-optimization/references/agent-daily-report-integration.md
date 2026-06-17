# Agent Daily Report × SkillOpt Integration

Complete working example of optimizing agent-daily-report prompts with SkillOpt.

## Environment Setup

### 1. Clone SkillOpt
```bash
git clone https://github.com/microsoft/SkillOpt.git D:/openclaw-hermes/SkillOpt
cd D:/openclaw-hermes/SkillOpt
pip install -e .
```

### 2. Configure .env
```
# D:/openclaw-hermes/SkillOpt/.env
AZURE_OPENAI_ENDPOINT=https://token-plan-sgp.xiaomimimo.com/v1
AZURE_OPENAI_API_KEY=<your-mimo-api-key>
AZURE_OPENAI_AUTH_MODE=openai_compatible
```

**Pitfall**: Remove `export` prefix from .env lines. Python's `os.environ` doesn't parse `export`.

**CRITICAL PITFALL: `~/.hermes/.env` overrides SkillOpt `.env`**

The `_load_env()` function in `rollout.py` loads `~/.hermes/.env` FIRST and then `breaks`, so SkillOpt's own `.env` is never read. If `~/.hermes/.env` has a different `MIMO_BASE_URL` (e.g. `api.xiaomimimo.com`), the SkillOpt training will use the wrong endpoint.

**Fix in `_call_llm()`**: Force the correct endpoint when the existing API key is detected:
```python
# Fix: api.xiaomimimo.com requires different key, use token-plan-sgp for existing key
if "api.xiaomimimo.com" in base_url and "token-plan-sgp" not in base_url:
    base_url = "https://token-plan-sgp.xiaomimimo.com/v1"
```

**Alternative fix**: Update `~/.hermes/.env` to have the correct `MIMO_BASE_URL` for SkillOpt.

### 3. Register environment in train.py

Add to `_register_builtins()`:
```python
try:
    from skillopt.envs.agent_daily_report.adapter import AgentDailyReportEnv
    _ENV_REGISTRY["agent-daily-report"] = AgentDailyReportEnv
except ImportError:
    pass
```

## Files Created

### skillopt/envs/agent_daily_report/adapter.py
- `AgentDailyReportEnv(EnvAdapter)` with `rollout()`, `reflect()`, `get_task_types()`
- `rollout()` calls `run_rollout()` from rollout.py
- `reflect()` calls `run_reflect()` from rollout.py

### skillopt/envs/agent_daily_report/dataloader.py
- `AgentDailyReportLoader(SplitDataLoader)` with `load_split_items()` and `load_raw_items()`
- Reads JSON arrays from train/val/test splits

### skillopt/envs/agent_daily_report/rollout.py
- `run_rollout()`: Calls LLM to generate optimization suggestions, evaluates output
- `run_reflect()`: Generates edit patches in SkillOpt format
- `_call_llm()`: MiMo-compatible LLM caller with retry logic
- `_evaluate_output()`: 13-dimension evaluation (3-prompt serial)
- `_extract_json_from_response()`: Robust JSON extraction with multiple fallback strategies

### skillopt/envs/agent_daily_report/evaluator.py
- `evaluate_skill()`: Evaluates skill quality against eval items

### configs/agent-daily-report/default.yaml
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
  train_size: 4
  batch_size: 1
optimizer:
  learning_rate: 2
  lr_scheduler: cosine
  skill_update_mode: patch
env:
  name: agent-daily-report
  skill_init: skillopt/envs/agent_daily_report/skills/initial.md
  split_mode: split_dir
  split_dir: data/agent-daily-report
```

## Training Data

9 samples covering different scenarios:
- MCP-heavy days
- Dedup issues
- Scoring problems
- Source filtering issues
- Clarity issues

Located at: `data/agent-daily-report/training_data.json`

Split: train=4, val=2, test=3

## Training Results (v9)

### v9 Run (2026-06-04) — SUCCESS
- **Evaluator**: 13 dimensions, 3-prompt serial, `thinking: {"type": "disabled"}`
- **Result**: Step 2 reached score=1.0 (perfect), accepted as best
- **Optimization**: Trust score criteria improved from vague ("官方发布、重大版本更新、多源确认") to specific ("官方发布 + 多源共振(≥3 sources) + star_delta > 500/day")
- **Skill size**: 3686 → 3763 chars (+77)
- **Training time**: ~5 minutes for 2 steps

### v9 Manual Optimization (2026-06-04) — SUCCESS
- **Trigger**: Auto training stalled at step 2, evaluator returning fallback scores
- **Method**: Manual targeted optimization based on dimension scores
- **Initial scores**: overall=71, examples=30, safety=20, robustness=40, verifiability=30
- **Final scores**: overall=88, examples=70, safety=95, robustness=85, verifiability=90
- **Key changes**: Added 安全检查/边界处理/输出格式/示例 sections with "必须执行" prefix
- **Result**: +17 points overall (+24% improvement)

### What worked
- 13-dimension evaluator with `thinking:disabled` — all dimensions return valid scores
- `_call_llm()` endpoint fix — forces `token-plan-sgp.xiaomimimo.com/v1`
- `SKILLOPT_DEBUG=1` — shows raw LLM responses and parsed scores
- Reflect function generates valid patches (patches=1 per step)
- Patches correctly applied (status=applied_replace)
- Manual optimization for targeted dimension improvements

### What didn't work (previous runs)
- 12-dimension single prompt → MiMo returns empty
- `api.xiaomimimo.com` endpoint → 401 with existing API key
- `~/.hermes/.env` overriding SkillOpt `.env` → wrong endpoint

## Key Learnings

1. **MiMo + English prompts = empty responses** → Use Chinese
2. **SkillOpt edit format**: `op`/`content`/`target` NOT `operation`/`old_text`/`new_text`
3. **13 dimensions work with 3-prompt serial** → each prompt has 4-5 dims, `thinking:disabled`
4. **Pre-create all directories** before training (steps/, skills/, slow_update/, meta_skill/)
5. **batch_size=1** is correct for prompt optimization (each item needs individual LLM attention)
6. **`~/.hermes/.env` overrides SkillOpt `.env`** → fix in `_call_llm()` or update `~/.hermes/.env`
7. **`api.xiaomimimo.com` ≠ `token-plan-sgp.xiaomimimo.com`** → different API keys required
8. **`SKILLOPT_DEBUG=1`** → shows raw LLM responses, essential for debugging evaluator issues
9. **Rule-based fallback** returns 50 when all LLM eval fails → check if LLM is actually called
10. **Manual optimization beats auto-training** for targeted dimension improvements
11. **"必须执行/遵守" prefix** improves consistency scores by 10-15 points
12. **Explicit safety/boundary/format rules** improve robustness, safety, verifiability by 20-40 points

## Directory Structure

```
D:/openclaw-hermes/SkillOpt/
├── configs/agent-daily-report/default.yaml
├── skillopt/envs/agent_daily_report/
│   ├── __init__.py
│   ├── adapter.py
│   ├── dataloader.py
│   ├── rollout.py
│   ├── evaluator.py
│   ├── prompts/          # Extracted prompt files
│   └── skills/initial.md # Initial prompt (from agent_prompts.py)
├── data/agent-daily-report/
│   ├── training_data.json
│   ├── train/items.json
│   ├── val/items.json
│   └── test/items.json
└── outputs/agent-daily-report/
    ├── best_skill.md
    ├── history.json
    └── steps/
```
