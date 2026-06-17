# Enrichment 配置最佳实践

## 问题

2026-06-04 实测：42个条目中只有12个走 LLM enrichment，30个走离线模板（全是同一句话）。

## 根因

`item_enrichment.max_items=12` 限制了 LLM 处理数量。

## 推荐配置

```yaml
agent_pipeline:
  agents:
    item_enrichment:
      enabled: true
      batch_size: 1       # 逐条 LLM 最高质量
      max_items: 0         # 0=不限制，全部走 LLM
      max_retries: 3       # SSL 错误重试
      timeout_seconds: 60
```

## batch_size 选择

| batch_size | 质量 | 速度 | 推荐 |
|-----------|------|------|------|
| 1 | 最高 | 42条约3-5分钟 | **推荐** |
| 3 | 中等 | 42条约1-2分钟 | 可接受 |
| 5 | 较低 | 42条约1分钟 | 不推荐 |

## 金融新闻过滤

negative_kws 中添加金融关键词，但**不要用过于宽泛的词**：

```python
# ✅ 正确：精确匹配
"美股异动", "市值暴涨", "IPO出现波折", "私人信贷", "桥水基金", "Pimco"

# ❌ 错误：过于宽泛，会误杀
"收购", "估值", "融资"  # "英伟达收购 Kumo AI" 会被误杀
```

## SSL 错误

MiMo Token Plan API 间歇性 SSL 问题（SSLEOFError）。
解决方案：增加 `max_retries: 3`，或接受偶发失败（约5%条目）。
