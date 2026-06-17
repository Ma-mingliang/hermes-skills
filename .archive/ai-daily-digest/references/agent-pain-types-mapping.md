# Agent问题类型映射表

> 每个已知Agent的问题类型和痛点描述（按9种问题类型框架）

## 9种问题类型

| 类型 | 说明 |
|------|------|
| 能力缺失型 | AI可以解决但没有好的使用方案 |
| 使用不便型 | 人使用AI时的不便之处 |
| 成本过高型 | API/部署成本不可控 |
| 安全风险型 | AI行为不可控 |
| 效率低下型 | AI工作流程繁琐 |
| 知识壁垒型 | 不知道怎么用AI |
| 协作困难型 | 多Agent/多人协作不便 |
| 数据孤岛型 | Agent间数据不互通 |
| 行业落地型 | AI技术难以落地到具体行业 |

## 已验证映射

```python
AGENT_PAIN_TYPES = {
    "anomalyco/opencode": ("成本过高型", "Claude Code/Codex付费门槛高（$3~15/M），开源开发者无法使用编码Agent"),
    "anthropics/claude-code": ("能力缺失型", "AI能写代码，但缺乏深度推理能力，无法处理复杂架构设计和多文件重构"),
    "google-gemini/gemini-cli": ("使用不便型", "Google生态缺乏CLI入口，开发者需要在浏览器中操作Agent，无法在终端中直接使用"),
    "openai/codex": ("能力缺失型", "OpenAI缺乏专用编码Agent，ChatGPT无法直接执行代码和操作文件系统"),
    "zhayujie/CowAgent": ("效率低下型", "Agent每次对话从零开始，缺乏任务分解+记忆管理+多Agent协作，复杂任务需要人工拆分"),
    "AstrBotDevs/AstrBot": ("使用不便型", "AI Agent分散在不同平台（微信/Discord/Telegram），需要逐个配置，缺乏统一管理界面"),
    "TauricResearch/TradingAgents": ("行业落地型", "AI技术难以落地到金融领域，传统量化工具缺乏市场理解能力，无法处理非结构化数据"),
    "eosphoros-ai/DB-GPT": ("知识壁垒型", "非技术人员无法使用数据库，需要学习SQL语言，知识壁垒高"),
    "HolmesGPT/holmesgpt": ("效率低下型", "SRE需要手动分析告警和日志，工作流程繁琐，问题定位耗时长"),
    "karpathy/autoresearch": ("效率低下型", "科研流程繁琐，文献调研+实验设计+论文写作耗时"),
}
```

## CowAgent核心功能
- 任务分解：将复杂任务拆分为子任务
- 记忆管理：跨会话记忆，记住上下文
- 多Agent协作：多个Agent协同工作
- 持续学习：从执行中学习优化

## AstrBot核心功能
- 多渠道接入：支持微信/Discord/Telegram等
- 插件系统：功能按需扩展
- 中文优化：针对中文用户优化
- WebUI：可视化管理界面

## 使用方法

在生成报告时：
1. 先查AGENT_PAIN_TYPES获取问题类型和描述
2. 如果没有对应条目，根据9种问题类型框架判断
3. 不能用"缺乏XXX"的市场空白描述
