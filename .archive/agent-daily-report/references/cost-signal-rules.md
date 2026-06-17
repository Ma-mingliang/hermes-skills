# Cost Signal Extraction Rules

## 触发条件

以下任一条件满足时，item 应包含 cost_signal 字段：
- primary_category == "Model"
- source == "model_docs"
- title/summary 包含 pricing/price/cache/token/cost/计费/缓存/价格 等关键词

## 字段规范

```json
{
  "cost_signal": {
    "has_pricing": false,
    "has_cache": false,
    "input_price": null,
    "cached_input_price": null,
    "output_price": null,
    "currency": "",
    "unit": "per_million_tokens",
    "context_window": null,
    "rate_limit": null,
    "provider": "",
    "model": "",
    "api_compatibility": {
      "openai_compatible": null,
      "anthropic_compatible": null
    },
    "cost_impact": "lower|higher|neutral|unknown",
    "routing_impact": "recommended|watch|avoid|unknown"
  }
}
```

## 价格提取正则

```python
# 标准格式: $0.25 / 1M tokens 或 $0.25/million
r"\$([\d.]+)\s*/\s*(?:1[mM]|million)"

# 缓存价格: cached input $0.03/1M
r"cached\s*(?:input)?\s*\$([\d.]+)"

# 中文格式: 输入价格 ¥2/百万token
r"(?:输入|output).*?(?:¥|\$)([\d.]+)"
```

## 单位标准化

| 原始 | 标准化 |
|------|--------|
| per 1M tokens | per_million_tokens |
| per million tokens | per_million_tokens |
| per 1000 tokens | per_thousand_tokens |
| per request | per_request |

## cost_impact 判断

- **lower**: cheaper/reduced/降价/免费/free/budget
- **higher**: expensive/increased/涨价/rate limited/pricier
- **neutral**: 有价格但无变化信号
- **unknown**: 无法判断

## routing_impact 判断

- **recommended**: cost_impact=lower 且 provider 已知
- **watch**: 有价格信息但无明确优劣
- **avoid**: cost_impact=higher 或 rate limit 严格
- **unknown**: 无足够信息

## 禁止事项

1. 不得编造价格数值。提取不到时 input_price/output_price = null。
2. 不得假设 currency。没有 $ 或 ¥ 符号时 currency = ""。
3. 不得假设 context_window。没有明确数值时 = null。
4. cost_impact 不得凭空判断为 lower/higher。没有变化信号时 = unknown。
