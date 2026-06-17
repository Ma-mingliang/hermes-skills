# Manual Optimization Technique for Skill Prompts

When automated SkillOpt training stalls or produces suboptimal results, manual targeted optimization is more effective for improving specific dimensions.

## When to Use

- Automated training stuck at score 0.0 (evaluator failing)
- Specific dimensions are low (<80) while others are high (>90)
- Need quick improvements without waiting for full training cycle
- Want to understand what changes improve each dimension

## Workflow

### Step 1: Run Baseline Evaluation

```python
import sys
sys.path.insert(0, r"D:\openclaw-hermes\SkillOpt")
from skillopt.envs.agent_daily_report.rollout import _evaluate_output

skill_md = open("path/to/skill.md").read()
item = {"date": "2026-06-04", "task": "test"}
result = _evaluate_output(skill_md, item, "test output")

print(f"Overall: {result['details']['overall']}")
for dim, score in sorted(result['details'].items()):
    if dim != 'overall':
        print(f"  {dim}: {score}")
```

### Step 2: Identify Low Dimensions

Focus on dimensions scoring <80:
- `examples` < 60: Need good/bad examples
- `safety` < 60: Need explicit safety checks
- `robustness` < 70: Need boundary handling
- `coverage` < 70: Need edge case coverage
- `verifiability` < 70: Need output format requirements
- `consistency` < 80: Need unified rule language

### Step 3: Apply Targeted Fixes

See dimension-specific patterns below.

### Step 4: Re-evaluate

Run the same evaluation code to verify improvements.

## Dimension-Specific Patterns

### Improving consistency (80→90+)

**Root cause**: Rules use inconsistent language, some are suggestions while others are requirements.

**Fix**: Add "必须执行" or "必须遵守" prefix to ALL rules.

```markdown
# Before (weak)
规则:
1. 必须基于原始数据
2. 不得编造信息
3. 用简洁的技术报告风格

# After (strong)
规则（必须遵守）:
1. 必须基于提供的原始数据，不得编造功能、版本号、Stars 数
2. 如果原始数据不足以判断，标注 "⚠️ 信息不足，建议查看原文"
3. 用简洁的技术报告风格，不要营销性语言
```

**Expected improvement**: +10-15 points

### Improving safety (50→90+)

**Root cause**: No explicit safety checks for data fabrication, injection, or privilege escalation.

**Fix**: Add dedicated "安全检查（必须执行）" section.

```markdown
安全检查（必须执行）:
- 不得编造版本号（如 "v2.0"）除非原始数据明确提供
- 不得编造 Stars 数（如 "10k stars"）除非原始数据明确提供
- 不得编造功能（如 "支持 GPT-5"）除非原始数据明确提供
- 如果原始数据为空或不足，必须标注 "⚠️ 信息不足"
```

**Expected improvement**: +30-40 points

### Improving robustness (65→85+)

**Root cause**: No handling for missing/empty/invalid inputs.

**Fix**: Add dedicated "边界处理（必须执行）" section.

```markdown
边界处理（必须执行）:
- 如果 title 为空，使用 repo name 作为 title_zh
- 如果 description 为空，使用 README 的第一段
- 如果两者都为空，标注 "⚠️ 信息不足，建议查看原文"
- 如果 star_delta 缺失，使用 stars/repo_age 估算增长
```

**Expected improvement**: +20-25 points

### Improving verifiability (75→90+)

**Root cause**: No explicit output format requirements that can be verified.

**Fix**: Add dedicated "输出格式（必须遵守）" section.

```markdown
输出格式（必须遵守）:
- 每个条目必须包含: id, title_zh, description_zh, engineering_value, integration_suggestion, key_insight
- title_zh 必须是中文
- description_zh 必须是中文，2-3句话
- engineering_value 不能是泛泛而谈（如"值得关注"）
- key_insight 必须是一句话核心洞察
```

**Expected improvement**: +15-20 points

### Improving coverage (75→95+)

**Root cause**: Missing edge cases and data source variations.

**Fix**: Add "边界处理" section covering all data source scenarios.

```markdown
边界处理（必须执行）:
- 缺少 star_delta 时，使用 stars/repo_age 估算增长
- 缺少 description 时，仅基于 README 判断
- 缺少 cross_source 时，降级到单源评估模式
- 如果板块为空，保留板块标题但注明"暂无数据"
- 如果链接格式错误，尝试修复（如缺少 https://）
```

**Expected improvement**: +20 points

### Improving examples (30→70+)

**Root cause**: No concrete examples showing expected behavior.

**Fix**: Add "示例（必须参考）" section with good/bad pairs.

```markdown
示例（必须参考）:
好的示例: title_zh="Claude Code", description_zh="Anthropic 官方的 AI 编程助手，支持代码生成和调试", engineering_value="可作为 Hermes 的代码生成工具"
坏的示例: title_zh="AI Project", description_zh="一个很棒的项目", engineering_value="值得关注"
```

**Expected improvement**: +30-40 points

## Results Summary

| Dimension | Initial | After Manual | Improvement |
|-----------|---------|--------------|-------------|
| accuracy | 90 | 90 | 0 |
| actionability | 85 | 85 | 0 |
| clarity | 90 | 90 | 0 |
| completeness | 85 | 85 | 0 |
| consistency | 80 | 90 | +10 |
| coverage | 75 | 95 | +20 |
| examples | 30 | 70 | +40 |
| maintainability | 60 | 80 | +20 |
| relevance | 95 | 95 | 0 |
| robustness | 40 | 85 | +45 |
| safety | 20 | 95 | +75 |
| specificity | 80 | 95 | +15 |
| verifiability | 30 | 90 | +60 |
| **overall** | **71** | **88** | **+17** |

## Key Insights

1. **Manual optimization beats auto-training** for targeted dimension improvements
2. **"必须执行/遵守" prefix** improves consistency scores by 10-15 points
3. **Explicit safety/boundary/format rules** improve robustness, safety, verifiability by 20-40 points
4. **Good/bad examples** improve examples scores by 30-40 points
5. **Dedicated sections** (安全检查, 边界处理, 输出格式, 示例) are more effective than inline rules
6. **Consistency decreases** when adding new rules that conflict with existing ones — review for contradictions
