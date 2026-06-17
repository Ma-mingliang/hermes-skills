# 9种问题类型框架 — Agent/Skills痛点描述

## 框架定义

每个Agent/Skills/组件的描述，都必须解释：这是为了解决AI服务于人类过程中遇到的什么问题。

| 问题类型 | 说明 | 示例 |
|----------|------|------|
| 能力缺失型 | AI可以解决但没有好的使用方案 | AI能写代码但没有好的编码Agent → Claude Code |
| 使用不便型 | 人使用AI时的不便之处 | Token消耗太高 → caveman/OpenSquilla |
| 成本过高型 | API/部署成本不可控 | Claude Code $200太贵 → deepclaude降本99% |
| 安全风险型 | AI行为不可控 | Agent删除文件 → AiSOC安全运营 |
| 效率低下型 | AI工作流程繁琐 | 手动配置Harness → VAEN打包复用 |
| 知识壁垒型 | 不知道怎么用AI | 新手不会配置 → karpathy-skills |
| 协作困难型 | 多Agent/多人协作不便 | 调试Agent只能单人 → Multiplayer Debug |
| 数据孤岛型 | Agent间数据不互通 | 文件系统不统一 → Mirage虚拟文件系统 |
| 行业落地型 | AI技术难以落地到具体行业 | 医学诊断AI化 → 临床辅助Agent |

## 已验证的Agent痛点映射

| Agent | 问题类型 | 痛点描述 |
|-------|---------|---------|
| OpenCode | 成本过高型 | Claude Code/Codex付费门槛高（$3~15/M），开源开发者无法使用编码Agent |
| Claude Code | 能力缺失型 | AI能写代码，但缺乏深度推理能力，无法处理复杂架构设计和多文件重构 |
| Gemini CLI | 使用不便型 | Google生态缺乏CLI入口，开发者需要在浏览器中操作Agent，无法在终端中直接使用 |
| Codex | 能力缺失型 | OpenAI缺乏专用编码Agent，ChatGPT无法直接执行代码和操作文件系统 |
| CowAgent | 效率低下型 | Agent每次对话从零开始，缺乏任务分解+记忆管理+多Agent协作，复杂任务需要人工拆分 |
| AstrBot | 使用不便型 | AI Agent分散在不同平台（微信/Discord/Telegram），需要逐个配置，缺乏统一管理界面 |
| TradingAgents | 行业落地型 | AI技术难以落地到金融领域，传统量化工具缺乏市场理解能力，无法处理非结构化数据 |
| DB-GPT | 知识壁垒型 | 非技术人员无法使用数据库，需要学习SQL语言，知识壁垒高 |
| HolmesGPT | 效率低下型 | SRE需要手动分析告警和日志，工作流程繁琐，问题定位耗时长 |
| AutoResearch | 效率低下型 | 科研流程繁琐，文献调研+实验设计+论文写作耗时 |

## 描述规则

1. **禁止使用"缺乏XXX"作为痛点描述** — 这是市场空白描述，不是问题类型描述
2. **必须先判断问题类型** — 再用该类型的描述方式来写痛点
3. **必须说明Agent的核心功能** — 不能只写"Agent缺乏XXX"，要写"Agent的核心功能是XXX，解决了YYY问题"
4. **CowAgent/AstrBot等必须有具体核心功能描述** — 不能泛泛而谈
