---
name: ai-daily-digest-balanced
description: "AI日报折中版规则（5-8K字符）。压缩版见SKILL.md，完整版见SKILL-full.md。"
version: "5.2.0-balanced"
---

# AI Daily Digest — 折中版规则

## 分类铁律（完整版）

**判断流程**（2026-05-30修正）：
```
Step 1: 描述含"skill(s)" → 📚 Skills
Step 2: 主要是.md文件（.md > .py） → 📚 Skills
Step 3: 描述含"mcp server"/"model context protocol" → 🔌 MCP（优先MCP板块，不放组件）
Step 4: 描述含"for ai agents"/"for claude"/"let ai agents" → 🧩 Agent组件
Step 5: 描述含"ai agent"/"agent for"/能独立执行任务 → 🤖 Agent
Step 6: 以上都不满足 → 🧩 Agent组件
```

**关键区别**：
- **Agent**：用AI帮你做事（写代码、回答问题、执行任务）
- **组件**：帮你管理AI服务，或给Agent提供基础设施（runtime/框架/SDK）
- **MCP**：Agent的工具接口，优先放MCP板块
- **CLI不是判定标准**：Agent和组件都可能有CLI
- **"能独立运行"≠Agent**：runtime/框架是组件不是Agent
- **"for agents"是关键信号**：说明是给Agent用的基础设施

**全能Agent** = 通用平台（Claude Code/Cursor/OpenHands/Hermes/OpenClaw）— 很少！
**专精Agent** = 垂直领域（DB-GPT=数据/HolmesGPT=SRE/html-anything=设计）
**有API ≠ 全能！"平台" ≠ 全能！**

**误判案例**：ARIS→Skills(不是Agent)、mcp-context-forge→组件(不是Agent)、html-anything→专精Agent(不是全能)

## 描述原则

通俗易懂，解释解决AI服务人类的什么问题。不限于：能力缺失型/使用不便型/成本过高型/安全风险型/效率低下型/知识壁垒型/协作困难型/数据孤岛型/行业落地型

## 报告结构

```
一、Agent生态
   全能型Agent（📌使用指南 + 🆕新出现+前辈对比 + ⭐高星）
   专精型Agent（🆕新出现+前辈对比 + ⭐高星）
   🧩 Agent组件（🆕新组件+说明解决哪些Agent问题 + ⭐高星组件）

二、Skills市场（⭐高星 + 🆕新Skills按6类分，每类含前辈对比）
   第一类：减少token | 第二类：约束行为 | 第三类：增加功能
   第四类：科研辅助 | 第五类：检测正常工作 | 第六类：补充类

三、📊 模型动态（三层：官网/排名/调用）
四、📰 行业热点 + 🏭 行业应用（至少3个行业，不限GitHub）
五、🔌 MCP动态
六、📊 数据面板（HN/GitHub/分类/API统计）
七、🔮 核心信号（3-7条：趋势/安全/生态/模型/市场/行业）
```

## 前辈对比（Agent和Skills都必须！）

每个新Agent/Skill必须找前辈对比：相似/不同/解决什么问题/原理差别
对比表列：功能、成本、自主性⭐、易用性⭐、适用场景

## 📝 Agent描述示例（Nanobot）

```
🆕 Nanobot — 超轻量级AI Agent
- **Stars**: ⭐ 43,332
- **定位**: OpenClaw精神续作，极简主义AI Agent
- **GitHub**: https://github.com/HKUDS/nanobot

**应用领域**：
1. 个人助理：日程管理、信息整理、任务提醒
2. 开发辅助：代码生成、调试、文档编写
3. 内容创作：写作、翻译、摘要
4. 数据分析：数据清洗、可视化、报告生成
5. 自动化工作流：定时任务、多系统集成

**核心功能**：
- 多渠道聊天：支持微信、Discord、Telegram等
- 记忆系统：跨会话记忆，个性化服务
- MCP协议：标准化工具连接
- 插件扩展：功能按需加载
- WebUI：可视化管理界面

**技术原理**：
- 精简核心：只保留Agent循环核心（~1000行代码）
- 模块化设计：功能通过插件扩展
- 标准协议：支持MCP，兼容主流工具
- 轻量部署：Python 3.11+，pip一键安装

**与OpenClaw对比**：
| 维度 | OpenClaw | Nanobot |
|------|----------|---------|
| 复杂度 | 中等 | 极简 |
| 安装 | 复杂 | pip install |
| 资源占用 | 中等 | 极低 |
| 扩展性 | 中等 | 高（插件） |

**Nanobot解决的问题**：
1. OpenClaw安装复杂 → 一键安装
2. OpenClaw资源占用高 → 超轻量设计
3. OpenClaw扩展困难 → 插件系统
4. 缺乏WebUI → 内置可视化界面
```

## 📊 微信推送分段格式

**分段结构**：
```
[1] Agent生态：📌使用指南 + 🆕新全能Agent对比（含五星评分对比表） + ⭐高星全能Agent
[2] Agent生态续：🆕新专精Agent对比 + ⭐高星专精Agent
[3] Skills市场：⭐高星Skills + 🆕新Skills第1-2类（含前辈对比）
[4] Skills续：第3-6类（含前辈对比）
[5] 🧩Agent组件（在Agent生态下面）：🆕新组件（说明解决哪些Agent的问题） + ⭐高星组件
[6] 📊模型动态：三层监控（官网/排名/调用）
[7] 🔌MCP + 📰行业热点 + 📊行业应用
[8] 数据面板 + 🔮核心信号
```

**对比表列**：功能、成本、自主性(⭐评分)、易用性(⭐评分)、适用场景

## 工作流程

- 102源（source_registry.yaml），全部必须访问
- 00:00-06:00 持续访问：GitHub API每小时≤60次，循环执行
- 其他源穿插在GitHub等待间隙
- 06:30 推送微信
- 限流时等待后重试，不放弃
- Python urllib是唯一可靠API方式（WSL不可用）
- 不要用delegate_task（会编造数据）

**数据采集分阶段执行**（避免5分钟超时）：
```
Phase 1（00:00-02:00）：API源（HN/GitHub）→ 保存到phase1.json
Phase 2（02:00-04:00）：RSS源+网页源 → 保存到phase2.json
Phase 3（04:00-06:00）：解析+生成报告 → 保存到report.md
每个Phase不超过4分钟
```

## 模型监控

- 三层：官网(Claude/GPT/Gemini/DeepSeek/MiMo/Qwen/Kimi/MiniMax/GLM) → 排名(artificialanalysis.ai) → 调用(OpenRouter)
- SPA站点需browser渲染，不可用时标注"未获取"
- 版本号精确到小版本，**禁止硬编码版本号**，每次实时获取

## 行业应用

覆盖至少3个行业：教育/医学/工业/企业/金融/法律/安全/农业/交通/娱乐
不限于GitHub，可以是任何网站新闻
不需要Stars，需要：解决什么行业问题+技术原理+来源链接

## 推送

- 无字数限制，按内容自然分段
- **内容质量优先，不拼凑段数**（2026-05-30教训：为了凑8段每段太薄，丢失full版要求的深度）
- **宁可4段高质量，不要8段敷衍**——用户明确要求"不必拼凑，不必考虑分段限制"
- **限流解决方案（2026-05-30更新）**：
  - 日常推送（cron）：用final response自动推送，绕过send_message，不会限流
  - 非日常推送（手动）：合并为2-3段长消息，每段间隔30-60秒
  - 限流后：减少消息数量才是根本方案，等待只是临时措施

## ⚠️ 关键Pitfalls（完整版）

### P0: 分类验证（最重要！）
- **有Python ≠ Agent！** 必须按判断流程逐项验证
- **误判案例**：ARIS(Stars 10K+)实际是Skills，不是Agent
- **验证方法**：GitHub API获取根目录，统计.md和.py文件数量

### P1: Agent描述必须详细
- **不能一句话敷衍**（如"超轻量级AI Agent"）
- **必须包含**：应用领域、核心功能、技术原理、与前辈对比
- **参考Nanobot示例**

### P2: 前辈对比必须做
- **Agent和Skills都必须找前辈对比**
- **对比内容**：相似/不同/解决什么问题/原理差别
- **对比表列**：功能、成本、自主性⭐、易用性⭐、适用场景

### P3: 子任务数据必须验证
- **delegate_task返回的数据可能完全编造**
- **已确认编造**：GitHub仓库URL（404）、Stars数（捏造）、排名数据（无来源）
- **验证流程**：GitHub API验证URL和Stars，browser验证排名

### P4: 微信限流处理
- **每段间隔15秒**可稳定发送8段，无限流
- **限流时等待后重试**，不放弃剩余段落
- **降级策略**：60s→120s→300s→暂停做其他→回来重试

### P5: access_log不要保留bytes对象
- **fetch_url返回的data字段是bytes**
- **json.dump前必须剥离或转base64**
- **否则报错**：Object of type bytes is not JSON serializable

### P6: execute_code有5分钟超时
- **数据采集必须分阶段执行**
- **Phase1采集→保存→Phase2补充→Phase3解析+报告**
- **单阶段不要超过4分钟**

### P7: 模型版本不能硬编码
- **禁止**在SKILL.md中写死版本号（如"Gemini 2.5 Flash"）
- **正确做法**：每次日报生成时用browser访问artificialanalysis.ai实时读取
- **browser失败时**：跳过排名板块，标注"今日未能获取"

### P8: 微信推送格式一致性
- **不能自行改变结构**，必须严格按分段格式输出
- **板块顺序**：①Agent生态 ②Skills市场 ③模型动态 ④行业应用 ⑤数据面板 ⑥核心信号
- **Agent必须包含对比、拆分、归纳三步分析**

### P9: Agent组件在Agent生态下面
- **不是独立板块**，合并到Agent生态下
- **必须说明组件解决哪些Agent的什么问题**

### P10: 描述通俗易懂
- **解释解决AI服务人类的什么问题**
- **不限于**：能力缺失型/使用不便型/成本过高型/安全风险型/效率低下型/知识壁垒型/协作困难型/数据孤岛型/行业落地型

### P11: 行业应用至少3个行业
- **覆盖**：教育/医学/工业/企业/金融/法律/安全/农业/交通/娱乐
- **不限于GitHub**，可以是任何网站新闻
- **不需要Stars**，需要：解决什么行业问题+技术原理+来源链接

### P12: 数据采集必须记录访问日志
- **每次访问记录到access_log.json**：源名+时间+状态+数据量
- **任务完成后输出统计**：源访问统计: 总102源, 成功X个, 失败Y个, 降级Z个

### P13: 分类-报告一致性（2026-05-30新增）
- **问题**：数据采集阶段正确分类了项目，但写报告时凭印象或搜索来源重新分类
- **错误案例**：ADHD（描述含"a skill for coding agents"）在Phase 4被正确分类为[skill]，但写报告时因出现在"AI+agent"搜索结果中，被错误放入"🆕 新出现Agent"板块
- **根因**：采集阶段的分类标签没有传递到报告生成阶段
- **修复**：
  1. 数据采集阶段必须为每个项目打分类标签（agent/component/skill）
  2. 报告生成时**必须查询分类标签**，不能凭搜索来源或印象决定板块
  3. 如果一个项目出现在多个搜索结果中，以分类代码的结果为准
  4. 分类不明确时，重新执行分类判断流程（Step 1-5）

- **详细案例**：见 references/classification-lessons-2026-05-30.md

## 参考文件

- 完整版：SKILL-full.md（40K字符，含102源列表、详细示例、所有Pitfalls）
- 源列表：D:/openclaw-hermes/sources/source_registry.yaml
- 报告模板：references/report-template-v3.md
- Python采集模式：references/python-collection-pattern.md
- 分类决策树：references/classification-decision-tree.md
- 模型版本追踪：references/model-version-tracking.md
- GitHub API策略：references/github-api-strategy.md
- 微信推送格式：references/report-template-v2.md
