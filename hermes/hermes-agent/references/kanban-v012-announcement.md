# Hermes Agent Kanban Multi-Agent Feature

## 来源
- **推文**: https://x.com/NousResearch/status/2050997692977844324
- **发布时间**: 2026年5月4日
- **版本**: v0.12.0 引入，当前 v0.14.0 已包含

## 功能摘要

Hermes Agent now has multi-agent via the Kanban, new in v0.12.0.

- Agents claim tasks from a board, work in parallel, and hand off when blocked
- You watch progress and unblock from one easy view instead of juggling terminals
- Demo视频: https://t.co/SsRIaa1lvs

## 数据（截至抓取时）
- 271 回复 / 623 转帖 / 5,945 喜欢 / 4,386 书签 / 145.2万 查看

## 完整命令速查

| 命令 | 说明 |
|------|------|
| `hermes kanban init` | 初始化 kanban.db（幂等） |
| `hermes kanban boards` | 管理看板（每个项目/工作流一个 board） |
| `hermes kanban create "标题"` | 创建任务 |
| `hermes kanban list` | 列出任务 |
| `hermes kanban show <id>` | 任务详情 + 事件历史 |
| `hermes kanban assign <id> <profile>` | 分配任务 |
| `hermes kanban reclaim` | 释放运行中的 worker claim |
| `hermes kanban reassign <id> <profile>` | 重新分配 |
| `hermes kanban claim` | Agent 原子认领 ready 任务 |
| `hermes kanban complete <id>` | 标记完成 |
| `hermes kanban block <id> --reason "X"` | 阻塞 |
| `hermes kanban unblock <id>` | 解除阻塞 |
| `hermes kanban comment <id> "内容"` | 添加评论 |
| `hermes kanban link <parent> <child>` | 添加依赖 |
| `hermes kanban unlink <parent> <child>` | 移除依赖 |
| `hermes kanban watch` | 实时事件流 |
| `hermes kanban stats` | 统计 |
| `hermes kanban archive` | 归档已完成任务 |
| `hermes kanban diagnostics` | 活跃诊断 |

## 配置（config.yaml）

```yaml
kanban:
  dispatch_in_gateway: true       # Gateway 内嵌 dispatcher
  dispatch_interval_seconds: 60   # 每 60 秒检查 ready 任务
  failure_limit: 2                # 失败 2 次后停止重试
```

## 关键 Pitfalls

1. **无 Web UI**: Kanban 没有 dashboard 标签页，纯 CLI 操作
2. **依赖 Gateway**: Dispatcher 运行在 Gateway 进程内，Gateway 停止时任务永远停在 `ready`
3. **WSL 不可用时启动 Dashboard**: 用 Python subprocess 而非 terminal()：
   ```python
   import subprocess, os
   proc = subprocess.Popen(
       ["hermes", "dashboard", "--port", "9119", "--no-open"],
       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
       shell=True, creationflags=subprocess.CREATE_NO_WINDOW
   )
   ```
4. **DB 位置**: `~/.hermes/kanban.db` (SQLite)
5. **Profile 即 assignee**: `hermes kanban boards` 显示可用 profile，claim 时用 profile 名
