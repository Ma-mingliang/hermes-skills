# Growth Delta 24h 归一化修复 (2026-06-04)

## 问题

`calculate_historical_growth` 计算 `star_delta_24h` 时，直接用昨天快照的原始差值，不考虑实际时间间隔。

当 pipeline 在一天内多次运行（如 23:05 和次日 00:37），间隔只有 1.5h，但 delta 被当作 24h 值使用。

## 影响

- CodexPlusPlus: raw=+71 (1.5h) → 归一化=+1,117/day，rate=9.1%，应为 A 级
- MedSkillOS: raw=+52 (1.5h) → 归一化=+818/day，应为 B 级
- 2026-06-04 实测：13个项目被误杀

## 修复

文件：`scripts/github_state.py`

```python
# 归一化：当间隔不足24h时，将 delta 等效换算为 24h 值
delta_24h_raw = delta_24h
if delta_24h is not None and interval_hours is not None and interval_hours > 0 and not is_full_24h:
    delta_24h = round(delta_24h / interval_hours * 24)
```

metrics 新增 `star_delta_24h_raw` 字段保留原始值。

## 诊断方法

```python
# 检查快照间隔
snaps = repo_state["snapshots"]
dates = sorted(snaps.keys())
for i in range(1, len(dates)):
    t1 = datetime.fromisoformat(snaps[dates[i-1]]["collected_at"])
    t2 = datetime.fromisoformat(snaps[dates[i]]["collected_at"])
    hours = (t2 - t1).total_seconds() / 3600
    delta = snaps[dates[i]]["stars"] - snaps[dates[i-1]]["stars"]
    if hours < 23:
        normalized = round(delta / hours * 24)
        print(f"{dates[i]}: interval={hours:.1f}h raw={delta} normalized={normalized}")
```
