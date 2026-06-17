#!/usr/bin/env python3
"""
Reasoning Trace 定期清理脚本
用法: python scripts/cleanup-traces.py [keep_days=30]

清理规则:
- .json 文件: 按 important/modifications 标记决定保留
- .jsonl 文件: 按纯日期清理（Plugin hook 原始事件日志，无元数据标记）
- 空目录: 清理后自动删除
"""
import os
import sys
import json
from datetime import datetime, timedelta

def get_real_stats(traces_dir):
    """手动统计 traces/ 目录下的所有文件（.json + .jsonl），不依赖 get_storage_stats()"""
    stats = {
        "total_files": 0, "total_size_kb": 0,
        "json_files": 0, "json_kb": 0,
        "jsonl_files": 0, "jsonl_kb": 0,
        "date_dirs": 0, "old_dirs": 0,
    }
    if not os.path.isdir(traces_dir):
        return stats
    cutoff = datetime.now() - timedelta(days=30)
    for date_dir in os.listdir(traces_dir):
        date_path = os.path.join(traces_dir, date_dir)
        if not os.path.isdir(date_path):
            continue
        stats["date_dirs"] += 1
        try:
            dir_date = datetime.strptime(date_dir, "%Y-%m-%d")
            if dir_date < cutoff:
                stats["old_dirs"] += 1
        except ValueError:
            pass
        for filename in os.listdir(date_path):
            fp = os.path.join(date_path, filename)
            if not os.path.isfile(fp):
                continue
            sz = os.path.getsize(fp) / 1024
            stats["total_files"] += 1
            stats["total_size_kb"] += sz
            if filename.endswith('.json'):
                stats["json_files"] += 1
                stats["json_kb"] += sz
            elif filename.endswith('.jsonl'):
                stats["jsonl_files"] += 1
                stats["jsonl_kb"] += sz
    return stats

def cleanup_jsonl(traces_dir, cutoff):
    """手动清理过期 .jsonl 文件（API cleanup_traces 不处理 .jsonl）"""
    deleted = 0
    freed_kb = 0
    for date_dir in os.listdir(traces_dir):
        date_path = os.path.join(traces_dir, date_dir)
        if not os.path.isdir(date_path):
            continue
        try:
            dir_date = datetime.strptime(date_dir, "%Y-%m-%d")
        except ValueError:
            continue
        if dir_date >= cutoff:
            continue
        for filename in list(os.listdir(date_path)):
            if filename.endswith('.jsonl'):
                fp = os.path.join(date_path, filename)
                sz = os.path.getsize(fp) / 1024
                os.remove(fp)
                deleted += 1
                freed_kb += sz
    return deleted, freed_kb

def cleanup_empty_dirs(traces_dir):
    """删除清理后为空的日期目录"""
    removed = 0
    for date_dir in sorted(os.listdir(traces_dir)):
        date_path = os.path.join(traces_dir, date_dir)
        if os.path.isdir(date_path) and len(os.listdir(date_path)) == 0:
            os.rmdir(date_path)
            removed += 1
    return removed

def main():
    keep_days = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    traces_dir = os.path.expanduser("~/.hermes/traces")
    skill_dir = os.path.expanduser("~/.hermes/skills/reasoning-trace")
    sys.path.insert(0, skill_dir)
    from client import get_trace_client

    # Pre-cleanup stats
    pre = get_real_stats(traces_dir)
    print(f"Pre-cleanup: {pre['total_files']} files ({pre['total_size_kb']:.2f} KB)")

    # Step 1: .json cleanup via instance method (NOT the wrapper)
    client = get_trace_client()
    json_result = client.cleanup(keep_days=keep_days, keep_important=True, keep_with_modifications=True)
    print(f"JSON cleanup: deleted={json_result.get('deleted_files',0)}, kept={json_result.get('kept_files',0)}")

    # Step 2: .jsonl cleanup (manual)
    cutoff = datetime.now() - timedelta(days=keep_days)
    jsonl_deleted, jsonl_freed = cleanup_jsonl(traces_dir, cutoff)
    print(f"JSONL cleanup: deleted={jsonl_deleted}, freed={jsonl_freed:.2f} KB")

    # Step 3: empty dirs
    empty_removed = cleanup_empty_dirs(traces_dir)
    print(f"Empty dirs removed: {empty_removed}")

    # Post-cleanup stats
    post = get_real_stats(traces_dir)
    freed = pre['total_size_kb'] - post['total_size_kb']
    print(f"Post-cleanup: {post['total_files']} files ({post['total_size_kb']:.2f} KB)")
    print(f"Freed: {freed:.2f} KB ({freed/1024:.2f} MB)")

if __name__ == "__main__":
    main()
