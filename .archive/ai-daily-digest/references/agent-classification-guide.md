# Agent/Skills/Agent组件 分类验证指南

## 分类定义

| 类别 | 定义 | 判断标准 | 示例 |
|------|------|---------|------|
| **全能Agent** | 通用型平台 | 有API+可独立运行+通用领域 | Claude Code, Cursor, Nanobot, OpenHands |
| **专精Agent** | 垂直领域平台 | 有API+可独立运行+特定领域 | DB-GPT(数据), HolmesGPT(SRE), Devin(编程) |
| **Agent组件** | 跨平台优化系统 | 有代码，不能独立运行，依赖其他Agent平台 | ECC, MCP Server, Hooks, Gateway |
| **Skills** | .md规则文档 | 纯Markdown，约束AI行为 | Caveman.md, karpathy-skills, ARIS |

## 验证流程（2026-05-29修正版，必须对每个项目执行）

```
1. 读GitHub描述 → 含"skill(s)"? → 📚 Skills
2. 查仓库language → 纯Markdown? → 📚 Skills
3. 查topics → "claude-code-skills"? → 📚 Skills
4. 需要其他Agent平台（Claude Code/Cursor等）？ → 🧩 Agent组件
5. 能独立运行 + 有API/Web UI？ → 🤖 Agent（CLI不算）
6. 以上都不满足 → 🧩 Agent组件
```

**⚠️ CLI不是判定标准**：Claude Code有`claude`CLI但是Agent，ECC有`ecc`CLI但是组件——CLI只是接口形式

## 已确认的分类错误案例

| 项目 | 错误分类 | 正确分类 | 原因 |
|------|---------|---------|------|
| ARIS (⭐10,982) | 专精Agent | **Skills** | 描述写"Markdown-only skills" |
| Anthropic-Cybersecurity-Skills (⭐11,873) | 专精Agent | **Skills** | "754 structured cybersecurity skills" |
| mcp-context-forge (⭐3,787) | 专精Agent | **Agent组件** | AI Gateway/代理层，不是独立Agent |
| ADHD (⭐506) | Agent组件 | **Skills** | 描述含"skill for coding agents"，Tree-of-Thought推理规则文档 |

## 关键规则

- **绝不能凭stars数或名气判断分类**
- **必须读描述、查language、查topics**
- **全能Agent和专精Agent都是Agent，区别在通用vs垂直**
- **Skills可以有Python代码（用于安装/生成.md），但核心产物必须是.md**
- **Agent组件依赖其他Agent平台，不能独立运行**
- **CLI不是分类依据**：Agent和组件都可能有CLI（Claude Code有CLI但是Agent，ECC有CLI但是组件）
- **"需要其他Agent平台"是区分Agent和组件的关键**
