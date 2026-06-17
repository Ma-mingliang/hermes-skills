#!/usr/bin/env python3
"""
AI日报数据验证脚本
验证数据时间戳，区分今日/本周/历史
"""

import json
from datetime import datetime, timedelta

def verify_data_timestamps(hn_items, gh_repos, today_str, week_ago_str):
    """验证数据时间戳，区分今日/本周/历史"""
    
    # HN数据分类
    hn_today = []  # 今日新闻
    hn_week = []   # 本周新闻（非今日）
    hn_old = []    # 更早新闻
    
    for h in hn_items:
        created = h.get("created", "")[:10]
        if created == today_str:
            hn_today.append(h)
        elif created >= week_ago_str:
            hn_week.append(h)
        else:
            hn_old.append(h)
    
    # GitHub数据分类
    gh_today = []   # 今日创建
    gh_week = []    # 本周创建（非今日）
    gh_old = []     # 历史项目（高星参考）
    
    for r in gh_repos:
        created = r.get("created", "")[:10]
        if created == today_str:
            gh_today.append(r)
        elif created >= week_ago_str:
            gh_week.append(r)
        else:
            gh_old.append(r)
    
    # 输出验证报告
    print("[数据验证]")
    print(f"HN: 今日{len(hn_today)}条, 本周{len(hn_week)}条, 更早{len(hn_old)}条")
    print(f"GitHub: 今日{len(gh_today)}个, 本周{len(gh_week)}个, 历史高星{len(gh_old)}个")
    
    # 验证规则
    issues = []
    
    if len(hn_today) == 0:
        issues.append("今日HN为0，报告中不能出现'今日新闻'板块")
    
    if len(gh_today) == 0 and len(gh_week) == 0:
        issues.append("本周GitHub新增为0，报告中不能出现'🆕新出现'板块")
    
    if issues:
        print("\n[验证问题]")
        for issue in issues:
            print(f"  ⚠️ {issue}")
    
    return {
        "hn": {"today": hn_today, "week": hn_week, "old": hn_old},
        "github": {"today": gh_today, "week": gh_week, "old": gh_old},
        "issues": issues
    }

def check_report_accuracy(report, verification):
    """检查报告标题是否与数据匹配"""
    
    issues = []
    
    # 检查🆕板块
    if "🆕 新出现" in report:
        if len(verification["github"]["today"]) == 0 and len(verification["github"]["week"]) == 0:
            issues.append("报告有🆕板块，但本周GitHub新增为0")
    
    # 检查今日新闻
    if "今日新闻" in report or "今日HN" in report:
        if len(verification["hn"]["today"]) == 0:
            issues.append("报告有'今日新闻'，但今日HN为0")
    
    # 检查HN热点标注
    if "本周HN热点" in report:
        # 检查是否有HN热度>100的项目
        high_heat = [h for h in verification["hn"]["week"] if h.get("points", 0) > 100]
        if len(high_heat) == 0:
            issues.append("报告标注'本周HN热点'，但没有HN热度>100的项目")
    
    if issues:
        print("\n[报告准确性检查]")
        for issue in issues:
            print(f"  ❌ {issue}")
    
    return issues

# 示例用法
if __name__ == "__main__":
    import sys
    
    # 读取数据
    out_dir = "D:/openclaw-hermes/data/daily/2026-05-31"
    
    with open(f"{out_dir}/phase1_full.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    week_ago = datetime.now() - timedelta(days=7)
    week_ago_str = week_ago.strftime("%Y-%m-%d")
    
    # 验证数据
    verification = verify_data_timestamps(
        data["hn"]["items"],
        data["github"]["repos"],
        today_str,
        week_ago_str
    )
    
    # 读取报告
    with open(f"{out_dir}/report_fixed.md", "r", encoding="utf-8") as f:
        report = f.read()
    
    # 检查报告准确性
    check_report_accuracy(report, verification)
