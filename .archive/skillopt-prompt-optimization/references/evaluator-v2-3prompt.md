# Evaluator v2: 13-Dimension, 3-Prompt Serial Evaluation

**File**: `D:\openclaw-hermes\SkillOpt\skillopt\envs\agent_daily_report\rollout.py` (in `_evaluate_output`)
**Also**: `D:\openclaw-hermes\SkillOpt\skillopt\envs\agent_daily_report\evaluator.py` (standalone version)

## Design

3 serial prompts per eval item, evaluating 13 dimensions total:

| Prompt | Dimensions | Weights |
|--------|-----------|---------|
| 1 — Core | relevance(15%), completeness(15%), accuracy(15%), specificity(15%) | 60% |
| 2 — Execution | actionability(10%), clarity(10%), coverage(10%), consistency(10%) | 40% |
| 3 — Quality | robustness(10%), verifiability(10%), examples(5%), safety(5%), maintainability(5%) | 35% |

Total weight = 135%, normalized in `_weighted_score()`.

## Key Implementation

```python
payload = {
    "thinking": {"type": "disabled"},  # MiMo fix: MUST disable thinking
    "max_tokens": 512,                 # Sufficient for 4-5 dimension JSON
    "temperature": 0.1,
}

def _retry_call(fn, *args, max_retries=2):
    for attempt in range(max_retries + 1):
        result = fn(*args)
        parsed = _parse_json_response(result) if isinstance(result, str) else result
        if parsed is not None:
            return parsed
    return None

def _weighted_score(dim_scores: dict) -> float:
    total = 0.0
    weight_used = 0.0
    for dim, weight in DIMENSIONS.items():
        if dim in dim_scores:
            total += dim_scores[dim] * weight
            weight_used += weight
    return round(total / weight_used, 1) if weight_used > 0 else 50.0
```

## Debug Mode

Set `SKILLOPT_DEBUG=1` to see raw LLM responses and parsed scores:

```bash
SKILLOPT_DEBUG=1 python scripts/train.py --config configs/agent-daily-report/default.yaml
```

Output shows:
```
[EVAL_P1] response=```json {"relevance": 95, ...}```
[EVAL_P1] parsed={'relevance': 95, 'completeness': 70, ...}
[EVAL] scores1={...} scores2={...} scores3={...}
```

## Return Format (rollout.py)

```python
{
    "hard": 1.0,           # 1.0 if overall >= 70, else 0.0
    "soft": 0.71,          # overall / 100.0
    "details": {
        "relevance": 95, "completeness": 70, "accuracy": 90, "specificity": 100,
        "actionability": 85, "clarity": 90, "coverage": 40, "consistency": 70,
        "robustness": 30, "verifiability": 40, "examples": 60, "safety": 20,
        "maintainability": 70, "overall": 71
    }
}
```

## Return Format (evaluator.py standalone)

```python
{
    "score": 72.5,
    "num_evaluated": 5,
    "dimension_averages": {"relevance": 78.0, ...},
    "per_item": [
        {
            "weighted": 72.5,
            "dimensions": {...},
            "prompts_ok": [True, True, True]
        }
    ]
}
```

## Why 13 Dimensions

The original 5 dimensions (clarity, completeness, specificity, actionability, consistency) were too coarse. Added:
- **relevance**: Is it related to the task? (prevents generic prompts)
- **accuracy**: Are instructions correct? (catches errors)
- **coverage**: Does it cover edge cases? (data sources, formats, boundaries)
- **robustness**: Handles abnormal inputs? (empty data, format errors)
- **verifiability**: Has verification rules? (can check output correctness)
- **examples**: Good/bad examples? (helps LLM understand expectations)
- **safety**: Anti-injection/anti-privilege-escalation checks?
- **maintainability**: Modular, well-commented?

## Fallback: Rule-Based Evaluation

When all 3 LLM prompts fail (returns `{}`), falls back to rule-based scoring:

```python
if not scores1 and not scores2 and not scores3:
    score = 50
    if len(skill_md) > 2000: score += 10
    if len(re.findall(r'^##\s+', skill_md, re.MULTILINE)) >= 4: score += 10
    if len(re.findall(r'(?:必须|不得|禁止|应该)', skill_md)) >= 2: score += 10
    if len(re.findall(r'(?:示例|例如)', skill_md)) >= 1: score += 10
    score = max(0, min(100, score))
```

## Key Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| thinking mode enabled | MiMo returns empty for eval prompts | `thinking: {"type": "disabled"}` in payload |
| Too many dimensions in one prompt | Inconsistent or missing scores | Split into 3 prompts (4-5 dims each) |
| max_tokens too low | JSON truncated | Use 512 for eval prompts, 1024 for standalone |
| Fallback returns 50 | All scores stuck at 0.50 | Check if LLM calls are actually failing (use SKILLOPT_DEBUG=1) |
