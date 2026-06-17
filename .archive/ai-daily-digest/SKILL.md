---
name: ai-daily-digest
description: "AI日报+月报生成 — 脚本+Agent协作模式。脚本处理数据收集/验证/分类（确定性工作），Agent负责报告撰写/趋势分析（创造性工作）。含月度合订本（聚合上月日报→五大板块月报.md+.docx）。触发词：AI日报/生成今日AI日报/AI月报/AI news digest。NOTE: 当用户说'日报'、'report'、'AI日报'且未明确说'AI新闻'时，默认使用 agent-daily-report（Agent工程情报）。本skill用于AI新闻类日报。"
version: "7.2.0"
---

# AI Daily Digest v7.2 — 脚本+Agent协作

> **⚠️ 选择指南**：用户说"agent日报"/"report"/"agent情报"时，用 `agent-daily-report`。本 skill 用于通用AI新闻日报（面向非技术读者）。
> 执行模式：脚本做确定性工作，Agent做创造性工作，双重质量保障。
> 📋 月度合订本 → 见 `ai-monthly-digest` 技能（聚合上月日报 → 五大板块月报 .md + .docx）

---

## ⚠️ 铁律（违反任何一条 = 任务失败）

1. **必须用todo工具列出Step 1-8，逐步标记完成** — 不跳步
2. **必须运行脚本收集数据** — 不要手动调API（脚本已处理DDG限流、分类白名单、时间验证）
3. **数据必须区分今日/本周/历史** — 脚本自动区分，Agent不能覆盖
4. **分类必须用脚本输出** — 不能凭印象重新分类
5. **每个新Agent/Skill必须有前辈对比** — 对比表+文字分析
6. **报告格式必须逐项对照模板** — 不能自行增删板块
7. **推送前必须运行质量检查脚本** — 不通过不推送
8. **没有来源的数据不能写入报告** — 标⚠️或删除
9. **不确定的内容标⚠️或删除** — 宁可漏报不要错报
10. **每步完成后必须验证** — 执行→验证→通过→下一步

---

## 工作流程（8步，严格按顺序执行）

### Step 1: 加载配置与准备（Agent）

**必须读取的文件**：
- `checklists/01-data-collection.md` — 数据收集清单

**执行清单**：
- [ ] 用todo列出Step 1-8
- [ ] 确认今天日期（YYYY-MM-DD）
- [ ] 确认输出路径：`D:/openclaw-hermes/data/daily/YYYY-MM-DD/report.md`
- [ ] 创建输出目录：`mkdir -p D:/openclaw-hermes/data/daily/YYYY-MM-DD/`
- [ ] 检查是否有同日旧报告（有则走冲突处理）
- [ ] 读取过去3天日报标题（去重基线）

---

### Step 2: 多源数据收集（脚本+Agent）

**必须读取的文件**：
- `checklists/01-data-collection.md` — 数据收集详细清单

**运行脚本**：
```bash
python "C:/Users/lenovo_mml/.hermes/skills/news/ai-daily-digest/scripts/ai_daily_digest_v4.py"
```

脚本自动完成：
- HN Algolia API（9个关键词，每个15条）
- GitHub API（Agent/Skills/MCP分类搜索）
- 专精Agent垂直领域搜索（DB-GPT/HolmesGPT/TradingAgents等）
- 数据验证（区分今日/本周/历史）
- 分类（P24决策树+白名单）

**Agent补充收集**（脚本未覆盖的源）：
- 36氪RSS：`https://36kr.com/feed`
- 量子位：`https://www.qbitai.com/`
- 机器之心：`https://www.jiqizhixin.com/`
- 模型官网（9个）：Claude/GPT/Gemini/GLM/MiMo/DeepSeek/Kimi/MiniMax/Qwen
- HuggingFace Daily Papers

**⚠️ 子任务无法访问网页**：delegate_task创建的子任务默认没有web工具。
补充收集必须在主任务中用 `execute_code + urllib` 完成，不要委托给子任务。
详见 `references/subagent-web-limitation.md`。

**⚠️ 访问记录**（必须）：
- 每次访问记录：源名+时间+状态+数据量
- 任务完成后输出统计：`源访问统计: 总X源, 成功Y个, 失败Z个`

**执行清单**：
- [ ] 运行脚本，确认exit_code=0
- [ ] 检查输出文件存在
- [ ] 记录数据量（HN多少条、GitHub多少个）
- [ ] 补充收集脚本未覆盖的源
- [ ] 如果脚本失败，检查错误并重试

---

### Step 3: 数据验证与交叉引用（脚本+Agent）

**必须读取的文件**：
- `checklists/02-data-verification.md` — 数据验证清单

**脚本已自动验证时间戳。Agent额外检查**：

**交叉引用分析**：
- 统计每个事件在多少源中出现
- ≥5源 → 🔴 极高重要（置顶）
- 3-4源 → 🟡 重要
- 1-2源 → ⚪ 低置信观察

**⚠️ 关键：重复出现的内容是热点，必须标注**

**执行清单**：
- [ ] 读取脚本输出中的验证结果
- [ ] 确认今日/本周/历史分类正确
- [ ] 确认没有非本周数据混入"今日"板块
- [ ] 如果今日数据为0，报告中不能出现"今日新闻"板块
- [ ] 交叉引用分析，标注热点

---

### Step 4: 分类到板块（脚本+Agent）

**必须读取的文件**：
- `checklists/03-classification.md` — 分类清单
- `references/classification-decision-tree.md` — 分类决策树

**分类优先级**：MCP > Agent组件 > Agent > Skills

**分类流程**（必须按顺序执行）：
1. 描述含"skill(s)" → 📚 Skills
2. 主要是.md文件（.md > .py） → 📚 Skills
3. 描述含"mcp server"/"model context protocol" → 🔌 MCP
4. 描述含"for ai agents"/"for claude" → 🧩 Agent组件
5. 描述含"ai agent"/"agent for" → 🤖 Agent
6. 以上都不满足 → 🧩 Agent组件

**执行清单**：
- [ ] 使用脚本输出的分类结果
- [ ] 检查已知误判白名单
- [ ] 确认每个项目只出现在一个板块
- [ ] 记录分类统计

---

### Step 5: 生成完整报告（Agent）

**必须读取的文件**：
- `checklists/04-agent-report.md` — Agent报告清单
- `checklists/05-skills-report.md` — Skills报告清单
- `checklists/06-model-industry-mcp.md` — 模型/行业/MCP清单
- `references/pain-point-framework.md` — 9种问题类型框架

**报告结构**（必须严格遵守，不能增删板块）：

```
# 🤖 AI 日报 | YYYY年MM月DD日

> 数据来源：HN Algolia ✅ | GitHub API ✅ | [其他源]
> 共 N 条精选

---

## 一、🤖 Agent生态（🔴 极高重要）

> **Agent定义**：可独立运行、有API接口、能执行任务的程序/平台

### 📌 使用指南（少写，或留链接）

### 🆕 新出现的全能Agent（必须含前辈对比）
- 每个Agent：热度+功能+解决什么问题（通俗易懂）+GitHub链接
- 📊 前辈对比（表格）：功能、成本、自主性⭐、易用性⭐、适用场景
- 🔍 拆分：按某个维度排序
- 📋 归纳：按场景推荐

### ⭐ 高星全能Agent（多维度对比表）

### 🆕 新出现的专精Agent（必须含前辈对比）
（同上格式。当日没有新的→推荐5个高星专精Agent）

### ⭐ 高星专精Agent

### 🧩 Agent组件（在Agent生态下面，不是独立板块！）
> **Agent组件定义**：有代码但不能独立运行，增强现有Agent的扩展层
> **必须说明组件解决哪些Agent的什么问题+原理**

### 🆕 新组件
### ⭐ 高星组件

---

## 二、🛠️ Skills市场（🔴 极高重要）

> **Skills定义**：.md规则文档，约束AI按规则执行，不能独立运行

### 📉 第一类
（减少token消耗 — 原理、算法、示例、效果、GitHub链接、真实案例）

### 🔒 第二类
（约束agent行为）

### ⚡ 第三类
（增加功能）

### 🔬 第四类
（科研辅助）

### 🔍 第五类
（检测正常工作 — 验证/监控/审计类skill，确保Agent输出质量和系统运行正常。含verification-loop、skill-stocktake、canary-watch、cache-audit、security-scan等）

### 📦 第六类
（补充类/其他 — 独立于前5类之外的skills、资源/索引/元信息集合。含awesome-*系列、hermes-atlas、skill-scout、hermes-agent等配置文档类skill）

> ⚠️ **关键格式规则**：标题必须是 `### 📉 第一类`（不带冒号和描述后缀）。
> quality_check.py 使用字符串匹配 — `### 第一类：减少token消耗` 将导致 FAIL。
> 描述性文字放在下一行括号中，而非标题冒号后面。

（每个Skill：Stars+痛点+原理+案例+GitHub链接+前辈对比）

---

## 三、📊 模型动态

> **三层监控体系**：
> - 第一层（模型官网）：Claude/GPT/Gemini/DeepSeek/MiMo/Qwen/Kimi/MiniMax/GLM
> - 第二层（排名网站）：artificialanalysis.ai/lmarena.ai/openrouter.ai
> - 第三层（调用网站）：openrouter.ai/together.ai

（每个模型事件必须包含：模型名称+版本号+事件描述+热度+链接）
（模型对比网站链接：OpenRouter/DesignArena/ArtificialAnalysis/OpenCode/ChatbotArena）

---

## 四、📰 行业热点 + 🏭 行业应用

**A. AI行业重大事件**
- 融资、收购、政策、AI安全事件、AI伦理讨论、AI人才流动
- 每个事件必须包含：事件标题+热度+说明+原文链接

**B. AI行业应用（每天必须覆盖至少3个行业！）**
- 表格格式：行业|事件|来源，附链接
- 10大行业覆盖：🎓教育/🏥医学/🏭工业/🏢企业/💰金融/⚖️法律/🔒安全/🌾农业/🚗交通/🎮娱乐
- 行业选择优先级：(1)当日热点行业 (2)近期持续关注行业(AI+医疗/AI+金融) (3)冷门但有突破的行业(轮换)
- 每个行业应用需说明：解决什么问题+技术原理

---

## 五、🔌 MCP动态

> **MCP定义**：Model Context Protocol，AI Agent的"USB接口"，让Agent连接外部工具和数据源

**MCP监控标准**（满足任一项即纳入）：
- 新发布的MCP服务器（Stars > 100）
- Stars > 5000 的MCP服务器有重大更新
- MCP协议本身有重要变更（版本、规范、安全公告）
- MCP生态重要事件（新SDK语言支持、重大收购、安全漏洞）
- 多源交叉确认的热点MCP项目（≥3源）

**覆盖内容**：
- MCP新项目介绍（含多维度评估：社区热度/功能完整度/集成便利性/安全风险/维护活跃度）
- MCP重要更新（协议变更、重大功能）
- MCP生态趋势（热门类别、增长方向）
- MCP安全问题（漏洞、扫描器、权限风险）

**MCP七大分类**（带emoji图标）：
| 分类 | 说明 |
|------|------|
| 🌐 浏览器控制 | 控制浏览器、网页交互、爬虫（Playwright MCP等） |
| 💻 代码智能 | 代码分析、LSP、代码搜索、重构（GitHub MCP等） |
| 🗄️ 数据库 | 数据库连接、查询、Schema管理（PostgreSQL MCP等） |
| 🔗 工作流自动化 | CI/CD、任务编排、流程自动化（n8n MCP等） |
| 🔌 API集成 | 第三方API封装（搜索/邮件/日历/文件等）（Exa MCP等） |
| 🔒 安全 | 安全扫描、漏洞检测、权限管理（Security MCP等） |
| 🏗️ 开发框架 | MCP开发SDK、脚手架、测试工具（FastMCP等） |

**MCP评估方法**（每个项目至少评估3个维度）：
- 🌟 社区热度：Stars数、增长趋势、讨论活跃度
- 🔧 功能完整度：覆盖的MCP能力范围、工具数量
- 📦 集成便利性：安装难度、配置复杂度、文档质量
- 🛡️ 安全风险：权限范围、数据暴露风险、是否有安全审计
- 🔄 维护活跃度：最近更新时间、Issue响应速度

---

## 六、📊 数据面板

| 类别 | 统计项 |
|------|--------|
| HN | 总条数、去重后、最高热度 |
| GitHub | 总项目数、去重后 |
| 分类 | 🤖全能Agent、🤖专精Agent、📚Skills、🧩组件、🔌MCP |
| 模型 | 事件数 |
| 行业 | 事件数 |
| API | 总调用/成功/限流 |

---

## 七、🔮 核心信号（3-7条）

**信号类型**：
1. 趋势信号：某个方向正在兴起
2. 安全信号：Agent/MCP/模型的安全问题
3. 生态信号：某个生态快速成熟
4. 模型信号：模型格局变化
5. 市场信号：定价/商业模式变化
6. 行业信号：AI在某个行业的重大应用

**⚠️ 信号必须基于当日数据，不能凭空推测**

---

## 八、📖 AI基础知识（每日一则）

**核心逻辑**：AI发展有两条相互促进的主线
- 主线1：提高AI能力（让AI更强大）
- 主线2：让AI更好地解决人类问题（让AI更有用）

**每日内容结构**：
- 🎯 今日目标
- 📌 核心概念（定义、类比、图示）
- 💡 为什么重要
- ❓ 常见误解
- 🔗 延伸阅读（GitHub教程链接）
- 📝 今日小测验

**⚠️ 关键规则**：
1. 问题→方案结构：不能把问题和方案分开讲
2. 两条主线标注：每个热词必须标注属于哪条主线
3. 交互分析：展示主线1如何促进主线2，主线2如何促进主线1

---

## 📊 数据来源透明度

| 板块 | 来源 | 状态 |
|------|------|------|
| HN热点 | HN Algolia API | ✅ X条 |
| GitHub项目 | GitHub API | ✅ X个 |
| 模型版本 | [来源] | ✅/⚠️/❌ |
| 行业应用 | [来源] | ✅/⚠️/❌ |
| AI基础知识 | 基于知识 | ⚠️ |
```

**9种问题类型框架**（描述痛点时使用）：

| 类型 | 说明 | 示例 |
|------|------|------|
| 能力缺失型 | AI能解决但没有好的方案 | AI能写代码但没有好的编码Agent |
| 使用不便型 | 人使用AI时的不便 | Token消耗太高 |
| 成本过高型 | API/部署成本不可控 | Claude Code $200太贵 |
| 安全风险型 | AI行为不可控 | Agent删除文件 |
| 效率低下型 | 工作流程繁琐 | 手动配置Harness |
| 知识壁垒型 | 不知道怎么用AI | 新手不会配置 |
| 协作困难型 | 多Agent/多人协作不便 | 调试Agent只能单人 |
| 数据孤岛型 | Agent间数据不互通 | 文件系统不统一 |
| 行业落地型 | AI技术难以落地 | 医学诊断AI化 |

**执行清单**：
- [ ] 按模板顺序生成，不增删板块
- [ ] 每个新Agent/Skill有前辈对比表+文字分析
- [ ] 痛点描述按9种问题类型框架
- [ ] 行业应用≥3个行业
- [ ] 所有项目有GitHub链接
- [ ] 数据来源标注✅/⚠️/❌
- [ ] 报告写入 `D:/openclaw-hermes/data/daily/YYYY-MM-DD/report.md`

---

### Step 6: 质量检查（脚本+Agent）

**必须读取的文件**：
- `checklists/07-push.md` — 推送清单
- `references/quality-check-75.md` — 完整质量检查清单

**运行质量检查脚本**：
```bash
python "C:/Users/lenovo_mml/.hermes/skills/news/ai-daily-digest/scripts/quality_check.py" D:/openclaw-hermes/data/daily/YYYY-MM-DD/report.md
```

**Agent额外检查**（脚本无法覆盖的）：
- 每个项目是否来自数据收集（不是凭记忆写的）
- 前辈对比是否有文字分析（不只是表格）
- 痛点是否按9种问题类型框架
- 数据来源透明度是否完整

**⚠️ 质量检查脚本的精确匹配规则**：脚本用字符串匹配，不是语义理解。
- "拆分分析"必须包含"按自主性"或"按成本"或"对比分析"（不是"按Stars"）
- Skills标题格式必须是 `### 📉 第一类`（不能有冒号）
- 详见 `references/quality-check-patterns.md`

**执行清单**：
- [ ] 运行质量检查脚本，确认exit_code=0
- [ ] 检查脚本输出的FAIL项，逐一修复
- [ ] Agent额外检查（4项）
- [ ] 修复后重新运行脚本验证
- [ ] 全部通过才进入Step 7

---

### Step 7: 推送（Agent）

**推送模式**：
- **当前聊天**（用户说"推送到这里"）：直接在回复中输出完整报告
- **微信**（cron模式）：按[1/N]...[N/N]格式分段，每段约2000字符
- **本地保存**：写入 `D:/openclaw-hermes/data/daily/YYYY-MM-DD/report.md`

详见 `references/wechat-push-pattern.md`（分段算法、推送目标格式、已知问题）。

**执行清单**：
- [ ] 确认推送目标
- [ ] 按格式分段（如需要）
- [ ] 推送
- [ ] 确认推送成功

---

### Step 8: 留存与复盘（Agent）

**执行清单**：
- [ ] 保存原始搜索数据到 `D:/openclaw-hermes/data/daily/YYYY-MM-DD/`
- [ ] 记录本次执行的问题
- [ ] 更新skill（如有新的Pitfall）
- [ ] 更新脚本（如有新的数据源）

---

## 月度合订本（Monthly Digest）

> 聚合上月所有日报，按五大板块输出月度合订本。

### 触发条件

- "生成上月 AI 月度合订本" / "AI 月报" / "上月 AI 合集" / "monthly AI digest"

### 输入/输出

| 项目 | 路径 |
|------|------|
| 日报源 | `D:/openclaw-hermes/data/daily/YYYY-MM-DD/report.md` |
| 分类配置 | `D:/openclaw-hermes/sources/taxonomy_config.yaml` |
| Markdown输出 | `D:/openclaw-hermes/data/monthly/YYYY-MM/monthly_report.md` |
| Word输出 | `D:/openclaw-hermes/data/monthly/YYYY-MM/monthly_report.docx` |

### 月度工作流

1. **确定目标月份**: 当前日期为月初第1天 → 目标为上个月
2. **读取日报文件**: 遍历 `data/daily/YYYY-MM-*/report.md`
3. **读取 taxonomy_config.yaml**: 五大板块定义（模型动态/Agent生态/Skills市场/行业应用/AI基础教育）
4. **聚合分析**: 提取各板块内容，识别跨日重复（标注"🔥 持续热点"），按重要性排序
5. **生成 monthly_report.md**: 按五大板块结构输出
6. **生成 monthly_report.docx**: 使用 python-docx（微软雅黑 11pt，Table Grid 样式）
7. **推送**: 输出摘要版到 final response

### 月度报告结构

```markdown
# 🤖 AI 月度合订本 | YYYY年M月
## 📖 本月概览
## 一、📊 模型动态
## 二、🤖 Agent 生态
## 三、🛠️ Skills 市场
## 四、🏭 行业应用
## 五、📖 AI 基础教育（历史回填）
## 📊 月度数据统计
## 🔮 月度核心信号（5-7条）
```

### 月度 Pitfalls

| ID | 规则 | 违反后果 |
|----|------|---------|
| M1 | 日报天数可能不完整，如实标注覆盖范围 | 误导读者 |
| M2 | taxonomy_config.yaml 在 `sources/` 下，不在 `data/daily/` 下 | 文件找不到 |
| M3 | Windows 上用 execute_code + Python，不要 terminal | 命令执行失败 |
| M4 | DOCX 用 python-docx，不是 .NET DocxGenerator | DOCX生成失败 |
| M5 | 跨日重复事件必须标注"🔥 持续热点"和连续天数 | 丢失热点追踪 |
| M6 | 模型/Agent/Skills 数据必须带 Stars + GitHub 链接 | 无数据支撑 |
| M7 | 每月输出必须同时生成 .md 和 .docx | 缺少格式 |

## 详细参考（按需加载）

执行过程中需要详细信息时，用 `skill_view(name, file_path)` 加载：

| 文件 | 何时加载 |
|------|---------|
| `checklists/01-data-collection.md` | Step 2 需要了解数据收集细节 |
| `checklists/02-data-verification.md` | Step 3 需要了解验证规则 |
| `checklists/03-classification.md` | Step 4 分类有疑问时 |
| `checklists/04-agent-report.md` | Step 5 写Agent板块时 |
| `checklists/05-skills-report.md` | Step 5 写Skills板块时 |
| `checklists/06-model-industry-mcp.md` | Step 5 写模型/行业/MCP时 |
| `checklists/07-push.md` | Step 7 推送时 |
| `references/pitfalls-complete.md` | 执行中遇到问题时查阅 |
| `references/classification-decision-tree.md` | 分类有疑问时 |
| `references/report-template-v3.md` | 需要完整报告模板时 |
| `references/quality-check-75.md` | 需要完整质量检查清单时 |
| `references/pain-point-framework.md` | 写痛点描述时 |
| `references/source-layers.md` | 了解数据源分层时 |
| `references/execution-learnings-2026-05-31.md` | 质量检查FAIL时查阅修复方法 |
| `references/quality-check-patterns.md` | 质量检查脚本的精确匹配规则 |
| `references/wechat-push-pattern.md` | 微信分段推送最佳实践 |
| `references/quality-check-format-quirks.md` | quality_check.py的精确格式要求（Step 6必读） |
| `references/v4-script-output-format.md` | v4脚本输出JSON结构（Step 3/4必读） |
| `references/supplement-data-collection.md` | 36氪/HuggingFace补充收集方法（Step 2） |
| `references/update-log-2026-06-01.md` | v7.1→v7.2 更新日志（Skills/MCP/组件/行业变更摘要） |

---

## 关键Pitfalls（精简版，完整版见references/pitfalls-complete.md）

| ID | 规则 | 违反后果 |
|----|------|---------|
| P50 | DDG最多1个查询，失败就切HN+GitHub | 全部限流，数据为0 |
| P43 | 必须按清单逐步执行，不能跳步 | 报告质量低 |
| P48 | 数据必须区分今日/本周/历史 | 误导读者 |
| P49 | 时间戳验证用当日0点 | 数据时间错误 |
| P24 | 分类必须走Step 1-6决策树 | 分类错误 |
| P13 | 分类-报告一致性 | 采集分类正确但报告放错板块 |
| P16 | 报告格式不能自行改变 | 用户要求重做 |
| P59 | 每个板块标注数据来源 | 用户质疑真实性 |
| P57 | 推送前必须运行验证循环 | 带错推送 |
| P58 | 每个项目必须来自数据收集 | 凭记忆编造 |
| P60 | quality_check.py格式：拆分分析用"按自主性"不用"按Stars"；Skills分类用"第X类"不加冒号 | 35/38通过卡在3个格式FAIL |
| P2.7 | 子任务搜索结果必须验证 | 编造数据 |
| P2.11 | 描述必须通俗易懂 | 读者不理解 |
| P60 | 子任务没有web工具时用execute_code+urllib | 子任务无法访问网页 |
| P61 | Skills标题格式不能有冒号 | 质量检查FAIL |
| P60 | quality_check.py期望"按自主性/按成本/对比分析"，不接受"按Stars排名" | 拆分分析FAIL |
| P61 | Skills板块第X类格式不能有冒号后缀（"第一类"✅ "第一类：减少token消耗"❌） | 无第X类格式FAIL |
| P62 | 子任务delegate_task没有web访问能力，补充收集必须用execute_code | 补充数据收集失败 |
| P63 | v4脚本categories字段是[name,details]列表对，不是字典 | 数据解析错误 |
| P64 | 今日无数据时报告不能有"今日新闻"板块，改用"本周"数据 | 数据时间错误 |
| P65 | terminal(WSL)不可用时用execute_code+subprocess.run()运行Python脚本 | 脚本无法执行 |
| P66 | 质量检查前先做格式预检（拆分分析用"按自主性"、Skills无冒号等），减少反馈循环 | 反复FAIL浪费时间 |

---

## 脚本清单

| 脚本 | 功能 | 何时运行 |
|------|------|---------|
| `scripts/ai_daily_digest_v4.py` | 数据收集+分类+验证 | Step 2 |
| `scripts/quality_check.py` | 报告格式验证 | Step 6 |
| `scripts/data_verification.py` | 数据时间验证 | Step 3（如需要） |

---

## Cron配置

- 时间：每天06:30
- 模式：final response自动推送
- 分段：按[1/N]...[N/N]格式
