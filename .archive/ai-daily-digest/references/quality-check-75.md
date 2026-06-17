# 质量检查清单 — 75项完整版

> 验证日期：2026-05-31
> 用途：报告生成后逐项对照，全部通过才能推送

## 使用方法

```python
def validate_report(report):
    checks = []
    def check(name, cond):
        checks.append({"name": name, "pass": cond})
    
    # 板块1: Agent生态 (18项)
    check("Agent定义", "Agent定义" in report)
    check("全能Agent板块", "全能型Agent" in report)
    check("专精Agent板块", "专精型Agent" in report)
    check("Agent组件板块", "Agent组件" in report)
    check("📌使用指南", "使用指南" in report)
    check("🆕新出现", "新出现" in report)
    check("⭐高星Agent", "高星" in report)
    check("🧩高星组件", "高星Agent组件" in report)
    check("对比表(Agent+Stars)", "| Agent" in report and "Stars" in report)
    check("对比含定位/成本/自主性/易用性", all(w in report for w in ["定位", "成本", "自主性", "易用性"]))
    check("🔍拆分分析", "拆分分析" in report)
    check("📋归纳", "归纳" in report)
    check("每个Agent有GitHub链接", report.count("github.com") >= 10)
    check("组件说明解决什么Agent的问题", "解决什么" in report)
    check("组件有原理说明", "核心原理" in report)
    check("Agent有应用领域", "应用领域" in report)
    check("Agent有技术原理", "技术原理" in report)
    check("新Agent有前辈对比", "前辈对比" in report)
    
    # 板块2: Skills市场 (12项)
    check("Skills定义", "Skills定义" in report)
    check("📉减少token", "📉" in report and "减少token" in report)
    check("🔒约束行为", "🔒" in report and "约束" in report)
    check("⚡增加功能", "⚡" in report and "增加功能" in report)
    check("🔬科研辅助", "🔬" in report and "科研" in report)
    check("🔍检测正常", "🔍" in report and "检测" in report)
    check("📦补充类", "📦" in report)
    check("Skills有痛点", "痛点" in report)
    check("Skills有原理", "原理" in report)
    check("Skills有案例", "案例" in report)
    check("Skills有GitHub链接", report.count("github.com") >= 15)
    check("Skills有前辈对比", "前辈对比" in report)
    
    # 板块3: 模型动态 (6项)
    check("模型官网监控", "官网" in report or "模型动态" in report)
    check("HN模型新闻", any(kw in report for kw in ["Claude", "DeepSeek", "Opus"]))
    check("OpenRouter数据", "OpenRouter" in report)
    check("对比网站链接", "openrouter.ai" in report)
    check("lmarena.ai", "lmarena.ai" in report)
    check("artificialanalysis.ai", "artificialanalysis.ai" in report)
    
    # 板块4: 行业热点 (6项)
    check("行业热点", "行业热点" in report)
    check("行业应用", "行业应用" in report)
    check("有表格", "| 行业" in report)
    check("有链接", "链接" in report)
    check("36kr来源", "36kr" in report)
    check("HN来源", "HN" in report)
    
    # 板块5: MCP动态 (11项)
    check("MCP定义", "MCP定义" in report or "Model Context Protocol" in report)
    check("MCP项目表", "| MCP" in report)
    check("MCP七大分类", "七大分类" in report)
    check("浏览器控制", "浏览器控制" in report)
    check("代码智能", "代码智能" in report)
    check("数据库", "数据库" in report)
    check("工作流", "工作流" in report)
    check("API集成", "API集成" in report)
    check("安全", "安全" in report)
    check("开发框架", "开发框架" in report)
    check("MCP有GitHub", "mcp" in report.lower() and "github.com" in report)
    
    # 板块6: 数据面板 (8项)
    check("数据面板", "数据面板" in report)
    check("HN统计", "HN" in report)
    check("GitHub统计", "GitHub" in report)
    check("全能Agent统计", "全能Agent" in report)
    check("专精Agent统计", "专精Agent" in report)
    check("Skills统计", "Skills" in report)
    check("组件统计", "Agent组件" in report)
    check("MCP统计", "MCP" in report)
    
    # 板块7: 核心信号 (3项)
    check("核心信号", "核心信号" in report)
    sig_count = len(re.findall(r'\d+\.\s+\*\*', report))
    check("信号>=3条", sig_count >= 3)
    check("信号有热度标注", "pts" in report)
    
    # 板块8: AI基础知识 (8项)
    check("AI基础知识", "AI基础" in report or "Day" in report)
    check("今日目标", "今日目标" in report)
    check("核心概念", "核心概念" in report)
    check("为什么重要", "为什么重要" in report)
    check("常见误解", "常见误解" in report)
    check("延伸阅读", "延伸阅读" in report)
    check("小测验", "小测验" in report)
    check("主线标注", "主线" in report)
    
    # 格式 (3项)
    check("板块顺序正确", report.index("Agent生态") < report.index("Skills市场") < report.index("模型动态"))
    check("无标题重复", report.count("# 一、") == 1)
    check("用emoji不用第X类", "第一类：" not in report and "第二类：" not in report)
    
    # 统计
    passed = sum(1 for c in checks if c["pass"])
    total = len(checks)
    failed = [c["name"] for c in checks if not c["pass"]]
    
    return {"passed": passed, "total": total, "failed": failed}
```

## 检查项分布

| 板块 | 检查项数 | 重点检查 |
|------|---------|---------|
| Agent生态 | 18 | 前辈对比、组件原理、GitHub链接 |
| Skills市场 | 12 | 6类emoji、痛点+原理+案例+前辈对比 |
| 模型动态 | 6 | 对比网站链接、HN模型新闻 |
| 行业热点 | 6 | 表格格式、来源链接 |
| MCP动态 | 11 | 七大分类全覆盖 |
| 数据面板 | 8 | 分类统计完整 |
| 核心信号 | 3 | 数量>=3、热度标注 |
| AI基础 | 8 | 主线标注、小测验 |
| 格式 | 3 | emoji编号、板块顺序 |

## 常见失败项

1. **Skills缺前辈对比** — 必须每个新Skill找同类前辈
2. **MCP分类不足** — 必须覆盖7大分类
3. **行业覆盖不足** — 至少3个行业
4. **用"第X类"而非emoji** — 必须用📉🔒⚡🔬🔍📦
5. **组件缺原理说明** — 必须说明解决什么Agent的什么问题
6. **数据来源不透明** — 量化效果数据必须有来源，无来源必须删除或标注"未能获取"
