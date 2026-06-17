# Agent Daily Report 提示词管理

## 概述
agent-daily-report 系统中所有 Agent 节点的提示词已抽离到独立文件，方便逐步修改和 SkillOpt 优化。

## 文件位置
```
D:\openclaw-hermes\agent-daily-report-skill\prompts\
├── README.md                           - 说明文档
├── trust_agent_system.txt              - Trust Agent 系统提示词
├── trust_agent_user_template.txt       - Trust Agent 用户模板
├── trust_verify_system.txt             - Trust Agent 验证器
├── enrichment_agent_system.txt         - Enrichment Agent 系统提示词
├── enrichment_agent_user_template.txt  - Enrichment Agent 用户模板
├── enrichment_verify_system.txt        - Enrichment Agent 验证器
├── editor_agent_system.txt             - Editor Agent 系统提示词
├── editor_agent_user_template.txt      - Editor Agent 用户模板
└── editor_verify_system.txt            - Editor Agent 验证器
```

## 9 个提示词

### Trust Agent（信任评估器）
- 评估 GitHub 项目的真实价值和可信度
- 评分标准：0-100，decision: keep/demote/drop
- 输出 JSON 数组

### Enrichment Agent（条目精修器）
- 生成中文摘要和工程价值判断
- 输出字段：title_zh, description_zh, engineering_value, integration_suggestion, key_insight

### Editor Agent（编辑器）
- 对日报初稿进行最终润色
- 检查：板块顺序、去重、语言风格、链接格式、数据来源保留

## SkillOpt 优化
配置文件：`D:\openclaw-hermes\SkillOpt\configs\agent-daily-report\`

使用流程：
```bash
cd D:\openclaw-hermes\SkillOpt

# 1. 准备训练数据
python configs/agent-daily-report/prepare_data.py

# 2. 运行训练
skillopt-train --config configs/agent-daily-report/default.yaml

# 3. 评估结果
skillopt-eval --config configs/agent-daily-report/default.yaml --skill outputs/agent-daily-report/best_skill.md

# 4. 应用优化
python configs/agent-daily-report/update_prompts.py --skill outputs/agent-daily-report/best_skill.md --output D:/openclaw-hermes/agent-daily-report-skill/scripts/agent_prompts.py
```

## 修改流程
1. 编辑对应的 `.txt` 文件
2. 运行 `python main.py --dry-run` 测试
3. 将修改更新到 `scripts/agent_prompts.py`
4. 提交变更
