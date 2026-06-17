# HN 采集逻辑详解

## 数据源

### Firebase API（不需要认证）
- 端点: `https://hacker-news.firebaseio.com/v0`
- 采集: topstories(50) + newstories(50) + beststories(50) = 最多 150 条
- **无 points 门槛** — newstories 返回最新 story，不管 points
- 时间字段: `time`（story 创建时间戳）

### Algolia Search（不需要认证）
- 端点: `https://hn.algolia.com/api/v1/search_by_date`
- 关键词: config.yaml 中 `hackernews.keywords`（32 个）
- 每关键词最多 20 条
- 过滤: `points>5, created_at_i>{72h_ago}`
- 时间字段: `created_at_i`（story 创建时间戳）

## 72h 过滤

**72h 是开贴时间（creation time），不是最后回复时间。**

```python
# Algolia API 参数
"numericFilters": f"points>5,created_at_i>{ts_72h_ago}"

# Firebase 代码过滤
_cutoff = int(time.time()) - 72 * 3600
unique = [s for s in unique if int(s.get("time", 0)) >= _cutoff or s.get("_source") == "algolia"]
```

注意: Algolia 来源的 story 跳过代码中的 72h 过滤（`_source == "algolia"`），但 Algolia API 自身有 `created_at_i>72h_ago` 参数。

## 处理流程

```
Firebase(150) + Algolia(32×20=640)
    ↓
去重 (URL + title)
    ↓
72h 过滤 (仅 Firebase，Algolia 跳过)
    ↓
关键词匹配 (title + text + url)
    ↓
输出
```

## 关键词匹配 (_is_relevant)

```python
def _is_relevant(self, story: Dict) -> bool:
    title = (story.get("title") or "").lower()
    text = (story.get("text") or "").lower()  # 含 HTML 正文
    url = (story.get("url") or "").lower()
    combined = f"{title} {text} {url}"
    return any(kw.lower() in combined for kw in self.keywords)
```

**问题（P60）**: 匹配太宽松，text 正文中顺带提及关键词就会被收入。
**问题（P63）**: text 字段包含 `story_text`（HTML），子串匹配会匹配到 HTML 标签内的内容。应先 strip HTML 再匹配。

### 误匹配示例（2026-06-02 实测）

| 条目 | 匹配关键词 | 匹配位置 | 实际主题 |
|---|---|---|---|
| Launch HN: Expanse (GPU Capacity) | "coding agent" | text 中 "frontier llm coding agents" | GPU 平台 |
| Ask HN: ChatGPT recommends tools | "AI agent" | text 中 "ai agents like chatgpt" | SEO/可见性 |
| Ask HN: war stories agentic apps | "AI agent" | text 中 "a team of ai agents at work" | 生产经验 |
| 768GB Intel Optane DIMMs | "Kimi" | URL 中 "kimi-k2-5" | 硬件跑 LLM |

### 建议修复

1. **title 匹配权重 > text 匹配** — title 必须命中关键词，或 text 中出现 ≥2 次
2. **URL 匹配加白名单** — 只匹配特定域名（github.com 等），不匹配文章 URL 中的模型名
3. **text 匹配加频率门槛** — 关键词在 text 中出现 ≥2 次才算命中
4. **排除 Ask HN/Launch HN 的低信号帖** — 这类帖子 text 内容往往只是举例提及

## 字段映射

### `_format_story` 输出字段

| 字段 | 来源 | 说明 |
|------|------|------|
| `source` | 硬编码 | "hackernews" |
| `source_group` | 硬编码 | "Developer Community" |
| `source_type` | 硬编码 | "story" |
| `title` | story.title | |
| `url` | story.url 或 hn_url | 外部链接优先 |
| `hn_url` | story.id | `https://news.ycombinator.com/item?id={id}` |
| `author` | story.by | |
| `published_at` | story.time | ISO 格式 |
| `metrics.points` | story.score | |
| `metrics.comments_count` | story.descendants | |
| `primary_category` | **硬编码** | **"Community"** ← BUG (P50) |

### 已知问题

1. **`primary_category` 硬编码为 "Community"**（P50）— 应按标题内容实体分类
2. **`id` 字段未存储** — Firebase 的 story ID 没有保存到标准化 item 中（`hn_url` 有，但 `id` 没有）
3. **`_source` 字段未保留** — 无法区分 Firebase vs Algolia 来源

## HN 链接获取

**正确方式**: 从 raw 数据的 `hn_url` 字段读取
```python
hn_url = item.get("hn_url", "")  # 已有，23/23 条都有
```

**错误方式**: 用 Algolia 按标题搜索（P56）
- 搜索 "Zerostack" 会匹配到 575pts 的旧 story（id=48164287）
- 实际采集的是 12pts 的新 story（id=48340468）
- 同一关键词可能匹配到不同时间的同名 story

## 重新评分（2026-06-02 实测）

原始评分（全部归类为 Community）: 1B
重新评分（按内容实体分类）: 1A + 17B = 18 条优质内容

### 评分公式

```
Total = Relevance(30) + Popularity(20) + Freshness(15) + Growth(15) + Utility(20) = 100
```

### 分类→评分映射

| 分类 | Relevance | Utility |
|------|-----------|---------|
| Coding Agent | 28 | 19 |
| MCP | 28 | 19 |
| Workflow | 22 | 19 |
| General Agent | 25 | 12 |
| Agent Framework | 22 | 12 |
| Tool / Plugin / Connector | 19 | 16 |
| Model | 17 | 6 |
| Community | 10 | 8 |

### 示例: Stanford AI Agent Guidelines = 77分 (A级)

| 维度 | 得分 | 依据 |
|------|------|------|
| Relevance | 25/30 | General Agent |
| Popularity | 16/20 | HN 458pts (>200 档) |
| Freshness | 15/15 | <24h |
| Growth | 9/15 | 140 comments (>100 档) |
| Utility | 12/20 | General Agent |
| **合计** | **77** | **≥70 → A级** |
