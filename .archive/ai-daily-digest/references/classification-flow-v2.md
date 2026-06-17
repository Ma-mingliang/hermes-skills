# 分类判断流程（2026-05-30最终修正版）

## 正确的分类流程

```
Step 1: 描述含"skill(s)" → 📚 Skills
Step 2: 主要是.md文件（.md > .py） → 📚 Skills
Step 3: 检查是否需要其他Agent平台（Claude Code、Cursor等）→ 需要 → 🧩 Agent组件
Step 4: 检查能否独立运行 + 有API/Web UI → 能 → 🤖 Agent（CLI不算）
Step 5: 以上都不满足 → 🧩 Agent组件
```

## 关键说明

- **CLI不是判定标准**：Agent和组件都可能有CLI
  - Claude Code有CLI → 但是Agent（能独立运行）
  - ECC有CLI → 但是组件（依赖其他Agent）
- **Agent**：能独立运行，不依赖其他Agent
- **组件**：依赖其他Agent平台，增强现有Agent

## 误判案例

| 项目 | 错误分类 | 正确分类 | 原因 |
|------|----------|----------|------|
| CopilotKit | 🤖 全能Agent | 🧩 Agent组件 | React组件框架，需要其他Agent平台 |
| n8n | 🧩 Agent组件 | 🤖 专精Agent | 独立的工作流自动化平台，能独立运行 |
| Dify | 🧩 Agent组件 | 🤖 专精Agent | 独立的Agent工作流开发平台，能独立运行 |
| open-webui | 🧩 Agent组件 | 🤖 专精Agent | 独立的用户界面平台，能独立运行 |
| ADHD | 🤖 Agent | 📚 Skills | 描述含"skill"，是.md规则文档 |
