# 日报数据源分析方法论 (2026-06-02)

## 流水线追踪方法

当需要诊断某个数据源的问题时，按以下步骤追踪：

### 1. 读取 source_status 表

从报告的 `## 0. 数据源状态` 表格中获取每个源的：
- Raw → Matched → Scored → Candidate → Displayed

### 2. 读取 scored 数据

```python
import os, json
base = "D:/openclaw-hermes/agent-daily-report-skill/data"
with open(os.path.join(base, "scored", "2026-06-02.json"), "r", encoding="utf-8") as f:
    scored = json.load(f)
items = scored.get("items", [])
```

按 source 分组统计 A/B/C/D 级别分布。

### 3. 读取 raw 数据

```python
with open(os.path.join(base, "raw", "2026-06-02.json"), "r", encoding="utf-8") as f:
    raw = json.load(f)
items = raw.get("items", [])
```

检查 `source_group`、`primary_category`、`metrics` 字段。

### 4. 读取 state 文件

```python
with open(os.path.join(base, "..", "state", "model_docs_state.json"), "r", encoding="utf-8") as f:
    state = json.load(f)
```

检查 hash_diff 变更检测的 `last_hash`、`last_changed`、`last_text_preview`。

## 评分公式验证

```python
detail = item.get("_score_detail", {})
detail_sum = sum(v for v in detail.values() if isinstance(v, (int, float)))
actual = item.get("score", 0)
diff = detail_sum - actual
flags = item.get("score_trace", {}).get("quality_flags", [])
```

如果 `diff > 0` 且 `flags` 包含 `generic_github_discovery_candidate`，说明被 discovery penalty 封顶。

## HN 分类验证

```python
# 检查 primary_category 是否硬编码为 "Community"
for item in hn_items:
    cat = item.get("primary_category", "?")
    if cat == "Community":
        # 可能是误分类，检查标题实际内容
        title = item.get("title", "").lower()
        if any(k in title for k in ["coding agent", "mcp", "browser agent"]):
            print(f"误分类: {title}")
```

## 关键词匹配验证

```python
# 正确的关键词位置
keywords = config.get("hackernews", {}).get("keywords", [])
# 不是 config.get("sources", {}).get("hackernews", {}).get("keywords", [])
```

## 时间戳验证

```python
from datetime import datetime, timezone, timedelta
now = datetime(2026, 6, 2, 19, 0, 0, tzinfo=timezone(timedelta(hours=8)))
for item in hn_items:
    pub = item.get("published_at", "")
    dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
    age = now - dt
    hours = age.total_seconds() / 3600
    if hours > 72:
        print(f"超出72h: {item.get('title','')}")
```

## Section Quota 分析

检查每个 section 的 Displayed 来源分布：
- 如果某个 section 只有 GitHub 条目，说明 quota 被 GitHub 占满
- 如果 external 源有 A/B 候选但 Displayed=0，说明 section quota 无跨源分配

## Growth Rate 计算

```python
for item in gh_items:
    stars = item.get("metrics", {}).get("stars", 0) or 0
    d24 = item.get("metrics", {}).get("star_delta_24h") or 0
    if stars >= 100 and d24 > 0:
        rate = (d24 / stars) * 100  # percentage
```

按增长率排序可发现"小项目爆发"模式（如 110⭐ 项目 +85/24h = 77% 增长率）。

## Quality Flag 惩罚分析

```python
for item in gh_items:
    detail = item.get("_score_detail", {})
    detail_sum = sum(v for v in detail.values() if isinstance(v, (int, float)))
    actual = item.get("score", 0)
    diff = detail_sum - actual
    flags = item.get("score_trace", {}).get("quality_flags", [])
    if diff > 0 and flags:
        print(f"  被惩罚: {item.get('title','')} | 明细={detail_sum}→实际={actual} | 扣{diff}分 | {flags}")
```

## External 源 A/B 候选排查

当 external_digests 的 Displayed=0 时：
1. 按子源分组统计 A/B 候选数
2. 检查 section quota 是否被 github/reddit 占满
3. 检查 generate_report.py 的 section 填充逻辑是否有源优先级
