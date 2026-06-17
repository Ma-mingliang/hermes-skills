---
name: ai-monthly-digest
description: "AI月度合订本生成 — 聚合上月所有日报，按taxonomy_config.yaml五大板块输出monthly_report.md + monthly_report.docx。触发词：AI月度合订本/AI月报/上月AI合集"
version: "1.0.0"
category: news
---

# AI Monthly Digest — 月度合订本生成

> 聚合上月所有日报，按五大板块输出月度合订本。

## 触发条件

- "生成上月 AI 月度合订本"
- "AI 月报"
- "上月 AI 合集"
- "monthly AI digest"

## 输入

- 上月所有日报：`D:/openclaw-hermes/data/daily/YYYY-MM-DD/report.md`
- 分类配置：`D:/openclaw-hermes/sources/taxonomy_config.yaml`（五大板块定义）

## 输出

| 文件 | 路径 |
|------|------|
| Markdown版 | `D:/openclaw-hermes/data/monthly/YYYY-MM/monthly_report.md` |
| Word版 | `D:/openclaw-hermes/data/monthly/YYYY-MM/monthly_report.docx` |

## 工作流程

### Step 1: 确定目标月份

- 当前日期为月初第1天（如6月1日）→ 目标月份为上个月（5月）
- 以 `YYYY-MM` 格式构造路径

### Step 2: 读取日报文件

```python
base = "D:/openclaw-hermes/data/daily"
reports = {}
for day in sorted(os.listdir(base)):
    if day.startswith("YYYY-MM"):
        report_path = os.path.join(base, day, "report.md")
        if os.path.exists(report_path):
            reports[day] = content
```

### Step 3: 读取 taxonomy_config.yaml

位于 `D:/openclaw-hermes/sources/taxonomy_config.yaml`，定义五大板块：
1. 📊 模型动态 (models)
2. 🤖 Agent 生态 (agents)
3. 🛠️ Skills 市场 (skills)
4. 🏭 行业应用 (industry)
5. 📖 AI 基础教育 (education)

### Step 4: 聚合分析

对五大板块分别：
- 提取所有日报中该板块的内容
- 识别跨日重复/持续热点（标注"🔥 持续热点"）
- 按重要性排序：🔴 ≥5源 > 🟡 3-4源 > ⚪ 1-2源
- 合并同类事件，保留最详细的描述

### Step 5: 生成 monthly_report.md

报告结构（必须严格遵守）：

```markdown
# 🤖 AI 月度合订本 | YYYY年M月

> 覆盖日期 / 数据来源 / 分类体系

## 📖 本月概览
（一段话概括本月最重大事件）

## 一、📊 模型动态
（新模型/价格变化/能力更新/学术前沿）

## 二、🤖 Agent 生态
（全能Agent/专精Agent/Agent组件/MCP动态）

## 三、🛠️ Skills 市场
（六大分类 + MCP动态，按skill类别组织）

## 四、🏭 行业应用
（A. AI行业重大事件 + B. 行业应用表格）

## 五、📖 AI 基础教育（历史回填）
（本月完成的每日概念教学汇总）

## 📊 月度数据统计
（覆盖天数/事件数/Agent数/Skills数/行业覆盖等）

## 🔮 月度核心信号（5-7条）
（趋势/安全/生态/模型/市场/行业/社会信号）
```

### Step 6: 生成 monthly_report.docx

使用 `python-docx`（已安装在 Anaconda 环境）：
- 标题：`🤖 AI 月度合订本 | YYYY年M月`
- 正文：微软雅黑 11pt
- 表格：Table Grid 样式，表头加粗
- 各板块标题：Heading 1 级别

### Step 7: 推送

输出摘要版到 final response（cron 模式自动推送），包含：
- 五大板块各1-2句话要点
- 🔮 核心信号列表
- 📂 文件路径

## 关键 Pitfalls

| ID | 规则 | 违反后果 |
|----|------|---------|
| M1 | 日报天数可能不完整（如仅5天），报告须在覆盖范围中如实标注 | 误导读者 |
| M2 | taxonomy_config.yaml 不在 `data/daily/` 下，在 `sources/` 下 | 文件找不到 |
| M3 | 使用 execute_code + Python 操作文件，terminal 在 Windows 上可能不可用 | 命令执行失败 |
| M4 | DOCX生成用 python-docx，不是 .NET DocxGenerator（后者需编译） | DOCX生成失败 |
| M5 | 跨日重复事件必须标注"🔥 持续热点"和连续天数 | 丢失热点追踪 |
| M6 | 模型/Agent/Skills数据必须带 Stars 数 + GitHub链接 | 无数据支撑 |
| M7 | 每月输出必须同时生成 .md 和 .docx | 缺少格式 |

## 依赖

- `python-docx`：DOCX 生成（Anaconda 环境已安装）
- `D:/openclaw-hermes/sources/taxonomy_config.yaml`：分类体系
- `D:/openclaw-hermes/data/daily/YYYY-MM-DD/report.md`：日报源文件
