# 分类教训总览（2026-05-30）

## 7个分类错误

| 项目 | 错误分类 | 正确分类 | 根因 |
|------|---------|---------|------|
| ADHD | 🤖Agent | 📚Skills | 凭搜索来源分类，未查分类标签 |
| Agent OSS | 🤖Agent | 🧩组件 | 机械匹配"能独立运行→Agent" |
| Gemini CLI | 🧩组件 | 🤖Agent | 代码bug："cli not in desc" |
| AutoRun | 🧩组件 | 🤖Agent | 代码bug同上 |
| WHOOP MCP | 🧩组件 | 🔌MCP | 通用分类优先，未用专用分类 |
| Vibecode | 🤖Agent | 📚Skills | 凭搜索来源分类 |
| OpenMobius | 🤖Agent | 📚Skills | 凭搜索来源分类 |

## 思维模式问题

### 错误模式：机械关键词匹配
```
描述含"runtime" → 能独立运行 → Agent（错误）
描述含"cli" → 排除Agent（错误）
```

### 正确模式：先理解→再分类→最后验证
1. **理解**：它是什么？谁用它？用它做什么？
2. **分类**：根据理解选择最具体的分类
3. **验证**：检查是否符合skill规则

## 关键判断规则

| 信号 | 含义 | 分类 |
|------|------|------|
| "for ai agents" / "for claude" | 给Agent用的基础设施 | 🧩组件 |
| "ai agent" / "agent for" | 用AI帮你做事 | 🤖Agent |
| "skill" / 主要是.md | 约束AI行为的规则 | 📚Skills |
| "mcp server" / "model context protocol" | Agent工具接口 | 🔌MCP |
| "runtime" / "framework" | 执行环境/框架 | 🧩组件 |
| "能独立运行" | 必要条件，非充分条件 | 需进一步判断 |

## 代码修复

```python
# 旧代码（错误）
elif ... and "cli" not in desc:  # 违反P0规则
    cls = "agent"

# 新代码（正确）
if "skill" in desc or "skill" in name:
    cls = "skill"
elif any(kw in desc for kw in ["mcp server", "model context protocol"]):
    cls = "mcp"
elif any(kw in desc for kw in ["for ai agents", "for claude", "let ai agents"]):
    cls = "component"
elif any(kw in desc for kw in ["ai agent", "agent for", "autonomous"]):
    cls = "agent"
else:
    cls = "component"
```
