# Codex 额度重置规则

> 用于 AI 日报「第六层：模型官方」中「OpenAI Codex官方公告」源的辅助参考。
> 最后验证：2026-06-01（重大修正：滚动窗口非固定周日）

## ⚠️ 关键结论：无法按固定日历日判定

**Codex 每周额度是按用户滚动的 7 天窗口，而非统一的固定重置日（如"每周日"）。**
因此**不能**按日历日推送"今日额度已重置"通知，因为每个用户的 `reset_at` 不同。

## 额度体系

Codex（ChatGPT Plus/Pro 用户的 agentic usage limit）有两套额度：

| 额度类型 | 重置周期 | 说明 |
|---------|---------|------|
| 5-hour rolling limit | 每 5 小时滚动（18,000 秒） | 5 小时窗口内的使用上限 |
| Weekly limit | **7 天滚动窗口（604,800 秒）** | 每用户独立的滚动窗口，非固定日历日 |

## 每周额度重置机制（2026-06-01 修正）

### 权威来源

| 来源 | 发现 | 置信度 |
|------|------|--------|
| [clankercode/quotas](https://github.com/clankercode/quotas) 研究文档 (2026-04-12) | 滚动窗口，非固定日历重置。`reset_at` 字段提供精确 Unix 时间戳 | **HIGH**（直接读取 openai/codex 仓库 OpenAPI 模型） |
| [metyatech/ai-quota](https://github.com/metyatech/ai-quota) 代码 | 按 `windowMinutes` 区分短窗/长窗，`resetAt` 来自 API 响应 | **HIGH**（生产代码，调用 `/backend-api/wham/usage`） |
| GitHub Issue [#7354](https://github.com/openai/codex/issues/7354) | 用户报告重置日期随使用量动态后移，"Weekly usage limit refresh dates seem to be variable" | **HIGH**（多名用户确认，已锁定为 resolved） |
| OpenAI 开发者社区 (2026-05-05) | 用户询问 "5 May" 含义，回复确认显示的是对应用户的特定重置日 | **MEDIUM**（社区回复，非官方） |

### 机制说明

1. **API 返回数据**：`GET https://chatgpt.com/backend-api/wham/usage` 返回 `secondary_window` 包含 `reset_at`（Unix 秒时间戳）和 `reset_after_seconds`（倒计时）
2. **窗口锚定**：7 天窗口锚定于用户**首次大量使用额度的时刻**，而非统一的 UTC 零点
3. **动态偏移**：持续使用会推迟重置时间（Issue #7354 确认），非简单滚动
4. **每个用户独立**：用户 A 可能在周一重置，用户 B 在周三，无法统一判定

### 之前报告的问题

早期社区报告曾提到"周日重置"（Issues #25441, #23192, #5999），这些可能是：
- 早期版本的行为（已被滚动窗口取代）
- 用户观测的巧合（锚定时间恰好在周日附近）
- 某段时间的临时策略

## 验证方法

### 查看当前用户的确切重置时间
1. **Web 界面**：`https://chatgpt.com/codex/cloud/settings/analytics`（显示本地时区的重置日期时间）
2. **Web 界面（旧）**：`https://chatgpt.com/codex/settings/usage`
3. **CLI**：`codex /status`（TUI 交互界面，显示 `resets at Mon 4/14` 等格式）

### 编程查询（需 Bearer Token）
```bash
curl -s 'https://chatgpt.com/backend-api/wham/usage' \
  -H 'Authorization: Bearer <access_token>' \
  -H 'ChatGPT-Account-Id: <account_id>' | \
  jq '.rate_limit.secondary_window.reset_at'
```
Token 位于 `~/.codex/auth.json`。

## 对 Cron 任务的启示

- ❌ 不能设置"每周一检查额度重置"的 cron — 无意义，非固定日
- ❌ 不能推送"今日 Codex 额度已重置"通知 — 无法确认
- ✅ 如需监控：直接调 API 读取 `reset_at` + `used_percent`，在 `used_percent` 降到 0 且 `reset_at` 刚过时触发
