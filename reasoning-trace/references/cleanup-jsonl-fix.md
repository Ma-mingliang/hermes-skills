# cleanup() 和 get_storage_stats() .jsonl 修复指南

**发现日期**: 2026-06-01  
**影响**: Plugin hook 自动生成的 `.jsonl` session trace 永远不会被清理，会无限累积

## 修复 1: cleanup() 方法（client.py ~第173行）

**原代码**:
```python
            # 遍历目录中的文件
            for filename in os.listdir(date_path):
                if not filename.endswith('.json'):
                    continue
                
                file_path = os.path.join(date_path, filename)
                stats["total_files"] += 1
                
                # 读取trace数据
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        trace_data = json.load(f)
                except:
                    continue
                
                # 检查是否应该保留
                should_keep = False
                
                # 保留标记为重要的trace
                if keep_important and trace_data.get("important", False):
                    should_keep = True
                    stats["important_files"] += 1
                
                # 保留有修改意见的trace
                if keep_with_modifications and trace_data.get("modifications"):
                    should_keep = True
                    stats["modification_files"] += 1
                
                # 删除或保留
                if should_keep:
                    stats["kept_files"] += 1
                else:
                    # 获取文件大小
                    file_size = os.path.getsize(file_path)
                    stats["freed_space_kb"] += file_size / 1024
                    
                    # 删除文件
                    os.remove(file_path)
                    stats["deleted_files"] += 1
```

**修复后**:
```python
            # 遍历目录中的文件
            for filename in os.listdir(date_path):
                is_json = filename.endswith('.json')
                is_jsonl = filename.endswith('.jsonl')
                if not (is_json or is_jsonl):
                    continue
                
                file_path = os.path.join(date_path, filename)
                stats["total_files"] += 1
                
                # .jsonl 文件：Plugin自动生成的事件日志，无 important/modifications 标记
                # 直接按日期清理（始终视为可删除）
                if is_jsonl:
                    file_size = os.path.getsize(file_path)
                    stats["freed_space_kb"] += file_size / 1024
                    os.remove(file_path)
                    stats["deleted_files"] += 1
                    continue
                
                # .json 文件：读取trace数据，检查保留条件
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        trace_data = json.load(f)
                except:
                    continue
                
                # 检查是否应该保留
                should_keep = False
                
                # 保留标记为重要的trace
                if keep_important and trace_data.get("important", False):
                    should_keep = True
                    stats["important_files"] += 1
                
                # 保留有修改意见的trace
                if keep_with_modifications and trace_data.get("modifications"):
                    should_keep = True
                    stats["modification_files"] += 1
                
                # 删除或保留
                if should_keep:
                    stats["kept_files"] += 1
                else:
                    # 获取文件大小
                    file_size = os.path.getsize(file_path)
                    stats["freed_space_kb"] += file_size / 1024
                    
                    # 删除文件
                    os.remove(file_path)
                    stats["deleted_files"] += 1
```

## 修复 2: get_storage_stats() 方法（client.py ~第278行）

**原代码**:
```python
                    # 统计文件
                    for filename in os.listdir(date_path):
                        if filename.endswith('.json'):
                            file_path = os.path.join(date_path, filename)
                            stats["traces"]["total_files"] += 1
                            stats["traces"]["total_size_kb"] += os.path.getsize(file_path) / 1024
```

**修复后**:
```python
                    # 统计文件（包括 .json 和 .jsonl）
                    for filename in os.listdir(date_path):
                        if filename.endswith('.json') or filename.endswith('.jsonl'):
                            file_path = os.path.join(date_path, filename)
                            stats["traces"]["total_files"] += 1
                            stats["traces"]["total_size_kb"] += os.path.getsize(file_path) / 1024
```

## 设计决策

- **`.jsonl` 文件按纯日期清理**：这些是 Plugin hook 的原始事件日志，无 `important` 或 `modifications` 字段，不适用保留逻辑
- **`.json` 文件保持现有逻辑**：含 `important`/`modifications` 元数据，按标志决定保留
- **`get_storage_stats()` 统计两者**：反映真实存储占用
