# 推送执行清单

## 📋 执行前确认
- [ ] 报告生成已完成
- [ ] 质量检查已通过
- [ ] 已获取所有报告内容

## 🔍 推送清单

### 1. 本地保存（必须）
**目标**：保存报告到本地文件

**必须保存的文件**：
- [ ] `D:/openclaw-hermes/data/daily/YYYY-MM-DD/report.md` — 完整报告
- [ ] `D:/openclaw-hermes/data/daily/YYYY-MM-DD/push_payload.json` — 推送内容
- [ ] `D:/openclaw-hermes/data/daily/YYYY-MM-DD/collection_log.json` — 数据收集日志
- [ ] `D:/openclaw-hermes/data/daily/YYYY-MM-DD/verification_log.json` — 数据验证日志
- [ ] `D:/openclaw-hermes/data/daily/YYYY-MM-DD/classification_log.json` — 分类日志
- [ ] `D:/openclaw-hermes/data/daily/YYYY-MM-DD/agent_report_log.json` — Agent报告日志
- [ ] `D:/openclaw-hermes/data/daily/YYYY-MM-DD/skills_report_log.json` — Skills报告日志
- [ ] `D:/openclaw-hermes/data/daily/YYYY-MM-DD/model_industry_mcp_log.json` — 模型/行业/MCP日志

**验证清单**：
- [ ] 所有文件是否保存成功
- [ ] 文件内容是否完整
- [ ] 文件格式是否正确

**输出**：
```
本地保存：
- 保存文件数：X
- 保存成功：Y
- 保存失败：Z
```

### 2. 分段策略（必须）
**目标**：将报告分段推送

**分段规则**：
- [ ] 按内容自然分段，无字数限制
- [ ] 每段开头标注板块图标（📊🤖🛠️🏭📖）和日期
- [ ] 段结构：
  - [1] Agent生态：📌使用指南 + 🆕新全能Agent对比 + ⭐高星全能Agent
  - [2] Agent生态续：🆕新专精Agent对比 + ⭐高星专精Agent
  - [3] Skills市场：第1-2类（含前辈对比）
  - [4] Skills续：第3-6类（含前辈对比）
  - [5] 🧩Agent组件
  - [6] 📊模型动态
  - [7] 🔌MCP + 📰行业热点 + 📊行业应用
  - [8] 数据面板 + 🔮核心信号

**验证清单**：
- [ ] 分段是否按内容自然分段
- [ ] 每段是否有板块图标和日期
- [ ] 段结构是否符合规则

**输出**：
```
分段策略：
- 总段数：X
- 分段规则：✅
- 段结构：✅
```

### 3. 推送确认（必须）
**目标**：确认每段推送成功

**推送方式**：
- **Cron模式**：在final response中直接输出，系统自动推送
- **交互模式**：调用send_message推送

**验证清单**：
- [ ] 每段是否推送成功
- [ ] 推送后是否确认
- [ ] 失败后是否重试

**输出**：
```
推送确认：
- 总段数：X
- 推送成功：Y
- 推送失败：Z
- 重试次数：W
```

### 4. 限流处理（必须）
**目标**：处理微信限流

**限流规则**：
- [ ] 发送间隔15秒
- [ ] 限流后等待60秒重试
- [ ] 最多重试3次
- [ ] 超过3次重试，暂停该步骤，稍后回来重试

**验证清单**：
- [ ] 是否设置发送间隔
- [ ] 限流后是否等待重试
- [ ] 是否记录限流次数

**输出**：
```
限流处理：
- 发送间隔：X秒
- 限流次数：Y
- 重试次数：Z
```

## ✅ 执行确认

**推送完成后，必须输出以下确认信息**：
```
📊 推送完成确认
====================
1. 本地保存：X个文件，保存成功Y，保存失败Z
2. 分段策略：总段数X，分段规则✅，段结构✅
3. 推送确认：总段数X，推送成功Y，推送失败Z
4. 限流处理：发送间隔X秒，限流次数Y，重试次数Z

总计：推送完成，共X段，成功Y段，失败Z段
```

## ⚠️ 异常处理

**如果本地保存失败**：
1. 检查目录是否存在
2. 检查文件权限
3. 如果仍失败，使用备用路径

**如果推送失败**：
1. 等待60秒重试
2. 最多重试3次
3. 如果3次都失败，暂停该步骤，稍后回来重试

**如果限流**：
1. 等待60秒重试
2. 最多重试3次
3. 如果3次都失败，暂停该步骤，稍后回来重试

## 📝 执行记录

**必须保存到**：`D:/openclaw-hermes/data/daily/YYYY-MM-DD/push_log.json`

**记录内容**：
```json
{
  "date": "2026-05-30",
  "local_save": {"files": 8, "success": 8, "failed": 0},
  "segmentation": {"total_segments": 9, "rules": true, "structure": true},
  "push_confirmation": {"total": 9, "success": 9, "failed": 0},
  "rate_limit": {"interval": 15, "limit_count": 0, "retry_count": 0}
}
```
