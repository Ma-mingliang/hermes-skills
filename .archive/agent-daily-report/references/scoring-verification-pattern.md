# 评分验证模式

## 概述

当用户报告"项目未推送"或"等级错误"时，不要假设用户报告准确。必须先验证实际数据再诊断 bug。

## 验证步骤

### 1. 读取评分数据

```python
import json

# 读取评分数据
file_path = "D:/openclaw-hermes/agent-daily-report-skill/data/scored/2026-06-04.json"
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

items = data.get('items', [])

# 查找项目
for item in items:
    if '项目名' in item.get('title', '').lower():
        print(f"Title: {item.get('title')}")
        print(f"Score: {item.get('score')}")
        print(f"Level: {item.get('importance_level')}")
        print(f"Quality Flags: {item.get('quality_flags')}")
        print(f"Trust Score: {item.get('trust_score')}")
        print(f"Trust Reason: {item.get('trust_reason')}")
        print(f"Primary Category: {item.get('primary_category')}")
        print(f"Source: {item.get('source')}")
        break
```

### 2. 验证评分计算

```python
# 检查评分计算是否正确
detail = item.get('_score_detail', {})
calculated = (detail.get('relevance', 0) + 
              detail.get('popularity', 0) + 
              detail.get('freshness', 0) + 
              detail.get('growth', 0) + 
              detail.get('utility', 0))

print(f"Calculated score: {calculated}")
print(f"Actual score: {item.get('score')}")
print(f"Score match: {calculated == item.get('score')}")
```

### 3. 验证等级分配

```python
# 检查等级分配是否正确
score = item.get('score', 0)
if score >= 85:
    expected_level = 'S'
elif score >= 70:
    expected_level = 'A'
elif score >= 55:
    expected_level = 'B'
elif score >= 40:
    expected_level = 'C'
else:
    expected_level = 'D'

print(f"Expected level (score={score}): {expected_level}")
print(f"Actual level: {item.get('importance_level')}")
print(f"Level match: {expected_level == item.get('importance_level')}")
```

### 4. 检查 Trust Decision

```python
# 检查是否有 Trust Decision 降级
trust_score = item.get('trust_score')
trust_reason = item.get('trust_reason', '')

if trust_score is not None:
    print(f"Trust Score: {trust_score}")
    print(f"Trust Reason: {trust_reason}")
    
    # 检查是否被降级
    if 'Demoted:' in trust_reason:
        print("⚠️ 项目被 Trust Decision 降级")
    
    # 检查是否被升级
    if 'Promoted:' in trust_reason:
        print("✅ 项目被 Trust Decision 升级")
```

### 5. 检查日均增长保底

```python
# 检查是否有日均增长保底
daily_avg = item.get('daily_avg_growth')
quality_flags = item.get('quality_flags', [])

if daily_avg is not None:
    print(f"Daily avg growth: {daily_avg} stars/day")
    
if 'daily_avg_growth_boost' in quality_flags:
    print("✅ 项目被日均增长保底B级机制提升")
```

### 6. 确认是否在报告中

```bash
# 在报告中搜索项目
grep -i "项目名" data/reports/Agent_Daily_Report_2026-06-04.md
```

## 常见原因

### 1. Trust Decision 降级

**表现**：score 正确，但 level 被降低
**原因**：trust_score 在 30-60 之间，且原因包含特定降级关键词
**诊断**：检查 `trust_score` 和 `trust_reason` 字段

**降级关键词**：
- "bug修复" / "bug fix"
- "缺乏独立价值" / "lacks independent value"
- "pr缺乏" / "pr lacks"
- "修复pr" / "fix pr"

**非降级原因**：
- "无多源共振证据"（2026-06-05 修改后不再降级）
- "星标数据缺失"
- "无描述"

### 2. Quality Flags 封顶

**表现**：score 被封顶到 54 分
**原因**：`quality_flags` 包含 `generic_github_discovery_candidate`
**诊断**：检查 `quality_flags` 字段

### 3. 增长门控未通过

**表现**：项目不在报告中
**原因**：`quality_flags` 包含 `github_growth_gate_not_reportable`
**诊断**：检查 `quality_flags` 和 `github_growth_gate` 字段

### 4. 数据刷新延迟

**表现**：用户看到的是旧数据
**原因**：报告已更新，但用户查看的是旧版本
**诊断**：检查报告生成时间

### 5. 日均增长保底B级

**表现**：原始评分 < 55，但最终 level=B
**原因**：日均增长 ≥ 20 stars/day，触发保底机制
**诊断**：检查 `daily_avg_growth` 和 `quality_flags` 中的 `daily_avg_growth_boost`

## 实际案例

### 案例1：native-feel-skill（2026-06-05）

**用户报告**：score=60 但 level=C，未推送
**实际验证**：
- score=60 → level=B（正确，阈值55）
- quality_flags=None（无 cap）
- 项目已在报告中（`[B] 原生体验技能`）
- 无 Trust Decision 降级

**结论**：用户误判，数据正确

### 案例2：mastra-ai/mastra（2026-06-05）

**用户报告**：score=78 但 level=B，应该是 A
**实际验证**：
- score=78 → level=A（正确，阈值70）
- trust_score=50，trust_reason="星标数据缺失、无多源共振证据"
- 旧逻辑：trust_score 在 30-60 之间 → 降级到 B
- 新逻辑：原因不包含特定降级关键词 → 保持 A

**结论**：Trust Decision 逻辑已修复

### 案例3：pydantic/pydantic-ai（2026-06-05）

**用户报告**：score=68 但 level=C，应该是 B
**实际验证**：
- score=68 → level=B（正确，阈值55）
- trust_score=58，trust_reason="Bug修复PR，缺乏独立价值"
- 新逻辑：原因包含特定降级关键词 → 降级到 C

**结论**：降级合理（Bug修复PR，缺乏独立价值）

### 案例4：日均增长保底B级（2026-06-05）

**场景**：pydantic/pydantic-ai PR 项目，原始评分 52 分（C 级）
**日均增长**：23.8 stars/day（pydantic/pydantic-ai 仓库整体增长）
**保底机制**：日均增长 ≥ 20 → 评分提升到 55 分（B 级）
**quality_flags**：`daily_avg_growth_boost`
**结论**：保底机制生效，项目从 C 级提升到 B 级

## 关键理解

- **不要假设用户报告准确**——可能是数据刷新延迟、缓存、或用户查看了旧版本报告
- **评分验证**：score=60 对应 level=B（阈值55），score=68 对应 level=B（阈值55），score=78 对应 level=A（阈值70）
- **等级分布变化**：新逻辑下，A级项目增加3个（11→14），C级项目减少2个（212→210）
- **Trust Decision 降级是有意设计**，但仅对特定原因生效
- **Quality Flags 封顶是有意设计**，用于限制 Discovery Pool 新项目
- **日均增长保底B级**：当日均增长 ≥ 20 stars/day 时，评分被提升到至少 B 级（55分），通过 `daily_avg_growth_boost` quality_flag 标记
