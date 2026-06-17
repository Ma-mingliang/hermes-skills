# AI日报完整流程（2026-05-30总结）

基于多次执行教训总结的完整工作流程。推送前必须质量检查。

## 流程总览

```
① 加载配置 → ② 数据采集 → ③ 分类打标 → ④ 报告生成 → ⑤ 质量检查 → ⑥ 推送 → ⑦ 复盘 → ⑧ 更新skill
```

| 环节 | 时间 | 关键动作 | 已知教训 |
|------|------|---------|---------|
| ① 加载配置 | 2min | 加载full版skill | 默认加载core版，缺关键规则 |
| ② 数据采集 | 30-60min | 分阶段采集102源 | 只做了7源，行业应用缺链接 |
| ③ 分类打标 | 同步 | Step 1-6逐项判断 | 4个分类错误（凭印象判断） |
| ④ 报告生成 | 15min | 按模板逐板块 | 40%内容缺失 |
| ⑤ 质量检查 | 5min | 逐板块核对skill | 完全跳过 |
| ⑥ 推送 | 5min | 2-3段+30秒间隔 | 8段触发限流 |
| ⑦ 复盘 | 5min | 对比skill要求 | 做了但不完整 |
| ⑧ 更新skill | 5min | 添加pitfall | 做了3次修正 |

---

## ① 加载配置（2分钟）

- 加载skill（**必须full版**，skill_view默认加载core版）
- 读取source_registry.yaml（102源）
- 检查GitHub API额度
- 确认推送方式（cron日常/手动非日常）

---

## ② 数据采集（分阶段，每阶段≤4分钟）

### Phase 1: API源
- GitHub API（新项目+热门+releases）→ **同步打分类标签**
- HN Algolia（AI热帖）
- OpenRouter（模型定价）

### Phase 2: RSS源
- 36kr RSS（行业新闻+**必须保存链接**）
- V2EX（中文社区）
- 国际媒体RSS（The Verge/TechCrunch）

### Phase 3: 补充源
- 模型官网（定价/版本）
- 行业媒体（量子位/机器之心）
- 降级重试（之前失败的源）

---


## ②.5 数据验证（时间戳）（2026-05-31新增，必须执行）

**⚠️ 必须区分"今日/本周/历史"，不能只检查是否在7天窗口内**

```python
def verify_data(hn_items, gh_repos, today_str, week_ago_str):
    """验证数据时间戳，区分今日/本周/历史"""
    # HN数据分类
    hn_today = [h for h in hn_items if h.get("created","")[:10] == today_str]
    hn_week = [h for h in hn_items if h.get("created","")[:10] >= week_ago_str and h.get("created","")[:10] != today_str]
    hn_old = [h for h in hn_items if h.get("created","")[:10] < week_ago_str]
    
    # GitHub数据分类
    gh_today = [r for r in gh_repos if r.get("created","")[:10] == today_str]
    gh_week = [r for r in gh_repos if r.get("created","")[:10] >= week_ago_str and r.get("created","")[:10] != today_str]
    gh_old = [r for r in gh_repos if r.get("created","")[:10] < week_ago_str]
    
    return {
        "hn": {"today": hn_today, "week": hn_week, "old": hn_old},
        "github": {"today": gh_today, "week": gh_week, "old": gh_old}
    }
```

**报告模板要求**：
- 高星Agent标注"本周热门"而非"今日新增"
- 新Agent标注"本周HN热点"
- 数据面板增加"今日/本周/历史"分类统计

**验证清单**：
- [ ] 是否调用了verify_data()函数
- [ ] 数据面板是否区分"今日/本周/历史"
- [ ] 高星Agent是否标注"本周热门"

---

## ②.5 去重机制（必须执行，最高优先级）
**目标**：确保整个流程中无重复项目

**三个阶段的去重机制**：

1. **搜索阶段去重**：
```python
collected_projects = set()  # 已收集项目集合

def collect_with_dedup(project):
    if project["name"] in collected_projects:
        return None  # 跳过重复
    collected_projects.add(project["name"])
    return project
```

2. **分类阶段去重**：
```python
classified_projects = {}  # 已分类项目字典

def classify_with_dedup(project):
    if project["name"] in classified_projects:
        return classified_projects[project["name"]]  # 返回已分类结果
    # 执行分类...
    classified_projects[project["name"]] = category
    return category
```

3. **报告阶段验证**：
```python
def check_report_duplicates(report_content):
    # 检查报告中是否有重复项目出现在不同板块
    # 如有重复，保留第一次出现的板块，删除后续重复
    pass
```

**验证清单**：
- [ ] 搜索阶段：是否建立已收集项目集合
- [ ] 分类阶段：是否建立已分类项目字典
- [ ] 报告阶段：是否执行重复检查
- [ ] 整个流程：是否记录去重统计


## ②.6 SPA站点抓取方案（必须执行）
**问题**：SPA（单页应用）站点需要JavaScript渲染，传统抓取方法无法获取数据

**解决方案**：

### 1. 首选方案：Crawlee (Python版本)
```python
# 安装
# pip install crawlee playwright browserforge
# playwright install

from crawlee.crawlers import PlaywrightCrawler  # 注意：是 crawlee.crawlers 不是 crawlee.playwright_crawler

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

### 2. 备选方案：Playwright + Python
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

### 3. AI驱动方案：LLM Scraper
```python
# 安装
# pip install llm-scraper

from llm_scraper import LLMScraper

scraper = LLMScraper()
data = scraper.scrape('https://artificialanalysis.ai')
print(data)
```

### 4. 降级策略
当SPA站点无法访问时，按以下顺序降级：
1. **第一降级**：使用OpenRouter API获取模型列表和价格
2. **第二降级**：使用GitHub Trending获取模型相关项目
3. **第三降级**：使用HN搜索模型相关新闻

**验证清单**：
- [ ] 是否安装了Crawlee或Playwright
- [ ] 是否测试了SPA站点抓取
- [ ] 是否处理了JavaScript渲染
- [ ] 是否提取了结构化数据
- [ ] SPA站点失败时是否执行降级策略

## ③ 分类打标（采集时同步执行）

**⚠️ Step 0 必须先查已知项目表（2026-05-30新增，极度重要）：**

```python
# 先查 KNOWN_CLASSIFICATIONS 表（见 references/classification-python-function.md）
full_name = repo.get("full_name", "")
if full_name in KNOWN_CLASSIFICATIONS:
    cat, subcat = KNOWN_CLASSIFICATIONS[full_name]
    return cat, subcat  # 跳过 Step 1-6
```

**为什么必须 Step 0**：hermes-agent(⭐173K)、opencode(⭐167K)、superpowers(⭐212K) 这类高星项目，描述措辞模糊，启发式规则必然误判。速查表是唯一的可靠分类方式。

**然后走Step 1-6流程，不能凭印象判断：**

```
Step 1: 描述含"skill(s)" → Skills
Step 2: 主要是.md文件 → Skills
Step 3: 描述含"mcp server"/"model context protocol" → MCP（优先MCP板块）
Step 4: 描述含"for ai agents"/"for claude"/"let ai agents" → 组件
Step 5: 描述含"ai agent"/"agent for"/能独立执行任务 → Agent
Step 6: 以上都不满足 → 组件
```

**已知误判案例**：
| 项目 | 错误分类 | 正确分类 | 错误原因 |
|------|---------|---------|---------|
| ADHD | Agent | Skills | 凭搜索来源判断，未走Step 1 |
| Agent OSS | Agent | 组件 | 凭"能独立运行"判断，未走Step 4 |
| WrenAI | Agent | 组件 | 凭功能判断，忽略"Give AI agents" |
| HexStrike | Agent | MCP | 凭名称判断，忽略"MCP server" |
| Gemini CLI | 组件 | Agent | 代码bug："cli not in desc" |
| hermes-agent | 组件 | Agent(全) | 2026-05-30：describe "agent that grows" 但代码未匹配 |
| opencode | 组件 | Agent(全) | 2026-05-30："open source coding agent" 被误判为框架 |
| superpowers | 组件 | Skill | 2026-05-30："agentic skills framework" = skills仓库非组件 |

---

## ④ 报告生成（按模板逐板块）

### 一、Agent生态
- 使用指南（少写+链接）
- 新全能Agent（前辈对比表：功能/成本/自主性/易用性/适用场景）
- 高星全能Agent（对比表+拆分+归纳）
- 新专精Agent（前辈对比）— 当日没有新的推荐5个高星的
- 高星专精Agent
- 新组件（解决什么问题+原理+适用Agent+GitHub链接）
- 高星组件（ECC等）

### 二、Skills市场（6类）
每个Skill必须包含：GitHub链接+痛点类型+原理+案例+前辈对比+高星Skills对比

### 三、模型动态
- 第一层：模型官网（9个模型厂商）
- 第二层：排名网站（OpenRouter实测）
- 第三层：调用网站（价格变化）

### 四、行业应用（≥3行业+可点击链接+技术原理）

### 五、MCP动态（新MCP+安全问题+Agent关联）

### 六、数据面板
### 七、核心信号（3-7条）
### 八、AI基础教育（每日一则）

---


### 详细质量检查要求（必须逐项核对）

#### 1. Skills板块检查
- [ ] 每个Skill是否有完整的原理分析（🎯原理+🔧操作+📊效果+👤案例）
- [ ] 每个Skill是否有前辈对比表
- [ ] 每个Skill是否有真实使用案例
- [ ] 每个Skill是否有GitHub链接

#### 2. MCP板块检查
- [ ] 是否搜索了具体MCP项目
- [ ] 每个MCP项目是否有GitHub链接+Stars+功能
- [ ] 是否有生态趋势分析
- [ ] 是否有与Agent/Skills的关联

#### 3. 模型动态检查
- [ ] 模型版本是否精确到小版本
- [ ] 是否有综合能力排名
- [ ] 是否有编码能力排名
- [ ] 是否有性价比排名
- [ ] SPA站点失败时是否执行降级策略

#### 4. 格式检查
- [ ] 板块顺序是否正确：Agent生态 → Skills市场 → 模型动态 → 行业应用 → MCP动态 → 数据面板 → 核心信号
- [ ] 无板块标题重复
- [ ] 所有事件是否有可点击的原文链接

#### 5. 内容完整性检查
- [ ] 行业应用覆盖≥3个行业
- [ ] 每个事件说明解决什么行业问题
- [ ] 每个事件说明技术原理

## ⑤ 质量检查（推送前必须执行，逐项核对skill）

**⚠️ 必须加载skill，逐板块对照skill要求核对，不能凭记忆检查。**

```
检查顺序：
1. 加载skill（skill_view加载full版）
2. 逐板块读取报告内容
3. 对照skill要求逐项检查
4. 缺失项标记为待补充
5. 补充完成后再检查
6. 全部通过后才进入推送
```

**逐板块检查清单：**

```
□ Agent生态：
  □ 使用指南（链接）
  □ 新全能Agent（前辈对比表）
  □ 高星全能Agent（对比表+拆分+归纳）
  □ 新专精Agent（前辈对比）— 没有新的推荐5个高星
  □ 高星专精Agent
  □ 新组件（解决什么问题+原理+适用Agent+链接）
  □ 高星组件（ECC等）

□ Skills市场：
  □ 6类都有覆盖
  □ 每个Skill有GitHub链接
  □ 每个Skill有痛点类型
  □ 每个Skill有原理分析（原理+操作+效果+案例）
  □ 每个Skill有前辈对比
  □ 有高星Skills对比（html-anything等）

□ 模型动态：
  □ 第一层：模型官网（9个厂商）
  □ 第二层：排名网站（OpenRouter）
  □ 第三层：调用网站（价格变化）
  □ 版本精确到小版本

□ 行业应用：
  □ ≥3个行业
  □ 每个事件有可点击链接
  □ 每个事件有技术原理

□ MCP动态：
  □ 新MCP服务器（stars>100）
  □ MCP重要更新
  □ MCP安全问题
  □ 与Agent/Skills关联
  □ 分类正确（MCP server不是Agent）

□ 数据面板：源统计+分类统计
□ 核心信号：3-7条+基于数据
□ 教育板块：每日一则
```

**不通过 → 补充 → 再检查 → 通过后才推送**

---

## ⑥ 推送

**日常（cron）**：final response自动推送，不会限流

**非日常（手动）**：
- 合并为2-3段长消息（每段3000-4000字）
- **每段间隔≥60秒**（30秒会触发ret=-2限流，2026-05-31验证）
- 限流后等待120s→300s→600s
- 超过3次限流→保存到本地→告知用户

---

## ⑦ 复盘优化（必须执行，不能跳过）

**⚠️ 即使推送失败，也必须完成复盘和更新skill。中途停下=没做。**

**执行完整性检查清单**：
- [ ] 列出了所有执行步骤的实际结果
- [ ] 对比了预期结果，标记差异
- [ ] 追踪了每个差异的根因（思维追踪法：实际→预期→根因）
- [ ] 记录了所有问题和解决方案
- [ ] 更新了skill（添加pitfall）
- [ ] 确认下次执行能避免同样问题

- 对比skill要求，记录缺失板块
- 分析分类错误原因
- 更新检查清单
- 记录推送问题

---

## ⑧ 更新skill

- 新pitfall → 添加到SKILL.md
- 分类规则修正 → 更新Step 1-6
- 推送策略调整 → 更新P17
- 质量检查清单 → 添加到流程
