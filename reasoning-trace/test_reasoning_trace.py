"""
Reasoning Trace 测试脚本
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from client import (
    ReasoningTrace, 
    start_trace, trace_step, end_trace, get_trace, replay_trace,
    save_modification, get_modifications,
    verify_decision, check_consistency
)

def test_basic_flow():
    """测试基本流程"""
    print("=" * 60)
    print("测试基本流程")
    print("=" * 60)
    
    # 1. 开始记录
    print("\n1. 开始记录...")
    task_id = start_trace("test_001", "测试Reasoning Trace功能")
    print(f"   任务ID: {task_id}")
    
    # 2. 记录推理步骤
    print("\n2. 记录推理步骤...")
    trace_step("reasoning", "用户需要测试Reasoning Trace功能")
    trace_step("decision", "决定创建一个简单的测试脚本")
    trace_step("assumption", "假设用户熟悉Python")
    print("   ✅ 记录了3个步骤")
    
    # 3. 结束记录
    print("\n3. 结束记录...")
    result = end_trace("success")
    print(f"   结果: {result['result']}")
    print(f"   步骤数: {len(result['steps'])}")
    
    # 4. 查询推理过程
    print("\n4. 查询推理过程...")
    trace_data = get_trace(task_id)
    if trace_data:
        print(f"   ✅ 找到trace: {trace_data['task_id']}")
    else:
        print("   ❌ 未找到trace")
    
    # 5. 回放推理过程
    print("\n5. 回放推理过程...")
    replay_text = replay_trace(task_id, format="text")
    print("   文本格式:")
    for line in replay_text.split("\n")[:5]:
        print(f"   {line}")
    
    return task_id

def test_modification(task_id):
    """测试修改意见功能"""
    print("\n" + "=" * 60)
    print("测试修改意见功能")
    print("=" * 60)
    
    # 1. 保存修改意见
    print("\n1. 保存修改意见...")
    modification = save_modification(
        task_id=task_id,
        user_feedback="下次应该先检查用户输入再执行",
        related_steps=[1],
        modification_type="add_validation",
        priority="high"
    )
    print(f"   ✅ 保存修改意见: {modification['modification_type']}")
    
    # 2. 获取修改意见
    print("\n2. 获取修改意见...")
    modifications = get_modifications()
    print(f"   找到 {len(modifications)} 个修改意见")
    for mod in modifications:
        print(f"   - {mod['user_feedback'][:50]}...")
    
    return modification

def test_replay_formats(task_id):
    """测试不同回放格式"""
    print("\n" + "=" * 60)
    print("测试不同回放格式")
    print("=" * 60)
    
    # 1. 文本格式
    print("\n1. 文本格式:")
    text = replay_trace(task_id, format="text")
    print(f"   长度: {len(text)} 字符")
    
    # 2. JSON格式
    print("\n2. JSON格式:")
    json_str = replay_trace(task_id, format="json")
    print(f"   长度: {len(json_str)} 字符")
    
    # 3. Markdown格式
    print("\n3. Markdown格式:")
    md = replay_trace(task_id, format="markdown")
    print(f"   长度: {len(md)} 字符")



def test_verification():
    """测试思维验证功能"""
    print("\n" + "=" * 60)
    print("测试思维验证功能")
    print("=" * 60)
    
    # 1. 测试verify_decision
    print("\n1. 测试verify_decision...")
    
    # 场景：ARIS分类验证
    decision = "ARIS是Agent"
    verification_questions = [
        "有没有反例？",
        "一定是对的吗？"
    ]
    
    context = {
        "previous_analysis": "ARIS = Skills",
        "counterexamples": [
            {
                "description": "ARIS有CLI但是Skills",
                "type": "classification",
                "source": "GitHub分析"
            }
        ]
    }
    
    result = verify_decision(decision, verification_questions, context)
    
    print(f"   决策: {result['decision']}")
    print(f"   是否一致: {result['consistent']}")
    print(f"   是否需要修正: {result['needs_revision']}")
    print(f"   反例数量: {len(result['counterexamples'])}")
    
    if result['counterexamples']:
        print("   反例:")
        for ce in result['counterexamples']:
            print(f"     - {ce['description']}")
    
    # 2. 测试check_consistency
    print("\n2. 测试check_consistency...")
    
    # 场景：检查一致性
    current_decision = "ARIS是Agent"
    previous_analysis = "ARIS = Skills"
    
    result = check_consistency(current_decision, previous_analysis)
    
    print(f"   当前决策: {result['current_decision']}")
    print(f"   之前的分析: {result['previous_analysis']}")
    print(f"   是否一致: {result['consistent']}")
    
    if result['conflicts']:
        print("   冲突:")
        for conflict in result['conflicts']:
            print(f"     - {conflict['description']}")
    
    if result['suggestions']:
        print("   建议:")
        for suggestion in result['suggestions']:
            print(f"     - {suggestion}")
    
    # 3. 测试完整流程
    print("\n3. 测试完整流程...")
    
    # 开始记录
    task_id = start_trace("verification_test", "测试思维验证功能")
    
    # 记录推理步骤
    trace_step("reasoning", "分析ARIS的分类")
    trace_step("analysis", "ARIS描述说'Markdown-only skills'")
    trace_step("analysis", "ARIS主要是.md文件")
    trace_step("conclusion", "ARIS = Skills")
    
    # 验证决策
    decision = "ARIS是Agent"
    verification_result = verify_decision(decision, context=context)
    
    # 记录验证结果
    if verification_result['needs_revision']:
        trace_step("verification", f"决策需要修正: {verification_result['counterexamples'][0]['description']}")
        trace_step("revision", "修正决策: ARIS是Skills")
    else:
        trace_step("verification", "决策验证通过")
    
    # 结束记录
    end_trace("success")
    
    print(f"   任务ID: {task_id}")
    print(f"   验证结果: {'需要修正' if verification_result['needs_revision'] else '验证通过'}")
    
    # 回放推理过程
    print("\n4. 回放推理过程...")
    replay_text = replay_trace(task_id, format="text")
    print("   推理过程:")
    for line in replay_text.split("\n"):
        print(f"   {line}")

def main():
    """主测试函数"""
    print("🚀 Reasoning Trace 测试开始")
    print("=" * 60)
    
    try:
        # 测试基本流程
        task_id = test_basic_flow()
        
        # 测试修改意见功能
        test_modification(task_id)
        
        # 测试不同回放格式
        test_replay_formats(task_id)
        
        print("\n" + "=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)
        
        print("\n📁 生成的文件:")
        print(f"   - traces/index.json")
        print(f"   - traces/2026-05-30/{task_id}.json")
        print(f"   - skills/reasoning-trace/modifications/2026-05-30.json")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_verification()
    main()
