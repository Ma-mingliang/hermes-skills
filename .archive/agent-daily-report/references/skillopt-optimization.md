# SkillOpt 提示词优化工作流

## 概述

使用 Microsoft SkillOpt 优化 agent-daily-report 的 9 个 Agent 提示词。

## 文件位置

```
D:\openclaw-hermes\SkillOpt\
├── configs\agent-daily-report\
│   ├── default.yaml          # SkillOpt 配置
│   ├── prepare_data.py       # 数据准备脚本
│   ├── update_prompts.py     # 更新提示词脚本
│   └── README.md             # 使用说明
├── skillopt\envs\agent-daily-report\
│   └── skills\initial.md    # 初始 skill 文件
└── data\agent-daily-report\ # 训练数据目录
```

## 提示词文件

```
D:\openclaw-hermes\agent-daily-report-skill\prompts\
├── trust_agent_system.txt
├── trust_agent_user_template.txt
├── trust_verify_system.txt
├── enrichment_agent_system.txt
├── enrichment_agent_user_template.txt
├── enrichment_verify_system.txt
├── editor_agent_system.txt
├── editor_agent_user_template.txt
└── editor_verify_system.txt
```

## 使用流程

```bash
cd D:\openclaw-hermes\SkillOpt

# 1. 准备训练数据
python configs/agent-daily-report/prepare_data.py

# 2. 运行训练
skillopt-train --config configs/agent-daily-report/default.yaml

# 3. 评估结果
skillopt-eval --config configs/agent-daily-report/default.yaml --skill outputs/agent-daily-report/best_skill.md

# 4. 应用优化结果
python configs/agent-daily-report/update_prompts.py --skill outputs/agent-daily-report/best_skill.md --output D:/openclaw-hermes/agent-daily-report-skill/scripts/agent_prompts.py
```

## 配置

- optimizer: mimo-v2.5-pro
- target: mimo-v2.5-pro
- num_epochs: 4
- train_size: 100
- batch_size: 10
- learning_rate: 3

## 优化目标

| Agent | 优化目标 |
|-------|----------|
| Trust Agent | 提高项目评估准确率 10-20% |
| Enrichment Agent | 提高中文摘要质量 15-25% |
| Editor Agent | 提高报告润色效果 10-15% |

## 限制

- SkillOpt 优化自然语言提示词，不优化代码
- 需要高质量训练数据（建议 100+ 样本）
- 训练过程可能需要数小时
- 使用 mimo-v2.5-pro 可降低成本
