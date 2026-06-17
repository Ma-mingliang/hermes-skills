# Daily Average Growth Calculation

## Overview

Added on 2026-06-05 to improve growth scoring by using multi-day average instead of single-day delta.

## Motivation

Single-day growth (star_delta_24h) can be volatile — spikes or drops don't reflect sustained growth. Daily average growth calculated from snapshot history provides a smoother, more reliable metric.

**Correlation**: Single-day vs daily average correlation coefficient = 0.901 (strong), but individual projects can diverge significantly (e.g., husu/loom: single-day +1 vs daily average +122).

## Implementation

### Location
- `scripts/score_items.py` → `score_growth()` and `_calc_daily_avg_growth()`

### Calculation Logic

```python
def _calc_daily_avg_growth(self, item):
    # 1. Get repo name from item
    repo = item.get("repo") or item.get("_extra", {}).get("repo", "")
    
    # 2. Load state file
    state_path = "D:/openclaw-hermes/agent-daily-report-skill/state/github_repo_state.json"
    
    # 3. Get first and last snapshots
    snapshots = state["repos"][repo]["snapshots"]
    sorted_dates = sorted(snapshots.keys())
    first_date, last_date = sorted_dates[0], sorted_dates[-1]
    
    # 4. Calculate daily average
    first_stars = snapshots[first_date]["stars"]
    last_stars = snapshots[last_date]["stars"]
    days_diff = (last_dt - first_dt).days
    
    daily_avg = (last_stars - first_stars) / days_diff
    
    # 5. Store in item
    item["daily_avg_growth"] = daily_avg
    return daily_avg
```

### Scoring Thresholds

| Daily Average | Growth Score |
|---------------|--------------|
| > 500 | 15 |
| > 200 | 12 |
| > 100 | 9 |
| > 50 | 6 |
| > 20 | 3 |

### Fallback Logic

1. **First**: Try daily average growth (from snapshot history)
2. **Second**: Use single-day growth (star_delta_24h)
3. **Third**: Use realtime spike data
4. **Fourth**: Use star count as last resort

## Daily Average Growth Boost

**Rule**: Projects with daily average ≥ 20 stars/day are guaranteed at least B level (55 points).

**Implementation** in `calculate_score()`:
```python
daily_avg = item.get("daily_avg_growth")
if daily_avg is not None and daily_avg >= 20:
    b_threshold = self.thresholds.get("B", 55)
    if total < b_threshold:
        total = b_threshold
        item.setdefault("quality_flags", []).append("daily_avg_growth_boost")
```

**Effect** (2026-06-05):
- Before: 19 items boosted to B level
- After threshold adjustment (≥20): 19 items (reduced from 118 with >0 threshold)

## Pitfalls

### P84: Missing `import os`

**Symptom**: `_calc_daily_avg_growth` always returns None

**Root cause**: Module top didn't have `import os`, but function used `os.path.exists()`. The `except: return None` swallowed the `NameError`.

**Debug technique**: Change `except: return None` to `except Exception as e: print(f"Error: {e}")` to reveal the actual error.

**Fix**: Added `import os` to module top.

**Lesson**: 
1. Always import all dependencies at module top
2. `except: return None` is the most dangerous error handling pattern
3. Verify None returns aren't caused by exceptions

### P85: Threshold Too Low

**Symptom**: 118/264 items boosted to B level (including 0.2 stars/day)

**Root cause**: Initial threshold was `daily_avg > 0`, too permissive.

**Fix**: Changed to `daily_avg >= 20 stars/day`.

**Lesson**: Boost mechanisms must have reasonable lower bounds to preserve grade differentiation.

## Top Repos by Daily Average Growth (2026-06-05)

| Repo | Stars | Daily Avg | Period |
|------|------:|----------:|--------|
| BigPizzaV3/CodexPlusPlus | 13,469 | 797.5 | 4 days |
| anthropics/defending-code-reference-harness | 1,172 | 334.0 | 3 days |
| tastyeffectco/sandboxes | 391 | 291.0 | 1 day |
| microsoft/SkillOpt | 4,925 | 232.2 | 4 days |
| google-deepmind/science-skills | 1,550 | 211.8 | 4 days |
| ClaudioDrews/memory-os | 829 | 195.0 | 4 days |
| opensquilla/opensquilla | 2,743 | 186.3 | 3 days |
| browser-use/browser-use | 97,221 | 178.0 | 4 days |

## Verification

After changes, verify:
```python
# 1. Check function works
scorer = Scorer(config)
item = {"repo": "microsoft/SkillOpt", ...}
daily_avg = scorer._calc_daily_avg_growth(item)
assert daily_avg is not None
assert daily_avg > 0

# 2. Check boost applied
item = {"repo": "some-repo", "score": 40, ...}
scorer.calculate_score(item)
assert item["importance_level"] == "B"
assert "daily_avg_growth_boost" in item.get("quality_flags", [])

# 3. Check boost NOT applied for low growth
item = {"repo": "low-growth-repo", "score": 40, ...}
scorer.calculate_score(item)
assert item["importance_level"] == "C"
