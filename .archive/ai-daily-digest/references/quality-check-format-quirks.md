# Quality Check Script Format Requirements

> These are the EXACT format expectations of `scripts/quality_check.py`.
> Violating any of these causes FAIL even if content is correct.

## 拆分分析 (Split Analysis)

The check looks for: `"按自主性" in report or "按成本" in report or "对比分析" in report`

✅ CORRECT:
```
### 🔍 拆分分析

**按自主性排名**：
1. **Agent A** — ⭐100,000
```

❌ WRONG (will FAIL):
```
### 🔍 拆分分析

**按Stars排名**：
1. **Agent A** — ⭐100,000
```

## 第X类格式 (Category Format)

The check looks for: `"第一类：" not in report and "第二类：" not in report`

This means category titles must NOT have colon+suffix.

✅ CORRECT:
```
### 📉 第一类
### 🔒 第二类
### ⚡ 第三类
### 🔬 第四类
### 🔍 第五类
### 📦 第六类
```

❌ WRONG (will FAIL):
```
### 📉 第一类：减少token消耗
### 🔒 第二类：约束agent行为
```

## emoji编号 (Emoji Numbering)

The check looks for: `"第二类：" not in report and "第三类：" not in report`

Same rule as above — no colon after category names anywhere in the report.

## 6类emoji覆盖

Must contain ALL 6 emojis: `📉 🔒 ⚡ 🔬 🔍 📦`

If a category has no data, still include the heading:
```
### 🔬 第四类

暂无数据
```

## Other Checks

- `Agent定义` must appear in report
- `全能Agent` or `全能型Agent` must appear
- `专精Agent` or `专精型Agent` must appear
- `对比含定价` — table must have `定价` or `成本` column
- `GitHub链接>=3` — at least 3 github.com links
- `Skills定义` must appear
- `Skills有原理` — must contain `原理`
- `MCP定义` or `Model Context Protocol` must appear
- `数据面板` must appear
- `核心信号` must appear, with ≥3 numbered items (`1. **...`)
- `AI基础` or `Day` must appear
- `今日目标`, `核心概念`, `延伸阅读`, `小测验` all required
- `板块顺序` — Agent生态 < Skills市场 < 模型动态
- `无标题重复` — exactly one `# 一、`
