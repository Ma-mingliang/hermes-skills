# SkillOpt - Skill 文档优化工具

## 概述
Microsoft 出品的 Skill 文档优化工具（⭐4619），通过迭代训练优化自然语言 skill 文档。

## 安装信息
- 仓库：`D:\openclaw-hermes\SkillOpt`
- PyPI 包：`skillopt 0.1.0`
- 许可证：MIT

## CLI 命令
- `skillopt-train` — 训练优化 skill
- `skillopt-eval` — 评估 skill 效果

## 配置（使用 mimo v2.5 pro）
已配置 `.env` 文件：
```bash
export AZURE_OPENAI_ENDPOINT=https://token-plan-sgp.xiaomimimo.com/v1
export AZURE_OPENAI_API_KEY=<MIMO_API_KEY>
export AZURE_OPENAI_AUTH_MODE=openai_compatible
```

## 核心概念
- 模型权重 → Skill 文档（Markdown）
- 前向传播 → Rollout（目标执行任务）
- 损失/梯度 → Reflect（优化器生成编辑补丁）
- SGD 步骤 → 应用补丁到 skill

## 性能提升（基于 GPT-5.5）
- 直接聊天：+23.5 分
- Codex CLI：+24.8 分
- Claude Code：+19.1 分

## 优化 agent-daily-report prompts
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

## 注意事项
- SkillOpt 只优化自然语言的 skill 文档（Markdown），不优化代码
- 使用 `AZURE_OPENAI_*` 环境变量名，即使是 OpenAI-compatible 模式
- 训练数据需要高质量，建议至少 100 个样本
