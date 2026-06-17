# MiMo 空响应修复方案

## 根本原因

MiMo v2.5 默认开启 thinking 模式，导致：
- 响应被存到 `reasoning_content` 而非 `content`
- 非流式响应：`choices[0].message.content` 为空
- 流式响应：`delta.content` 为空，`delta.reasoning_content` 有内容

## 解决方案

### 1. 请求参数：禁用 thinking

```python
payload = {
    "model": "mimo-v2.5-pro",
    "messages": [...],
    "thinking": {"type": "disabled"},  # 关键！
    "max_completion_tokens": 4096,
}
```

### 2. 非流式响应解析：fallback 链

```python
message = response.choices[0].message
content = message.content or ""
if not content:
    content = getattr(message, "reasoning_content", "") or ""
if not content:
    content = getattr(message, "reasoning", "") or ""
```

### 3. 流式响应解析：fallback 链

```python
# 在流式循环中
delta = chunk.choices[0].delta
if delta.content:
    content_parts.append(delta.content)
elif getattr(delta, "reasoning_content", None):
    content_parts.append(delta.reasoning_content)
elif getattr(delta, "reasoning", None):
    content_parts.append(delta.reasoning)
```

## Provider Profile 配置

参考 DeepSeek provider profile，创建 Xiaomi provider profile：

```python
class XiaomiProviderProfile(ProviderProfile):
    def build_api_kwargs_extras(self, *, reasoning_config=None, model=None, **context):
        extra_body = {}
        top_level = {}
        
        # 默认禁用 thinking
        enabled = False
        if isinstance(reasoning_config, dict) and reasoning_config.get("enabled") is True:
            enabled = True
        
        extra_body["thinking"] = {"type": "enabled" if enabled else "disabled"}
        return extra_body, top_level
```

**Provider Aliases**: `xiaomi`, `mimo`, `xiaomi-mimo`, `xiaomi-token-plan`

## SkillOpt 集成

在 `rollout.py` 的 `_call_llm` 函数中添加：

```python
payload = {
    "model": "mimo-v2.5-pro",
    "messages": [...],
    "thinking": {"type": "disabled"},  # 关键！
    "max_completion_tokens": 4096,
}
```

**评估函数 fallback**: 当 LLM 评估返回空时，使用规则评估：
- 数值阈值数量（star>=100 等）
- 操作规则数量（必须、不得、禁止等）
- section 数量
- 示例数量
- 长度奖励/惩罚

## 测试结果 (2026-06-04 验证)

```
✓ 你好 → "你好！很高兴见到你！😊 ..."
✓ 1+1= → "2"
✓ 输出数字: 42 → "42"
✓ 评分JSON → {"score": 10, "reason": "..."}
✓ LLM评估 → JSON解析成功, overall: 74
```

## 相关参考

- DeepSeek provider profile: `hermes-home/plugins/model-providers/deepseek/__init__.py`
- Kimi provider profile: 类似模式，使用 `reasoning_effort` 参数
- SkillOpt 集成: `references/skillopt-integration.md`
