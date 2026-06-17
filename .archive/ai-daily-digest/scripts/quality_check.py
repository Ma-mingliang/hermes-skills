#!/usr/bin/env python3
"""
AI日报质量检查脚本
自动验证报告是否符合ai-daily-digest skill要求
用法: python quality_check.py <report_path>
退出码: 0=全部通过, 1=有未通过项
"""

import re, sys, os

def check_report(report_path):
    with open(report_path, "r", encoding="utf-8") as f:
        report = f.read()

    checks = []

    def check(name, condition, detail=""):
        status = "PASS" if condition else "FAIL"
        checks.append({"name": name, "pass": condition, "detail": detail})
        print(f"  [{status}] {name}" + (f" ({detail})" if detail else ""))

    print("=" * 60)
    print(f"质量检查: {report_path}")
    print("=" * 60)

    # 板块1: Agent生态
    print("\n[板块1] Agent生态")
    check("Agent定义", "Agent定义" in report)
    check("全能Agent", "全能型Agent" in report or "全能Agent" in report)
    check("专精Agent", "专精型Agent" in report or "专精Agent" in report)
    check("Agent组件", "Agent组件" in report)
    check("使用指南", "使用指南" in report)
    check("高星Agent", "高星" in report)
    check("对比表", "| Agent" in report)
    check("对比含定价", "定价" in report or "成本" in report)
    check("拆分分析", "按自主性" in report or "按成本" in report or "对比分析" in report)
    check("归纳推荐", "归纳" in report or "推荐" in report)
    check("GitHub链接>=3", report.count("github.com") >= 3)
    check("组件解决问题", "解决什么" in report)

    # 板块2: Skills市场
    print("\n[板块2] Skills市场")
    check("Skills定义", "Skills定义" in report)
    emoji_cats = ["📉", "🔒", "⚡", "🔬", "🔍", "📦"]
    missing = [c for c in emoji_cats if c not in report]
    check("6类emoji覆盖", len(missing) == 0, f"缺失: {missing}")
    check("Skills有GitHub", "github.com" in report)
    check("Skills有原理", "原理" in report)
    check("无第X类格式", "第一类：" not in report and "第二类：" not in report)

    # 板块3: 模型动态
    print("\n[板块3] 模型动态")
    check("模型动态", "模型动态" in report)
    check("模型新闻", any(kw in report for kw in ["Claude", "DeepSeek", "Opus", "GPT"]))
    check("对比网站", "openrouter.ai" in report or "lmarena.ai" in report)

    # 板块4: 行业热点
    print("\n[板块4] 行业热点")
    check("行业热点", "行业" in report)
    check("有表格", "|" in report and "---" in report)
    check("有链接", "链接" in report or "http" in report)

    # 板块5: MCP动态
    print("\n[板块5] MCP动态")
    check("MCP定义", "MCP定义" in report or "Model Context Protocol" in report)
    check("MCP项目", "MCP" in report)

    # 板块6: 数据面板
    print("\n[板块6] 数据面板")
    check("数据面板", "数据面板" in report)
    check("HN统计", "HN" in report)
    check("GitHub统计", "GitHub" in report)

    # 板块7: 核心信号
    print("\n[板块7] 核心信号")
    check("核心信号", "核心信号" in report)
    sig_count = len(re.findall(r'\d+\.\s+\*\*', report))
    check("信号>=3条", sig_count >= 3, f"实际{sig_count}条")

    # 板块8: AI基础知识
    print("\n[板块8] AI基础知识")
    check("AI基础知识", "AI基础" in report or "Day" in report)
    check("今日目标", "今日目标" in report)
    check("核心概念", "核心概念" in report)
    check("延伸阅读", "延伸阅读" in report)
    check("小测验", "小测验" in report)

    # 格式
    print("\n[格式]")
    check("板块顺序", report.index("Agent生态") < report.index("Skills市场") < report.index("模型动态"))
    check("无标题重复", report.count("# 一、") == 1)
    check("emoji编号", "第二类：" not in report and "第三类：" not in report)

    # 链接统计
    print("\n[链接统计]")
    gh_links = len(re.findall(r"github\.com/\S+", report))
    total_links = len(re.findall(r"https?://\S+", report))
    print(f"  GitHub链接: {gh_links}个")
    print(f"  总链接: {total_links}个")

    # 总结
    total = len(checks)
    passed = sum(1 for c in checks if c["pass"])
    failed = total - passed

    print(f"\n{'='*60}")
    print(f"结果: {passed}/{total} 通过, {failed} 未通过")

    if failed > 0:
        print("\n未通过项:")
        for c in checks:
            if not c["pass"]:
                print(f"  FAIL: {c['name']}")

    return {"total": total, "passed": passed, "failed": failed}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        report_path = sys.argv[1]
    else:
        report_path = "D:/openclaw-hermes/data/daily/2026-05-31/report.md"

    result = check_report(report_path)
    sys.exit(0 if result["failed"] == 0 else 1)
