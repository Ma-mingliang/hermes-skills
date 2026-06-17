# 分类-报告一致性修复记录 (2026-05-30)

## 问题

数据采集阶段（Phase 1-4）正确分类了项目，但写报告时凭印象或搜索来源重新分类，导致项目被放入错误板块。

## 错误案例

**ADHD** (github.com/UditAkhourii/adhd, ⭐542)
- 描述: "ADHD — a **skill** for coding agents. Tree-of-thought with pruning"
- Phase 4 分类代码结果: `[skill]` ✅
- 报告中放置位置: "🆕 新出现Agent" ❌
- 正确位置: "📚 Skills市场"

## 根因分析

1. 数据采集使用多个搜索查询（"AI+agent"、"claude+skill"等）
2. ADHD出现在"AI+agent"搜索结果中（因为描述含"agents"）
3. 写报告时，我凭"搜索来源"（agent搜索）而非"分类标签"（skill）决定板块
4. 采集阶段和报告生成之间的分类标签没有传递

## 修复方案（已实施）

### 代码层面
数据采集时为每个项目打分类标签：
```python
if "skill" in desc or "skill" in name:
    cls = "skill"
elif any(kw in desc for kw in ["plugin", "extension", "for claude", ...]):
    cls = "component"
elif any(kw in desc for kw in ["api", "web ui", "platform", ...]):
    cls = "agent"
else:
    cls = "component"
```

### 流程层面
报告生成时按分类标签分组：
```python
skills = [r for r in data if r["classification"] == "skill"]
agents = [r for r in data if r["classification"] == "agent"]
components = [r for r in data if r["classification"] == "component"]
```

## 修复效果验证

修复后分类统计：
- 📚 Skills: 19个（含ADHD、Vibecode、guizang等）
- 🧩 Components: 21个（含Agent OSS、Cursor Status Light等）
- 🤖 Agents: 2个

ADHD正确放在Skills板块 ✅

## 涉及文件

- SKILL.md: 新增P13简要规则
- references/SKILL-balanced.md: 新增P13含错误案例
- SKILL-full.md: 新增P13完整修复流程+验证命令
