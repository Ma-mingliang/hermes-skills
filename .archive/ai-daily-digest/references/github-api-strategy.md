# GitHub API 限流策略与数据获取方法

> 2026-05-29 通过实际执行总结的经验

## GitHub API 限流规则

- **未认证**：60次/小时
- **认证（token）**：5000次/小时
- **403响应时**：读取 `X-RateLimit-Reset` 头（Unix时间戳），等待后重试
- **正确做法**：每小时≤60次，分散调用，每次间隔60秒
- **错误做法**：只在第一个小时调用60次就放弃

## 执行策略

```
00:00-01:00  GitHub API 60次 + 其他源穿插
01:00-02:00  GitHub API 60次 + 其他源穿插
...循环直到所有项目验证完成...
06:30        推送微信
```

## Python urllib 获取方法（WSL/terminal不可用时）

```python
import urllib.request, json

# HN Algolia API（无限制）
url = "https://hn.algolia.com/api/v1/search?query=AI+agent&tags=story&hitsPerPage=15"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode())

# GitHub API（60次/小时）
url = "https://api.github.com/search/repositories?q=AI+agent&sort=stars&order=desc&per_page=15"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode())

# GitHub 仓库文件列表（用于分类验证）
url = "https://api.github.com/repos/{owner}/{repo}/contents/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as resp:
    files = json.loads(resp.read().decode())
```

## SPA站点数据获取（模型排名）

- **artificialanalysis.ai** — SPA单页应用，web_fetch只拿到静态骨架
- **lmarena.ai** — SPA，需browser渲染
- **openrouter.ai** — SPA，需browser渲染
- **正确做法**：用browser工具完整渲染页面
- **降级方案**：browser不可用时标注"未获取"，绝不用旧数据填充
- **用户截图优先级最高**：用户提供的手机截图 > browser > web_fetch

## 已验证可用的API端点

| 端点 | 方法 | 限制 | 可靠性 |
|------|------|------|--------|
| HN Algolia API | urllib | 无 | ✅ 最可靠 |
| GitHub REST API | urllib | 60次/小时 | ✅ 可靠 |
| 36氪 RSS | urllib | 无 | ✅ 可靠 |
| V2EX RSS | urllib | 无 | ✅ 可靠 |
| Linux.do RSS | urllib | 无 | ✅ 可靠 |
| Reddit JSON API | urllib | - | ❌ 返回0字节 |
| Google/Bing/DuckDuckGo | urllib | - | ❌ 不可靠 |
| RSSHub代理中文源 | urllib | - | ❌ 大部分403 |

## 子任务数据验证规则

- **delegate_task返回的数据可能完全编造**
- 已确认编造案例：GitHub仓库URL（404）、Stars数（捏造）、排名数据（无来源）
- **验证流程**：
  1. 子任务返回GitHub项目 → urllib验证URL
  2. 子任务返回stars数 → GitHub API确认
  3. 子任务返回模型版本 → browser访问排行榜确认
  4. **未验证数据不能写入报告**
