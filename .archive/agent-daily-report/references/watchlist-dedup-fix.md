# Watchlist 去重修复 (2026-06-04)

## 问题

同一 repo 的不同形态（repo 本体 vs release/issue 事件）的 `normalized_entity` 不同，导致去重逻辑未捕获：

- `langchain-ai/langgraph` (tracking=watchlist) → Watch List 表格
- `langchain-ai/langgraph - 1.2.4` (release 事件) → Agent/Coding Agent 正文

违反 P60："连续跟踪的项目不重复进入正文"。

## 修复

`generate_report.py` 新增辅助函数：

```python
def _extract_repo_from_item(self, item: Dict) -> str:
    """从 item 中提取 repo 全名（owner/name），用于 watchlist 去重"""
    entity = item.get("normalized_entity", "")
    if entity and "/" in entity and not entity.startswith("http"):
        parts = entity.split("/")
        if len(parts) >= 2:
            return f"{parts[0]}/{parts[1]}".lower()
    url = item.get("url", "")
    if "github.com/" in url:
        parts = url.split("github.com/")[-1].split("/")
        if len(parts) >= 2:
            return f"{parts[0]}/{parts[1]}".lower()
    repo = item.get("repo", "")
    if repo and "/" in repo:
        return repo.lower()
    return ""
```

在 `select_display_items` 中，添加 agent_items 过滤：

```python
agent_items = grouped.get("Agent Framework", []) + grouped.get("General Agent", []) + grouped.get("Coding Agent", [])
# P60: 排除已进入 watchlist 的同一 repo 的 release/issue/PR 事件
watchlist_repos = {self._extract_repo_from_item(i) for i in github_items if i.get("discovery_type") == "watchlist_change"}
agent_items = [i for i in agent_items if self._extract_repo_from_item(i) not in watchlist_repos or i.get("discovery_type") == "watchlist_change"]
```

## 注意

- `_extract_repo_from_item` 从 normalized_entity、URL、repo 三个字段提取 repo 全名
- 只排除非 watchlist_change 类型的条目（保留 watchlist 本身的展示）
- 其他 section（MCP、Workflow/Skill、Tools）也需要类似过滤，但优先级较低
