# Growth Gate 诊断方法论 (2026-06-03)

## 问题

报告输出"历史增长异常项目: 暂无"，但 state 有 3 天快照且多个仓库日均增长 >100。

## 根因分析

23个日均>=100的仓库，只有4个通过全部过滤。过滤漏斗：

```
23 个日均>=100
  ├─ 5 个因 tracking_status=archived/dropped 被 _find_growth_anomalies 跳过
  ├─ 4 个因 has_strong_agent_signal=False 被 evaluate_github_growth_gate 拒绝
  ├─ 10 个因 __pycache__ 旧字节码（P68）被旧逻辑拒绝
  └─ 4 个通过 ✅ (SkillOpt, science-skills, browser-use, opensquilla)
```

## 四层过滤诊断

当 growth 诊断需要排查时，逐层检查：

### 1. `_find_growth_anomalies` 前置过滤
```python
if rn in already or rn in watch:  # 已在 candidates 中 → 跳过 (P66)
    continue
if st in ("archived", "dropped", ""):  # 状态过滤
    continue
if not is_reportable_github_growth_repo(repo_like):  # negative_keywords
    continue
```

### 2. `has_strong_agent_signal(repo)` 
检查 description/topics 是否包含强 Agent 信号词。弱信号仓库（如 GordenPPTSkill、claude-fuer-deutsches-recht）被拒绝。

### 3. `evaluate_github_growth_gate` 内部过滤
```python
# is_valid_star_delta_24h(stars, d24) — d24 不能为 None 或负数
# d24 < 100 → 不 eligible
# d24 >= 50 and stars >= 1000 → observation_only（不 reportable）
# stars >= 10000 → observation_only
# stars < 1000 and d24 < 200 → probation_high_delta_under_1k（不 reportable）
# stars >= 5000 and rate < 0.01 → 不 reportable
```

### 4. `__pycache__` 问题 (P68)
修改 `.py` 文件后，Python 优先加载 `.pyc`。**必须清除所有 `__pycache__` 目录**：
```python
import shutil, os
base = "D:/openclaw-hermes/agent-daily-report-skill"
for root, dirs, _ in os.walk(base):
    for d in dirs:
        if d == "__pycache__":
            shutil.rmtree(os.path.join(root, d))
```

## 诊断脚本

```python
import json, sys
sys.path.insert(0, "D:/openclaw-hermes/agent-daily-report-skill/scripts")
import importlib, collect_github
importlib.reload(collect_github)  # 避免 __pycache__

state = json.load(open("state/github_repo_state.json"))
for rn, rs in state["repos"].items():
    snaps = rs.get("snapshots", {})
    dates = sorted(snaps.keys())
    if len(dates) < 2: continue
    deltas = [snaps[dates[i]]["stars"] - snaps[dates[i-1]]["stars"] for i in range(1, len(dates))]
    if not deltas or sum(deltas)/len(deltas) < 100: continue
    
    m = rs.get("metrics", {})
    repo_like = {"full_name": rn, "description": rs.get("description",""), "topics": rs.get("topics",[])}
    gate = collect_github.evaluate_github_growth_gate(repo_like, m)
    blocked = rs.get("tracking_status","") in ("archived","dropped","")
    final = collect_github.has_strong_agent_signal(repo_like) and gate.get("reportable") and not blocked
    print(f"{'✅' if final else '❌'} {rn}: gate={gate.get('reportable')}, reason={gate.get('reason')}, blocked={blocked}")
```

## 用户展示偏好

列出仓库时必须附带具体功能描述。数据来源：
1. candidates.json 的 description/summary 字段
2. 无描述时从 GitHub API `GET /repos/{name}` 获取 description
