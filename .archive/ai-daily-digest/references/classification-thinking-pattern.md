# 分类思维模式（2026-05-30）

## 错误模式：机械关键词匹配

```
描述含"cli" → 排除Agent
描述含"runtime" → 是Agent
描述含"server" → 是组件
```

**问题**：没有理解"它是什么、谁用它、用它做什么"，只做字符串匹配。

## 正确模式：先理解→再分类→最后验证

### Step 1: 理解它是什么
问三个问题：
- **它是什么**：Agent？运行时？框架？工具？文档？
- **谁用它**：终端用户？开发者？其他Agent？
- **用它做什么**：帮你做事？帮你管理AI服务？给Agent提供基础设施？

### Step 2: 分类
根据理解选择分类：
- **用AI帮你做事**（写代码、回答问题、执行任务）→ 🤖 Agent
- **帮你管理AI服务**（配置、监控、CLI工具）→ 🧩 组件
- **给Agent提供基础设施**（runtime、框架、SDK）→ 🧩 组件
- **约束AI行为的规则文档**（.md文件）→ 📚 Skills
- **Agent的工具接口**（MCP server）→ 🔌 MCP

### Step 3: 验证
检查是否符合skill分类流程（P0 Step 1-6）

## 实战案例

### Agent OSS（cognitive runtime）
- 描述："recursive evidence-gated cognitive runtime for memory-native ai agents"
- 理解：runtime是Agent的执行环境，"for ai agents"说明给Agent用
- 分类：🧩 组件（Agent的基础设施，不是Agent本身）
- 类比：Node.js是Web应用的runtime，但Node.js不是Web应用

### Gemini Antigravity CLI（终端AI Agent）
- 描述："gemini antigravity 2.0 cli google terminal ai agent tool"
- 理解：终端工具，用Gemini帮你做事（写代码、问答）
- 分类：🤖 Agent（用AI帮你做事，不是管理AI服务）
- 类比：Claude Code也是CLI，但它是Agent

### Model Studio CLI（阿里云百炼CLI）
- 描述："Official Model Studio CLI（阿里云百炼 CLI）built for AI Agent frameworks"
- 理解：CLI工具，帮你管理阿里云百炼平台的AI服务
- 分类：🧩 组件（帮你管理AI服务，不是用AI帮你做事）
- 类比：aws cli是AWS的管理工具，但aws cli不是Agent

### WHOOP MCP（健康数据MCP）
- 描述："Model Context Protocol server giving Claude full read + write access to WHOOP data"
- 理解：MCP server，给Claude提供WHOOP数据访问
- 分类：🔌 MCP（优先MCP板块，不放组件）

## 关键信号

| 信号 | 含义 |
|------|------|
| "for ai agents" | 给Agent用的 → 组件 |
| "ai agent for" | 用AI做事 → Agent |
| "mcp server" | Agent工具接口 → MCP |
| "cli for [平台]" | 平台管理工具 → 组件 |
| "terminal ai agent" | 终端AI助手 → Agent |
| "runtime for agents" | Agent执行环境 → 组件 |
