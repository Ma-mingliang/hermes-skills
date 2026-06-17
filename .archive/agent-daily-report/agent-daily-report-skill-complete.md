# Agent Daily Report Skill Complete Documentation

整合时间：2026-06-01 16:09:06 +08:00

本文档将 `agent-daily-report` skill 目录中的主文件、参考文件、模板文件与其他文本内容整合为一个完整文档。原始文件边界已保留，便于后续追溯和维护。

## 文件清单

| 顺序 | 文件 | 大小(bytes) | 修改时间 | 说明 |
|---:|---|---:|---|---|
| 1 | `SKILL.md` | 16045 | 2026-06-01 16:09:01 | skill 主说明、元数据、系统定位、架构、运行方式、规则总览 |
| 2 | `references/source_status_spec.md` | 4375 | 2026-06-01 15:24:31 | source_status 统一状态规范 |
| 3 | `references/search-strategy.md` | 4392 | 2026-06-01 15:27:02 | 信息源权重与搜索策略 |
| 4 | `references/github-collector-architecture.md` | 3271 | 2026-06-01 16:06:57 | GitHub Intelligence Collector 四池架构与生命周期设计 |
| 5 | `references/collector_patterns.md` | 7540 | 2026-06-01 15:24:01 | 各采集器降级链与配置模式 |
| 6 | `references/classification-rules.md` | 3282 | 2026-06-01 15:22:59 | 分类规则与标签规则 |
| 7 | `references/scoring-formulas.md` | 2431 | 2026-06-01 15:26:00 | 唯一评分公式细则 |
| 8 | `references/scoring-system.md` | 2496 | 2026-06-01 14:22:36 | Deprecated 评分系统参考，保留原文 |
| 9 | `references/implementation-patterns.md` | 8664 | 2026-06-01 16:05:33 | 实现模式、陷阱与代码片段 |
| 10 | `templates/config-template.yaml` | 5031 | 2026-06-01 16:08:15 | 配置模板 |

## 整合说明

- 本次使用动态扫描生成，已包含所有 `.md`、`.yaml`、`.yml`、`.json`、`.txt` 源文件。
- 旧产物 `agent-daily-report-skill-complete.md` 已排除，避免递归合并。
- `references/scoring-system.md` 已标记 deprecated；本文档仍完整保留其原文，供历史追溯。

---

# Source File: SKILL.md

---
name: agent-daily-report
description: "Daily Agent ecosystem intelligence report. Collects from 10 sources with unified source_status, RSS fallback, hash diff detection. Covers GitHub, HackerNews, LinuxDo, V2EX, NodeSeek, Model Docs, Reddit, Product Hunt, HuggingFace, Framework Docs."
version: "3.1.0"
tags: ["agent", "mcp", "workflow", "skill", "coding-agent", "research", "intelligence", "developer-community"]
---

# Agent Daily Report v2.1

每日 Agent 生态情报日报系统。

## 系统定位

面向 Hermes / OpenClaw / Claude Code / Coding Agent / MCP / Workflow / Skill 的工程情报日报。

## When to Use

- 用户说"agent日报"、"agent情报"、"agent ecosystem report"
- 需要追踪 Agent 生态最新动态
- 需要发现可集成到 Hermes 的新工具/MCP/Skill

## Key Difference from ai-daily-digest

| 维度 | agent-daily-report | ai-daily-digest |
|------|-------------------|-----------------|
| 定位 | Agent 工程情报 | AI 新闻日报 |
| 信息源 | 10源，GitHub为主(35%) | HN+GitHub+36氪 |
| 分类 | 13类严格分类 | 3大类(Agent/Skills/组件) |
| 评分 | 5维度100分 | 无量化评分 |
| 重点 | 可操作性、可集成性 | 新闻覆盖面 |
| 目标用户 | Agent 开发者 | 通用 AI 读者 |

## 系统位置

```
D:/openclaw-hermes/agent-daily-report-skill/
```

## 运行方式

```bash
cd D:/openclaw-hermes/agent-daily-report-skill
python main.py                      # 完整运行
python main.py --dry-run            # 预览，不写状态不推送
python main.py --sources github,v2ex # 只运行指定源
python main.py --no-push            # 不推送
python main.py --debug              # 详细日志
python main.py --date 2026-06-01    # 指定日期
python main.py --output test.md     # 自定义输出路径
```

### Collector --test 模式

每个 collector 支持独立测试：
```bash
python scripts/collect_github.py --test
python scripts/collect_v2ex.py --test
python scripts/collect_hackernews.py --test
# ... 其他 collector 同理
```
输出 JSON，不写正式数据文件，不更新长期 state。

输出：`data/reports/Agent_Daily_Report_YYYY-MM-DD.md`

## 架构

```
main.py                     # 主入口，safe_collect 保证单源失败不中断
scripts/
  source_status.py          # 统一状态规范（9种枚举 + auth/strategy_used）
  collect_github.py         # GitHub 四池架构: Watch/Discovery/Growth/Event + Lifecycle
  github_state.py           # GitHub repo state管理: 快照/增长计算/生命周期
  collect_hackernews.py     # Firebase API + Algolia Search（72h限制，story only）
  collect_linuxdo.py        # RSS → JSON → HTML fallback
  collect_v2ex.py           # V2EX API
  collect_nodeseek.py       # RSS only（https://rss.nodeseek.com/）
  collect_model_docs.py     # hash diff 变更检测（含首次baseline）
  collect_reddit.py         # RSS first + OAuth API optional
  collect_producthunt.py    # RSS first + GraphQL API optional
  collect_huggingface.py    # HuggingFace API
  collect_framework_docs.py # hash_diff 变更检测
  rss_parser.py             # feedparser → ET → regex 三级解析
  normalize_items.py        # 数据标准化 + negative_keywords 过滤
  deduplicate_items.py      # URL去重 + 标题去重 + 事件级合并
  classify_items.py         # 内容实体优先分类
  score_items.py            # 评分 + actionability 评估
  generate_report.py        # 报告生成（含 Source Status 表 + section quota）
state/
  source_state.json         # NodeSeek RSS endpoint 缓存
  model_docs_state.json     # 模型文档 hash 缓存
  daily_state.json          # 每日运行状态
data/
  reports/                  # 日报输出
  raw/                      # 原始数据
  scored/                   # 评分数据
  source_status/            # 各源状态 JSON
logs/
  run.log                   # 运行日志
```

## 统一 source_status 规范

所有 collector 返回 `(items, source_status)` 元组。source_status 中不包含 items。

9 种状态：
| 状态 | 含义 |
|------|------|
| success | 正常采集且有关键词命中 |
| success_no_match | 采集成功但无关键词命中 |
| checked_no_change | 文档类：页面无变化（hash diff）或首次 baseline |
| skipped_disabled | config 中 enabled=false |
| skipped_missing_auth | 缺少必需的环境变量（仅限纯API源） |
| failed_network | 网络失败、超时、DNS 失败 |
| failed_parse | 响应无法解析 |
| failed_auth | 认证失败（401/403） |
| failed_rate_limited | 被限流（429） |

source_status 结构（无 items 字段）：
```json
{
  "source": "name",
  "enabled": true,
  "status": "success",
  "auth": "ok|missing|failed|none|n/a",
  "strategy_used": "api|rss|rss_fallback|hash_diff|scrape|api_and_search|api_degraded",
  "raw_count": 100,
  "matched_count": 10,
  "selected_count": 0,
  "errors": [],
  "warnings": []
}
```

selected_count 由 main.py 在评分筛选后回填。

## 信息源权重与策略

| 信息源 | 权重 | 策略 | 认证 |
|--------|------|------|------|
| GitHub | 35% | api / api_limited | token_optional |
| Hacker News | 15% | api_and_search | 无 |
| LinuxDo | 10% | rss→json→html | 无 |
| 模型文档 | 10% | hash_diff（含baseline） | 无 |
| Reddit | 8% | rss_first + api_optional | OAuth optional |
| V2EX | 6% | api | 无 |
| Product Hunt | 5% | rss_first + api_optional | token optional |
| NodeSeek | 4% | rss | 无 |
| Hugging Face | 4% | api | HF_TOKEN optional |
| 框架文档 | 3% | hash_diff | 无 |

## 采集器 fallback 策略

| 采集器 | 策略 | 缺认证行为 |
|--------|------|-----------|
| GitHub | API (token_optional) | 有token→认证API；无token→未认证API降级（减少请求量）；API失败→failed_network/failed_rate_limited |
| Hacker News | Firebase API + Algolia Search | 无需认证；Algolia限72h；默认只抓story；合并后先去重再过滤 |
| LinuxDo | RSS → JSON → HTML fallback | 无需认证 |
| NodeSeek | RSS only (rss.nodeseek.com) | 无需认证 |
| Model Docs | hash_diff 变更检测 | 无需认证；首次运行只保存baseline |
| Reddit | RSS first → OAuth API optional | 缺 token 用 RSS，返回 success |
| Product Hunt | RSS first → GraphQL API optional | 缺 token 用 RSS，返回 success |
| V2EX | API | 无需认证 |
| HuggingFace | API | 无需认证 |
| Framework Docs | hash_diff 变更检测 | 无需认证 |

## GitHub Intelligence Collector (v3.0)

四池架构：

| Pool | 职责 | 展示规则 |
|------|------|---------|
| Watch Pool | 固定核心项目监控（10个） | 无变化不展示，有变化才进日报 |
| Discovery Pool | GitHub Search 新项目发现 | 经 lifecycle D0 分流后，仅 spike/强相关展示 |
| Growth Pool | 历史快照增长 + 实时 stargazers | star_delta_24h/7d/30d + realtime spike |
| Event Pool | release / issue / PR 事件 | 重要事件进对应板块 |

Lifecycle: discovered → spike_hold → probation_7d → candidate_30d → watchlist → archived / dropped

state/github_repo_state.json 记录每个 repo 的 snapshot、metrics、lifecycle 状态。
缺失历史 delta = null，不写成 0。
首次运行只建 baseline，历史增长榜暂无数据。

## 分类体系（13类 — 内容实体优先）

分类规则：**内容实体优先，不按 source 简单分类**。
- 不得简单用 source == producthunt 就归 Product
- 不得简单用 source in [hackernews, linuxdo, v2ex, nodeseek, reddit] 就归 Community
- HN/Reddit/LinuxDo/V2EX/NodeSeek 上的 MCP 内容 → primary_category = MCP，secondary_categories 包含 Community
- Product Hunt 上的 AI IDE → primary_category = Coding Agent 或 Product，secondary_categories 记录 Product

1. **Model**: 大模型、专用模型、代码模型
2. **Agent Framework**: Agent 编排框架、多 Agent 框架
3. **General Agent**: 通用任务执行 Agent
4. **Specialized Agent**: 垂直领域 Agent
5. **Coding Agent**: 代码生成、修复、测试 Agent
6. **MCP**: Model Context Protocol 生态
7. **Tool / Plugin / Connector**: 工具与连接器
8. **Workflow**: 多步骤任务流程
9. **Skill**: 可复用能力包
10. **Research**: 学术论文
11. **Product**: 商业产品
12. **Business**: 融资、收购
13. **Community**: 社区讨论（仅当内容无强实体信号时）

## 评分规则

总分 0-100 = relevance(30) + popularity(20) + freshness(15) + growth(15) + utility(20)

**唯一评分公式**。`references/scoring-system.md` 已标记 deprecated，代码不得引用。

- **S (85-100)**: 必须推送
- **A (70-84)**: 重点关注
- **B (55-69)**: 普通收录
- **C (40-54)**: 备选
- **D (0-39)**: 忽略

Community 来源不天然低分。按内容主题评分：与 MCP / Coding Agent / Workflow / Model API 强相关的社区讨论获得较高 relevance 和 utility。

## report_layout (section quota)

日报按 section quota 输出，不是只按总分平铺。

| Section | target | max |
|---------|--------|-----|
| total_selected_items | 35 | 45 |
| top_events | 5 | 6 |
| github_growth | 5 | 8 |
| agent_coding_agent | 4 | 6 |
| mcp | 3 | 5 |
| workflow_skill | 3 | 5 |
| tools_connectors | 3 | 5 |
| model_api | 3 | 5 |
| community_signals | 3 | 5 |
| producthunt | 2 | 4 |
| insights | 3 | 3 |
| recommendations | 3 | 5 |

## Actionability 评估

每个入选 item 包含 actionability 字段：
```json
{
  "level": "high|medium|low",
  "recommended_action": "Evaluate for Hermes integration",
  "hermes_integration": "tool|skill|workflow|watch_only|ignore",
  "effort": "low|medium|high"
}
```

## 事件级合并

使用 normalized_entity + event_type + date_bucket 生成 event_key。
同一事件来自 GitHub、HN、Reddit、LinuxDo 等多个来源时合并为 related_items。
多源共振提高评分（+3/相关源）。

## Negative Keywords

过滤非 AI Agent 内容：
real estate agent, travel agent, insurance agent, sales agent, hiring, job, recruiting, coupon, giveaway, scholarship, estate, realtor, broker, travel agency

## 中文关键词

智能体、代码智能体、编程智能体、工具调用、函数调用、工作流、自动化、上下文、长上下文、提示词、记忆、多智能体、浏览器控制、电脑控制

## arXiv / Research

daily report 默认不采集 arXiv（weekly_only）。
只有极高价值论文才进入每日。
Research Weekly 单独输出。

## RSS 解析优先级

1. feedparser（首选）
2. xml.etree.ElementTree（次选）
3. regex（fallback）

## V2EX 采集规范

策略: Classic Public API first, 不需要认证, 不使用 HTML scrape。
- endpoints: latest.json, hot.json, show.json?node_name={node}
- 默认 nodes: programmer, create, qna, python, go, nodejs, linux, cloud, server, openai, ai, jobs
- jobs 节点低权重，命中 hiring/job/recruiting 时触发 negative_keywords

## Quality Gates

- 空标题、空 URL、空 summary 过滤
- 低信号社区帖（无工具名/模型名/配置/价格/部署信息）降分或丢弃
- 同一 source 占比 ≤ 45%
- 同一 category 占比 ≤ 35%
- 低质量模式: 求推荐、水一贴、闲聊、招聘、优惠券、抽奖、薅羊毛

## Cost Signal

Model/API/Provider/Pricing/Cache 相关 item 自动提取 cost_signal：
- has_pricing, has_cache, input_price, output_price
- cost_impact: lower/higher/neutral/unknown
- routing_impact: recommended/watch/avoid/unknown
- 提取不到数值时字段为 null，不编造

## Schema Version

所有 JSON 输出顶层必须包含 schema_version="2.0"。
读取旧文件时缺 schema_version 按 legacy 处理，写 warning，不崩溃。

## 空日报策略

- selected_items < 10 时仍生成日报
- 报告标记 **Low Signal Day**
- 保留 Source Status 表
- 今日洞察改为"数据不足，不生成强趋势判断"
- 不强行把 C/D 级内容补进正文
- daily_state.report_summary.low_signal_day = true

## 同源去重与跨源合并

同源重复 = 噪声，删除或合并，只保留最完整/最高分 item。
不同 source 提到同一项目/事件 = 强信号，合并为 related_items，提高 cross_source_count 和 score。
- 同源去重: URL exact match + title similarity ≥ 0.90
- 跨源合并: title similarity ≥ 0.85 + entity match, +3/related source, max +10

## 日报板块

日报开头展示 Source Status 表：

| Source | Auth | Strategy Used | Status | Raw | Matched | Selected | Notes |
|---|---|---|---|---:|---:|---:|---|

正文板块（按 section quota 输出）：
1. 今日关键事件
2. GitHub 高增长项目
3. Agent / Coding Agent 动态
4. MCP 生态
5. Workflow / Skill
6. Tool / Plugin / Connector
7. 模型与 API 变化
8. 开发者社区信号
9. Product Hunt 新产品
10. 今日洞察
11. 今日建议关注

## 环境变量

| 变量 | 必需 | 用途 |
|------|------|------|
| GITHUB_TOKEN / GITHUB_PERSONAL_ACCESS_TOKEN | 否 | GitHub API（有则认证，无则降级） |
| REDDIT_CLIENT_ID | 否 | Reddit OAuth（缺则 RSS fallback） |
| REDDIT_CLIENT_SECRET | 否 | Reddit OAuth |
| REDDIT_USER_AGENT | 否 | Reddit User-Agent |
| PRODUCTHUNT_TOKEN | 否 | Product Hunt GraphQL（缺则 RSS fallback） |
| HF_TOKEN | 否 | HuggingFace API |

## Key Pitfalls

| ID | 问题 | 解决 |
|----|------|------|
| P1 | `.env` 中是 `GITHUB_PERSONAL_ACCESS_TOKEN` 不是 `GITHUB_TOKEN` | collect_github.py 加 fallback 检查两个名字 |
| P2 | source_status 的 auth/strategy_used 需在函数签名声明 | make_source_status 加参数 |
| P3 | Python patch 替换时 STATUS_SUCCESS 被部分匹配到 STATUS_SUCCESS_NO_MATCH | 替换顺序：先长后短 |
| P4 | NodeSeek RSS candidates 全部不可用 | 改用 https://rss.nodeseek.com/ |
| P5 | Reddit/PH 缺 token 时返回 skipped_missing_auth | RSS first + API optional |
| P6 | collect_hn.py 缺少 Optional 导入 | py_compile 验证所有 import |
| P7 | 单个 collector 异常导致日报中断 | main.py 用 safe_collect() 包裹 |
| P8 | WSL 下 write_file/read_file 失败 | 用 execute_code 内 open() |
| P9 | 采集返回 0 条≠失败 | 用 source_status 枚举判断 |
| P10 | source_status 中包含 items 字段 | 已移除，selected_count 由 main.py 回填 |
| P11 | Community 来源天然低分 | 按内容主题评分，MCP/Agent 讨论高分 |
| P12 | source == producthunt 就归 Product | 内容实体优先，PH 上的 AI IDE 归 Coding Agent |
| P13 | Model Docs 首次运行无 baseline | 首次只保存 hash，不进日报 |
| P14 | Framework Docs 用 scrape 而非 hash_diff | 已改为 hash_diff |
| P15 | HN Algolia 无时间限制 | 限72小时 |
| P16 | scoring-system.md 被代码引用 | 已标记 deprecated，代码不得引用 |

## 输出

- 日报: `data/reports/Agent_Daily_Report_YYYY-MM-DD.md`
- 原始数据: `data/raw/YYYY-MM-DD.json`
- 评分数据: `data/scored/YYYY-MM-DD.json`
- 源状态: `data/source_status/YYYY-MM-DD.json`
- 运行日志: `logs/run.log`

## References

- 实现位置：`D:/openclaw-hermes/agent-daily-report-skill/`
- 配置文件：`config.yaml`
- source_status 规范：`scripts/source_status.py`
- 采集器模式：各 `scripts/collect_*.py`
- **实现模式：`references/implementation-patterns.md`** — safe_collect wrapper, RSS fallback, hash_diff, endpoint discovery, dual API
- **评分公式：`references/scoring-formulas.md`** — 唯一评分公式
- **分类规则：`references/classification-rules.md`** — 内容实体优先
- **~~评分系统：`references/scoring-system.md`~~** — DEPRECATED，不得引用
- **GitHub 架构：`references/github-collector-architecture.md`** — 四池架构、Lifecycle、state 结构

---

# Source File: references/source_status_spec.md

# Source Status 统一规范 v2.1

## 9 种状态枚举

| Status | 含义 | 何时使用 |
|---|---|---|
| `success` | 正常采集，有匹配数据 | raw_count > 0, matched_count > 0 |
| `success_no_match` | 采集成功但无关键词命中 | raw_count > 0, matched_count = 0 |
| `checked_no_change` | 文档类源：hash 未变或首次 baseline | 仅用于 hash_diff 变更检测 |
| `skipped_disabled` | config 中 enabled=false | 配置禁用 |
| `skipped_missing_auth` | 缺少 token/client_id/secret | 仅限纯 API 源（不能降级） |
| `failed_network` | 网络失败/DNS/超时/5xx | 连接层错误 |
| `failed_parse` | 响应无法解析 | RSS/JSON/HTML/GraphQL 解析失败 |
| `failed_auth` | 认证信息存在但认证失败 | 401, 403 |
| `failed_rate_limited` | 被限流 | 429 |

## 统一返回结构（无 items 字段）

```python
{
    "source": "reddit",
    "enabled": True,
    "status": "success",
    "auth": "missing",          # ok / missing / failed / n/a / none
    "strategy_used": "rss",     # api / rss / rss_fallback / api_and_search / hash_diff / scrape / api_degraded
    "raw_count": 257,
    "matched_count": 48,
    "selected_count": 0,        # main.py 在评分后回填
    "errors": [],
    "warnings": ["OAuth missing, used RSS fallback"]
}
```

**source_status 中不包含 items。** items 由 collector 直接返回。

**selected_count 由 main.py 在评分筛选后回填**，collector 初始返回 0。

### auth 字段取值
| 值 | 含义 |
|---|---|
| `ok` | 认证正常 |
| `missing` | 缺少认证环境变量（但可能有降级策略） |
| `failed` | 认证信息存在但认证失败 |
| `n/a` | 该源不需要认证 |
| `none` | 明确标注无认证需求 |

### strategy_used 字段取值
| 值 | 含义 |
|---|---|
| `api` | 纯 API 调用（有认证） |
| `api_degraded` | API 调用（无认证，降级模式） |
| `rss` | RSS 采集 |
| `rss_fallback` | 原计划用 API，降级为 RSS |
| `api_and_search` | Firebase API + Algolia Search 组合 |
| `hash_diff` | 文档 hash 变更检测 |
| `scrape` | HTML 页面关键词检测 |
| `rss+json+html` | 多级 fallback（LinuxDo） |

## Collector 返回签名

所有 collector 必须返回 `Tuple[List[Dict], Dict]`：

```python
def collect_xxx(config: Dict[str, Any]) -> Tuple[List[Dict], Dict]:
    return items, source_status
```

## main.py 安全调用模式

```python
def safe_collect(name, collect_fn, config, logger):
    try:
        items, source_status = collect_fn(config)
        return items, source_status
    except Exception as e:
        return [], make_source_status(
            source=name, status="failed_network",
            errors=[f"Collector exception: {e}"],
        )
```

关键规则：单个 collector 异常不能中断日报生成。

## selected_count 回填

main.py 在评分筛选后回填 selected_count：

```python
# After scoring
selected_per_source = {}
for item in scored_items:
    if item.get("importance_level") in ["S", "A", "B"]:
        src = item.get("source", "unknown")
        selected_per_source[src] = selected_per_source.get(src, 0) + 1
for name, st in all_statuses.items():
    st["selected_count"] = selected_per_source.get(name, 0)
```

## source_status.py 工厂函数

提供快捷函数避免重复代码：
- `skipped_disabled(source)` → `([], status)`
- `skipped_missing_auth(source, missing_vars)` → `([], status)`
- `failed_network(source, error)` → `([], status)`
- `failed_parse(source, error)` → `([], status)`
- `failed_auth(source, error)` → `([], status)`
- `failed_rate_limited(source, error)` → `([], status)`

## 日报 Source Status 表格

日报开头必须展示：

```
| Source | Auth | Strategy Used | Status | Raw | Matched | Selected | Notes |
|---|---|---|---|---:|---:|---:|---|
| GitHub | missing | api_degraded | ✅ success | 15 | 15 | 8 | Data collected successfully |
| LinuxDo | n/a | rss | ✅ success | 52 | 7 | 4 | Data collected successfully |
| Model Docs | n/a | hash_diff | ⚪ checked_no_change | 8 | 0 | 0 | All pages checked, no hash change |
| Model Docs | n/a | hash_diff | ⚪ checked_no_change | 6 | 0 | 0 | baseline initialized (first run) |
```

Notes 生成规则按9种状态分别处理。

---

# Source File: references/search-strategy.md

# Search Strategy Reference (v2.1)

## Source Weights (content value, not request count)

| Source | Weight | Role |
|--------|--------|------|
| GitHub | 35% | Discover projects, track growth, find releases/issues/PRs (token_optional) |
| LinuxDo/V2EX/NodeSeek | 20% | Chinese dev real experience, deployment, cost, API routing |
| Hacker News | 15% | Early signal from international dev community (72h Algolia limit) |
| Model Docs | 10% | API changes, pricing, context, tool calling, compatibility (hash_diff + baseline) |
| Reddit | 8% | Real user feedback, comparisons, migration trends (RSS first) |
| Product Hunt | 5% | New Agent/AI IDE/automation product launches (RSS first) |
| Hugging Face | 4% | Open models, demos, tool-use/code models |
| Framework Docs | 3% | MCP/LangGraph/OpenHands/CrewAI/AutoGen infrastructure changes (hash_diff) |
| arXiv | Weekly | Research trends, not daily priority |

## GitHub (35%) — What to Collect

### Token Strategy
- 有 GITHUB_TOKEN 或 GITHUB_PERSONAL_ACCESS_TOKEN → 认证 API，正常 rate limit
- 无 token → 未认证 API 降级采集，减少请求量（max_results_no_token: 20）
- 只有 API 访问失败或限流时才返回 failed_network / failed_rate_limited

### A. New/High-Growth Repos
- Search by keywords: agent, ai-agent, mcp, workflow, coding-agent, tool-use, browser-agent, computer-use
- Track: stars, forks, star_delta_24h, topics, language

### B. Releases
- From watch_repos: OpenHands, LangGraph, AutoGen, CrewAI, PydanticAI, Mastra, MCP servers, browser-use, aider, SWE-agent
- Focus: new Agent capabilities, MCP support, tool calling, runtime/sandbox, breaking changes

### C. Issues
- High-comment issues = user pain points, feature requests, roadmap signals

### D. Pull Requests
- PRs often reflect trends before releases

## Chinese Developer Communities (20%)

### LinuxDo
- Focus: Claude Code, Codex, Cursor, OpenClaw, Hermes, DeepSeek, Kimi, GLM, Mimo, MCP, API routing, LiteLLM, deployment, cost optimization
- Value: real testing, configuration methods, pitfall experiences

### V2EX
- Nodes: program, share, qa, ai, dev
- Focus: Claude Code, Codex, Cursor, AI IDE, MCP, Agent, automation scripts

### NodeSeek
- Focus: Agent deployment, API gateway, LiteLLM, model relay, server config

## Hacker News (15%)

- Sources: top/new/best stories + Algolia keyword search
- **Algolia 限最近 72 小时**
- **默认只抓 story**，comment 在 story 入选后补充
- **合并 Firebase + Algolia 后先去重再过滤**
- Focus: points, comments depth, GitHub project links

## Model Official Docs (10%)

- **hash_diff 变更检测**，不是新闻源
- **首次运行只保存 baseline，不进入日报**
- Providers: Anthropic, OpenAI, DeepSeek, Kimi, GLM, Mimo

## Reddit (8%)

- **RSS first + API optional**
- 缺 token → RSS fallback → success（不返回 skipped_missing_auth）
- Subreddits: r/ClaudeAI, r/OpenAI, r/LocalLLaMA, r/ChatGPTCoding, r/selfhosted

## Product Hunt (5%)

- **RSS first + GraphQL API optional**
- 缺 token → RSS fallback → success（不返回 skipped_missing_auth）
- Focus: AI agent, AI IDE, coding assistant, workflow, automation

## Hugging Face (4%)

- Focus: agent, tool-use, function-calling, code, reasoning, computer-use

## Agent Framework Docs (3%)

- **hash_diff 变更检测**（与 model_docs 同逻辑）
- Providers: MCP, LangGraph, OpenHands, CrewAI, AutoGen

## Data Volume Targets

| Stage | Count |
|-------|-------|
| Raw collected | 300-800 |
| After normalization + negative_keywords | 150-400 |
| After scoring (candidates) | 60-120 |
| Selected for report | 25-45 |

## Deduplication & Merging

Same event from multiple sources should merge:
- GitHub repo + HN discussion + Reddit feedback → merged item with related_items
- Merged items get score boost (+3 per related source)
- Event-level: normalized_entity + event_type + date_bucket

## Negative Keywords

非 AI Agent 内容过滤：
real estate agent, travel agent, insurance agent, sales agent, hiring, job, recruiting, coupon, giveaway, scholarship

## 中文关键词

智能体、代码智能体、编程智能体、工具调用、函数调用、工作流、自动化、上下文、长上下文、提示词、记忆、多智能体、浏览器控制、电脑控制

---

# Source File: references/github-collector-architecture.md

# GitHub Intelligence Collector Architecture (v3.0)

## 四池架构

| Pool | 职责 | 类 | 展示规则 |
|------|------|-----|---------|
| Watch Pool | 固定10核心项目监控 | WatchPool | report_only_on_change |
| Discovery Pool | GitHub Search新项目发现 | DiscoveryPool | 经lifecycle分流后展示 |
| Growth Pool | 历史快照+实时stargazers | RealtimeGrowthDetector | spike/增长异常展示 |
| Event Pool | release/issue/PR | WatchPool methods | 重要事件进对应板块 |

## 核心类

- `GitHubClient`: API客户端, token_env_candidates, api/api_limited, rate limit
- `WatchPool`: 固定repos, change_thresholds, event_keywords
- `DiscoveryPool`: search queries, days_created/pushed, min_stars
- `RealtimeGrowthDetector`: stargazers API + starred_at, sample_rules, spike判断
- `LifecycleManager`: D0/D1/D7/D30 routing

## Lifecycle状态机

```
discovered
  ├── (realtime spike + strong relevance) → spike_hold → D1 → probation_7d → D7 → candidate_30d → D30 → watchlist
  ├── (realtime spike + weak relevance) → spike_hold → D1 → archived (if faded)
  ├── (no spike + strong relevance) → probation_7d
  ├── (no spike + low relevance) → archived
  └── (negative keyword) → dropped (cooldown 90d)
```

## state/github_repo_state.json 结构

```json
{
  "repo": "owner/name",
  "tracking_status": "discovered|spike_hold|probation_7d|candidate_30d|watchlist|archived|dropped",
  "snapshots": {"2026-06-01": {"stars": 100, "forks": 10, ...}},
  "metrics": {"star_delta_24h": null, "star_delta_7d": null, ...},
  "recent_star_window": {"is_realtime_spike": true, "spike_level": "high", ...},
  "review_history": [{"date": "...", "from_status": "...", "to_status": "...", "reason": "..."}]
}
```

关键规则: delta=null when no history (never 0). JST timezone. First run = baseline only.

## Config结构 (config.yaml github: section)

- token_env_candidates: [GITHUB_TOKEN, GITHUB_PERSONAL_ACCESS_TOKEN]
- unauthenticated_fallback: max_search_results=20, disable_expensive_calls=true
- search: 13 queries, days_created=30, days_pushed=14, min_stars=20
- watch_repos: 10 repos, change_thresholds, event_keywords
- historical_growth: state_file, metrics list
- realtime_growth: stargazers API, sample_rules (large/medium/small), failure_policy
- lifecycle: 7 statuses, d0/d1/d7/d30 routing rules, tracking_budget
- negative_keywords, category_keywords

## 采集执行顺序

1. Load config + state
2. Watch Pool (fixed repos)
3. Discovery Pool (search API)
4. For each discovery: snapshot → historical growth → realtime spike → D0 routing
5. spike_hold repos → D1 review
6. probation_7d repos → D7 review (if due)
7. candidate_30d repos → D30 review (if due)
8. Find growth anomalies from state
9. Save state, return items + source_status with lifecycle_summary

## 日报输出 (5 sub-sections)

1. GitHub 跟踪状态摘要
2. 今日实时爆发项目 (realtime_spike)
3. 今日新发现但未爆发项目 (new_discovery)
4. 历史增长异常项目 (historical_growth_spike)
5. Watch List 重要变化 (watchlist_change)

Archived/dropped only show counts. Watch List no-change = no display.

---

# Source File: references/collector_patterns.md

# Collector 降级链模式 (v2.1)

## RSS-first 社区采集器 (LinuxDo, NodeSeek)

```
RSS → JSON API → HTML 解析
```

### LinuxDo 降级链
1. RSS endpoints: `/latest.rss`, `/top.rss`, `/posts.rss`
2. JSON fallback: `/latest.json`, `/top.json` (Discourse JSON)
3. HTML fallback: `/latest`, `/top` (解析 `<a href="/t/...">`)
4. 关键词过滤 → 返回 source_status

### NodeSeek RSS-only（rss.nodeseek.com）
1. 请求 `https://rss.nodeseek.com/`
2. 用 rss_parser.py 解析（feedparser → ET → regex）
3. HTML fallback 默认关闭（`html_fallback.enabled: false`）
4. 关键词过滤 → 返回 source_status
5. 不绕过 403，不登录

## Firebase API + Algolia Search (Hacker News)

```
Firebase top/new/best → 并行获取 item/{id} → Algolia 按关键词搜索(72h) → 合并去重 → 关键词过滤
```

1. `collect_hackernews.py`（替代旧 `collect_hn.py`）
2. Firebase API: topstories + newstories + beststories
3. `ThreadPoolExecutor(max_workers=8)` 并行获取 item 详情
4. Algolia `search_by_date` 按关键词搜索，**限最近72小时**
5. **默认只抓 story**（`tags: "story"`），comment 在 story 入选后补充
6. **合并 Firebase + Algolia 后先去重再过滤**（by id + title）
7. 不需要认证，`auth="none"`, `strategy_used="api_and_search"`

## RSS-first + API optional (Reddit, Product Hunt)

```
有 token → 尝试 API → 成功则返回
无 token 或 API 失败 → RSS fallback → 返回 success/success_no_match
```

### Reddit RSS fallback
1. 检查 REDDIT_CLIENT_ID + REDDIT_CLIENT_SECRET
2. 有 → 获取 OAuth token → API 采集
3. 无 → 直接 RSS: `https://www.reddit.com/r/{sub}/{sort}/.rss`
4. RSS 用 rss_parser.py 解析（feedparser → ET → regex）
5. `www.reddit.com` 失败时 fallback 到 `old.reddit.com`
6. 返回 `success` + `strategy_used="rss"` + `auth="missing"`
7. **不返回** `skipped_missing_auth`（因为 RSS 成功了）

### Product Hunt RSS fallback
1. 检查 PRODUCTHUNT_TOKEN
2. 有 → GraphQL API: `posts(first: 50, order: RANKING)`
3. 无 → RSS: `https://www.producthunt.com/feed`
4. RSS 用 rss_parser.py 解析
5. 返回 `success` + `strategy_used="rss"` + `auth="missing"`

## token_optional API (GitHub)

```
有 token → 认证 API → 正常采集
无 token → 未认证 API → 降级采集（减少请求量）
API 失败/限流 → failed_network / failed_rate_limited
```

1. 检查 `GITHUB_TOKEN` 或 `GITHUB_PERSONAL_ACCESS_TOKEN`
2. 有 → 认证 API，正常 rate limit
3. 无 → 未认证 API，`max_results_no_token: 20`，`auth="missing"`, `strategy_used="api_degraded"`
4. 429 → `failed_rate_limited`
5. 网络失败 → `failed_network`
6. **不返回** `skipped_missing_auth`（因为可以降级采集）

## 文档变更检测器 (Model Docs, Framework Docs)

```
请求页面 → 提取正文 → 计算 hash → 与 state 比较
```

### hash_diff 模式
1. 请求页面，提取正文（去除 script/style/nav/footer）
2. SHA256 hash
3. 读取 `state/model_docs_state.json` 中上次 hash
4. **无历史 hash（首次运行）→ 只保存 baseline，不进入日报**，status=`checked_no_change`，warnings 写 "baseline initialized"
5. hash 相同 → `checked_no_change`
6. hash 不同 → 关键词匹配变化片段
7. 有命中 → `success`，无命中 → `success_no_match`

### state 结构
```json
{
  "deepseek:https://api-docs.deepseek.com": {
    "last_hash": "abc123",
    "last_checked": "2026-06-01T09:00:00+00:00",
    "last_changed": "2026-05-30T09:00:00+00:00"
  }
}
```

### Framework Docs
与 model_docs 使用同样的 hash_diff 逻辑，不再使用普通 scrape。

## RSS 解析优先级

```
feedparser → xml.etree.ElementTree → regex
```

1. feedparser（首选）：最完整的 RSS/Atom 解析
2. ElementTree（次选）：标准库，无额外依赖
3. regex（fallback）：最后手段

## 事件级合并

```
normalized_entity + event_type + date_bucket → event_key
同一事件多来源 → related_items + score boost
```

1. 从 title 提取 normalized_entity（去版本号、去前缀）
2. event_type: release / issue / pr / launch / mention
3. date_bucket: published_at[:10]
4. 同 event_key 的 items 合并：最高分为主，其余为 related_items
5. 多源共振：+3 分/相关源

## Negative Keywords

过滤非 AI Agent 内容，在 normalize_items.py 中执行：
- real estate agent, travel agent, insurance agent, sales agent
- hiring, job, recruiting, coupon, giveaway, scholarship
- estate, realtor, broker, travel agency

## config.yaml 模式

### 社区源 (linuxdo, nodeseek)
```yaml
linuxdo:
  enabled: true
  strategy: rss_first
  auth_required: false
  public_only: true
  base_url: "https://linux.do"
  rss_endpoints: [...]
  json_fallback: { enabled: true, endpoints: [...] }
  html_fallback: { enabled: true, pages: [...] }
  keywords: [...]
  request: { timeout_seconds: 20, min_interval_seconds: 5, user_agent: "..." }
```

### 文档源 (model_docs, framework_docs)
```yaml
model_docs:
  enabled: true
  strategy: hash_diff
  check_mode: change_detection
  providers:
    deepseek:
      enabled: true
      name: "DeepSeek"
      pages: ["https://api-docs.deepseek.com"]
  keywords: [...]

framework_docs:
  enabled: true
  strategy: hash_diff
  providers: [...]
```

### RSS-first + API optional 源 (reddit, producthunt)
```yaml
reddit:
  enabled: true
  strategy: rss_first
  auth_required: false
  api_optional: true
  client_id_env: "REDDIT_CLIENT_ID"
  client_secret_env: "REDDIT_CLIENT_SECRET"
  ...

producthunt:
  enabled: true
  strategy: rss_first
  auth_required: false
  api_optional: true
  token_env: "PRODUCTHUNT_TOKEN"
  ...
```

### token_optional API 源 (github)
```yaml
github:
  enabled: true
  token_env: GITHUB_PERSONAL_ACCESS_TOKEN
  token_optional: true
  max_results: 50
  max_results_no_token: 20
```

### Firebase + Algolia 源 (hackernews)
```yaml
hackernews:
  enabled: true
  strategy: api_and_search
  auth_required: false
  algolia:
    enabled: true
    base_url: "https://hn.algolia.com/api/v1/search_by_date"
  limits:
    algolia_max_age_hours: 72
  keywords: [...]
```

## Pitfalls

- **不能把"0条匹配"当失败**：`success_no_match` ≠ `failed_network`
- **文档源用 `checked_no_change`**：没有更新是正常状态，不是失败
- **文档源首次运行**：只保存 baseline，不进日报，status=`checked_no_change`
- **缺 token + RSS 成功 = `success`**：不是 `skipped_missing_auth`
- **GitHub 无 token = `api_degraded`**：不是 `skipped_missing_auth`
- **缺 token + API only = `skipped_missing_auth`**：只有纯 API 源才跳过
- **HTML fallback 不能绕 Cloudflare**：只解析公开页面
- **RSS endpoint 要缓存到 state**：避免每次重新探测
- **collector 异常必须被 main.py 捕获**：不能导致日报中断
- **token_env 命名**：GitHub 检查 `GITHUB_TOKEN` 和 `GITHUB_PERSONAL_ACCESS_TOKEN` 两个名字
- **HN Algolia 限 72h**：避免抓到过时内容
- **HN 默认只抓 story**：comment 在 story 入选后补充
- **合并后先去重再过滤**：Firebase + Algolia 合并后按 id+title 去重
- **Negative keywords 过滤**：排除 real estate agent 等非 AI 内容
- **事件级合并**：同一事件多来源合并为 related_items，提高评分

---

# Source File: references/classification-rules.md

# Classification Rules Reference (v2.1 — Content Entity Priority)

## Core Principle

**内容实体优先，不按 source 简单分类。**

- source == producthunt ≠ Product（PH 上的 AI IDE 归 Coding Agent）
- source in [hackernews, linuxdo, v2ex, nodeseek, reddit] ≠ Community（MCP 讨论归 MCP）
- secondary_categories 记录来源属性（Community/Product）

## Priority Order (first match wins)

1. source == arxiv → **Research**
2. title 含 "mcp" / "model context protocol" → **MCP**（任何 source）
3. title 含 "coding agent" / "claude code" / "cursor" / "aider" / "copilot" / "codex" / "ai ide" → **Coding Agent**（任何 source）
4. title 含 "openhands" / "browser agent" / "computer-use agent" / "openclaw" / "hermes" → **General Agent**（任何 source）
5. title 含 "db-gpt" / "sre agent" / "finance agent" / "research agent" → **Specialized Agent**
6. title 含 "langgraph" / "autogen" / "crewai" / "pydantic-ai" / "mastra" / "agents sdk" → **Agent Framework**
7. source_group == model_docs → **Model**
8. source == huggingface AND type == model → **Model**
9. source_group == framework_docs → **Agent Framework**
10. title 含 "firecrawl" / "browser-use" / "tavily" / "exa" / "connector" / "plugin" → **Tool / Plugin / Connector**
11. title 含 "workflow" / "pipeline" / "dag" / "orchestration" → **Workflow**
12. title 含 "skill" / "prompt template" → **Skill**
13. source == producthunt AND 无强内容信号 → **Product**
14. title 含 "funding" / "raises" / "acquisition" → **Business**
15. source in [hackernews, linuxdo, v2ex, nodeseek, reddit] AND 无强内容信号 → **Community**
16. Default → **Community**

## Secondary Categories

- source in [hackernews, linuxdo, v2ex, nodeseek, reddit] 且 primary ≠ Community → secondary 含 Community
- source == producthunt 且 primary ≠ Product → secondary 含 Product

## Examples

| 标题 | source | primary | secondary |
|------|--------|---------|-----------|
| "MCP Server for PostgreSQL" | hackernews | MCP | Community |
| "Claude Code now supports MCP" | reddit | MCP | Community |
| "New AI IDE: CodePilot" | producthunt | Coding Agent | Product |
| "LangGraph 0.3 released" | hackernews | Agent Framework | Community |
| "Best local LLM for coding?" | linuxdo | Community | — |
| "DeepSeek API pricing update" | reddit | Community | — |

## Actionability Assessment

- **high**: title 含 hermes/openclaw/skill/mcp/workflow/claude code
- **medium**: category in [MCP, Tool, Workflow, Skill, Coding Agent]
- **low**: everything else

## Tag Generation

Based on category:
- MCP → [mcp, tool-use]
- Model → [model, llm]
- Coding Agent → [coding-agent, agent]
- General Agent → [agent, autonomous]
- Agent Framework → [framework, sdk]
- Tool / Plugin / Connector → [tool, plugin]
- Workflow → [workflow, automation]
- Skill → [skill, prompt]
- Research → [research, paper]
- Product → [product]
- Business → [business]
- Community → [community]

Content-based:
- "open-source" in title → add "open-source"
- "github" in url → add "github"
- "browser" in title → add "browser-agent"
- "gui" or "computer" in title → add "gui-agent"

---

# Source File: references/scoring-formulas.md

# Scoring Formulas (v2.1)

## Total Score = Relevance(30) + Popularity(20) + Freshness(15) + Growth(15) + Utility(20) = 100

**这是唯一有效的评分公式。** `references/scoring-system.md` 已标记 deprecated，代码不得引用它。

## Relevance (0-30)

**按内容实体评分，不按 source 评分。Community 来源不天然低分。**

- Coding Agent / MCP / General Agent: 25-28
- Agent Framework / Workflow / Skill: 20-24
- Model / Tool / Specialized Agent: 15-19
- Community 中的强内容（MCP/Coding Agent/Workflow/Model API 讨论）: 20-22
- Community 中的中等内容: 16
- Community 默认: 10
- Research / Product / Business: 10

## Popularity (0-20)

GitHub stars: >50K=20, >10K=16, >3K=12, >1K=8, >100=4
HN score: >500=20, >200=16, >100=12, >50=8, >20=4
Community (LinuxDo/V2EX): >100 replies or >50 likes=16, >50/20=12, >20/10=8
Reddit: >1000 score or >200 comments=18, >500/100=14, >100/50=10
Product Hunt: >500 votes=18, >200=14, >100=10
HuggingFace: >1000 likes=16, >500=12, >100=8

## Freshness (0-15)

- <24h: 15
- <3d: 10
- <7d: 5
- >7d: 0

## Growth (0-15)

GitHub star_delta_24h: >1000=15, >500=12, >200=9, >100=6, >50=3
HN/Reddit comments velocity: >200=12, >100=9, >50=6, >20=3
Community reply velocity: >50=10, >20=7, >10=4

## Utility (0-20)

**按内容主题评分，Community 来源不天然低分。**

- Directly enhances Hermes (hermes/openclaw/skill/mcp/workflow): 19
- Usable for Skill/Workflow: 16
- Community high-value (MCP/Coding Agent/Workflow/Model API 讨论): 16
- Community medium-value (model/llm/prompt/automation/deploy): 12
- Informs Agent architecture: 12
- Community default: 8
- Trend awareness: 6

## Importance Levels

- S (85-100): Must push
- A (70-84): Key focus
- B (55-69): Normal inclusion
- C (40-54): Backup
- D (0-39): Ignore

## Deduplication + Merging

- URL dedup: same URL → keep higher score
- GitHub repo merge: same repo from search + watch_list + release → merge, boost score by +3 per related item
- Title similarity >0.85 → deduplicate
- **Event-level merge**: same entity + event_type + date → merge, +3 per related source

## Actionability (per item)

```json
{
  "level": "high|medium|low",
  "recommended_action": "Evaluate for Hermes integration",
  "hermes_integration": "tool|skill|workflow|watch_only|ignore",
  "effort": "low|medium|high"
}
```

---

# Source File: references/scoring-system.md

# ⚠️ DEPRECATED — Scoring System (5 Dimensions, 0-100)

> **This file is DEPRECATED as of v2.0.**
> The only valid scoring formula is: relevance(30) + popularity(20) + freshness(15) + growth(15) + utility(20) = 100.
> Do NOT reference this file in code. Use `references/scoring-formulas.md` instead.

---

# Scoring System (5 Dimensions, 0-100)

## Dimension 1: Relevance Score (0-30)

| Level | Score | Criteria |
|-------|-------|---------|
| 强相关 | 25-30 | Agent Framework, General Agent, Specialized Agent, Coding Agent, MCP, Workflow, Skill |
| 中相关 | 15-24 | Tool/Plugin/Connector, Model, Research |
| 弱相关 | 5-14 | AI 工具、LLM、模型 |
| 无关 | 0-4 | 非 AI 内容 |

## Dimension 2: Popularity Score (0-25)

### GitHub (Stars)
| Stars | Score |
|-------|-------|
| > 50,000 | 25 |
| > 10,000 | 20 |
| > 3,000 | 15 |
| > 1,000 | 10 |
| > 100 | 5 |

### Hacker News (Score)
| HN Score | Score |
|----------|-------|
| > 500 | 25 |
| > 200 | 20 |
| > 100 | 15 |
| > 50 | 10 |

### Hugging Face (Likes)
| Likes | Score |
|-------|-------|
| > 1,000 | 20 |
| > 500 | 15 |
| > 100 | 10 |
| > 50 | 5 |

### arXiv
默认 5-15，若作者/机构/Benchmark 强则更高

## Dimension 3: Freshness Score (0-15)

| Age | Score |
|-----|-------|
| < 24 hours | 15 |
| < 3 days | 10 |
| < 7 days | 5 |
| > 7 days | 0 |

## Dimension 4: Growth Score (0-20)

### GitHub (star_delta_24h)
| 24h Stars | Score |
|-----------|-------|
| > 1,000 | 20 |
| > 500 | 16 |
| > 200 | 12 |
| > 100 | 8 |
| > 50 | 5 |

### HN (comments/讨论热度)
| Comments | Score |
|----------|-------|
| > 200 | 15 |
| > 100 | 10 |
| > 50 | 5 |

## Dimension 5: Utility Score (0-10)

| Level | Score | Criteria |
|-------|-------|---------|
| 高 | 8-10 | 可直接用于 Hermes/OpenClaw/Claude Code |
| 中 | 5-7 | 可用于 Agent 开发 |
| 低 | 2-4 | 仅理论相关 |
| 无 | 0-1 | 无直接价值 |

## Importance Levels

| Level | Score Range | Action |
|-------|------------|--------|
| S | 85-100 | 必须推送，关键事件 |
| A | 70-84 | 值得重点关注 |
| B | 55-69 | 普通收录 |
| C | 40-54 | 备选 |
| D | 0-39 | 忽略 |

## Current Implementation Notes

v1.0.0 使用规则评分，部分维度实现简化：
- growth_score: GitHub 暂用 stars 代替 star_delta_24h（需 state 文件积累）
- utility_score: 基于 category 和关键词推断
- arXiv: 固定分值

---

# Source File: references/implementation-patterns.md

# Implementation Patterns (v3.1)

## Pattern: safe_collect Wrapper

main.py must wrap every collector in a safe wrapper that catches all exceptions. Single-source failures must never block report generation.

```python
def safe_collect(name, fn, config, logger):
    try:
        return fn(config)
    except Exception as e:
        logger.error(f"  {name} exception: {e}")
        from source_status import make_source_status
        et = "failed_parse" if any(k in str(e).lower() for k in ("parse", "json", "xml")) else "failed_network"
        return [], make_source_status(source=name, status=et, errors=[str(e)])
```

## Pattern: RSS Fallback for Auth-Gated Sources

When a source requires OAuth/API token but user hasn't set one:
1. Check env vars first
2. If missing, attempt RSS fallback (public feeds)
3. Return `success` or `success_no_match` (NOT `skipped_missing_auth`)
4. Set `auth="missing"`, `strategy_used="rss"` or `"rss_fallback"`
5. Add warning: "OAuth missing, used RSS fallback"

This pattern applies to Reddit and Product Hunt. The key insight: missing auth + successful RSS = success, not skip.

## Pattern: token_optional API (GitHub)

When a source has public API access but benefits from auth:
1. Check env vars for token (candidates list)
2. If present → authenticated API, normal rate limit, `strategy_used="api"`
3. If absent → unauthenticated API, reduced request volume, `strategy_used="api_limited"`
4. Set `auth="ok"` or `auth="missing"`
5. Return `success` or `success_no_match` (NOT `skipped_missing_auth`)
6. Only return `failed_network` / `failed_rate_limited` when API itself fails

## Pattern: hash_diff Change Detection for Doc Sources

For model docs / framework docs that don't produce "new items" daily:
1. Fetch page, extract text (strip script/style/nav/footer)
2. SHA256 hash of cleaned text
3. Compare with `state/{source}_state.json` previous hash
4. **No previous hash (first run) → save baseline only, do NOT enter report**
   - Status: `checked_no_change`
   - Warning: "baseline initialized (first run)"
5. Same hash → `checked_no_change` (not failure, not no_match)
6. Different hash → extract diff snippet, keyword match on diff
7. Matched → `success`, no match → `success_no_match`

State file structure per-key: `{last_hash, last_checked, last_changed}`

## Pattern: GitHub 4-Pool Architecture

GitHub collector uses 4 pools:
- **Watch Pool**: Fixed core repos (report_only_on_change)
- **Discovery Pool**: GitHub Search API (new repos found by keywords)
- **Growth Pool**: Historical snapshots + realtime stargazers detection
- **Event Pool**: releases / issues / PRs

Lifecycle: discovered → spike_hold → probation_7d → candidate_30d → watchlist → archived / dropped

Key rules:
- Watch repos: no change = no display
- New discoveries: D0 routing (realtime spike → spike_hold, strong relevance → probation_7d, weak → archived)
- spike_hold: D1 review, if faded → archived (never auto-promote to watchlist)
- probation_7d: D7 review, growth → candidate_30d
- candidate_30d: D30 review, sustained → watchlist
- Historical delta=null when no snapshot exists (never write 0)
- First run only builds baseline, no growth anomalies reported

## Pattern: Same-Source Dedup vs Cross-Source Merge

**Same source duplicates = noise.** Delete/merge, keep highest-scored or most complete.
- Phase 1: URL exact match within source + title similarity ≥ 0.90

**Cross source mentions = signal.** Merge as related_items, boost score.
- Phase 2: URL match across sources → related_items + cross_source_count
- Phase 2b: Title similarity ≥ 0.85 across sources → related_items
- Boost: +3 per related source, max +10

**Event-level merge**: normalized_entity + event_type + date_bucket

## Pattern: Quality Gates

Three levels:
1. **item_level**: empty title/URL/summary → drop; short title → drop; negative keywords → drop; low-quality patterns (求推荐, 水一贴, etc.) → drop
2. **community_level**: posts without tool/model/API/config/deployment signal → drop or lower score
3. **report_level**: max_same_source_ratio ≤ 45%; max_same_category_ratio ≤ 35%

Apply AFTER scoring, BEFORE report generation. Don't filter too early — extract signals first, then judge quality.

## Pattern: Cost Signal Extraction

For Model/API/Pricing/Cache related items, extract:
```python
{
    "has_pricing": bool, "has_cache": bool,
    "input_price": float|null, "output_price": float|null,
    "currency": "USD"|"", "unit": "per_million_tokens",
    "provider": str, "cost_impact": "lower"|"higher"|"neutral"|"unknown",
    "routing_impact": "recommended"|"watch"|"avoid"|"unknown"
}
```
NEVER fabricate numeric values. null when unknown.

## Pattern: Schema Version

All JSON outputs must include `schema_version: "2.0"` at top level.
When reading old files without schema_version, treat as legacy, write warning, don't crash.

## Pattern: Low Signal Day

When selected_items < threshold:
1. Still generate report (don't skip)
2. Add "Low Signal Day" banner
3. Insights: "数据不足，不生成强趋势判断"
4. Recommendations: only deterministic suggestions
5. DO NOT backfill with C/D level content
6. Set daily_state.report_summary.low_signal_day = true

## Pattern: Collector --test Mode

Every collector supports `--test` via `if __name__ == "__main__"`:
```python
if __name__ == "__main__":
    import argparse, json as _json, yaml as _yaml
    _p = argparse.ArgumentParser()
    _p.add_argument("--test", action="store_true")
    _args = _p.parse_args()
    if _args.test:
        # Load config, run collector, output JSON
        # Don't write to data/ or state/ files
```

## Pattern: CLI Arguments for main.py

```bash
python main.py --dry-run              # Preview, no push, no state write
python main.py --sources github,v2ex  # Run specific sources only
python main.py --no-push              # Generate but don't push
python main.py --debug                # Verbose logging
python main.py --date 2026-06-01      # Override report_date
python main.py --output test.md       # Custom output path
python main.py --write-state          # Write state even in dry-run
```

--sources must validate against known collector names. --dry-run defaults to no state write.

## Pattern: Python String Replace Order Trap

When doing find-and-replace on Python source code:
- `STATUS_SUCCESS` is a substring of `STATUS_SUCCESS_NO_MATCH`
- Replacing `STATUS_SUCCESS` first corrupts `STATUS_SUCCESS_NO_MATCH`
- **Always replace longer strings first**, or use regex word-boundary match

## Pattern: Patch Matching Failures

When using skill_manage(action='patch') or execute_code string replacement:
- old_string must match EXACTLY (whitespace, indentation, line endings)
- Multi-line YAML/Python replacements are fragile — verify the old string exists first
- If patch fails, read the file and check actual content before retrying
- Variable names may differ from what you assumed (e.g., `items` vs `same_source_deduped`)
- Always verify after patching

## Pattern: Function Signature + Return Dict Sync

When adding new fields to a data structure returned by a factory function:
- Add the field as a parameter to the function signature
- Add it to the returned dict
- Missing this = `TypeError: unexpected keyword argument`

## Pattern: Windows/WSL File Write

On Windows with WSL relay instability:
- `write_file` tool and `read_file` tool may fail with WSL errors
- Fallback: use `execute_code` with Python `open()` + `f.write()`
- This bypasses the WSL layer entirely

**IMPORTANT**: Within `execute_code`, `from hermes_tools import write_file` writes to a SANDBOX filesystem, NOT the actual project directory. Always use Python's built-in `open()` for actual file I/O inside execute_code.

## Env Var Naming: GitHub Token

`.hermes/.env` has `GITHUB_PERSONAL_ACCESS_TOKEN`, code may expect `GITHUB_TOKEN`.
Solution: collect_github.py uses `token_env_candidates` list, checks both names.

## Pattern: Section Quota in Report Generation

generate_report.py uses report_layout config for per-section item limits:
```python
def _section_items(self, items, section_name, min_level="B"):
    sec = self.section_config.get(section_name, {})
    target = sec.get("target_items", 3)
    max_items = sec.get("max_items", self.max_items)
    # Filter by importance level, then cap at max_items
```

Each section uses its own section_name key to look up target/max from config.

---

# Source File: templates/config-template.yaml

```yaml
# Agent Daily Report v3.1 Config Template
# Copy to config.yaml and customize

system:
  name: agent-daily-report
  version: "3.1.0"
  description: "Agent 工程情报日报系统"
  target: "Hermes / OpenClaw / Claude Code / Coding Agent / MCP / Workflow / Skill"

runtime:
  timezone: "Asia/Tokyo"
  report_date_mode: "local_date"
  collection_window:
    default_hours: 24
    hackernews_hours: 72
    github_created_days: 30
    github_pushed_days: 14
    reddit_time_filter: "day"
    producthunt_days: 1
    v2ex_hours: 48
    linuxdo_hours: 48
    nodeseek_hours: 48

sources:
  github:
    enabled: true
    weight: 0.35
  hackernews:
    enabled: true
    weight: 0.15
  developer_communities:
    enabled: true
    weight: 0.2
    sub_sources:
      linuxdo:
        enabled: true
        weight: 0.1
      v2ex:
        enabled: true
        weight: 0.06
      nodeseek:
        enabled: true
        weight: 0.04
  model_docs:
    enabled: true
    weight: 0.1
  reddit:
    enabled: true
    weight: 0.08
  producthunt:
    enabled: true
    weight: 0.05
  huggingface:
    enabled: true
    weight: 0.04
  framework_docs:
    enabled: true
    weight: 0.03
  arxiv:
    enabled: false
    schedule: weekly

github:
  enabled: true
  weight: 0.35
  auth_required: false
  token_optional: true
  token_env_candidates:
  - GITHUB_TOKEN
  - GITHUB_PERSONAL_ACCESS_TOKEN
  request:
    base_url: "https://api.github.com"
    timeout_seconds: 30
    min_interval_seconds: 1
    max_retries: 3
    user_agent: "HermesAgentDailyReport/3.0"
    api_version_header: "2022-11-28"
  unauthenticated_fallback:
    enabled: true
    max_search_results: 20
    disable_expensive_calls: true
    disable_realtime_growth: true
  search:
    enabled: true
    days_created: 30
    days_pushed: 14
    min_stars: 20
    max_results_per_query: 30
    queries:
    - agent
    - ai-agent
    - mcp
    - model-context-protocol
    - workflow
    - coding-agent
    - browser-agent
    - tool-use
  watch_repos:
    enabled: true
    report_only_on_change: true
    repos:
    - OpenHands/OpenHands
    - langchain-ai/langgraph
    - microsoft/autogen
    - crewAIInc/crewAI
    - pydantic/pydantic-ai
    - modelcontextprotocol/servers
    - browser-use/browser-use
    - aider-AI/aider
  realtime_growth:
    enabled: true
    max_repos_per_run: 50
  lifecycle:
    enabled: true
    tracking_budget:
      max_active_tracked_repos: 300
      max_new_discoveries_per_day: 50

v2ex:
  enabled: true
  strategy: api
  auth_required: false
  base_url: "https://www.v2ex.com"
  nodes:
  - programmer
  - create
  - qna
  - python
  - ai
  limits:
    max_total_items: 200

scoring:
  weights:
    relevance: 30
    popularity: 20
    freshness: 15
    growth: 15
    utility: 20
  thresholds:
    S: 85
    A: 70
    B: 55
    C: 40
    D: 0

report:
  max_items_per_section: 10
  min_score: 55
  output_dir: data/reports

report_layout:
  total_selected_items:
    target: 35
    max: 45
  sections:
    top_events:
      target_items: 5
      max_items: 6
    github_growth:
      target_items: 5
      max_items: 8
    agent_coding_agent:
      target_items: 4
      max_items: 6
    mcp:
      target_items: 3
      max_items: 5
    workflow_skill:
      target_items: 3
      max_items: 5
    tools_connectors:
      target_items: 3
      max_items: 5
    model_api:
      target_items: 3
      max_items: 5
    community_signals:
      target_items: 3
      max_items: 5
    producthunt:
      target_items: 2
      max_items: 4
    insights:
      target_items: 3
      max_items: 3
    recommendations:
      target_items: 3
      max_items: 5

quality_gates:
  enabled: true
  item_level:
    require_url: true
    min_title_length: 8
    drop_empty_title: true
    drop_empty_summary: true
  report_level:
    min_score_for_report: 55
    max_same_source_ratio: 0.45
    max_same_category_ratio: 0.35
  low_quality_patterns:
  - "求推荐"
  - "水一贴"
  - "闲聊"

cost_signal:
  enabled: true

empty_report_policy:
  enabled: true
  low_signal_threshold: 10
  generate_report_even_if_empty: true
  do_not_fill_low_quality_items: true

deduplication:
  same_source:
    enabled: true
    url_exact_match: true
    title_similarity_threshold: 0.90
  cross_source:
    enabled: true
    merge_as_related_items: true
    title_similarity_threshold: 0.85
    boost_per_related_source: 3
    max_cross_source_bonus: 10

negative_keywords:
- real estate agent
- travel agent
- insurance agent
- sales agent
- hiring
- job
- recruiting
- coupon
- giveaway

logging:
  level: INFO
  file: logs/run.log

state:
  daily_state: state/daily_state.json
  github_repo_state: state/github_repo_state.json
  model_docs_state: state/model_docs_state.json
  source_state: state/source_state.json
```

---
