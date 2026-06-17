# Agent Pipeline Implementation Reference (v3.2)

## 文件结构

```
scripts/
  agent_pipeline.py         # 管道控制器 (~400 行)
  agent_llm_client.py       # LLM 客户端 (~130 行)
  agent_prompts.py          # prompt 模板 (~220 行)
  enrich_report_with_agent.py # 离线降级模板 (已有)
```

## 核心函数

### agent_pipeline.py

```python
def run_agent_pipeline(scored, config, report_date, source_statuses, low_signal, logger, base_dir, write_state):
    """主入口。返回 (scored, selected_items, report_md)"""
    # Phase 7a: export candidates.json
    # Phase 7b: run_trust_agent() → apply_trust_decisions()
    # Phase 7c: select_report_items()
    # Phase 7d: run_enrichment_agent() → merge_enriched()
    # Phase 7e: generate_report() → draft.md
    # Phase 7f: run_editor_agent() → final.md

def _verify_and_retry_json(client, system_prompt, verify_system, user_prompt, verify_prompt_fn, verify_args_fn, max_rounds=2, logger=None):
    """通用多轮验证包装器。Round 1: 执行, Round 2+: 验证→修正→重执行"""

def _verify_and_retry_text(client, system_prompt, verify_system, user_prompt, verify_prompt_fn, verify_args_fn, max_rounds=2, logger=None):
    """文本模式多轮验证（用于 Editor Agent）"""
```

### agent_llm_client.py

```python
class AgentLLMClient:
    def __init__(self, llm_config):  # 从 config.yaml 读取 api_key_env, base_url_env, default_model
    def is_configured(self) -> bool:  # 检查 API key 是否设置
    def call_json(self, system_prompt, user_prompt, model=None, temperature=None) -> Dict:  # JSON 响应
    def call_text(self, system_prompt, user_prompt, model=None, temperature=None) -> str:  # 文本响应
```

## LLM 调用链路

```
config.yaml agent_pipeline.llm
    → AgentLLMClient(config)
    → 读取 env: AGENT_PIPELINE_API_KEY, AGENT_PIPELINE_BASE_URL
    → HTTP POST {base_url}/chat/completions
    → response_format: json_object (for call_json)
```

## 验证器 prompt 结构

每个验证器输出 JSON: `{"valid": bool, "issues": [...], "corrections": [...]}`

- TRUST_VERIFY_SYSTEM: 检查 decision/score 一致性、reason 有实质、无遗漏
- ENRICHMENT_VERIFY_SYSTEM: 检查 title_zh 是中文、不编造数据、不泛泛
- EDITOR_VERIFY_SYSTEM: 检查 Source Status 表存在、不新增条目、不修改数值

## 降级路径

```
LLM configured?
  ├── Yes → Agent 执行 → 验证 → 通过/重试
  └── No → Trust: skip, Enrichment: offline_template, Editor: rules_fallback
```

## 调用量估算 (batch_size=1)

| Agent | items | rounds | 调用次数 |
|-------|-------|--------|---------|
| Trust | ~12 | 2 | ~24 |
| Enrichment | ~12 | 2 | ~24 |
| Editor | 1 | 2 | ~2 |
| **合计** | | | **~50/天** |

## 已知 Pitfalls

- P43: low_signal 必须在 agent pipeline 入口处计算
- P44: enrich_report_with_agent 必须 lazy import
- P45: --dry-run 时不写 intermediate 文件
- P46: 完整 pipeline 超过 5 分钟，必须用后台执行
- P48: enabled=true 但 LLM 未配置时静默降级
- P49: yaml.dump() 破坏 config.yaml 注释
