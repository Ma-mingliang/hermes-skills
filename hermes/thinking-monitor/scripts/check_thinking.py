#!/usr/bin/env python3
"""
思维快速检查脚本 (Thinking Quick Check)
========================================
在做出重要决策前运行此脚本进行快速自检。

Usage:
    python check_thinking.py                    # 交互式检查
    python check_thinking.py --auto             # 自动输出清单
    python check_thinking.py --bias-check       # 仅偏差检查
"""

import sys


def print_banner():
    print("""
╔══════════════════════════════════════════════╗
║         ⚡ 思维快速检查 ⚡                    ║
║     Thinking Monitor Quick Check             ║
╚══════════════════════════════════════════════╝
""")


def thinking_quick_check():
    """4-dimension quick check"""
    checks = [
        {
            "icon": "🧠",
            "question": "我有没有跳步？",
            "detail": "推理链是否完整？前提→推理→结论是否清晰？",
            "red_flags": [
                "直接从问题跳到结论，缺中间步骤",
                "没有显式列出前提/假设",
                "推理中使用了未说明的隐含知识",
            ],
        },
        {
            "icon": "🛡️",
            "question": "反方观点是什么？",
            "detail": "是否有确认偏差？备选方案是否被认真考虑？",
            "red_flags": [
                "只搜索了支持当前观点的证据",
                "第一个想出的方案就采用了",
                "没有认真评估至少2个替代方案",
            ],
        },
        {
            "icon": "📚",
            "question": "我的信息够吗？",
            "detail": "是否使用了多源验证？是否存在知识盲区？",
            "red_flags": [
                "关键决策只依赖1个信息来源",
                "没有对重要事实进行交叉验证",
                "没有标注不确定的区域",
            ],
        },
        {
            "icon": "⚡",
            "question": "这个分析深度合适吗？",
            "detail": "任务复杂度(1-5)是否与分析深度匹配？",
            "red_flags": [
                "简单任务过度分析（10+步推理）",
                "复杂任务草率下结论",
                "工具调用次数与任务复杂度的比率异常",
            ],
        },
        {
            "icon": "❓",
            "question": "我的置信度合理吗？",
            "detail": "是否使用了绝对化表述？不确定性是否被标注？",
            "red_flags": [
                "使用了'一定''肯定''绝对'等绝对化词语",
                "高确定性断言但缺乏证据支撑",
                "没有标注置信度/概率范围",
            ],
        },
    ]

    print_banner()
    for i, check in enumerate(checks, 1):
        print(f"\n{i}. {check['icon']} {check['question']}")
        print(f"   → {check['detail']}")
        print(f"   🚩 红旗信号:")
        for flag in check['red_flags']:
            print(f"      □ {flag}")

    print("\n" + "-" * 50)
    print("\n📋 请逐条确认上述检查点后，再继续执行任务。\n")


def bias_checklist():
    """Cognitive bias self-check"""
    biases = [
        ("确认偏差", "我是否在回避反面证据？只搜索支持性信息？"),
        ("锚定效应", "我是否过度依赖第一个方案？替代方案被真正评估了吗？"),
        ("过度自信", "我是否把假设当成确定事实？确定性表述有证据吗？"),
        ("幸存者偏差", "我是否只考虑了成功案例，忽略了失败案例？"),
        ("可用性启发", "我是否被近期/最易回忆的信息过度影响？"),
        ("框架效应", "换个方式/角度问自己，结论会变吗？"),
        ("沉没成本", "我是否因为已经投入了而努力坚持当前方向？"),
        ("基本归因错误", "我是否只归因于个人/Agent，忽略了系统/环境因素？"),
    ]

    print_banner()
    print("📋 偏差自检清单\n")

    warning_count = 0
    for name, question in biases:
        print(f"  □ {name}: {question}")
        # In auto mode with --strict, ask for input
        if "--strict" in sys.argv:
            answer = input(f"    通过? (y/n/回车=跳过): ").strip().lower()
            if answer == 'n':
                print(f"     ⚠️ 请先解决 {name} 再继续！")
                warning_count += 1

    print("\n" + "-" * 50)
    if warning_count > 0:
        print(f"🔴 发现 {warning_count} 个未通过的偏差检查，建议暂停并自我纠正。")
    else:
        print("✅ 偏差检查完成。如未发现明显问题，可以继续。")

    return warning_count


def main():
    if "--bias-check" in sys.argv:
        bias_checklist()
    elif "--auto" in sys.argv:
        # Non-interactive output
        print("""
⚡ 思维快速检查 (Auto Mode)

1. 🧠 逻辑链完整？  前提→推理→结论无跳跃？  [  ]
2. 🛡️ 反方观点？    确认偏差？备选方案？    [  ]
3. 📚 信息充分？    多源验证？盲区标注？    [  ]
4. ⚡ 效率匹配？    复杂度 vs 分析深度？    [  ]
5. ❓ 置信度合理？  绝对化？不确定性标注？  [  ]

偏差清单:
  □ 确认偏差  □ 锚定效应  □ 过度自信  □ 幸存者偏差
  □ 可用性启发  □ 框架效应  □ 沉没成本  □ 基本归因错误
""")
    else:
        thinking_quick_check()
        bias_checklist()


if __name__ == "__main__":
    main()
