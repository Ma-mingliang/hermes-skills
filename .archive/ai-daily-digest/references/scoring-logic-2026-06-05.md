# Scoring Logic Updates (2026-06-05)

## Trust Decision Logic Changes

Modified `agent_pipeline.py` - `apply_trust_decisions()` function:

### New Rules
1. **Only demote for specific reasons**: Bug修复PR, 缺乏独立价值
2. **Remove demotion for other reasons**: 无多源共振证据, 星标数据缺失
3. **Promote for multi-source resonance**: B→A, C→B (if positive, no negation)

### Demote Keywords
```python
demote_keywords = ["bug修复", "bug fix", "缺乏独立价值", "lacks independent value", 
                   "pr缺乏", "pr lacks", "修复pr", "fix pr"]
```

### Multi-Source Resonance Detection
```python
# Negation patterns (don't promote)
negation_patterns = ["无多源", "无跨源", "no multi", "no cross", "缺乏多源", "lacks multi",
                     "无新增", "无.*共振", "缺乏.*共振", "无.*验证", "缺乏.*验证"]

# Positive patterns (promote)
positive_patterns = ["多源共振", "multi-source resonance", "cross-source verified", 
                     "多个来源验证", "multiple sources confirmed", "多源验证"]
```

## Daily Average Growth Calculation

Modified `score_items.py` - Added `_calc_daily_avg_growth()` function:

### Logic
1. Load snapshot history from `state/github_repo_state.json`
2. Calculate: `daily_avg = (last_stars - first_stars) / days_diff`
3. Store result in `item["daily_avg_growth"]`

### Pitfall: `os` Module Import
The `os` module MUST be imported at the top of `score_items.py`:
```python
import logging
import os  # REQUIRED for _calc_daily_avg_growth
import re
```
Without this, the function returns `None` with error "name 'os' is not defined".

### Scoring Thresholds
```python
if daily_avg > 500: return 15
elif daily_avg > 200: return 12
elif daily_avg > 100: return 9
elif daily_avg > 50: return 6
elif daily_avg > 20: return 3
```

## Daily Average Growth Boost (B Level Floor)

Modified `calculate_score()` in `score_items.py`:

```python
# 日均增长保底 B 级（仅对有显著增长的项目）
daily_avg = item.get("daily_avg_growth")
if daily_avg is not None and daily_avg >= 20:
    # 如果日均增长 >= 20 stars/day，确保至少 B 级
    b_threshold = self.thresholds.get("B", 55)
    if total < b_threshold:
        total = b_threshold
        item.setdefault("quality_flags", []).append("daily_avg_growth_boost")
```

### Effect
- Items with daily_avg >= 20 stars/day get boosted to B level minimum
- Prevents high-growth projects from being filtered out

## Level Distribution Changes

| Level | Before | After |
|-------|--------|-------|
| S | 0 | 0 |
| A | 11 | 13 |
| B | 26 | 43 |
| C | 212 | 192 |
| D | 15 | 16 |

## Key Items Affected

| Item | Old Level | New Level | Reason |
|------|-----------|-----------|--------|
| mastra-ai/mastra | B | A | Removed demotion |
| BigPizzaV3/CodexPlusPlus | B | A | Removed demotion |
| browser-use/browser-use | B | A | Multi-source resonance |
| pydantic/pydantic-ai | C | C | Kept demotion (Bug修复PR) |
| GordenSun/GordenPPTSkill | C | B | Daily avg growth boost |
