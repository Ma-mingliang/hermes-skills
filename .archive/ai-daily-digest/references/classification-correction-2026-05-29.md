# 分类流程修正历史（2026-05-29）

## 问题

旧分类流程有三个错误：
1. Step 3"可能是Agent"不是明确判断标准
2. Step 4-5顺序导致"能独立运行但无API"被错误归类为组件
3. 缺少检查"是否需要其他Agent平台"

## 关键发现：CLI不是判定标准

**问题**：旧流程将"有npm包/CLI/跨平台支持"作为组件判定条件
**错误**：Claude Code有CLI（`claude`命令），但是Agent，不是组件
**正确理解**：CLI只是接口形式，Agent和组件都可能有CLI

### 示例对比

| 项目 | CLI | 独立运行 | 依赖其他Agent | 分类 |
|------|-----|----------|---------------|------|
| Claude Code | ✅ `claude` | ✅ | ❌ | 🤖 Agent |
| ECC | ✅ `ecc` | ❌ | ✅ | 🧩 组件 |
| cavemem | ✅ `cavemem` | ❌ | ✅ | 🧩 组件 |
| ADHD | ❌ | ❌ | ✅ | 📚 Skills |

## 修正后的分类流程

```
Step 1: 描述含"skill(s)" → 📚 Skills
Step 2: 主要是.md文件（.md > .py） → 📚 Skills
Step 3: 检查是否需要其他Agent平台（Claude Code、Cursor等）→ 需要 → 🧩 Agent组件
Step 4: 检查能否独立运行 + 有API/Web UI → 能 → 🤖 Agent（CLI不算）
Step 5: 以上都不满足 → 🧩 Agent组件
```

**关键区别**：
- **Agent**：能独立运行，不依赖其他Agent
- **组件**：依赖其他Agent平台，增强现有Agent

## 修正状态

- ✅ SKILL-balanced.md：已修正
- ⏳ SKILL-full.md：待修正（明天12点提醒）
- ⏳ SKILL-core.md：待检查

## Balanced版本报告中的分类修正

| 项目 | 修正前 | 修正后 | 原因 |
|------|--------|--------|------|
| CopilotKit | 🤖 全能Agent | 🧩 Agent组件 | React组件框架，需要其他Agent平台 |
| n8n | 🧩 Agent组件 | 🤖 专精Agent | 独立的工作流自动化平台，能独立运行 |
| Dify | 🧩 Agent组件 | 🤖 专精Agent | 独立的Agent工作流开发平台，能独立运行 |
| open-webui | 🧩 Agent组件 | 🤖 专精Agent | 独立的用户界面平台，能独立运行 |
