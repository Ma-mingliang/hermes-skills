#!/usr/bin/env python3
"""
AI日报质量检查脚本 v2
新增：行业覆盖检查、专精Agent检查
"""

import re, sys, os

def check_report(report_path):
    """检查报告质量"""
    with open(report_path, "r", encoding="utf-8") as f:
        report = f.read()
    
    checks = []
    
    def check(name, cond, detail=""):
        checks.append({"name": name, "pass": cond, "detail": detail})
        s = "PASS" if cond else "FAIL"
        print(f"  [{s}] {name}" + (f" ({detail})" if detail else ""))
    
    print("=" * 60)
    print(f"质量检查: {report_path}")
    print("=" * 60)
    
    # 板块1: Agent生态
    print("\n[板块1] Agent生态")
    check("Agent定义", "Agent定义" in report)
    check("全能Agent", "高星全能Agent" in report)
    check("专精Agent", "高星专精Agent" in report)
    check("Agent组件", "Agent组件" in report)
    check("使用指南", "使用指南" in report)
    check("对比表", "| Agent" in report)
    check("前辈对比", "前辈对比" in report)
    check("GitHub链接>=10", report.count("github.com") >= 10)
    
    # 板块2: Skills市场
    print("\n[板块2] Skills市场")
    check("Skills定义", "Skills定义" in report)
    emoji_cats = ["📉", "🔒", "⚡", "🔬", "🔍", "📦"]
    check("6类emoji", all(c in report for c in emoji_cats))
    check("痛点", "痛点" in report)
    check("原理", "原理" in report)
    
    # 板块3: 模型动态
    print("\n[板块3] 模型动态")
    check("模型动态", "模型动态" in report)
    check("OpenRouter", "openrouter.ai" in report)
    
    # 板块4: 行业热点
    print("\n[板块4] 行业热点")
    check("行业热点", "行业" in report)
    industry_emojis = ["🏭", "💼", "🏥", "🎓", "💰", "⚖️", "🔐", "🌾", "🚗", "🎮"]
    found_ind = [e for e in industry_emojis if e in report]
    check("行业覆盖>=3", len(found_ind) >= 3, f"实际{len(found_ind)}个")
    
    # 板块5: MCP动态
    print("\n[板块5] MCP动态")
    check("MCP定义", "MCP" in report)
    check("MCP七大分类", "七大分类" in report)
    
    # 板块6: 数据面板
    print("\n[板块6] 数据面板")
    check("数据面板", "数据面板" in report)
    check("今日/本周/历史区分", "今日" in report and "本周" in report and "历史" in report)
    
    # 板块7: 核心信号
    print("\n[板块7] 核心信号")
    check("核心信号", "核心信号" in report)
    sig_count = len(re.findall(r'\d+\.\s+\*\*', report))
    check("信号>=3条", sig_count >= 3, f"实际{sig_count}条")
    
    # 板块8: AI基础知识
    print("\n[板块8] AI基础知识")
    check("AI基础", "AI基础" in report or "Day" in report)
    check("今日目标", "今日目标" in report)
    check("小测验", "小测验" in report)
    
    # 格式
    print("\n[格式]")
    check("无第X类", "第一类：" not in report and "第二类：" not in report)
    
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
    
    return {"passed": passed, "total": total, "failed": [c["name"] for c in checks if not c["pass"]]}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        report_path = sys.argv[1]
    else:
        report_path = "D:/openclaw-hermes/data/daily/2026-05-31/report_fresh.md"
    
    result = check_report(report_path)
    sys.exit(0 if result["failed"] == [] else 1)
