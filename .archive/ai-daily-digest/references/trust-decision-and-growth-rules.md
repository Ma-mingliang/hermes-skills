# 信任决策逻辑与日均增长计算

## 信任决策逻辑（Trust Decision Rules）

### 降级规则（必须遵守）

**只对特定原因降级**，以下原因才会触发降级：
- Bug修复PR、缺乏独立价值、pr lacks、fix pr

**以下原因不触发降级**：
- 无多源共振证据
- 星标数据缺失
- 可操作性评级为低
- Star增长异常（除非有明确欺诈证据）

### 提升规则（必须遵守）

**多源共振提升**：当原因包含正面多源共振关键词时，提升一级
- 正面关键词：多源共振、multi-source resonance、cross-source verified
- 否定模式检查：无多源、无跨源、缺乏多源、无新增、无.*共振

**提升映射**：
- B → A
- C → B
- D → C

### 实现位置
`scripts/agent_pipeline.py` → `apply_trust_decisions()` 函数

---

## 日均增长计算（Daily Average Growth）

### 计算方法
从 GitHub 快照历史计算日均增长：
```
日均增长 = (最新stars - 首次stars) / 天数差
```

### 评分规则
- 日均增长 ≥ 500 → growth score 15
- 日均增长 ≥ 200 → growth score 12
- 日均增长 ≥ 100 → growth score 9
- 日均增长 ≥ 50 → growth score 6
- 日均增长 ≥ 20 → growth score 3

### 保底B级规则
日均增长 ≥ 20 stars/day 的项目，确保至少B级（score ≥ 55）

### 优先级
1. 优先使用日均增长（从快照历史）
2. 其次使用单日增长（star_delta_24h）
3. 最后使用实时飙升数据

### 实现位置
`scripts/score_items.py` → `score_growth()` + `_calc_daily_avg_growth()`
