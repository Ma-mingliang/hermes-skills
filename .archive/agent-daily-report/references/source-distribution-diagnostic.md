# Source Distribution Diagnostic

当用户问"各源占比多少"或"为什么某源 Displayed=0"时，执行以下诊断流程。

## 诊断步骤

### 1. 读取 scored JSON

```python
import json
from collections import Counter, defaultdict

with open("data/scored/YYYY-MM-DD.json", "r", encoding="utf-8") as f:
    scored = json.load(f)
items = scored.get("items", [])
```

### 2. 按 source + importance_level 统计

```python
source_counts = Counter()
source_levels = defaultdict(lambda: Counter())
source_cats = defaultdict(lambda: Counter())

for item in items:
    src = item.get("source", "unknown")
    level = item.get("importance_level", "?")
    cat = item.get("primary_category", "?")
    source_counts[src] += 1
    source_levels[src][level] += 1
    source_cats[src][cat] += 1
```

### 3. 区分 A/B 候选 vs C/D 被过滤

```python
ab_sources = Counter()
cd_sources = Counter()
for item in items:
    level = item.get("importance_level", "?")
    src = item.get("source", "unknown")
    if level in ("A", "B"):
        ab_sources[src] += 1
    else:
        cd_sources[src] += 1
```

### 4. 检查 section quota 分配

对比 source_status 表的 Candidate 和 Displayed：
- 如果某源有 A/B 候选但 Displayed=0 → section quota 分配问题
- 如果某源全是 C/D → 评分/分类问题

### 5. 检查分类准确性

```python
# 找出被错误分类的条目
for item in items:
    src = item.get("source", "")
    cat = item.get("primary_category", "")
    title = item.get("title", "")
    # HN/Reddit 上的工具/MCP 内容不应归类为 Community
    if src in ("hackernews", "reddit") and cat == "Community":
        if any(kw in title.lower() for kw in ["mcp", "agent", "tool", "framework", "sdk"]):
            print(f"MISCLASSIFIED: {src} | {cat} | {title}")
```

## 已知问题模式

### Pattern 1: HN 全部归类为 Community
- 症状：hackernews 所有条目 primary_category = "Community"
- 根因：classify_items.py 对 HN 条目的分类逻辑可能将 source 直接映射为 Community
- 修复：检查 classify_items.py 是否有 `source == "hackernews"` 的特殊处理

### Pattern 2: RSS 条目 category 为空
- 症状：rss:Dev.to LLM 等条目的 primary_category 为空字符串
- 根因：RSS collector 未设置 primary_category，classify_items.py 也未处理
- 修复：RSS collector 应根据 feed 名称设置默认 category

### Pattern 3: MCP section 忽略 external 源
- 症状：MCP Registry 有 11 个 B 级条目，但 MCP section 只显示 reddit 条目
- 根因：generate_report.py 的 section 分配逻辑可能按 source 优先级排序，external 源被排在后面
- 修复：generate_report.py 应优先使用 MCP Registry/Glama 的条目填充 MCP section

### Pattern 4: Section quota 被单一源占满
- 症状：GitHub 占 66.7%，Reddit 占 33.3%，其他源全部 0%
- 根因：section quota 无源分配限制，GitHub 的 A/B 候选数量远超其他源
- 修复：增加 section quota 的源分配逻辑，每个 section 至少保留 1 个位置给非 GitHub 源

## 输出模板

```
🔍 日报数据源占比诊断报告

## 一、流水线数据
Raw N → Matched N → Scored N → A/B候选 N → Displayed N

## 二、各源 Matched 内容分类
| 信息源 | Raw | Matched | A/B | Displayed | 问题 |
|---|---:|---:|---:|---:|---|
...

## 三、根因分析
Bug 1: ...
Bug 2: ...

## 四、建议修复
1. ...
2. ...
```

## 完整诊断脚本（2026-06-02 实测）

```python
import os, json
from collections import Counter, defaultdict

base = "D:/openclaw-hermes/agent-daily-report-skill/data"
scored_file = os.path.join(base, "scored", "YYYY-MM-DD.json")
with open(scored_file, "r", encoding="utf-8") as f:
    scored = json.load(f)

items = scored.get("items", [])

# 1. 按 source + level 统计
source_counts = Counter()
source_levels = defaultdict(lambda: Counter())
source_cats = defaultdict(lambda: Counter())

for item in items:
    src = item.get("source", "unknown")
    level = item.get("importance_level", "?")
    cat = item.get("primary_category", "?")
    source_counts[src] += 1
    source_levels[src][level] += 1
    source_cats[src][cat] += 1

print(f"Total scored: {len(items)}")
for src, cnt in source_counts.most_common():
    levels = dict(source_levels[src])
    print(f"  {src}: {cnt}, levels={levels}")

# 2. A/B 候选 vs C/D 被过滤
ab_sources = Counter()
cd_sources = Counter()
for item in items:
    level = item.get("importance_level", "?")
    src = item.get("source", "unknown")
    if level in ("A", "B"):
        ab_sources[src] += 1
    else:
        cd_sources[src] += 1

print(f"\nA/B: {sum(ab_sources.values())}, C/D: {sum(cd_sources.values())}")

# 3. 显示 A/B 条目详情
for item in items:
    src = item.get("source", "")
    level = item.get("importance_level", "?")
    if level in ("A", "B") and src not in ("github", "reddit"):
        title = item.get("title", "")[:80]
        cat = item.get("primary_category", "?")
        score = item.get("score", 0)
        print(f"  [{level}] {score} | {src} | {cat} | {title}")

# 4. 检查分类错误
for item in items:
    src = item.get("source", "")
    cat = item.get("primary_category", "")
    title = item.get("title", "")
    if src == "hackernews" and cat == "Community":
        if any(kw in title.lower() for kw in ["mcp", "agent", "tool", "framework", "sdk", "coding"]):
            print(f"  MISCLASSIFIED: {src} | {cat} | {title[:60]}")
```
