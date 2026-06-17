# 数据验证工作流

## 问题背景

2026-05-31用户发现报告中"🆕 新出现的全能Agent（本周HN热点）"标题不准确：
- OpenCode创建于2025-04-30，不是"新出现的"
- HN热度只有2-6pts，不是"本周HN热点"
- 本周GitHub新增: 0个

## 正确的数据验证方法

### Step 1: 时间戳分类

```python
from datetime import datetime, timedelta

today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
today_str = today.strftime("%Y-%m-%d")
week_ago = today - timedelta(days=7)
week_ago_str = week_ago.strftime("%Y-%m-%d")

# HN数据分类
hn_today = []  # 今日新闻
hn_week = []   # 本周新闻（非今日）
hn_old = []    # 更早新闻

for h in hn_items:
    created = h.get("created", "")[:10]
    if created == today_str:
        hn_today.append(h)
    elif created >= week_ago_str:
        hn_week.append(h)
    else:
        hn_old.append(h)

# GitHub数据分类
gh_today = []   # 今日创建
gh_week = []    # 本周创建（非今日）
gh_old = []     # 历史项目（高星参考）

for r in gh_repos:
    created = r.get("created", "")[:10]
    if created == today_str:
        gh_today.append(r)
    elif created >= week_ago_str:
        gh_week.append(r)
    else:
        gh_old.append(r)
```

### Step 2: 输出验证报告

```
[数据验证]
HN: 今日{len(hn_today)}条, 本周{len(hn_week)}条, 更早{len(hn_old)}条
GitHub: 今日{len(gh_today)}个, 本周{len(gh_week)}个, 历史高星{len(gh_old)}个
```

### Step 3: 根据数据调整报告

**规则**：
1. 如果今日数据为0，报告中不能出现"今日新闻"板块
2. 如果本周数据为0，报告中不能出现"🆕新出现"板块
3. 报告标题必须与实际数据匹配：
   - 有今日新闻 → "今日新闻"
   - 只有本周新闻 → "本周热点"
   - 只有历史高星 → "高星项目介绍"

**示例**：
```
# 如果今日HN=0, 本周HN=197, 历史高星=47

## ⭐ 高星全能Agent（本周热门）  ← 正确
> **说明**：以下为本周HN讨论热度最高的全能Agent

## 🆕 新出现的全能Agent（本周HN热点）  ← 错误！本周没有新增
```

## 验证清单

- [ ] 是否执行了时间戳分类？
- [ ] 数据面板是否区分今日/本周/历史？
- [ ] 🆕板块是否存在？如果存在，是否有真正的新项目？
- [ ] 报告标题是否与数据匹配？
- [ ] HN热度是否>100pts才能标注"热点"？
