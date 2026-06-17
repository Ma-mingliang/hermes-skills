# 日报诊断方法论 (v1.0)

## 诊断流程

当日报 Displayed 数量异常低或用户质疑数据源占比时，按以下流程排查：

### Step 1: 流水线数据检查

```python
import os, json
base = "D:/openclaw-hermes/agent-daily-report-skill/data"

# 读取 scored 数据
with open(os.path.join(base, "scored", "2026-06-02.json"), "r", encoding="utf-8") as f:
    scored = json.load(f)
items = scored.get("items", [])

# 按源+级别统计
from collections import Counter, defaultdict
source_levels = defaultdict(lambda: Counter())
for item in items:
    source_levels[item.get("source", "?")][item.get("importance_level", "?")] += 1

for src, levels in sorted(source_levels.items()):
    total = sum(levels.values())
    ab = levels.get("A", 0) + levels.get("B", 0)
    print(f"  {src}: {total} items, A/B={ab}, levels={dict(levels)}")
```

### Step 2: 对比 Source Status

Source Status 中的 Candidate 和 Displayed 应与 scored 数据一致。
- Candidate = A + B 级条目数
- Displayed = 最终日报正文展示数
- 如果 Candidate > 0 但 Displayed = 0，说明 section quota 有问题

### Step 3: 检查分类准确性

```python
# 按源+分类统计
source_cats = defaultdict(lambda: Counter())
for item in items:
    source_cats[item.get("source", "?")][item.get("primary_category", "?")] += 1

for src, cats in sorted(source_cats.items()):
    print(f"  {src}: {cats.most_common(5)}")
```

**已知分类问题：**
- HN 条目全部归类为 "Community"（P50）
- RSS 条目 primary_category 为空（P51）

### Step 4: 检查 Section Quota 分配

```python
# 统计 Displayed 按源分布
# 从报告中读取 Displayed 列
displayed_by_source = {"github": 16, "reddit": 8, "others": 0}
total_displayed = sum(displayed_by_source.values())
for src, cnt in displayed_by_source.items():
    print(f"  {src}: {cnt/total_displayed*100:.1f}%")
```

**已知 quota 问题：**
- GitHub 独占大部分板块配额（P53）
- MCP 板块被 reddit 占满，忽略 MCP Registry（P52）

### Step 5: HN 重新评分

当 HN 分类错误时，用评分公式手动重新评分：

```python
def score_hn_item(title, points, comments, category):
    # Relevance
    rel_map = {"Coding Agent": 28, "MCP": 28, "General Agent": 25,
               "Agent Framework": 22, "Workflow": 22, "Skill": 22,
               "Tool / Plugin / Connector": 19, "Model": 17, "Community": 10}
    relevance = rel_map.get(category, 10)
    
    # Popularity
    if points >= 500: popularity = 20
    elif points >= 200: popularity = 16
    elif points >= 100: popularity = 12
    elif points >= 50: popularity = 8
    elif points >= 20: popularity = 4
    else: popularity = 2
    
    # Freshness (<24h = 15)
    freshness = 15
    
    # Growth
    if comments >= 200: growth = 12
    elif comments >= 100: growth = 9
    elif comments >= 50: growth = 6
    elif comments >= 20: growth = 3
    else: growth = 1
    
    # Utility
    util_map = {"Coding Agent": 19, "MCP": 19, "Workflow": 19,
                "Skill": 16, "Tool / Plugin / Connector": 16,
                "Agent Framework": 12, "General Agent": 12,
                "Model": 6, "Community": 8}
    utility = util_map.get(category, 8)
    
    return relevance + popularity + freshness + growth + utility
```

### Step 6: HN 链接反查

当 HN collector 未存储 story ID 时，用 Algolia API 反查：

```python
import urllib.request, urllib.parse, json

def get_hn_link(title_query):
    query = urllib.parse.quote(title_query)
    url = f"https://hn.algolia.com/api/v1/search?query={query}&tags=story&hitsPerPage=1"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
        hits = data.get("hits", [])
        if hits:
            return f"https://news.ycombinator.com/item?id={hits[0]['objectID']}"
    return None
```

## 常见根因

| 现象 | 根因 | 修复方向 |
|---|---|---|
| 单源 Displayed 占比 >50% | Section quota 无源分配限制 | generate_report.py 增加源分配逻辑 |
| 某源 Candidate>0 但 Displayed=0 | Section quota 被其他源占满 | 优先使用专用源条目 |
| 某源全部归类为 Community | 分类器对该源有 bug | 修复 classify_items.py |
| RSS 条目 category 为空 | collector 未设置 primary_category | 修复 RSS collector |
| HN 无讨论链接 | collector 未存储 story ID | 增加 hn_id 字段 |
