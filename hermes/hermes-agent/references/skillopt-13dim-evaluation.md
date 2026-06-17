# SkillOpt 13 维评估 + 手动调优指南

## 13 维评估（3 串行 prompt，2026-06-04 验证通过）

MiMo v2.5 Pro 可以可靠处理 13 维评估，只要拆分成 3 个串行 prompt。

### Prompt 1：核心维度（4 个）
| 维度 | 权重 | 评估内容 |
|------|------|----------|
| relevance | 15% | 是否与任务相关 |
| completeness | 15% | 是否覆盖所有必要规则 |
| accuracy | 15% | 信息是否正确 |
| specificity | 15% | 是否有具体数值阈值 |

### Prompt 2：执行维度（4 个）
| 维度 | 权重 | 评估内容 |
|------|------|----------|
| actionability | 10% | 是否可执行 |
| clarity | 10% | 是否清晰易懂 |
| coverage | 10% | 是否覆盖多个方面 |
| consistency | 10% | 是否前后一致 |

### Prompt 3：质量维度（5 个）
| 维度 | 权重 | 评估内容 |
|------|------|----------|
| robustness | 10% | 边界情况处理能力 |
| verifiability | 10% | 是否包含验证规则 |
| examples | 5% | 是否有好的示例 |
| safety | 5% | 是否有安全检查 |
| maintainability | 5% | 是否易于维护 |

### 实现要点

```python
def _eval_prompt_1(skill_md: str) -> dict:
    system = "你是评估器。只评估以下4个维度，每项 0-100 分。输出JSON。"
    user = f"评估：relevance, completeness, accuracy, specificity\n\n{skill_md[:1000]}"
    return _call_llm(system, user, max_tokens=512)

def _retry_call(fn, *args, max_retries=2):
    for attempt in range(max_retries + 1):
        result = fn(*args)
        parsed = _parse_json_response(result)
        if parsed is not None:
            return parsed
    return None

def _weighted_score(dim_scores: dict) -> float:
    weights = {"relevance": 0.15, "completeness": 0.15, "accuracy": 0.15, "specificity": 0.15,
               "actionability": 0.10, "clarity": 0.10, "coverage": 0.10, "consistency": 0.10,
               "robustness": 0.10, "verifiability": 0.10, "examples": 0.05,
               "safety": 0.05, "maintainability": 0.05}
    total = sum(dim_scores.get(d, 50) * w for d, w in weights.items())
    weight_used = sum(w for d, w in weights.items() if d in dim_scores)
    return round(total / weight_used, 1) if weight_used > 0 else 50.0
```

## 手动调优策略

### 过度优化陷阱
一次性修改太多维度会导致分数下降。原因：
1. 新增规则可能与原有规则冲突（consistency 下降）
2. 过于复杂的 skill 会让 LLM 困惑（clarity 下降）
3. 评估器对微小变化敏感（±2-3 分波动）

### 正确的调优流程
1. **识别最低分维度**：找出 <80 的维度
2. **最小改动**：只改 1-2 个维度，不碰高分维度
3. **验证**：运行评估确认分数没降
4. **重复**：如果还有低分维度，继续

### 调优示例

**初始分数**：82 分
- 低分：examples(30), safety(50), verifiability(70)

**第一次调优**（针对性）：
- 增加示例 → examples +20
- 增加安全检查 → safety +40
- 增加验证规则 → verifiability +20
- 结果：87 分

**第二次调优**（微调）：
- 统一"必须"表述 → consistency +10
- 增加更多示例 → examples +10
- 结果：88 分

**第三次调优**（过度）：
- 重写整个 skill → 所有维度下降
- 结果：72 分 ❌

### 评估非确定性
LLM 评估分数在 ±2-3 分范围内波动。使用多次评估取平均值：
```python
scores = [evaluate_skill(skill) for _ in range(3)]
avg = sum(s['overall'] for s in scores) / len(scores)
```

## MiMo API 配置

### Endpoint 选择
- **SGP（推荐）**：`https://token-plan-sgp.xiaomimimo.com/v1` — 现有 API key 有效
- **主站**：`https://api.xiaomimimo.com/v1` — 需要不同的 API key

### Timeout 配置
**关键 Pitfall**：`timeout_seconds: 0` 会导致 "Attempted to set connect timeout to 0" 错误，所有 RSS 源全部失败。

修复：所有 timeout 设置为 60 秒：
```yaml
rss_feeds:
  request:
    timeout_seconds: 60
agent_pipeline:
  llm:
    timeout_seconds: 60
agent_enrichment:
  provider:
    timeout_seconds: 60
```

### Rate Limiting
MiMo API 有速率限制（429 错误）。系统有自动重试机制：
- 等待 5 秒后重试
- 最多重试 4 次
- 失败后使用 offline fallback

## 相关文件

- SkillOpt 仓库：`D:\openclaw-hermes\SkillOpt`
- 日报系统：`D:\openclaw-hermes\agent-daily-report-skill`
- 评估器代码：`D:\openclaw-hermes\SkillOpt\skillopt\envs\agent_daily_report\evaluator.py`
- Rollout 代码：`D:\openclaw-hermes\SkillOpt\skillopt\envs\agent_daily_report\rollout.py`
