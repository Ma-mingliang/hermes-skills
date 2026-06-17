# Agent Daily Report 提示词优化工作流

## 概述

使用 SkillOpt 优化 agent-daily-report 的 9 个提示词。

## 提示词文件位置

```
D:\openclaw-hermes\agent-daily-report-skill\prompts\
├── README.md                           # 说明文档
├── trust_agent_system.txt              # Trust Agent 系统提示词
├── trust_agent_user_template.txt       # Trust Agent 用户模板
├── trust_verify_system.txt             # Trust Agent 验证器
├── enrichment_agent_system.txt         # Enrichment Agent 系统提示词
├── enrichment_agent_user_template.txt  # Enrichment Agent 用户模板
├── enrichment_verify_system.txt        # Enrichment Agent 验证器
├── editor_agent_system.txt             # Editor Agent 系统提示词
├── editor_agent_user_template.txt      # Editor Agent 用户模板
└── editor_verify_system.txt            # Editor Agent 验证器
```

## SkillOpt 配置

### 环境目录
```
D:\openclaw-hermes\SkillOpt\skillopt\envs\agent_daily_report\
├── __init__.py
├── adapter.py
├── dataloader.py
├── rollout.py
├── evaluator.py
└── skills\
    └── initial.md
```

### 配置文件
```
D:\openclaw-hermes\SkillOpt\configs\agent-daily-report\
├── default.yaml
├── prepare_data.py
├── update_prompts.py
├── README.md
└── SUMMARY.md
```

### 训练数据
```
D:\openclaw-hermes\SkillOpt\data\agent-daily-report\
├── training_data.json
├── train\items.json
├── val\items.json
└── test\items.json
```

## 训练流程

### 1. 准备训练数据
```bash
cd D:\openclaw-hermes\SkillOpt
python configs/agent-daily-report/prepare_data.py
```

### 2. 运行训练
```bash
set -a; source .env; set +a
python scripts/train.py --config configs/agent-daily-report/default.yaml
```

### 3. 评估结果
```bash
python scripts/eval_only.py --config configs/agent-daily-report/default.yaml --skill outputs/agent-daily-report/best_skill.md
```

### 4. 应用优化结果
```bash
python configs/agent-daily-report/update_prompts.py --skill outputs/agent-daily-report/best_skill.md --output D:/openclaw-hermes/agent-daily-report-skill/scripts/agent_prompts.py
```

## 评估维度（12 个）

| 维度 | 权重 | 说明 |
|------|------|------|
| relevance | 10% | 与 Agent 生态的相关性 |
| completeness | 10% | 输出的完整性 |
| accuracy | 10% | 信息的准确性 |
| actionability | 10% | 可操作性 |
| specificity | 15% | 提示词是否具体 |
| consistency | 10% | 提示词内部是否一致 |
| coverage | 15% | 是否覆盖所有必要规则 |
| clarity | 10% | 指令是否清晰 |
| dedup_effectiveness | 10% | 去重规则是否有效 |
| scoring_accuracy | 10% | 评分标准是否合理 |
| mcp_validation | 10% | MCP 验证规则是否完善 |
| source_filtering | 10% | 来源过滤规则是否有效 |

## 已知问题

1. **reflect 函数未生成补丁**：LLM 返回的 JSON 可能格式不正确，需要更 robust 的解析
2. **评估分数为 0**：rollout 函数需要集成评估逻辑
3. **训练数据不足**：需要更多样本（建议 10-20 个）

## 下一步改进

1. 改进 reflect 函数的 JSON 解析
2. 添加 fallback 机制
3. 增加训练数据
4. 添加调试信息
