# Obsidian 集成

## 推送后同步

AI 历史内容推送到手机后，也会同步到 Obsidian Vault。

### 同步路径
`D:/ObsidianVault/Learning/AI-History/`

### 文件命名
`Day-XX-热词.md`

### Frontmatter 格式
```yaml
---
date: YYYY-MM-DD
type: ai-education
day: X
topic: 热词名称
main_line: main1/main2/both
tags:
  - ai
  - education
  - history
ai-first: true
---
```

## 进度追踪

进度文件：`~/.hermes/ai-history-state.json`

```json
{
  "current_day": 15,
  "last推送_date": "2026-06-05",
  "total推送": 14,
  "history": [...]
}
```

## 成就系统

| 里程碑 | Day | 成就 |
|--------|-----|------|
| 🥉 | 7 | AI历史入门 |
| 🥈 | 14 | 深度学习理解者 |
| 🥇 | 18 | Transformer掌握者 |
| 💎 | 30 | 大模型时代理解者 |
| 👑 | 42 | Agent时代先驱 |
| 🏆 | 60 | AI通史大师 |
