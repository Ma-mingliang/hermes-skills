# Agent/Skills/Agent组件 精确分类决策树

> 2026-05-29 通过多次用户纠正总结的分类规则
> 2026-05-29 修正：CLI不是判定标准（Claude Code有CLI但是Agent，ECC有CLI但是组件）
> 修正历史：见 `references/classification-correction-2026-05-29.md`

## 决策树（2026-05-29修正版，按顺序执行）

```
Step 1: 描述含"skill(s)" → 📚 Skills
Step 2: 主要是.md文件（.md > .py） → 📚 Skills
Step 3: 检查是否需要其他Agent平台（Claude Code、Cursor等）→ 需要 → 🧩 Agent组件
Step 4: 能独立运行 + 有API/Web UI → 🤖 Agent（CLI不算）
Step 5: 以上都不满足 → 🧩 Agent组件
```

**关键修正说明**：
- **CLI不能作为判定Agent的条件**：Agent和组件都可能有CLI（Claude Code有`claude`CLI但是Agent，ECC有`ecc`CLI但是组件），判断核心是能否独立运行+是否依赖其他Agent平台
- **"需要其他Agent平台"是关键判断**：如果项目必须依附Claude Code/Cursor等才能工作，就是组件
- **删除了"有main.py"检查**：这不是必要条件，有些Agent没有main.py也能独立运行

## 三分类定义

| 分类 | 定义 | 判断标准 | 示例 |
|------|------|---------|------|
| 🤖 Agent | 有入口+可独立运行+有API | 独立运行 + API/Web UI/CLI | DB-GPT, HolmesGPT, TradingAgents, Claude Code |
| 📚 Skills | 纯.md文件集合 | .md > .py, 不能独立运行 | ARIS, Anthropic-Cybersecurity-Skills |
| 🧩 Agent组件 | 增强现有Agent的扩展层，有代码但不能独立运行。必须依赖Agent平台（Claude Code/Cursor等）才能工作 | (1) SDK/框架/Gateway/工具库/插件 (2) 虚拟文件系统/代理层 (3) 需要'for AI agents'/'for Claude'等上下文才能发挥作用 (4) 非独立入口（无自主API/WebUI） | ECC, mcp-context-forge, oxylabs-ai-studio-py, Mirage, OpenSquilla |

## Agent组件判定细则

> **核心原则**：Agent组件不能独立运行，必须依赖Agent平台。判断核心是 **"是否需要其他Agent平台"**。

**组件识别信号**（满足任一即可能为组件）：
1. **依赖声明**：README/描述含"for AI agents"/"for Claude Code"/"for Cursor"/"enhance your agent"
2. **无独立入口**：没有Web UI、没有独立API、没有CLI作为主入口
3. **增强层角色**：功能是"增强/扩展/优化"现有Agent，而非替换Agent
4. **插件/中间件形态**：作为插件、中间件、代理层、Gateway存在
5. **虚拟资源层**：虚拟文件系统、虚拟浏览器、虚拟环境（Mirage、BrowserBase等）

**组件 vs Agent 区分要点**：
| 判断维度 | Agent | 组件 |
|---------|-------|------|
| 独立性 | 可独立完成任务 | 必须嵌入Agent平台 |
| 入口 | 有API/WebUI/独立CLI | SDK/库/插件接口 |
| 角色 | 任务执行者 | 能力增强器 |
| 部署 | 独立部署运行 | 导入/集成使用 |

**⚠️ CLI不是判定标准！** Claude Code有CLI但是Agent，ECC有CLI但是组件 — CLI只是接口形式。

## 全能Agent vs 专精Agent

| 分类 | 定义 | 判断标准 | 示例 |
|------|------|---------|------|
| 全能Agent | 通用型平台 | 不限定任务领域 | Claude Code, Cursor, OpenHands, Hermes, OpenClaw |
| 专精Agent | 垂直领域 | 功能限定在某个领域 | html-anything=设计, DB-GPT=数据, HolmesGPT=SRE |

**⚠️ 有API ≠ 全能！** html-anything有API但是专精Agent（只做HTML设计）
**⚠️ "平台" ≠ 全能！** PilotDeck是平台但是任务导向

## 已知项目白名单（2026-05-31新增）

> **规则**：白名单优先于决策树。已知项目的分类直接使用，不走关键词匹配。
> **维护**：每次发现新的误判，立即加入白名单。

```python
KNOWN_PROJECTS = {
    # Agent - 全能
    "anthropics/claude-code": "agent_allround",      # 描述无"agent"但实际是全能Agent
    "google-gemini/gemini-cli": "agent_allround",     # topics含"mcp"但实际是Agent
    "openai/codex": "agent_allround",                 # 描述含"coding agent"但应为全能
    "zhayujie/CowAgent": "agent_allround",            # 描述含"skill"但实际是Agent Harness
    # Agent - 专精
    "anomalyco/opencode": "agent_specialized",        # 开源编码Agent
    "karpathy/autoresearch": "agent_specialized",     # 科研自动化Agent
    # Skills
    "obra/superpowers": "skills",                     # 描述含"system"但实际是Skills集合
    "anthropics/skills": "skills",                    # Anthropic官方Skills
    "addyosmani/agent-skills": "skills",              # Agent技能开发指南
    # Component
    "affaan-m/ECC": "component",                      # Agent组件系统（199K stars）
    "langflow-ai/langflow": "component",              # 工作流编排平台
    # MCP
    "punkpeye/awesome-mcp-servers": "mcp",            # MCP服务器集合
    "microsoft/playwright-mcp": "mcp",                # Playwright MCP
    "github/github-mcp-server": "mcp",                # GitHub MCP
    "PrefectHQ/fastmcp": "mcp",                       # MCP开发框架
}
```

## 已确认的误判案例

| 项目 | 误判为 | 正确分类 | 原因 |
|------|--------|---------|------|
| ARIS (⭐10,982) | 专精Agent | 📚 Skills | 描述写"Markdown-only skills"，0个.py文件 |
| Anthropic-Cybersecurity-Skills (⭐11,873) | 专精Agent | 📚 Skills | "754 structured cybersecurity skills"，纯.md |
| mcp-context-forge (⭐3,787) | 专精Agent | 🧩 Agent组件 | AI Gateway/代理层，不是独立Agent |
| oxylabs-ai-studio-py (⭐2,944) | 专精Agent | 🧩 Agent组件 | Python SDK，需集成到其他系统 |
| notte (⭐1,965) | 专精Agent | 🧩 Agent组件 | Web Agent框架，需集成使用 |
| html-anything (⭐5,357) | 全能Agent | 专精Agent（设计） | 只做HTML编辑，不是通用 |
| Mirage (⭐2,778) | 全能Agent | 🧩 Agent组件 | 虚拟文件系统，增强Agent |
| OpenSquilla (⭐2,087) | 全能Agent | 🧩 Agent组件 | Token高效优化层 |
| AI-Engineering-Coach (⭐1,678) | 全能Agent | 📚 Skills | 工程教练，可能是教程/规则 |
| Agent-Learning-Hub (⭐1,934) | 全能Agent | 📚 Skills/补充类 | 学习路线资料库，不是Agent |
| ADHD (⭐506) | Agent组件 | 📚 Skills | 描述含"skill for coding agents"，Tree-of-Thought推理规则文档 |
| **anthropics/claude-code** (⭐128K) | component | agent_allround | 描述无"agent"关键词，决策树Step 6默认为组件 (2026-05-31) |
| **google-gemini/gemini-cli** (⭐104K) | mcp | agent_allround | topics含"mcp"，决策树Step 3误判为MCP (2026-05-31) |
| **openai/codex** (⭐87K) | agent_specialized | agent_allround | 描述含"coding agent"被归为专精，实际是全能 (2026-05-31) |
| **obra/superpowers** (⭐213K) | component | skills | 描述含"system/框架"被归为组件，实际是Skills集合 (2026-05-31) |
| **CowAgent** (⭐44K) | skills | agent_allround | 描述含"skill"被归为Skills，实际是Agent Harness (2026-05-31) |

### 2026-05-31 教训：描述关键词匹配的局限性

**问题**：决策树依赖描述关键词，但知名项目的描述往往不含标准关键词：
- claude-code 描述："Anthropic's official CLI" — 无"agent"
- gemini-cli 描述："AI agent that runs in your terminal" — 有"agent"但topics含"mcp"优先命中
- codex 描述："coding agent" — 有"agent"但被归为专精

**根因**：描述关键词匹配对以下场景失效：
1. 知名项目描述极简（如"Official CLI"）
2. topics与描述冲突（topics含"mcp"但实际是Agent）
3. "coding agent"触发专精判断，但实际是全能

**修复**：白名单机制 — 已知项目直接用正确分类，不走决策树

## 验证方法

当GitHub API可用时（未403限流）：
1. `GET /repos/{owner}/{repo}/contents/` 获取根目录文件列表
2. 统计.py和.md文件数量
3. 检查是否有main.py/app.py/server.py
4. 检查是否有web/cli/docker目录

当GitHub API限流时（降级方案）：
1. 描述含"skill(s)/Markdown-only" → Skills
2. 描述含"SDK/library/framework/gateway/proxy" → Agent组件
3. 描述含"agent/assistant/platform/automation" → Agent
4. 名称含"awesome-/collection" → Skills/补充类

**⚠️ 有Python ≠ Agent！** 必须按决策树逐项判断
**⚠️ 有CLI ≠ 组件！** Claude Code有CLI但是Agent，ECC有CLI但是组件——CLI只是接口形式，不是分类依据
**⚠️ 凭stars数或名气判断分类是错误的！**
