# AI日报质量检查清单 (75项)

## 板块1: Agent生态 (18项)
- [ ] Agent定义
- [ ] 全能Agent板块
- [ ] 专精Agent板块
- [ ] Agent组件板块
- [ ] 📌使用指南
- [ ] 🆕新出现
- [ ] ⭐高星Agent
- [ ] 🧩高星组件
- [ ] 对比表(Agent+Stars)
- [ ] 对比含定位/成本/自主性/易用性
- [ ] 🔍拆分分析
- [ ] 📋归纳
- [ ] 每个Agent有GitHub链接 (>=10)
- [ ] 组件说明解决什么Agent的问题
- [ ] 组件有原理说明
- [ ] Agent有应用领域
- [ ] Agent有技术原理
- [ ] 新Agent有前辈对比

## 板块2: Skills市场 (12项)
- [ ] Skills定义
- [ ] 📉减少token
- [ ] 🔒约束行为
- [ ] ⚡增加功能
- [ ] 🔬科研辅助
- [ ] 🔍检测正常
- [ ] 📦补充类
- [ ] Skills有痛点
- [ ] Skills有原理
- [ ] Skills有案例
- [ ] Skills有GitHub链接 (>=15)
- [ ] Skills有前辈对比

## 板块3: 模型动态 (6项)
- [ ] 模型官网监控
- [ ] HN模型新闻
- [ ] OpenRouter数据
- [ ] 对比网站链接
- [ ] lmarena.ai
- [ ] artificialanalysis.ai

## 板块4: 行业热点 (6项)
- [ ] 行业热点
- [ ] 行业应用
- [ ] 有表格
- [ ] 有链接
- [ ] 36kr来源
- [ ] HN来源

## 板块5: MCP动态 (11项)
- [ ] MCP定义
- [ ] MCP项目表
- [ ] MCP七大分类
- [ ] 浏览器控制
- [ ] 代码智能
- [ ] 数据库
- [ ] 工作流
- [ ] API集成
- [ ] 安全
- [ ] 开发框架
- [ ] MCP有GitHub

## 板块6: 数据面板 (8项)
- [ ] 数据面板
- [ ] HN统计
- [ ] GitHub统计
- [ ] 全能Agent统计
- [ ] 专精Agent统计
- [ ] Skills统计
- [ ] 组件统计
- [ ] MCP统计

## 板块7: 核心信号 (3项)
- [ ] 核心信号
- [ ] 信号>=3条
- [ ] 信号有热度标注

## 板块8: AI基础知识 (8项)
- [ ] AI基础知识
- [ ] 今日目标
- [ ] 核心概念
- [ ] 为什么重要
- [ ] 常见误解
- [ ] 延伸阅读
- [ ] 小测验
- [ ] 主线标注

## 格式 (3项)
- [ ] 板块顺序正确
- [ ] 无标题重复
- [ ] 用emoji不用第X类

## 自动化检查脚本

```python
import re

def validate_report(report):
    checks = []
    def check(name, cond):
        checks.append({"name": name, "pass": cond})
    
    # 板块1
    check("Agent定义", "Agent定义" in report)
    check("全能Agent", "全能型Agent" in report)
    check("专精Agent", "专精型Agent" in report)
    check("Agent组件", "Agent组件" in report)
    check("使用指南", "使用指南" in report)
    check("高星Agent", "高星" in report)
    check("对比表", "| Agent" in report)
    check("拆分分析", "拆分分析" in report)
    check("归纳", "归纳" in report)
    check("GitHub链接", report.count("github.com") >= 10)
    
    # 板块2
    check("Skills定义", "Skills定义" in report)
    check("6类emoji", all(c in report for c in ["📉", "🔒", "⚡", "🔬", "🔍", "📦"]))
    check("痛点", "痛点" in report)
    check("原理", "原理" in report)
    
    # 板块3-8
    check("模型动态", "模型动态" in report)
    check("行业热点", "行业热点" in report)
    check("MCP动态", "MCP动态" in report)
    check("数据面板", "数据面板" in report)
    check("核心信号", "核心信号" in report)
    check("AI基础", "AI基础" in report or "Day" in report)
    check("今日目标", "今日目标" in report)
    check("小测验", "小测验" in report)
    
    # 格式
    check("无第X类", "第一类：" not in report and "第二类：" not in report)
    
    passed = sum(1 for c in checks if c["pass"])
    total = len(checks)
    failed = [c["name"] for c in checks if not c["pass"]]
    
    return {"passed": passed, "total": total, "failed": failed}
```
