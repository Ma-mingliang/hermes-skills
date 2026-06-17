# 行业覆盖策略 (2026-05-31)

## 问题

报告行业应用只有🏭工业和💼企业，缺少第3个行业。

## 根因

- 36kr新闻通常只覆盖工业/企业
- 没有从HN行业搜索结果中提取其他行业

## 解决方案

### 数据收集阶段

HN行业搜索关键词**必须**包含：
```python
industry_queries = [
    "AI healthcare",    # 🏥 医学
    "AI education",     # 🎓 教育
    "AI finance",       # 💰 金融
    "AI enterprise",    # 💼 企业
    "AI security",      # 🔐 安全
    "AI robotics",      # 🏭 工业/机器人
]
```

### 报告生成阶段

行业应用表格**必须**从多个来源填充：
1. 36kr → 通常覆盖工业/企业
2. HN行业搜索 → 补充医学/教育/金融/安全

### 验证阶段

```python
industry_emojis = ["🏭","💼","🏥","🎓","💰","⚖️","🔐","🌾","🚗","🎮"]
found = [e for e in industry_emojis if e in report]
assert len(found) >= 3, f"行业覆盖不足: {len(found)}/3"
```

## 行业分类映射

| 关键词 | 行业 | Emoji |
|--------|------|-------|
| healthcare/medical/诊断/药物 | 医学 | 🏥 |
| education/学习/教育/批改 | 教育 | 🎓 |
| finance/交易/投资/风控 | 金融 | 💰 |
| enterprise/企业/办公/客服 | 企业 | 💼 |
| security/安全/威胁/漏洞 | 安全 | 🔐 |
| robotics/工业/制造/质检 | 工业 | 🏭 |
| legal/法律/合同/合规 | 法律 | ⚖️ |
| agriculture/农业/种植 | 农业 | 🌾 |
|交通/自动驾驶/物流 | 交通 | 🚗 |
| entertainment/游戏/虚拟人 | 娱乐 | 🎮 |

## 验证清单

- [ ] 行业应用表格是否有≥3个不同行业emoji
- [ ] 是否从HN行业搜索结果中提取了非工业/企业行业
- [ ] HN行业搜索关键词是否包含 healthcare/education/finance
