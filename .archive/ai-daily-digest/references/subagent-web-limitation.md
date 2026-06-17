# 子任务Web访问限制与解决方案

## 问题描述

`delegate_task` 创建的子任务（subagent）默认只有 GitHub MCP 工具，**没有 web/browser/terminal 工具**。
因此子任务无法访问任意 URL（如 36kr.com、qbitai.com 等）。

## 错误表现

子任务返回：
```
I do NOT have access to:
- A web browsing / URL fetching tool
- A terminal/shell tool (to use curl/wget)
- Any way to access arbitrary websites
```

## 解决方案

### 方案1：在主任务中用 execute_code 直接收集（推荐）

```python
import urllib.request
import json

# 收集36氪RSS
req = urllib.request.Request("https://36kr.com/feed", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=30) as resp:
    content = resp.read().decode('utf-8', errors='replace')

# 收集HuggingFace Papers
req = urllib.request.Request("https://huggingface.co/api/daily_papers", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=30) as resp:
    papers = json.loads(resp.read().decode('utf-8'))
```

### 方案2：给子任务指定 toolsets

```python
delegate_task(
    tasks=[{
        "goal": "...",
        "toolsets": ["web", "browser"]  # 明确指定web工具
    }]
)
```

**注意**：即使指定了 toolsets，子任务的工具集也受限于主任务的配置。

### 方案3：使用 browser_navigate（适合SPA站点）

对于需要JavaScript渲染的站点（SPA），必须用 browser 工具：

```python
browser_navigate(url="https://www.qbitai.com/")
content = browser_snapshot(full=True)
```

## 最佳实践

1. **RSS/API类数据**：用 execute_code + urllib（确定性高）
2. **SPA站点数据**：用 browser_navigate + browser_snapshot
3. **并行收集**：多个独立数据源可以用 delegate_task 并行，但每个都要有 web toolsets
4. **避免子任务访问网页**：除非明确配置了 toolsets，否则子任务无法访问网页

## 相关 Pitfalls

- P60: 子任务没有web工具时用execute_code+urllib
- P50: DDG最多1个查询，失败就切HN+GitHub
