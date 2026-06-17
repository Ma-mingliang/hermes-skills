---
name: spa-data-fetching
description: SPA站点数据获取规则 - 排行榜等SPA网站必须用browser渲染，不能用web_fetch
tags: [data, browser, spa, leaderboard]
---

# SPA 站点数据获取规则

## 触发条件
当需要从以下网站获取实时数据时必须遵循：
- artificialanalysis.ai（模型排名）
- lmarena.ai（Chatbot Arena排名）
- openrouter.ai（模型使用热度）
- 任何 React/Vue/Next.js SPA 站点

## 核心规则

### ❌ 禁止
1. 用 web_fetch / curl 获取 SPA 站点数据 → 只拿到静态骨架/旧缓存
2. 用旧缓存数据"纠正"用户提供的新信息
3. 凭训练数据推测版本号（如从 4.0 推测出 4.8）
4. browser 失败时用旧数据填充排名板块
5. 在SKILL.md或文档中硬编码版本号（版本号会过时，必须实时获取）

### ✅ 正确做法
1. 必须用 browser 工具完整渲染页面后提取数据
2. browser 失败时跳过该板块，标注"今日未能获取"
3. 用户提供截图/信息 → 优先级最高，用vision_analyze读取
4. 确认数据日期：是否有 Last updated 时间戳
5. 如果browser不可用，尝试搜索该网站的API端点（通常返回JSON）

### 验证优先级
```
用户手机截图 > browser实时渲染 > web_fetch（SPA不可靠）> 子任务返回数据
```

## 终极方案：Python urllib（当terminal/WSL不可用时）

当 `terminal` 和 `execute_code` 中的 `terminal()` 都因WSL报错不可用时：
```python
import urllib.request, json
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode())
```

**已验证可用的API**（非SPA，urllib直接可获取JSON）：
- ✅ HN Algolia API (`hn.algolia.com/api/v1/`)
- ✅ GitHub REST API (`api.github.com/`)
- ❌ SPA站点（artificialanalysis.ai等）→ urllib拿到的仍是静态骨架，必须browser

## 判断 SPA 的方法
- curl 返回的 HTML 中几乎没有目标数据内容 → 是 SPA
- 页面依赖 JavaScript 动态渲染 → 是 SPA

## 已知 SPA 站点
| 站点 | 正确方式 | 备注 |
|------|---------|------|
| artificialanalysis.ai | browser | 15个benchmark综合排名 |
| lmarena.ai | browser | 用户投票ELO排名 |
| openrouter.ai | browser | 使用热度/价格 |
| GitHub API | curl ✅ | REST API，不是SPA |
| HN Algolia | curl ✅ | REST API，不是SPA |

## ⚠️ 子任务数据必须验证（2026-05-29教训）

delegate_task子任务返回的数据**可能完全编造**，包括：
- GitHub仓库URL（返回404）
- Stars数量（凭空捏造）
- 模型版本号（从命名规律推测）
- 排名数据（看似合理但无实际来源）

**验证流程**：
1. 子任务返回GitHub项目 → 用web_fetch验证URL是否404
2. 子任务返回stars数 → 用GitHub API确认
3. 子任务返回模型版本 → 用browser访问排行榜确认
4. **未经验证的子任务数据不能写入报告**

**已确认的编造案例（2026-05-29）**：
- 5个"hindsight"GitHub仓库全部404
- 子任务声称"1.8k stars"、"1.2k stars"均为捏造
- 子任务用HER论文概念包装成不存在的项目

## 程序化SPA抓取方案（2026-05-31新增）

当browser工具不可用或需要批量抓取SPA站点时，使用Crawlee + Playwright：

### 安装
```bash
pip install crawlee playwright browserforge
python -m playwright install
```

### 使用示例
```python
import asyncio
from crawlee.crawlers import PlaywrightCrawler

async def scrape_spa_site():
    crawler = PlaywrightCrawler(headless=True, browser_type='chromium')
    
    @crawler.router.default_handler
    async def request_handler(context):
        await context.page.wait_for_load_state('networkidle')
        title = await context.page.title()
        content = await context.page.content()
        # 提取数据...
    
    await crawler.run(['https://target-spa-site.com'])

asyncio.run(scrape_spa_site())
```

### 已验证的SPA站点
| 站点 | Crawlee测试结果 | 备注 |
|------|----------------|------|
| github.com/trending | ✅ 成功 | 684KB内容 |
| artificialanalysis.ai | ⚠️ Vercel安全检查 | 需要反检测或代理 |

### 已知限制
- **Vercel安全检查点**：artificialanalysis.ai等站点有Vercel安全检查，headless浏览器会被拦截
- **解决方案**：使用crawlee的指纹伪装功能，或使用代理，或降级到API数据源

### 依赖包版本（2026-05-31验证）
- crawlee: 1.7.1
- playwright: 1.60.0
- browserforge: 1.2.4

See `references/crawlee-spa-solution-2026-05-31.md` for **详细安装和使用指南**。

## 实战教训

See `references/spa-fetching-lesson-2026-05-29.md` for **2026-05-29真实案例**：用web_fetch旧缓存"纠正"了用户正确的Claude Opus 4.8/GPT-5.5版本号。
See `references/subagent-fabrication-lesson-2026-05-29.md` for **子任务数据编造案例**：5个GitHub仓库全部404，stars数全部捏造。
