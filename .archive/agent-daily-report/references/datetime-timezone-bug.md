# Datetime Timezone Bug (P86)

## 症状

GitHub 整源返回 `failed_network`，raw=0，其他源正常。

日志显示：
```
__main__ - ERROR -   github exception: can't subtract offset-naive and offset-aware datetimes
__main__ - DEBUG -   github: failed_network, raw=0, matched=0
```

## 根因

`github_state.py` 的 `_parse_snapshot_time()` 用 `datetime.fromisoformat()` 解析快照时间。

- 含 `Z` 或 `+08:00` 后缀 → 返回 **aware** datetime（有时区）
- 无后缀（如 `2026-06-06T14:54:08`）→ 返回 **naive** datetime（无时区）

当 `_snapshot_interval_hours()` 计算 `(newer_at - older_at)` 时，一个 aware + 一个 naive → TypeError。

## 修复

```python
# github_state.py → _parse_snapshot_time()
def _parse_snapshot_time(value: str) -> Optional[datetime]:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        # 确保始终返回 timezone-aware datetime
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=JST)
        return dt
    except Exception:
        return None
```

## 调试方法

在 `safe_collect` 中添加完整 traceback：

```python
def safe_collect(name, fn, config, logger):
    try:
        return fn(config)
    except Exception as e:
        import traceback
        logger.error(f"  {name} exception: {e}")
        logger.error(traceback.format_exc())
```

没有 traceback 时，`safe_collect` 只打印一行错误消息，无法定位到具体文件和行号。

## 预防

- 所有 `datetime.fromisoformat()` 调用后，检查 `.tzinfo is None`
- 存储 datetime 时统一使用 `.isoformat()` 带时区（`datetime.now(JST).isoformat()`）
- 对历史快照数据做兼容处理（假设无时区 = JST）
