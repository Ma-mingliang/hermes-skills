# Cron 定期清理的完整实现模式

**背景**: `cleanup_traces()` 不处理 `.jsonl` 文件，cron job 需要补充逻辑。

## 完整清理流程

⚠️ **Pitfall: `cleanup_traces()` 包装函数缺少 `keep_with_modifications` 参数**（2026-06-09 实测确认）
- `cleanup_traces()` (line 1094) 只接受 `keep_days` 和 `keep_important`，**不传 `keep_with_modifications`**
- 要使用完整功能，必须通过实例方法：`get_trace_client().cleanup(keep_days, keep_important, keep_with_modifications)`
- `get_storage_stats()` 会抛出 `Object of type datetime is not JSON serializable` 异常 — 不要直接 JSON 序列化其返回值，应手动遍历 traces/ 目录统计

```python
import os
import sys
import json
from datetime import datetime, timedelta

skill_dir = os.path.expanduser("~/.hermes/skills/reasoning-trace")
sys.path.insert(0, skill_dir)
from client import get_trace_client

# Step 1: 执行内置清理（仅 .json，用实例方法以支持 keep_with_modifications）
client = get_trace_client()
result = client.cleanup(keep_days=30, keep_important=True, keep_with_modifications=True)

# Step 2: 手动清理过期 .jsonl 文件（同上，略）
# Step 3: 清理空目录（同上，略）
```
# Step 2: 手动清理过期 .jsonl 文件
traces_dir = os.path.expanduser("~/.hermes/traces")
cutoff = datetime.now() - timedelta(days=30)
jsonl_deleted = 0
jsonl_freed_kb = 0

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
            jsonl_deleted += 1
            jsonl_freed_kb += sz

# Step 3: 清理空目录
for date_dir in sorted(os.listdir(traces_dir)):
    date_path = os.path.join(traces_dir, date_dir)
    if os.path.isdir(date_path) and len(os.listdir(date_path)) == 0:
        os.rmdir(date_path)
```

## 统计数据差异

`get_storage_stats()` 报告值 vs 实际值：

| 日期 | get_storage_stats() | 实际 | 差距 |
|------|-------------------|------|------|
| 2026-06-06 | 5 文件 / 5.83 KB | 522 文件 / 1.33 MB | 228倍 |
| 2026-06-09 | N/A (datetime序列化异常) | 654 文件 / 1.57 MB | — |

⚠️ `get_storage_stats()` 不仅遗漏 `.jsonl`，还会抛 `datetime is not JSON serializable` 异常。
**Cron 清理时必须用手动遍历统计，不要调用 `get_storage_stats()`。**

## 设计决策

- `.jsonl` 按纯日期清理：Plugin hook 原始事件日志，无 `important`/`modifications` 标记
- `.json` 保留现逻辑：含元数据，按标志决定保留
- 空目录删除：清理后目录为空则删除

## 完整可运行脚本

见 `scripts/cleanup-traces.py` — 封装了上述所有逻辑，可直接 `python ~/.hermes/skills/reasoning-trace/scripts/cleanup-traces.py [keep_days]` 运行。
