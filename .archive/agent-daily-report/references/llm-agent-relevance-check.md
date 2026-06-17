# LLM Agent 相关性判断 (P78)

## 问题

`has_strong_agent_signal` 基于关键词匹配，漏掉以下类型的项目：
- CodexPlusPlus：Codex 增强器，但描述不含 "agent" 关键词
- PaperSpine：Agent Skill，但描述不含 "skill" 关键词
- GordenPPTSkill：Agent Skill，同上

## 解决方案

对关键词不通过的候选，用 LLM 读取 README 逐个判断。

### 实现方式

1. 收集不通过 `has_strong_agent_signal` 的候选
2. 逐个获取 GitHub README（前 3000 字符）
3. 逐个调用 LLM 判断（batch_size=1，最准确）
4. LLM 返回 `{relevant: true/false, category: "...", reason: "..."}`

### Prompt 模板

```
System: 你是 Agent 生态情报分析专家。根据 README 判断该项目是否与 Agent 生态相关。

Agent 生态包括：AI Agent 框架/运行时、Coding Agent/代码生成、MCP 服务器/工具、
Agent Skill/可复用能力包、Agent 工作流编排、Agent 浏览器/终端自动化、
多智能体协作、Agent 记忆/上下文管理。

返回 JSON：{"relevant": true/false, "category": "分类", "reason": "一句话原因"}

User: 项目：{repo}\n\nREADME：\n{readme}
```

### 用户偏好

- **逐个判断**（非批量）：每个项目获得 LLM 全部注意力，不会互相干扰
- **Skill 必须收录**：只要是 Skill 或能增强 Agent 的工具都收录
- **增强器也要收录**：如 CodexPlusPlus 这类增强 Coding Agent 的工具

### 2026-06-04 实测结果

13个候选全部通过 LLM 判断（11个关键词通过 + 2个 LLM 兜底通过）：
- CodexPlusPlus：LLM 判断为 "Coding Agent 增强器"
- ian-xiaohei-illustrations：LLM 判断为 "Agent Skill"（生成插画）
- PaperSpine：LLM 判断为 "Agent Skill"
- GordenPPTSkill：LLM 判断为 "Agent Skill"
