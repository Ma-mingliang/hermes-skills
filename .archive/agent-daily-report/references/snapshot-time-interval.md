# 快照时间间隔

## 概述

GitHub 项目快照的时间间隔约为 24.6 小时（1天0小时33分钟）。这个间隔用于计算 star_delta_24h（24小时星标增长）。

## 实际数据（2026-06-05）

```
最新采集: 2026-06-05T11:03:17 (北京时间)
上次采集: 2026-06-04T10:30:17 (北京时间)
─────────────────────────────────────
时间差:   1天 0小时 33分钟
          ≈ 24.6 小时
```

## 快照存储

**存储位置**：`state/github_repo_state.json`

**快照结构**：
```json
{
  "repos": {
    "microsoft/SkillOpt": {
      "snapshots": {
        "2026-06-01": {"stars": 4696, "collected_at": "2026-06-01T10:30:17+08:00"},
        "2026-06-02": {"stars": 4720, "collected_at": "2026-06-02T10:30:17+08:00"},
        "2026-06-03": {"stars": 4750, "collected_at": "2026-06-03T10:30:17+08:00"},
        "2026-06-04": {"stars": 4800, "collected_at": "2026-06-04T10:30:17+08:00"},
        "2026-06-05": {"stars": 4925, "collected_at": "2026-06-05T11:03:17+08:00"}
      }
    }
  }
}
```

## Star Delta 计算

**计算公式**：
```python
# 从快照中获取星标数
stars_today = snapshots["2026-06-05"]["stars"]  # 4925
stars_yesterday = snapshots["2026-06-04"]["stars"]  # 4800

# 计算原始差值
delta_raw = stars_today - stars_yesterday  # 125

# 计算时间间隔（小时）
collected_at_today = datetime.fromisoformat(snapshots["2026-06-05"]["collected_at"])
collected_at_yesterday = datetime.fromisoformat(snapshots["2026-06-04"]["collected_at"])
interval_hours = (collected_at_today - collected_at_yesterday).total_seconds() / 3600  # 24.6

# 归一化到24小时（如果间隔不足24小时）
if interval_hours < 23:
    star_delta_24h = round(delta_raw / interval_hours * 24)
else:
    star_delta_24h = delta_raw
```

## 归一化逻辑

**触发条件**：快照间隔 < 23 小时

**归一化公式**：
```python
star_delta_24h = round(delta_raw / interval_hours * 24)
```

**示例**：
- 间隔 1.5 小时，delta_raw = 71
- 归一化后：round(71 / 1.5 * 24) = round(1136) = 1136
- 实际 24 小时增长：1136 星

**保留原始值**：
```python
metrics = {
    "star_delta_24h": 1136,  # 归一化后的值
    "star_delta_24h_raw": 71,  # 原始差值
    "interval_hours": 1.5
}
```

## 诊断流程

当用户问"收集的时间差值是多少"时：

```python
import json
from datetime import datetime

# 加载 GitHub state
state_path = "D:/openclaw-hermes/agent-daily-report-skill/state/github_repo_state.json"
with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

repos = state.get('repos', {})

# 检查时间间隔
count = 0
for repo, data in repos.items():
    if count >= 3:
        break
    
    snapshots = data.get('snapshots', {})
    if len(snapshots) >= 2:
        sorted_keys = sorted(snapshots.keys())
        latest_key = sorted_keys[-1]
        prev_key = sorted_keys[-2]
        
        latest_snapshot = snapshots[latest_key]
        prev_snapshot = snapshots[prev_key]
        
        print(f"{repo}:")
        print(f"  Latest: {latest_key}")
        print(f"  Previous: {prev_key}")
        
        # 计算时间差
        if latest_snapshot.get('collected_at') and prev_snapshot.get('collected_at'):
            try:
                latest_dt = datetime.fromisoformat(latest_snapshot['collected_at'].replace('Z', '+00:00'))
                prev_dt = datetime.fromisoformat(prev_snapshot['collected_at'].replace('Z', '+00:00'))
                diff = latest_dt - prev_dt
                print(f"  Time difference: {diff}")
                print(f"  Hours: {diff.total_seconds() / 3600:.1f}")
            except Exception as e:
                print(f"  Error calculating time difference: {e}")
        
        count += 1
```

## 关键理解

- **快照间隔**：约 24.6 小时（1天0小时33分钟）
- **归一化触发**：间隔 < 23 小时时才归一化
- **归一化目的**：确保 star_delta_24h 反映真实的 24 小时增长趋势
- **原始值保留**：star_delta_24h_raw 保留原始差值，用于诊断
- **诊断关键**：当用户问"时间差值"时，检查 collected_at 字段计算实际间隔
