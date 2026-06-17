"""
流程思维 Skill 测试脚本
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from client import (
    decompose_task, 
    get_process_template, 
    create_custom_process,
    execute_process,
    optimize_process,
    get_process_by_id,
    list_processes,
    format_process
)


def test_decompose_task():
    """测试任务拆分"""
    print("=" * 60)
    print("测试任务拆分")
    print("=" * 60)
    
    # 测试学习任务
    print("\n1. 测试学习任务拆分...")
    result = decompose_task("学习Python", task_type="learning")
    print(f"   任务: {result['task']}")
    print(f"   类型: {result['type']}")
    print(f"   环节数: {result['total_steps']}")
    print(f"   预计时间: {result['estimated_total_time']}")
    
    # 测试开发任务
    print("\n2. 测试开发任务拆分...")
    result = decompose_task("开发登录功能", task_type="development")
    print(f"   任务: {result['task']}")
    print(f"   类型: {result['type']}")
    print(f"   环节数: {result['total_steps']}")
    
    # 测试写作任务
    print("\n3. 测试写作任务拆分...")
    result = decompose_task("写技术博客", task_type="writing")
    print(f"   任务: {result['task']}")
    print(f"   类型: {result['type']}")
    print(f"   环节数: {result['total_steps']}")
    
    # 测试自动识别
    print("\n4. 测试自动识别任务类型...")
    result = decompose_task("学习机器学习")
    print(f"   任务: {result['task']}")
    print(f"   类型: {result['type']} (自动识别)")
    
    return result


def test_get_template():
    """测试获取模板"""
    print("\n" + "=" * 60)
    print("测试获取模板")
    print("=" * 60)
    
    # 获取学习模板
    print("\n1. 获取学习模板...")
    template = get_process_template("learning")
    print(f"   名称: {template['name']}")
    print(f"   类型: {template['type']}")
    print(f"   环节数: {template['total_steps']}")
    
    # 获取开发模板
    print("\n2. 获取开发模板...")
    template = get_process_template("development")
    print(f"   名称: {template['name']}")
    print(f"   类型: {template['type']}")
    
    # 获取写作模板
    print("\n3. 获取写作模板...")
    template = get_process_template("writing")
    print(f"   名称: {template['name']}")
    print(f"   类型: {template['type']}")


def test_format_process():
    """测试格式化流程"""
    print("\n" + "=" * 60)
    print("测试格式化流程")
    print("=" * 60)
    
    # 创建一个流程
    process = decompose_task("学习Python", task_type="learning")
    
    # 文本格式
    print("\n1. 文本格式:")
    text = format_process(process, format="text")
    print(text[:500])
    print("...")
    
    # JSON格式
    print("\n2. JSON格式:")
    json_str = format_process(process, format="json")
    print(f"   长度: {len(json_str)} 字符")
    
    # Markdown格式
    print("\n3. Markdown格式:")
    md = format_process(process, format="markdown")
    print(md[:500])
    print("...")


def test_custom_process():
    """测试自定义流程"""
    print("\n" + "=" * 60)
    print("测试自定义流程")
    print("=" * 60)
    
    # 创建自定义流程
    print("\n1. 创建自定义流程...")
    steps = [
        {
            "step": 1,
            "name": "准备",
            "description": "准备工作",
            "tasks": ["收集资料", "制定计划"],
            "estimated_time": "30分钟",
            "dependencies": []
        },
        {
            "step": 2,
            "name": "执行",
            "description": "执行任务",
            "tasks": ["按计划执行", "记录进度"],
            "estimated_time": "60分钟",
            "dependencies": [1]
        },
        {
            "step": 3,
            "name": "总结",
            "description": "总结经验",
            "tasks": ["总结经验", "改进方法"],
            "estimated_time": "30分钟",
            "dependencies": [2]
        }
    ]
    
    process = create_custom_process("自定义测试流程", steps)
    print(f"   ID: {process['id']}")
    print(f"   名称: {process['name']}")
    print(f"   环节数: {process['total_steps']}")
    
    return process


def test_list_processes():
    """测试列出流程"""
    print("\n" + "=" * 60)
    print("测试列出流程")
    print("=" * 60)
    
    processes = list_processes()
    print(f"\n找到 {len(processes)} 个流程:")
    for p in processes:
        print(f"  - {p['id']}: {p['name']} ({p['type']})")


def main():
    """主测试函数"""
    print("🚀 流程思维 Skill 测试开始")
    print("=" * 60)
    
    try:
        # 测试任务拆分
        test_decompose_task()
        
        # 测试获取模板
        test_get_template()
        
        # 测试格式化
        test_format_process()
        
        # 测试自定义流程
        test_custom_process()
        
        # 测试列出流程
        test_list_processes()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
