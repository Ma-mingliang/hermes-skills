#!/usr/bin/env python3
"""
Reasoning Trace 清理脚本
用于手动清理旧的trace文件
"""

import os
import sys
import argparse
from datetime import datetime

# 添加模块路径
skill_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, skill_dir)

from client import ReasoningTrace, get_storage_stats, cleanup_traces


def main():
    parser = argparse.ArgumentParser(description="清理Reasoning Trace文件")
    parser.add_argument("--keep-days", type=int, default=30, help="保留天数（默认30天）")
    parser.add_argument("--keep-important", action="store_true", default=True, help="保留重要trace")
    parser.add_argument("--no-keep-important", action="store_false", dest="keep_important", help="不保留重要trace")
    parser.add_argument("--stats", action="store_true", help="只显示统计信息")
    parser.add_argument("--dry-run", action="store_true", help="模拟运行，不实际删除")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Reasoning Trace 清理工具")
    print("=" * 60)
    
    # 获取存储统计
    print("
📊 当前存储统计:")
    stats = get_storage_stats()
    print(f"   traces目录:")
    print(f"     - 文件数: {stats['traces']['total_files']}")
    print(f"     - 总大小: {stats['traces']['total_size_kb']:.2f} KB")
    print(f"     - 日期目录数: {stats['traces']['date_dirs']}")
    print(f"   modifications目录:")
    print(f"     - 文件数: {stats['modifications']['total_files']}")
    print(f"     - 总大小: {stats['modifications']['total_size_kb']:.2f} KB")
    
    if args.stats:
        return
    
    # 执行清理
    print(f"
🧹 清理配置:")
    print(f"   保留天数: {args.keep_days}")
    print(f"   保留重要trace: {'是' if args.keep_important else '否'}")
    
    if args.dry_run:
        print("
⚠️ 模拟运行模式，不会实际删除文件")
        return
    
    print("
执行清理...")
    result = cleanup_traces(keep_days=args.keep_days, keep_important=args.keep_important)
    
    print("
📋 清理结果:")
    print(f"   总文件数: {result['total_files']}")
    print(f"   删除文件数: {result['deleted_files']}")
    print(f"   保留文件数: {result['kept_files']}")
    print(f"   重要文件数: {result['important_files']}")
    print(f"   有修改意见的文件数: {result['modification_files']}")
    print(f"   释放空间: {result['freed_space_kb']:.2f} KB")
    
    # 获取清理后的统计
    print("
📊 清理后统计:")
    stats_after = get_storage_stats()
    print(f"   traces目录:")
    print(f"     - 文件数: {stats_after['traces']['total_files']}")
    print(f"     - 总大小: {stats_after['traces']['total_size_kb']:.2f} KB")
    print(f"     - 日期目录数: {stats_after['traces']['date_dirs']}")
    
    print("
✅ 清理完成！")


if __name__ == "__main__":
    main()
