# Growth Gate 归一化修复 (2026-06-04)

## 问题

`calculate_historical_growth` 中 `star_delta_24h` 的计算：
```python
d1 = today - 1  # 找昨天的快照
snap_1d = snapshots.get(d1)
delta_24h = stars_today - snap_1d["stars"]  # 直接用原始差值
```

快照间隔不是精确24h（可能是1.5h、16.9h、23.5h、27.2h），导致：
- 1.5h 的 delta=71 被当作24h值，实际等效 1117/天
- 增长项目被门控误杀

## 修复

`github_state.py` 的 `calculate_historical_growth` 函数：

```python
snap_1d = snapshots.get(d1)
delta_24h = (stars_today - snap_1d["stars"]) if snap_1d else None
interval_hours = _snapshot_interval_hours(today_snap, snap_1d)
is_full_24h = bool(interval_hours is not None and interval_hours >= 23.0)

# 归一化：当间隔不足24h时，将 delta 等效换算为 24h 值
delta_24h_raw = delta_24h
if delta_24h is not None and interval_hours is not None and interval_hours > 0 and not is_full_24h:
    delta_24h = round(delta_24h / interval_hours * 24)
```

metrics 中新增 `star_delta_24h_raw` 字段保留原始值。

## 验证

| 项目 | 原始 delta | 间隔 | 归一化 delta_24h | 修复前 | 修复后 |
|------|-----------|------|-----------------|--------|--------|
| CodexPlusPlus | 71 | 1.5h | 1117 | ❌ rate=0.58% | ✅ rate=9.1% (A级) |
| MedSkillOS | 52 | 1.5h | 818 | ❌ <100 | ✅ <1k delta>=200 (B级) |

## 清理 __pycache__

批量修改 .py 后必须清理所有 __pycache__：
```python
import shutil, os
base = "D:/openclaw-hermes/agent-daily-report-skill"
for root, dirs, _ in os.walk(base):
    for d in dirs:
        if d == "__pycache__":
            shutil.rmtree(os.path.join(root, d))
```
