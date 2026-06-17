# Trust Decision Mechanism

## Overview

The Trust Agent evaluates GitHub projects and assigns trust scores (0-100). Based on the score and reason, projects can be kept, demoted, or dropped.

**Updated on 2026-06-05**: Modified to only demote for specific reasons and add multi-source resonance promotion.

## Trust Score Thresholds

| Trust Score | Decision |
|-------------|----------|
| ≥ 60 | keep (no change) |
| ≥ 30 | demote (downgrade one level, only for specific reasons) |
| < 30 | drop (remove from report) |

## Level Mapping

### Demotion
```
S → A
A → B
B → C
C → D
```

### Promotion (multi-source resonance)
```
B → A
C → B
D → C
```

## Decision Logic (2026-06-05 Update)

### 1. Check Multi-Source Resonance (Promote)

If reason contains positive multi-source keywords AND no negation patterns, promote one level.

**Positive patterns**:
- 多源共振
- multi-source resonance
- cross-source verified
- 多个来源验证
- multiple sources confirmed
- 多源验证

**Negation patterns** (prevent false promotion):
- 无多源
- 无跨源
- no multi
- no cross
- 缺乏多源
- lacks multi
- 无新增
- 无.*共振
- 缺乏.*共振
- 无.*验证
- 缺乏.*验证

### 2. Check Demotion Conditions

Only demote if reason contains specific keywords:
- bug修复
- bug fix
- 缺乏独立价值
- lacks independent value
- pr缺乏
- pr lacks
- 修复pr
- fix pr

**Other reasons (like "无多源共振证据") do NOT trigger demotion.**

### 3. Default Behavior

If no promotion or demotion conditions met, keep original level.

## Implementation

### Location
`scripts/agent_pipeline.py` → `apply_trust_decisions()`

### Code Logic

```python
def apply_trust_decisions(scored, decisions, trust_cfg):
    # 1. Check multi-source resonance
    has_multi_source = any(pattern in reason.lower() for pattern in positive_patterns)
    has_negation = any(pattern in reason.lower() for pattern in negation_patterns)
    
    if has_multi_source and not has_negation and decision != "drop":
        # Promote one level
        level = item.get("importance_level", "B")
        promote_map = {"B": "A", "C": "B", "D": "C"}
        if level in promote_map:
            item["importance_level"] = promote_map[level]
            return item
    
    # 2. Check demotion conditions
    demote_keywords = ["bug修复", "bug fix", "缺乏独立价值", ...]
    should_demote = any(keyword in reason.lower() for keyword in demote_keywords)
    
    if decision == "demote" and should_demote:
        # Demote one level
        level_map = {"S": "A", "A": "B", "B": "C", "C": "D"}
        item["importance_level"] = level_map.get(level, "D")
    elif decision == "demote":
        # Keep original level (reason doesn't match demote keywords)
        pass
```

## Real Cases (2026-06-05)

| Project | Score | Level | Trust Score | Trust Reason | Final Level |
|---------|------:|-------|------------:|--------------|-------------|
| mastra-ai/mastra | 78 | A | 50 | 星标数据缺失、无多源共振证据、可操作性评级为低 | A (kept) |
| BigPizzaV3/CodexPlusPlus | 73 | A | 35 | Star增长异常(24h+941)、无描述、无跨源验证 | A (kept) |
| pydantic/pydantic-ai | 68 | B | 58 | 评估的是Bug修复PR、缺乏独立价值 | C (demoted) |
| browser-use/browser-use | 70 | B | 70 | 项目直接面向AI Agent的浏览器自动化，有明确工程价值 | A (promoted) |

## Diagnosis

When user reports "wrong level" or "not pushed":

1. **Check trust_score and trust_reason**
   ```python
   item = find_item(title)
   print(f"trust_score: {item.get('trust_score')}")
   print(f"trust_reason: {item.get('trust_reason')}")
   ```

2. **Check if demotion was applied**
   - trust_score 30-60 AND reason contains demote keywords → demoted
   - trust_score 30-60 AND reason does NOT contain demote keywords → kept

3. **Check if promotion was applied**
   - Reason contains positive multi-source keywords AND no negation → promoted

4. **Common misconceptions**
   - "无多源共振证据" does NOT cause demotion (updated 2026-06-05)
   - quality_flags: None does NOT mean no demotion (demotion is from Trust Agent, not quality_flags)
   - Trust decisions are separate from scoring caps

## Changes Made (2026-06-05)

### Before
- Any trust_score 30-60 → demote (regardless of reason)
- No promotion mechanism

### After
- trust_score 30-60 → demote ONLY for specific reasons (bug fix PR, lacks independent value)
- Multi-source resonance → promote one level
- "无多源共振证据" no longer causes demotion

### User Requirements
1. Only keep demotion for pydantic/pydantic-ai (Bug修复PR，缺乏独立价值)
2. Remove demotion for mastra-ai/mastra and BigPizzaV3/CodexPlusPlus
3. Items with multi-source resonance should be promoted one level

## Related Pitfalls

| Pitfall | Description |
|---------|-------------|
| P82 | User reports "wrong level" but data is correct — verify before diagnosing |
| P83 | Trust demotion too broad — only demote for specific reasons |
| P84 | Missing import os causes silent failures |
| P85 | Daily avg growth boost threshold too low |
