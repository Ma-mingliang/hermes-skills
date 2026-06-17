# Growth Gate 快照间隔 Bug (P74)

## 问题

`calculate_historical_growth()` 用 `stars_today - snap_1d["stars"]` 计算 `star_delta_24h`，但不检查实际采集间隔是否 ~24h。当 pipeline 在同一天运行两次（如 6/3 23:05 和 6/4 00:37），间隔仅 1.5h，delta 被严重低估。

## 诊断方法

```python
import json
from datetime import datetime

state_path = "D:/openclaw-hermes/agent-daily-report-skill/state/github_repo_state.json"
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

for name, rs in state.get("repos", {}).items():
    metrics = rs.get("metrics", {})
    interval = metrics.get("star_delta_interval_hours")
    is_full = metrics.get("star_delta_is_full_24h")
    d24 = metrics.get("star_delta_24h")
    
    if interval and interval < 23 and d24 and d24 >= 30:
        # 被低估的项目
        corrected = d24 / interval * 24
        print(f"{name}: delta={d24} interval={interval}h → 24h等效={corrected:.0f}")
```

## 2026-06-04 实测数据

| 项目 | 快照间隔 | raw delta | 24h 等效 | 门控结果(raw) | 门控结果(修正) |
|------|---------|-----------|---------|-------------|-------------|
| CodexPlusPlus | 1.52h | 71 | 1,121 | ❌ rate=0.58% | ✅ rate=9.1% A级 |
| MedSkillOS | 1.52h | 52 | 821 | ❌ <100 stars | ✅ delta>=200 B级 |

## 根因

`github_state.py` L~4473:
```python
d1 = (datetime.strptime(today, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
snap_1d = snapshots.get(d1)
delta_24h = (stars_today - snap_1d["stars"]) if snap_1d else None
interval_hours = _snapshot_interval_hours(today_snap, snap_1d)
is_full_24h = bool(interval_hours is not None and interval_hours >= 23.0)
```

`interval_hours` 和 `is_full_24h` 已计算但未被 `evaluate_github_growth_gate` 使用。

## 修复方案

### 方案 A：在 calculate_historical_growth 中归一化（推荐）

```python
delta_raw = stars_today - snap_1d["stars"]
if interval_hours and interval_hours > 0:
    delta_24h = round(delta_raw / interval_hours * 24)
else:
    delta_24h = delta_raw
```

### 方案 B：在 growth gate 中检查 is_full_24h

```python
if not metrics.get("star_delta_is_full_24h", True):
    # 快照间隔不足24h，delta不可靠
    result["reason"] = "incomplete_24h_interval"
    return result
```

### 方案 C：混合方案

归一化 delta，同时标记 `is_full_24h=false` 供下游参考。

## 注意事项

- 归一化假设增长是均匀的，实际可能有突发增长（如 Hacker News 首页效应）
- 对于 <2h 的超短间隔，归一化可能过度放大噪声
- 建议：间隔 < 4h 时不归一化，而是标记为 "insufficient_interval"
