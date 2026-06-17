# 数据收集执行清单

## 📋 执行前确认
- [ ] 已加载skill（skill_view）
- [ ] 已确认今日日期：YYYY-MM-DD
- [ ] 已准备API token（GitHub/HN）

### 0. 搜索去重机制（必须执行，最高优先级）
**目标**：确保同一个项目只被收集一次，避免重复分类

**去重流程**：
```python
# 建立已收集项目集合
collected_projects = set()  # 项目名称集合

def collect_with_dedup(project):
    """收集前先检查是否已收集"""
    project_name = project["name"]
    
    # 检查是否已收集
    if project_name in collected_projects:
        print(f"⚠️ 项目 {project_name} 已收集，跳过重复收集")
        return None
    
    # 记录项目
    collected_projects.add(project_name)
    
    # 记录来源
    project["source_queries"] = []
    
    return project
```

**验证清单**：
- [ ] 是否建立已收集项目集合
- [ ] 收集前是否检查项目是否已收集
- [ ] 重复项目是否被跳过
- [ ] 是否记录项目来源（哪个搜索查询）

**输出**：
```
搜索去重统计：
- 总搜索结果：X
- 去重后：Y个
- 重复项目：Z个（已跳过）
```


## 🔍 数据收集清单

### 1. GitHub API收集（必须）
**目标**：收集今日新增/更新的AI Agent/Skills项目
**命令**：
```python
# 搜索今日新增的AI agent项目
url = "https://api.github.com/search/repositories?q=ai+agent+created:>2026-05-29&sort=stars&order=desc&per_page=20"
# 搜索今日新增的skills项目
url = "https://api.github.com/search/repositories?q=claude+skill+created:>2026-05-29&sort=stars&order=desc&per_page=20"
```

**验证**：
- [ ] 每个项目的created_at是否是近7天
- [ ] 每个项目的URL是否可访问（404检查）
- [ ] 每个项目的stars数是否真实（对比GitHub页面）

**输出**：
```
GitHub收集结果：
- 总项目数：X
- 今日新增：Y
- 验证通过：Z
- 验证失败：W
```

### 2. HN Algolia API收集（必须）
**目标**：收集今日AI相关热门帖子
**命令**：
```python
# 获取今天的时间戳
import time
today_timestamp = int(time.time()) - 86400  # 24小时前
url = f"https://hn.algolia.com/api/v1/search?query=AI+agent&tags=story&numericFilters=created_at_i>{today_timestamp}&hitsPerPage=20"
```

**验证**：
- [ ] 每个帖子的created_at_i是否是今天
- [ ] 每个帖子的URL是否可访问
- [ ] 每个帖子的热度（points）是否真实

**输出**：
```
HN收集结果：
- 总帖子数：X
- 今日新增：Y
- 验证通过：Z
- 最高热度：W
```

### 3. 36氪RSS收集（必须）
**目标**：收集今日中文AI新闻
**命令**：
```python
url = "https://36kr.com/feed"
# 解析XML，提取今日新闻
```

**验证**：
- [ ] 每个新闻的发布时间是否是今天
- [ ] 每个新闻的URL是否可访问
- [ ] 每个新闻是否与AI相关

**输出**：
```
36氪收集结果：
- 总新闻数：X
- 今日新增：Y
- AI相关：Z
```

### 4. 模型官网收集（必须）
**目标**：收集模型最新动态（版本/定价/更新）
**必须访问**：
- [ ] Claude: anthropic.com
- [ ] GPT: openai.com
- [ ] Gemini: deepmind.google
- [ ] DeepSeek: deepseek.com
- [ ] MiMo: xiaomimimo.com
- [ ] Qwen: qwen.ai
- [ ] Kimi: moonshot.cn
- [ ] MiniMax: minimax.chat

**验证**：
- [ ] 每个官网是否可访问
- [ ] 版本号是否是最新的
- [ ] 定价是否是最新的

**输出**：
```
模型官网收集结果：
- 访问成功：X/8
- 版本更新：Y
- 定价变化：Z
```

### 5. 模型排名收集（必须）
**目标**：收集模型能力排名
**必须访问**：
- [ ] artificialanalysis.ai — 综合排名
- [ ] lmarena.ai — 用户投票排名

**验证**：
- [ ] 排名数据是否是今日的
- [ ] 排名是否有重大变化
- [ ] SPA站点是否用browser渲染

**输出**：
```
模型排名收集结果：
- 访问成功：X/2
- 排名变化：Y
- 新上榜模型：Z
```

## ✅ 执行确认

**数据收集完成后，必须输出以下确认信息**：
```
📊 数据收集完成确认
====================
1. GitHub API：收集X个项目，今日新增Y个，验证通过Z个
2. HN API：收集X个帖子，今日新增Y个，最高热度Z
3. 36氪RSS：收集X条新闻，今日新增Y条，AI相关Z条
4. 模型官网：访问成功X/8，版本更新Y，定价变化Z
5. 模型排名：访问成功X/2，排名变化Y

总计：收集X个数据点，今日新增Y个，验证通过Z个
```

## ⚠️ 异常处理

**如果某个源收集失败**：
1. 记录失败原因
2. 等待30秒重试
3. 最多重试3次
4. 如果3次都失败，标记为"降级"，继续下一个源

**如果API限流**：
1. GitHub API限流：等待X-RateLimit-Reset时间
2. HN API限流：等待60秒重试
3. 36氪RSS限流：等待30秒重试

## 📝 执行记录

**必须保存到**：`D:/openclaw-hermes/data/daily/YYYY-MM-DD/collection_log.json`

**记录内容**：
```json
{
  "date": "2026-05-30",
  "github": {"total": 20, "today": 5, "verified": 18, "failed": 2},
  "hn": {"total": 15, "today": 10, "max_points": 281},
  "36kr": {"total": 20, "today": 8, "ai_related": 6},
  "model_official": {"success": 6, "failed": 2, "updates": 1},
  "model_ranking": {"success": 1, "failed": 1, "changes": 0}
}
```

### 详细收集要求（必须执行）

#### Skills收集要求
每个Skill必须收集以下信息：
1. **基础信息**：名称、Stars、GitHub链接
2. **痛点分析**：解决什么问题（能力缺失型/使用不便型/成本过高型/安全风险型/效率低下型/知识壁垒型/协作困难型/数据孤岛型/行业落地型）
3. **原理分析**：🎯原理+🔧操作+📊效果+👤案例
4. **前辈对比**：找到功能相似的高星前辈Skill，对比差异
5. **真实案例**：来自V2EX、知乎、GitHub等的真实使用案例

**验证清单**：
- [ ] 每个Skill是否有完整的原理分析（🎯🔧📊👤）
- [ ] 每个Skill是否有前辈对比表
- [ ] 每个Skill是否有真实使用案例

#### MCP收集要求
每个MCP项目必须收集以下信息：
1. **基础信息**：名称、Stars、GitHub链接
2. **功能描述**：能做什么
3. **适用场景**：在什么情况下使用
4. **与Agent/Skills的关联**：哪些Agent受益于这个MCP

**搜索策略**：
```python
# 搜索具体MCP项目
mcp_queries = [
    "mcp server",
    "model context protocol",
    "mcp-server",
    "mcp tools"
]

for query in mcp_queries:
    results = github_search(query, sort="stars")
    for project in results:
        # 验证是否为MCP项目
        if is_mcp_project(project):
            collect_mcp_project(project)
```

**验证清单**：
- [ ] 是否搜索了具体MCP项目
- [ ] 每个MCP项目是否有GitHub链接+Stars+功能
- [ ] 是否有生态趋势分析

#### 模型排名收集要求
当SPA站点无法访问时，使用以下降级策略：

1. **第一降级**：使用OpenRouter API获取模型列表和价格
2. **第二降级**：使用GitHub Trending获取模型相关项目
3. **第三降级**：使用HN搜索模型相关新闻

**验证清单**：
- [ ] SPA站点失败时是否执行降级策略
- [ ] OpenRouter数据是否正确解析（价格不能是$-1/M）
- [ ] 是否有编码能力、性价比排名


### SPA站点抓取方案（必须执行）

**问题**：SPA（单页应用）站点需要JavaScript渲染，传统抓取方法无法获取数据

**解决方案**：

#### 1. 首选方案：Crawlee (Python版本)
```python
# 安装
# pip install crawlee

from crawlee.playwright_crawler import PlaywrightCrawler

crawler = PlaywrightCrawler()

@crawler.router.default_handler
async def request_handler(context):
    # 等待JavaScript渲染完成
    await context.page.wait_for_selector('.ranking-table')
    
    # 提取数据
    data = await context.page.query_selector_all('.model-row')
    for item in data:
        name = await item.query_selector('.model-name')
        ranking = await item.query_selector('.ranking')
        print(f"Model: {await name.text_content()}, Ranking: {await ranking.text_content()}")

# 运行爬虫
await crawler.run(['https://artificialanalysis.ai'])
```

#### 2. 备选方案：Playwright + Python
```python
# 安装
# pip install playwright
# playwright install

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://artificialanalysis.ai')
    
    # 等待JavaScript渲染完成
    page.wait_for_selector('.ranking-table')
    
    # 提取数据
    data = page.query_selector_all('.model-row')
    for item in data:
        name = item.query_selector('.model-name')
        ranking = item.query_selector('.ranking')
        print(f"Model: {name.text_content()}, Ranking: {ranking.text_content()}")
    
    browser.close()
```

#### 3. AI驱动方案：LLM Scraper
```python
# 安装
# pip install llm-scraper

from llm_scraper import LLMScraper

scraper = LLMScraper()
data = scraper.scrape('https://artificialanalysis.ai')
print(data)
```

**验证清单**：
- [ ] 是否安装了Crawlee或Playwright
- [ ] 是否测试了SPA站点抓取
- [ ] 是否处理了JavaScript渲染
- [ ] 是否提取了结构化数据

**降级策略**：
1. **第一降级**：使用OpenRouter API获取模型列表和价格
2. **第二降级**：使用GitHub Trending获取模型相关项目
3. **第三降级**：使用HN搜索模型相关新闻

