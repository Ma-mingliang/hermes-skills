# Agent Architecture — 脚本+Agent 协作模式 (已实现 v3.2)

## 核心原则

参考 ai-daily-digest 的"脚本做确定性工作，Agent做创造性工作"模式。

脚本负责: 采集、标准化、去重、分类、评分、质量门控、报告渲染
Agent负责: 信任判断、内容润色、风格编辑

## 当前 Pipeline (v3.2)

```
┌─ 脚本 ─────────────────────────────────────────────────────┐
│ collect → normalize → dedup → classify → score → quality   │
└────────────────────────────────────────────────────────────┘
                    ↓ scored_items.json
┌─ Phase 7a: 导出 candidates.json ────────────────────────────┐
│ data/intermediate/{date}/candidates.json                    │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─ Phase 7b: GitHub Trust Agent (batch_size=1 + 多轮验证) ────┐
│ 输入: GitHub S/A/B + spike/growth 候选                      │
│ 输出: trust-decisions.json → apply → re-score              │
│ 无LLM: 跳过                                                │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─ Phase 7c: Select ──────────────────────────────────────────┐
│ selected_items = S/A/B → select_report_items               │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─ Phase 7d: Item Enrichment Agent (batch_size=1 + 多轮验证) ─┐
│ 输入: selected items 完整数据                               │
│ 输出: enriched-decisions.json → merge 回 items             │
│ 无LLM: 离线模板 (enrich_report_with_agent)                 │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─ Phase 7e: generate_report → draft.md ──────────────────────┐
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─ Phase 7f: Editor Agent (多轮验证) ─────────────────────────┐
│ 输入: draft.md + source_status + low_signal                │
│ 输出: final report.md                                      │
│ 无LLM: 纯规则 (去重+链接检查+格式)                         │
└─────────────────────────────────────────────────────────────┘
```

## 参考案例借鉴

| 案例 | 借鉴什么 | 用在哪里 |
|------|---------|---------|
| agents-radar (780⭐) | LLM 过滤非 AI 项目 | Trust Agent 判断逻辑 |
| ai-news-agent (2⭐) | candidate→decision JSON | Enrichment Agent I/O 模式 |
| ai-news-radar (843⭐) | 无 LLM 也能跑 | Editor Agent 降级策略 |

## 实现文件

| 文件 | 职责 |
|------|------|
| scripts/agent_pipeline.py | 管道控制器 + 3 个 Agent 逻辑 + _verify_and_retry |
| scripts/agent_llm_client.py | AgentLLMClient (call_json/call_text) |
| scripts/agent_prompts.py | 6 个 prompt (3 agent + 3 verify) |

## 多轮验证机制

```python
_verify_and_retry_json(client, system, verify_system, user, verify_prompt_fn, verify_args_fn, max_rounds=2)
```

Round 1: Agent 执行 → 输出
Round 2: 验证器检查 → valid? 接受 : 带修正反馈重跑

每个 Agent 有独立验证 prompt:
- TRUST_VERIFY_SYSTEM: 检查 decision/score 一致性、reason 质量
- ENRICHMENT_VERIFY_SYSTEM: 检查中文质量、不编造数据
- EDITOR_VERIFY_SYSTEM: 检查 Source Status 存在、不新增条目

## batch_size=1 策略

用户明确要求"不必在意用时"，选择质量优先：
- batch=1: 每个 item 独立 LLM 调用，全部注意力
- 验证失败只重跑 1 个 item
- 每天 ~50 次 LLM 调用，MiMo Token Plan 成本可控

## 配置

```yaml
agent_pipeline:
  enabled: true
  llm:
    api_key_env: AGENT_PIPELINE_API_KEY
    base_url_env: AGENT_PIPELINE_BASE_URL
    default_model: mimo-v2.5-pro
    temperature: 0.2
    max_retries: 3
```

## 与 ai-daily-digest 的区别

| 维度 | ai-daily-digest | agent-daily-report (v3.2) |
|------|----------------|--------------------------|
| Agent 介入点 | Step 5 (整块报告撰写) | 3个精确节点 |
| Agent 职责 | 全部创造性工作 | 只做判断/润色/补充 |
| 验证 | 无 | 每个 Agent 多轮自验证 |
| 降级 | 需要 LLM | 无 LLM 也能跑 |
| 中间产物 | 无 | 5 个 JSON/MD 文件可审查 |
| batch_size | N/A | 1 (质量优先) |
