# Agent Pipeline 限制条件详解

## 执行时间限制

| 组件 | 超时时间 | 说明 |
|------|----------|------|
| 整体 pipeline | 5-15 分钟 | 需后台执行（run_pipeline.py --background） |
| LLM 调用 | 180 秒 | max_retries: 3 |
| Source Verification | 20 秒 | max_items: 45 |
| Trust Agent | 120 秒 | max_items: 30 |
| Enrichment Agent | 60 秒 | batch_size: 1 |
| Editor Agent | 60 秒 | max_input: 30000 字符 |

## Trust Agent 限制

- max_items: 30（最多处理 30 个项目）
- batch_size: 5（每批 5 个项目）
- timeout_seconds: 120（2 分钟超时）
- trust_threshold_keep: 60（>= 60 保留）
- trust_threshold_demote: 30（30-60 降级，< 30 删除）

评分标准：
```
90-100: 官方发布、重大版本更新、多源确认
70-89:  确认与 Agent 生态相关、增长合理
50-69:  可能相关但证据不足
30-49:  与 Agent 生态关系弱
0-29:   与 Agent 生态无关
```

## Enrichment Agent 限制

- batch_size: 1（每个项目独立一次 LLM 调用，P77 确认）
- max_items: 0（不限制，P76 修复）
- timeout_seconds: 60（1 分钟超时）
- 输出字段: title_zh、description_zh、engineering_value、integration_suggestion、key_insight

## Editor Agent 限制

- max_input_chars: 30000（最大输入 30000 字符）
- segmented_enabled: true（启用分段处理）
- segment_max_chars: 12000（每段最大 12000 字符）
- segment_max_segments: 30（最多 30 段）
- fallback_to_rules: true（LLM 失败时用纯规则）

禁止项：
- 不得新增未经数据验证的信息
- 不得修改 Stars/评分等数值
- 不得删除 Source Status 表
- 不得删除"数据来源""上榜原因""页面确认""确认摘要""用途与最佳实践""工程价值""集成建议"

## 验证限制

所有 Agent: 最多 2 轮验证（max_rounds=2）

| Agent | 验证内容 |
|-------|----------|
| Trust | decision 与 score 一致性、reason 有实质、无遗漏 |
| Enrichment | title_zh 是中文、不编造数据、engineering_value 不泛泛 |
| Editor | Source Status 表存在、不新增条目、不修改数值 |

## LLM 配置

- default_model: mimo-v2.5-pro
- temperature: 0.2
- max_retries: 3
- timeout_seconds: 180

## 降级策略

| Agent | 有 LLM | 无 LLM |
|-------|--------|--------|
| Trust | LLM 评估 trust_score | 跳过，保留原评分 |
| Enrichment | LLM 生成中文摘要 | 离线模板 |
| Editor | LLM 润色报告 | 纯规则 |
