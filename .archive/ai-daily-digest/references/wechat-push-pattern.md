# 微信分段推送最佳实践

## 两种推送模式

| 模式 | 触发方式 | 发送工具 | 典型场景 |
|------|---------|---------|---------|
| **Cron 自动推送** | cron job 调度 | 最终响应（final response） | 每日定时推送，无人值守 |
| **交互式推送** | 用户手动说"推送" | `send_message(action="send", ...)` | 用户在聊天中手动触发 |

### Cron 模式（当前使用）
- 只需在最终响应中输出完整内容，系统自动投递到微信
- 不需要调用 `send_message`
- 仍然使用 `[1/N]...[N/N]` 分段格式，系统会逐段发送
- 失败时在最终响应中说明原因即可

### 交互式模式
- 逐段调用 `send_message(action="send", target="weixin:<user_id>@im.wechat", message=chunk)`
- 各段之间系统已内置速率控制，不需要手动 sleep

## 分段策略

- 每段约 **1800-2000字符**（微信消息有长度限制）
- 使用 `[1/N]` `[2/N]` ... `[N/N]` 格式标识分段
- 分段应在段落/板块边界断开，不要在表格中间断开

## 分段算法

```python
chunk_size = 2000
chunks = []
lines = report.split('\n')
current_chunk = ""
current_size = 0

for line in lines:
    line_size = len(line) + 1
    if current_size + line_size > chunk_size and current_chunk:
        chunks.append(current_chunk.strip())
        current_chunk = line + '\n'
        current_size = line_size
    else:
        current_chunk += line + '\n'
        current_size += line_size

if current_chunk.strip():
    chunks.append(current_chunk.strip())
```

## 互动式推送参考

在非 cron 的交互式场景中，可以逐段调用：
```python
send_message(action="send", target="weixin:<chat_id>", message=chunk)
```
从 `send_message(action="list")` 获取目标（格式：`weixin:<user_id>@im.wechat`）。
系统已内置速率控制，不需要手动 sleep。

## 已知问题

- 部分Markdown格式在微信中不渲染（如表格）
- 超长链接可能被微信截断
- emoji在部分设备上显示异常
- **iLink API 频率限制**：连续发送多段会触发 `rate limited`（ret=-2），需等待 5-10 分钟恢复。交互式推送时每段间隔建议 ≥60 秒
- **agent-daily-report 推送也受此限制**：虽然 agent-daily-report 是独立项目，但微信推送走同一个 iLink API

## 验证清单

- [ ] 分段数正确（与预期一致）
- [ ] 每段都有 `[N/M]` 标识
- [ ] 最后一段有数据来源透明度表
- [ ] 所有段都发送成功（检查send_message返回的success=true）
