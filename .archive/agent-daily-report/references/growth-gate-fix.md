# Growth Gate Fix (2026-06-03)

## 问题

`evaluate_github_growth_gate()` 在 `collect_github.py` 中定义，决定增长信号是否可报告。

原始规则过于严格：
- 1k-5k 区间要求 daily_rate >= 20%，导致 SkillOpt (+143, 3.2%) 被拒
- <1k 区间直接 return 不 reportable，导致 memory-os (+309) 被拒
- archived 状态仓库被完全跳过，导致 loom (+242) 被拒

## 代码变更

### 变更1: <1k 区间 (collect_github.py L204)

```python
# BEFORE
if stars < 1000:
    result["reason"] = "probation_high_delta_under_1k"
    return result

# AFTER
if stars < 1000:
    if d24 >= 200:
        result.update({
            "reportable": True,
            "mandatory": d24 >= 500,
            "level_hint": "S" if d24 >= 500 else "A" if d24 >= 300 else "B",
            "reason": "under_1k_high_delta_200plus",
        })
        return result
    result["reason"] = "probation_high_delta_under_1k"
    return result
```

### 变更2: 1k-5k 区间 (collect_github.py L218)

```python
# BEFORE
if rate >= 0.20:
    result.update({
        "reportable": True,
        "mandatory": True,
        "level_hint": "S" if d24 >= 500 else "A",
        "reason": "one_k_repo_20pct_growth",
    })

# AFTER
if d24 >= 100:
    result.update({
        "reportable": True,
        "mandatory": d24 >= 300,
        "level_hint": "S" if d24 >= 500 else "A" if d24 >= 300 else "B",
        "reason": "one_k_repo_high_delta_100plus",
    })
```

## 修改后规则

| 区间 | reportable 条件 | 分级 |
|------|----------------|------|
| stars < 100 | 不eligible | — |
| <1k | delta >= 200 | S≥500 / A≥300 / B≥200 |
| 1k-5k | delta >= 100 | S≥500 / A≥300 / B≥100 |
| >=5k | daily_rate >= 1% | B / A≥10% |

## 验证

```bash
# 清理 __pycache__
rm -rf D:/openclaw-hermes/agent-daily-report-skill/scripts/__pycache__

# 语法检查
python -c "import py_compile; py_compile.compile('D:/openclaw-hermes/agent-daily-report-skill/scripts/collect_github.py', doraise=True)"
```

## 遗留问题

- P66: `_find_growth_anomalies()` L1008 的 `if rn in already: continue` 导致已进 candidates 的仓库不参与增长检测
- archived 状态仓库仍被跳过（L1018: `if st in ("archived", "dropped", "")`）
