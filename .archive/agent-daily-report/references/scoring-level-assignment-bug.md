# Scoring Level Assignment Bug (P82)

**Date**: 2026-06-05
**Symptom**: `yetone/native-feel-skill` score=60 but importance_level=C (should be B, threshold≥55)

## Resolution

**实际验证结果**：项目评分和等级是正确的！

- score: 60 ✅
- importance_level: B ✅（≥55 是 B 级）
- quality_flags: None ✅（无 cap）
- trust_score: None ✅（无降级）
- 项目已在报告中 ✅（标题为 `[B] 原生体验技能`）

**用户误判原因**：用户可能是查看了旧版本报告或记错了等级阈值。

## Scoring System

- Total = relevance(30) + popularity(20) + freshness(15) + growth(15) + utility(20)
- **No normalization** — raw weighted sum, max 100
- Level thresholds: S≥85, A≥70, B≥55, C≥40, D≥0

## 关键发现：Trust Agent 降级机制

本次诊断过程中发现了 Trust Agent 的降级机制，这是导致其他项目等级低于评分的常见原因。

**降级逻辑**（`agent_pipeline.py` L377-384）：
```
trust_score ≥ 60 → keep (保持原级)
trust_score ≥ 30 → demote (降一级)
trust_score < 30 → drop (移除)
```

**降级映射**：S→A, A→B, B→C, C→D

**实际案例**：
| 项目 | 评分 | 原始等级 | trust_score | 降级后 | 原因 |
|------|------|----------|-------------|--------|------|
| mastra-ai/mastra | 78 | A | 50 | B | 星标数据缺失、无多源共振证据 |
| BigPizzaV3/CodexPlusPlus | 73 | A | 35 | B | Star增长异常(24h+941)、无描述 |
| pydantic/pydantic-ai | 68 | B | 58 | C | 评估的是Bug修复PR、缺乏独立价值 |

详见 `references/trust-decision-mechanism.md`

## Diagnostic Script

```python
import json

# Load scored items
with open("data/scored/2026-06-04.json") as f:
    data = json.load(f)

items = data.get('items', [])
for item in items:
    if "native-feel" in item.get("title", "").lower():
        print(f"score: {item.get('score')}")
        print(f"level: {item.get('importance_level')}")
        print(f"quality_flags: {item.get('quality_flags')}")
        print(f"trust_score: {item.get('trust_score')}")
        print(f"trust_reason: {item.get('trust_reason')}")
        print(f"growth_gate: {item.get('github_growth_gate')}")
        break
```

## Lessons Learned

1. **不要假设用户报告准确** — 必须验证实际数据
2. **检查 Trust Agent 降级** — trust_score 在 30-60 之间会被降一级
3. **检查多个位置** — 项目可能在报告的不同部分（GitHub 跟踪状态表 vs 正文）
4. **确认阈值** — 确保用户和 agent 对等级阈值的理解一致
