---
name: agent-daily-report
description: "Daily Agent ecosystem intelligence report. 11 collectors + 3 Agent nodes (Trust/Enrichment/Editor) with multi-round verification. 16 external sub-sources. Unified source_status (12 states). Cron 6am → WeChat delivery."
version: "3.3.0"
tags: ["agent", "mcp", "workflow", "skill", "coding-agent", "research", "intelligence", "developer-community"]
---

# Agent Daily Report v3.2

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
| 信息源 | 11源(含外部日报)，GitHub为主(35%) | HN+GitHub+36氪 |
| 分类 | 13类严格分类 | 3大类(Agent/Skills/组件) |
| 评分 | 5维度100分 | 无量化评分 |
| 重点 | 可操作性、可集成性 | 新闻覆盖面 |
| 目标用户 | Agent 开发者 | 通用 AI 读者 |

## 系统位置

```
D:/openclaw-hermes/agent-daily-report-skill/
```

## 运行方式

### run_pipeline.py（推荐，避免超时）

完整 pipeline（11源采集 + Agent pipeline）需要 5-15 分钟。`execute_code` 有 300s 硬超时会杀掉子进程。**必须用 `run_pipeline.py --background`**：

```bash
cd D:/openclaw-hermes/agent-daily-report-skill
python run_pipeline.py --background  # 后台运行（独立进程，DETACHED_PROCESS，不受超时限制）
python run_pipeline.py --status      # 查看状态（PID、内存、CPU、报告时间、日志进度）
python run_pipeline.py --log         # 查看最新日志尾部
python run_pipeline.py --kill        # 终止运行中的进程
python run_pipeline.py               # 前台运行（阻塞，仅用于短测试）
```

### main.py 直接运行（仅用于短测试）

```bash
python main.py --dry-run --debug     # 预览，不写状态不推送（推荐测试方式）
python main.py --sources github      # 只运行指定源
python main.py --no-push --debug     # 完整采集但不推送
python main.py --date 2026-06-01     # 指定日期
python main.py --output test.md      # 自定义输出路径
```

### 轮询完成模式

```python
import subprocess, sys, time
SKILL_DIR = "D:/openclaw-hermes/agent-daily-report-skill"
subprocess.run([sys.executable, 'run_pipeline.py', '--background'], cwd=SKILL_DIR)
for i in range(180):  # 180 * 10s = 30min
    time.sleep(10)
    r = subprocess.run([sys.executable, 'run_pipeline.py', '--status'], cwd=SKILL_DIR, capture_output=True, text=True)
    if '已退出' in r.stdout or '无运行记录' in r.stdout:
        break
```

**铁律**：不要用 execute_code + subprocess.run 跑完整 pipeline（P67：300s 超时杀进程）。不要用 terminal(background=True)（Windows WSL 兼容问题）。

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
  agent_pipeline.py         # Agent 管道控制器 (Trust→Enrichment→Editor，含多轮验证)
  agent_llm_client.py       # 统一 LLM 客户端 (OpenAI-compatible HTTP)
  agent_prompts.py          # 3 个 Agent + 3 个验证器的 prompt 模板
  enrich_report_with_agent.py # 离线 enrichment 模板 (Agent 降级时使用)
  source_status.py          # 统一状态规范（12种枚举 + auth/strategy_used）
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
  collect_external_digests.py # 外部日报信源（10子源: agents-radar/ai-news-agent/awesome-lists/releases/MCP注册站）
  source_health.py          # 源健康趋势追踪（30天历史, streak, signal_density）
  cost_signal.py            # 成本信号提取（pricing/cache/provider）
  time_utils.py             # 时区/时间窗口工具
  mcp_server.py             # MCP Server（list_reports/get_latest/search/source_health）
  opml_import.py            # OPML/RSS订阅源导入
  rss_parser.py             # feedparser → ET → regex 三级解析
  normalize_items.py        # 数据标准化 + negative_keywords 过滤
  deduplicate_items.py      # URL去重 + 标题去重 + 事件级合并
  classify_items.py         # 内容实体优先分类
  score_items.py            # 评分 + actionability 评估
  generate_report.py        # 报告生成（含 Source Status 表 + section quota）
  verify_system.py          # 系统健康检查脚本
AGENTS.md                   # Hermes 自主维护指南 (诊断/修复/命令参考)
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

12 种状态（v3.1）：
| 状态 | 含义 |
|------|------|
| success | 正常采集且有关键词命中 |
| success_no_match | 采集成功但无关键词命中 |
| checked_no_change | 文档类：页面无变化（hash diff）或首次 baseline |
| skipped_disabled | config 中 enabled=false |
| skipped_missing_auth | 缺少必需的环境变量（仅限纯API源） |
| skipped_no_config | 缺少必需的配置项 |
| skipped_no_stable_api | 无稳定公开API（v3.1新增） |
| skipped_requires_api_key | 需要API key但未配置（v3.1新增） |
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

## 信息源权重与策略 (11源)

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
| 外部日报 | 3% | GitHub Issues / Pages JSON | token_optional |

### 外部日报信源

采集同生态项目的日报、MCP Registry、Awesome List 作为信源 (v2.0)：

| 项目 | Stars | 类型 | 采集方式 |
|------|-------|------|---------|
| agents-radar (duanyytop) | 780 | GitHub Issues | API: /repos/{repo}/issues |
| ai-news-agent (nickzren) | 2 | GitHub Issues | API: labels=ai-digest |
| ai-news-radar (LearnPrompt) | 843 | GitHub Pages JSON | HTTP GET /data/*.json | **已移除**（2026-06-05，用户要求） |

这些项目的日报本身就是有价值的 Agent 生态情报。

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
| External Digests | 3% | github_issues/commits/releases/registry | token_optional |

### External Digests 子源

| 子源 | 类型 | 状态 | 说明 |
|------|------|------|------|
| agents-radar | github_issues | ✅ | 780⭐, 10源日报 |
| ai-news-agent | github_issues | ✅ | 25 RSS源日报 |
| ai-news-radar | github_pages_json | ⏭ | 843⭐, 已移除（2026-06-05） |
| awesome-mcp-servers | awesome_commits | ✅ | 88k⭐, 新MCP server |
| awesome-ai-agents | awesome_commits | ✅ | 16k⭐, 新AI agent |
| awesome-llm-apps | awesome_commits | ✅ | 43k⭐, 新LLM app |
| official-mcp-registry | mcp_registry | ✅ | 官方MCP Registry, cursor分页 |
| glama-mcp | mcp_registry | ✅ | Glama MCP目录, 公开API |
| smithery | mcp_registry | ⏭ | 需要SMITHERY_API_KEY |
| mcp-so | mcp_registry | ⏭ | 无稳定公开JSON API, 已禁用 |
| ai-tool-releases | github_releases | ✅ | 13个AI工具/框架发布 |

## GitHub Intelligence Collector (v3.0)

四池架构：

| Pool | 职责 | 展示规则 |
|------|------|---------|
| Watch Pool | 固定核心项目监控（10个） | 无变化不展示，有变化才进日报 |
| Discovery Pool | GitHub Search 新项目发现 | 经 lifecycle D0 分流后，仅 spike/强相关展示 |
| Growth Pool | 历史快照增长 + 实时 stargazers | star_delta_24h/7d/30d + realtime spike |
| Event Pool | release / issue / PR 事件 | 重要事件进对应板块 |

### Growth Pool 门控规则 (v3.2)

`evaluate_github_growth_gate()` 决定增长信号是否可报告（P65 已修复，P74 归一化修复）：

| 区间 | reportable 条件 | 分级 |
|------|----------------|------|
| stars < 100 | 不eligible | — |
| <1k | delta >= 200 | S≥500 / A≥300 / B≥200 |
| 1k-5k | delta >= 100 | S≥500 / A≥300 / B≥100 |
| >=5k | daily_rate >= 1% | B / A≥10% |

**P74 归一化**：当快照间隔 < 23h 时，delta_24h = round(delta_raw / interval_hours * 24)。原始值保存在 `star_delta_24h_raw`。

**P74 归一化**：当快照间隔不足24h时，`star_delta_24h` 自动归一化为等效24h值。原始值保留在 `star_delta_24h_raw`。公式：`delta_24h = round(delta_raw / interval_hours * 24)`

**P74 归一化**：当快照间隔 < 23h 时，delta_24h = round(delta_raw / interval_hours * 24)。metrics 中 star_delta_24h_raw 保留原始值。

**P75 Agent 相关性判断**：关键词不通过的项目，用 LLM 逐个读 README 判断是否与 Agent 生态相关。用户要求：Skill 和增强器无论内容主题都应纳入。

前置过滤：`has_strong_agent_signal(repo)` 关键词匹配 → 不通过则 LLM 读 README 兜底 → negative_keywords 排除。

前置过滤：需要 `has_strong_agent_signal(repo)` 为 true；negative_keywords 命中的仓库被排除。

**归一化**：当快照间隔 < 23h 时，delta 自动归一化为 24h 等效值（`delta_raw / interval_hours * 24`）。详见 `references/growth-normalization-fix.md`。

**过滤漏斗**（2026-06-03 实测）：23个日均>=100仓库 → 仅4个通过全部过滤：
- 5个因 tracking_status=archived/dropped 被跳过
- 4个因 has_strong_agent_signal=False 被拒
- 10个因 __pycache__ 旧字节码被旧逻辑拒绝（P68）
- 4个通过：SkillOpt、science-skills、browser-use、opensquilla

详见 `references/growth-gate-diagnosis.md`（诊断脚本+四层过滤详解）。

**用户偏好**：列出仓库时必须附带功能描述。数据来源：candidates.json description → GitHub API GET /repos/{name} → 无描述标注"(无描述)"。

### Growth 异常诊断流程

当报告输出"历史增长异常项目: 暂无"但 state 有快照数据时：

```python
# 1. 确认快照存在
state = json.load(open("state/github_repo_state.json"))
for rn, rs in state["repos"].items():
    snaps = rs.get("snapshots", {})
    if len(snaps) >= 2:
        dates = sorted(snaps.keys())
        delta = snaps[dates[-1]]["stars"] - snaps[dates[-2]]["stars"]
        if delta >= 100:
            print(f"{rn}: +{delta} tracking={rs.get('tracking_status')}")

# 2. 检查 metrics 是否已计算
# metrics.star_delta_24h 应该非 None

# 3. 检查 evaluate_github_growth_gate 的返回
from scripts.collect_github import evaluate_github_growth_gate
gate = evaluate_github_growth_gate(repo_like, metrics)
print(gate)  # reportable, reason, level_hint
### Growth 异常诊断流程

当报告输出"历史增长异常项目: 暂无"但 state 有快照数据时，按 `references/growth-gate-diagnosis.md` 的诊断流程排查：
1. 确认快照存在
2. 检查 has_strong_agent_signal / is_reportable_github_growth_repo / tracking_status / evaluate_github_growth_gate 四层过滤
3. 清理 __pycache__ 后重跑
4. **P74 新增**：检查快照间隔是否 < 23h，如果是则 star_delta_24h 应已归一化（round(delta_raw / interval_hours * 24)）
5. **P75 新增**：关键词不通过的项目，用 LLM 读 README 判断 Agent 相关性

已知过滤漏斗（2026-06-03实测）：23个日均>=100仓库中仅4个通过全部过滤。主要瓶颈：archived被跳过(5个)、weak_agent_signal(4个)、__pycache__旧代码(10个)。P74 修复后，1.5h 间隔的项目（如 CodexPlusPlus +71→+1117）可正确通过门控。
已知过滤漏斗（2026-06-03实测）：23个日均>=100仓库中仅4个通过全部过滤。主要瓶颈：archived被跳过(5个)、weak_agent_signal(4个)、__pycache__旧代码(10个)。
**2026-06-04 新发现**：快照间隔不足 24h 导致 delta 被低估（P74），CodexPlusPlus 实际 rate=9.1% 被误报为 0.58%。

Lifecycle: discovered → spike_hold → probation_7d → candidate_30d → watchlist → archived / dropped

state/github_repo_state.json 记录每个 repo 的 snapshot、metrics、lifecycle 状态。
缺失历史 delta = null，不写成 0。
首次运行只建 baseline，历史增长榜暂无数据。

### Growth 异常诊断流程

当报告输出"历史增长异常项目: 暂无"但 state 有快照数据时：

```python
# 1. 确认快照存在
state = json.load(open("state/github_repo_state.json"))
for rn, rs in state["repos"].items():
    snaps = rs.get("snapshots", {})
    if len(snaps) >= 2:
        dates = sorted(snaps.keys())
        delta = snaps[dates[-1]]["stars"] - snaps[dates[-2]]["stars"]
        if delta >= 100:
            print(f"{rn}: +{delta} tracking={rs.get('tracking_status')}")

# 2. 检查 metrics 是否已计算
# metrics.star_delta_24h 应该非 None

# 3. 检查 evaluate_github_growth_gate 的返回
from scripts.collect_github import evaluate_github_growth_gate
gate = evaluate_github_growth_gate(repo_like, metrics)
print(gate)  # reportable, reason, level_hint

# 4. 检查 _find_growth_anomalies 的过滤条件
# - rn in already/watch → 被跳过
# - tracking_status in (archived, dropped, "") → 被跳过
# - not has_strong_agent_signal → 被跳过
```

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

**不使用归一化**：各维度直接加权求和，每个 item 独立计算，不受其他 item 影响。没有跨项目归一化、排名归一化或 min-max 缩放。

### 日均增长指标 (2026-06-05 新增)

`score_growth()` 优先使用**日均增长**（从快照历史计算），其次使用单日增长。

**计算逻辑**：
1. 从 `state/github_repo_state.json` 的快照历史计算：`daily_avg = (last_stars - first_stars) / days_diff`
2. 评分阈值：>500→15, >200→12, >100→9, >50→6, >20→3
3. 无日均数据时回退到 `star_delta_24h`（单日增长）

**日均增长保底B级**：当日均增长 ≥ 20 stars/day 时，评分被提升到至少 B 级（55分）。通过 `daily_avg_growth_boost` quality_flag 标记。

**相关性**：单日增长与日均增长的相关系数为 0.901（强相关），但个别项目差异显著（如 husu/loom 单日+1 vs 日均+122）。

**实现位置**：`scripts/score_items.py` → `score_growth()` 和 `_calc_daily_avg_growth()`

**P84 调试经验**：`_calc_daily_avg_growth` 使用 `os.path.exists()` 但模块顶部未 `import os`，`except: return None` 吞掉异常。调试时改 `except Exception as e: print(f"Error: {e}")` 立即发现问题。

- **S (85-100)**: 必须推送
- **A (70-84)**: 重点关注
- **B (55-69)**: 普通收录
- **C (40-54)**: 备选
- **D (0-39)**: 忽略

Community 来源不天然低分。按内容主题评分：与 MCP / Coding Agent / Workflow / Model API 强相关的社区讨论获得较高 relevance 和 utility。

### Quality Flag 惩罚机制

Discovery Pool 新发现的项目（lifecycle=probation_7d）会被标记 `generic_github_discovery_candidate`，评分被强制封顶到 **54 分（C 级上限）**。Watch List 项目不受影响。

| 项目类型 | quality_flags | 评分行为 |
|----------|--------------|---------|
| Watch Pool | [] | 明细之和 = 实际得分 |
| Discovery Pool | [generic_github_discovery_candidate] | 实际得分 = min(明细之和, 54) |

**已知问题**：高增长 Discovery 项目被误杀（如 CodexPlusPlus +918/24h 被压到 54 分）。详见 P61。

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


## 配置变更记录 (2026-06-04)

### 已解除的限制
- 所有 Agent timeout_seconds: 0（无限制）
- Trust Agent max_items: 0（无限制）
- Trust Agent batch_size: 1（从 5 改为 1）
- Enrichment Agent batch_size: 1（保持不变）
- Editor Agent batch_size: 1（保持不变）

### 新增文件
- `prompts/` 目录：9 个独立提示词文件（从 agent_prompts.py 提取）
- `LIMITATIONS.md`：20 类限制条件汇总
- `AGENT_LIMITATIONS.md`：Agent Pipeline 限制详解

### SkillOpt 集成
- 环境目录：`D:\openclaw-hermes\SkillOpt\skillopt\envs\agent_daily_report\`
- 配置目录：`D:\openclaw-hermes\SkillOpt\configs\agent-daily-report\`
- 12 个评估维度：relevance, completeness, accuracy, actionability, specificity, consistency, coverage, clarity, dedup_effectiveness, scoring_accuracy, mcp_validation, source_filtering

## 2026-06-02 用户反馈改进规则

### 1. 候选池表（新增板块）
日报末尾新增"候选池"表，包含所有候选项目：
| 项目 | Stars | 24h增长 | 增长率 | 分类 | 简要说明 | 来源 |
让读者自行判断哪些值得深入查看。

### 2. HuggingFace 判别标准
- 不是有新模型就放 A 级
- 必须满足以下条件之一才能放 A 级：
  - 知名机构发布（如 Google、Meta、Microsoft 等）
  - Star 增长异常（>100/天）
  - 社区热议（>10 条高质量评论）
- 否则降为 B 级或不收录

### 3. 异常增长项目规则（细化）
| 项目规模 | 增长阈值 | 处理方式 |
|----------|----------|----------|
| <24h 项目 | 算百分比，判断能否今日超 100 | 能超 100 → 必须放 |
| <24h 项目 | >80 但不能超 100 | 可以放 |
| 1k+ stars | 需要 80+ 增长 | 达标才放 |
| <1k stars | 需要 200+ 增长 | 达标才放 |
| 10k+ stars | — | 放入 watchlist |

### 4. 去重机制
- 昨天发过的项目 → 只放 watchlist，不进正文
- 前几天发过的项目 → 只放 watchlist，不进正文
- 有版本更新才在 watchlist 里说明变化
- 避免重复推荐同一项目

### 5. MCP 验证机制
GitHub 上的 MCP 必须进行 GitHub 验证：
- Star 数 > 100
- 最近 7 天有更新
- README 完整性（有安装说明、使用示例）
- 有实际代码（非空仓库）
不符合要求 → 不推荐，当没有这个

### 6. Skill 来源限制
- 必须是 GitHub 上今日异常增长的
- 不能从 reddit/HN 等地方随便找
- 必须有 star 数据支撑
- 无 star 数据 → 不收录
- **用户明确要求（2026-06-04）**：增强器（如 CodexPlusPlus）、Skill（如 PPT 生成、插画生成）都要收录，不管内容主题是什么

### 6b. Agent 相关性判断（2026-06-04 新增）
- **关键词匹配**作为第一层过滤（快）
- **LLM 读 README** 作为第二层过滤（准确）：关键词不通过的项目，获取 README 后逐个调 LLM 判断
- 逐个调用优于批量调用（批量注意力下降，13个一起发准确率下降）
- LLM 返回 `{relevant: bool, category: str, reason: str}`
- 增强器、Skill 一律收录（用户 2026-06-04 确认）

### 7. 模型与 API 变化范围
只关注以下两个来源：
- model_docs：模型文档变更
- framework_docs：框架文档变更
不从其他来源采集模型变化信息

### 8. External Digests 推送规则
- A 类且中文 → 推送到对应板块位置
- 英文或 B/C 类 → 不推送，仅作为数据源

### 9. 过滤无关信息源
过滤与 Agent 生态无关的内容：
- 纯图像处理工具（如 iLoveIMG 替代品）
- 纯安全事件（如 npm 包被攻陷）
- 纯开发工具（如端口管理工具）
除非与 Agent/MCP/Workflow 强相关

### 9b. External Digests Enrichment 质量（2026-06-04）
- `item_enrichment.max_items` 必须设为 0（不限制），否则超出部分走离线模板，同一句话重复30次
- batch_size=3 保质，42条约需14次 LLM 调用（1-2分钟）
- 金融/硬件等非 Agent 生态的 external 条目应被过滤，减少无效 enrichment

### 10. Watchlist 规则
- 10k+ stars 的项目自动进入 watchlist
- 连续跟踪的项目不重复进入正文
- 有版本更新才在 watchlist 里说明变化
- watchlist 只展示：项目名、Stars、24h增长、变化说明


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

金融/投资/股市（P77 新增，与 Agent 生态无关）：
美股异动, 市值暴涨, 市值最高, 涨超, 暴跌, IPO出现波折, 私人信贷, 基金创始人, 桥水基金, 高盛首席, Goldman Sachs CEO, Pimco, 纳斯达克, 港交所, 债市, 股市, 私募

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
- 同一 source 占比 ≤ 45%（**注意：2026-06-02 实测 GitHub 占 66.7%，此规则未生效**）
- 同一 category 占比 ≤ 35%
- 低质量模式: 求推荐、水一贴、闲聊、招聘、优惠券、抽奖、薅羊毛
- **Section quota 应按源权重分配**，避免单一源占满所有板块（P55）

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

## 源健康趋势 (source_health.py)

每次运行后自动记录 source_status 到 `state/source_health_history.json`。
保留 30 天历史，追踪：
- success_rate / failure_rate / no_match_rate
- signal_density = avg_matched / avg_raw
- current_streak (连续 N 天同一状态)
- last_success / last_failure 日期

Hermes 可调用 `get_unhealthy_sources()` 识别连续失败的源并自主修复。

## MCP Server (mcp_server.py)

其他 Agent 可查询日报数据：

| Tool | 功能 |
|------|------|
| list_reports | 列出可用报告日期 |
| get_latest | 获取最新报告 |
| get_report | 按日期获取报告 |
| search | 关键词搜索 |
| source_health | 源健康趋势 |

支持 stdio 和 HTTP 两种模式。

## OPML 导入 (opml_import.py)

用户可导入 RSS reader 的 OPML 文件，自动添加到 `config.custom_rss.feeds`。
支持标准 OPML XML 格式。

## Hermes 自主维护 (AGENTS.md)

AGENTS.md 供 Hermes Agent 在日报系统出问题时自主参考：
- 快速诊断流程: source_status → health → keywords → token
- 自主修复: 关键词不匹配、API变更、外部信源更新、state清理
- 运行命令参考
- 关键 Pitfalls 清单

Hermes 在遇到日报问题时应先读 AGENTS.md，再决定修复方案。

### GitHub 跟踪状态表

日报的"GitHub 跟踪状态"必须生成完整的 markdown 表格，不能只写"详见 Source Status 表"。

表格格式：
```markdown
### GitHub 跟踪状态

| 项目 | Stars | 24h增长 | 状态 | 分类 | 最近更新 |
|------|------:|--------:|------|------|----------|
| browser-use/browser-use | 97,202 | +168 | watchlist | Tool / Plugin / Connector | 2026-06-01 |
| ... | ... | ... | ... | ... | ... |

> 状态说明：watchlist=持续跟踪, probation_7d=7天观察期, archived=已归档
```

数据来源：`state/github_repo_state.json` 的 repos 字段，按 stars 降序排列 Top 20。

### 待观察项目（新增板块）

从社区/新闻中发现的 GitHub 项目，需观察 24h star 变化后再决定是否推荐。

```markdown
### 待观察项目

> 从社区/新闻中发现的GitHub项目，需观察24h star变化后再决定是否推荐。

| 项目 | 来源 | Stars | 发现日期 | 状态 | 说明 |
|------|------|------:|----------|------|------|
| [getpaseo/paseo](https://github.com/getpaseo/paseo) | HackerNews | 7,771 | 2026-06-05 | 待观察 | Coding agents from your phone, desktop and CLI |

> 观察规则：发现后记录初始star数，24h后再次检查，若增长≥50则纳入推荐。
```

**触发条件**：HackerNews/Reddit/LinuxDo 等社区来源中提到 GitHub 项目时，自动加入待观察列表。
**操作**：添加到 `state/github_repo_state.json`，tracking_status=candidate_30d，next_check_date=明天。

### 更新信息（新增板块）

已跟踪项目的版本更新、重要 PR、架构变化等信息。

```markdown
### 更新信息

> 已跟踪项目的版本更新、重要PR、架构变化等信息。

#### pydantic/pydantic-ai - v1.106.0
- **分类**: Agent Framework
- **链接**: [release链接]
- **Stars**: 17,525
- **摘要**: 版本更新内容
- **工程价值**: 对Hermes用户的实际价值
- **集成建议**: 是否需要立即升级
- **关键判断**: 核心洞察
- **可操作性**: low | Track trend only | 集成: ignore
```

**触发条件**：Watch List 项目有新版本发布、重要 PR 合并、架构变化时。
**位置**：在 Watch List 重要变化之后、待观察项目之前。

### 自动GitHub项目发现（2026-06-05 新增）

从 HackerNews/Reddit/LinuxDo/NodeSeek/ProductHunt 等非 GitHub 来源自动提取 GitHub 链接，添加到观察列表。

**实现**：
- `collect_hackernews.py`：`_format_story` 方法提取 URL 和 text 中的 `github.com/{owner}/{repo}` 链接，存入 `github_repo` / `github_url` 字段
- `github_link_enricher.py`：`add_to_watch_list()` 函数将新发现的项目写入 `state/github_repo_state.json`，状态为 `candidate_30d`，`next_check_date` 设为明天
- `generate_report.py`：新增 "待观察项目" 子栏目，显示从社区发现的 GitHub 项目

**观察规则**：发现后记录初始 star 数，24h 后再次检查，若增长 ≥50 则纳入推荐。

**触发条件**：`item.source in ("hackernews", "reddit", "producthunt", "linuxdo", "nodeseek")` 且 `github_repo` 非空且不在已有 state 中。

## 日报板块

日报开头展示 Source Status 表：

| Source | Auth | Strategy Used | Status | Raw | Matched | Selected | Notes |
|---|---|---|---|---:|---:|---:|---|

正文板块（按 section quota 输出）：
1. 今日关键事件
2. GitHub 高增长项目
   - GitHub 跟踪状态表（Top 20，markdown 格式）
   - 今日实时爆发项目
   - 今日新发现项目
   - 每日异常增长项目
   - Watch List 重要变化
   - 更新信息（版本更新/PR/架构变化）
   - 待观察项目（社区发现，需24h观察）
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
| SMITHERY_API_KEY | 否 | Smithery MCP Registry（缺则 skipped_requires_api_key） |
| AGENT_PIPELINE_API_KEY | 否 | Agent Pipeline LLM（缺则走降级模式） |
| AGENT_PIPELINE_BASE_URL | 否 | Agent Pipeline LLM base URL（默认 OpenAI） |

## 配置变更记录 (2026-06-04)

| 配置项 | 旧值 | 新值 | 原因 |
|--------|------|------|------|
| agent_pipeline.agents.item_enrichment.max_items | 12 | 0 | 原来只有12条走LLM，剩下全用离线模板。改为0=不限制，全部走LLM |
| agent_pipeline.agents.item_enrichment.batch_size | 3 | 1 | 用户要求逐条调用LLM，质量最高 |

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
| P17 | source_status.py 常量被 patch 截断 | STATUS_SKIPPED_MISSING_AUTH 变成 "skippe...auth", STATUS_FAILED_AUTH 变成 "***"。patch 替换时 old_string 匹配到不完整行。修复：整个文件重写而非逐行 patch |
| P18 | execute_code write_file 写沙箱不写磁盘 | hermes_tools.write_file 在 execute_code 中写到沙箱，不用 open() 则文件不落盘。必须用 `with open(path, 'w') as f: f.write(content)` |
| P19 | collector --test 缺 import | __main__ 块必须 import os, json, yaml, argparse。否则 NameError。用 `import argparse, json as _json` 模式避免与模块级冲突 |
| P20 | V2EX API 返回数据但 matched=0 | V2EX hot/latest 可能不含 Agent 关键词。164 raw / 0 matched 是 success_no_match，不是失败。需检查关键词是否覆盖实际 V2EX 内容 |
| P21 | make_source_status(items=...) 导致 HN/Reddit/PH 全部失败 | collector 不得向 make_source_status 传 items 参数。items 由 collector 直接返回为元组第一项。修复：正则删除所有 `items=matched[...]` 和 `items=items[...]` |
| P22 | collector --test 读不到 token | --test 模式不经过 main.py 的 load_env_file()。每个 collector 的 __main__ 块必须先加载 .env：`for _ep in [_Path.home()/".hermes"/".env", _Path(__file__).parent.parent/".env"]: ...` |
| P23 | generate_report 收到 C/D 级内容导致 selected_count≠正文数 | main.py 必须在 quality_gates 后过滤 `selected_items = [i for i in scored if importance_level in ("S","A","B")]`，只传 selected_items 给 generate_report |
| P24 | HN Firebase 故事超过 72h 进入日报 | Algolia 有 72h 过滤但 Firebase 没有。必须在 dedup 后、关键词过滤前添加 final_age_filter：`int(s.get("time",0)) >= cutoff` |
| P25 | V2EX _is_relevant 只匹配 title 导致低命中率 | hot/latest 必须传 title+content+node+url 给 _is_relevant。node 通过 `topic.get("node",{}).get("name","")` 获取 |
| P26 | Low Signal Day 仍输出"X方向活跃"趋势 | low_signal=true 时 _generate_insights 必须返回诊断信息而非趋势。_generate_recommendations 必须返回确定性建议（修复失败源、检查关键词等） |
| P27 | report_layout target_items 未使用 | _section_items 必须读取 config 的 target_items 和 max_items，先填 target 再 cap 到 max |
| P28 | `__pycache__` 导致旧代码运行 | 批量修改 .py 文件后必须清除**所有** `__pycache__` 目录（主目录 + scripts/ + tests/），不只是 scripts/。用 `execute_code` 遍历清理：`for root, dirs, _ in os.walk(base): [shutil.rmtree(os.path.join(root, d)) for d in dirs if d == '__pycache__']`。否则 Python 优先加载 .pyc 而非 .py |
| P29 | main.py 变量作用域错误 | selected_items/sel_count 必须在 quality_gates 之后、backfill 之前定义 |
| P30 | GitHub --test 超时 | --test 改为轻量模式：只验证 auth + 抓 1 个 watch repo |
| P29 | main.py 变量作用域错误 | selected_items/sel_count 必须在 quality_gates 之后定义 |
| P30 | make_source_status(items=...) | HN/Reddit/PH collector 传了 items 参数导致 TypeError。正则删除所有 items=matched[:] |
| P31 | collector --test 读不到 token | __main__ 块必须先加载 .env |
| P32 | V2EX matched=0 | hot/latest 只传 title 给 _is_relevant，必须传 title+content+node+url |
| P33 | HN Firebase >72h 旧帖 | Algolia 有 72h 过滤但 Firebase 没有，必须加 final_age_filter |
| P34 | Low Signal Day 仍输出趋势 | low_signal=true 时 _generate_insights 必须返回诊断信息 |
| P35 | report_layout target_items 未使用 | _section_items 必须读 target_items 和 max_items |
| P36 | config.yaml 替换失败 | YAML 中的引号转义导致 old_string 不匹配，用 execute_code + open() 直接操作 |
| P37 | 全脚本无 Agent 判断 | 参考 ai-news-agent 的 candidate→decision JSON 模式插入 Agent 节点 |
| P38 | ai-news-radar 端点错误 | 旧端点 `/data/latest.json` 返回 0。正确端点: `/data/latest-24h.json`，fallback 到 raw.githubusercontent.com |
| P39 | source_status 常量截断 | STATUS_SKIPPED_MISSING_AUTH 和 STATUS_FAILED_AUTH 被 patch 截断为 "skippe...auth" 和 "***"。必须整个文件重写 |
| P40 | smithery 返回 success_no_match 而非 skipped | collector 返回空列表时被合并器覆盖为 success_no_match。需要用 _pending_skip 哨兵机制传递跳过状态 |
| P41 | mcp.so 无稳定 API 每天报错 | enabled=false 降级为 skipped_disabled。无稳定API的源不应作为失败源 |
| P42 | YAML config 替换边界错误 | external_sources 嵌套在 external_digests 内时，替换脚本找错了顶级 key 边界导致行合并。需要验证行首缩进 |
| P43 | low_signal 在 agent_pipeline 调用时未定义 | main.py 中 low_signal 原来在 generate_report 前才计算，但 agent_pipeline 需要它。必须提前到 agent pipeline 入口处计算 |
| P44 | agent_pipeline.py 缺 import 导致 NameError | agent_pipeline.py 从 enrich_report_with_agent 导入 build_offline_enrichment_record，但只在 except 块内 lazy import，避免主路径依赖 |
| P45 | --dry-run 时不写 intermediate 文件 | agent_pipeline 的 write_state 由 main.py 的 write_state 控制，--dry-run 时 write_state=False，不会生成 data/intermediate/ |
| P46 | 完整 pipeline 超时 | execute_code 300s 硬超时杀子进程；terminal(background=True) 在 Windows 上触发 WSL 错误。**必须用 subprocess.Popen + DETACHED_PROCESS 启动独立后台进程**，psutil 轮询，最长等 30 分钟。详见 `references/long-running-pipeline.md` |
| P47 | WeChat context_token 过期导致推送失败 | iLink rate limiting (ret=-2) 后 token 变 stale。清理 `~/.hermes/weixin/accounts/*context-tokens.json` + 用全局 `Hermes_Gateway.cmd` 重启（不能用项目 hermes.bat，因为项目级缺少微信配置） |
| P48 | agent_pipeline enabled=true 但 LLM 未配置 | config.yaml 中 agent_pipeline.enabled=true，但 AGENT_PIPELINE_API_KEY 未设置时会走降级模式（Trust 跳过，Enrichment 用离线模板，Editor 用规则）。不会报错，只是静默降级 |
| P49 | YAML dump 破坏注释 | yaml.dump() 不保留注释和自定义格式。修改 config.yaml 时用 execute_code + 逐行文本替换，不要 yaml.safe_load + yaml.dump |
| P50 | HN 全部归类为 Community | classify_items.py 对 HN 条目的分类逻辑有 bug，所有 HN 条目都被归类为 "Community"，导致 relevance=10, utility=8。实际 HN 内容包含 Coding Agent、MCP、Tool、Workflow 等。修复：HN 条目应按标题内容实体分类，不按 source 简单分类 |
| P51 | RSS 条目 primary_category 为空 | RSS collector 采集的条目 primary_category 字段为空，导致无法分配到对应板块，全部被过滤。修复：RSS collector 必须设置 primary_category |
| P52 | MCP 板块忽略 external 源 | MCP section target=3~5，但被 reddit 的 MCP 条目占满后，21 个 B 级 MCP Registry/Glama 条目被忽略。修复：generate_report.py 的 section 填充逻辑应优先使用专用源（如 MCP Registry）的条目 |
| P53 | Section quota 无源分配限制 | GitHub 独占 66.7% Displayed，其他源被挤掉。修复：section quota 应按源权重分配，单一源占比不超过 45% |
| P54 | HN collector 不存储 story ID | collect_hackernews.py 只存储外部 URL，不存储 HN story ID，导致无法构造讨论链接。修复：raw 数据中增加 hn_id 字段，URL 优先使用 HN 讨论链接 |
| P55 | External Digests A/B 条目 Displayed=0 | 33 个 A/B 候选（MCP Registry 21、agents-radar 5、ai-news-radar 5、ai-news-agent 1、ai-tool-releases 1）全部 Displayed=0。根因是 P52+P53 |
| P50 | 手动拆分日报逐段发送触发持久限流 | 日报通常 20-30K 字符，拆分后 6-7 条消息（每条 ~3500 字符）。**2026-06-04 实测：连续发送 4 条即触发 iLink 账户级限流（ret=-2），限流后即使等 60 秒重试仍失败，限流持续数小时**。解决方案：(1) 最多连续发 3 条，第 4 条前必须等 2 分钟；(2) 用 cron job 的 final response 自动推送；(3) 一旦收到 ret=-2，**立即停止**，告知用户已发送/剩余部分，等 2-6 小时恢复。**绝对不要**在限流后每 15-60 秒重试——会延长限流时间。**铁律：先 read_file 读取实际报告，不得凭记忆编造内容** |
| P50 | 微信拆分发送限流 | 日报拆分后 6-7 条消息（每条 ~3500 字符）。**2026-06-04 实测：连续发送 4 条即触发 iLink 账户级限流（ret=-2），第1-3条成功，第4条失败**。**铁律：最多连续发 3 条，第 4 条前必须等 2 分钟**。收到 ret=-2 立即停止，等 2-6 小时恢复。不要重试 |
| P52 | HN 条目全部归类为 Community | 2026-06-02 实测：23条HN条目全部 primary_category="Community"，但实际包含 Coding Agent、MCP、Tool 等。根因：classify_items.py 对 HN 条目的分类逻辑可能将 source 直接映射为 Community 而非按内容实体分类。修复：检查 classify_items.py 的 HN 分支 |
| P53 | RSS 条目 primary_category 为空 | 2026-06-02 实测：37条 RSS matched 条目的 primary_category 字段为空字符串，导致无法分配到对应板块。根因：RSS collector 未设置 primary_category。修复：RSS collector 应根据 feed 名称（Dev.to LLM → Coding Agent/Model，Dev.to Agent → Agent Framework）设置默认 category |
| P54 | MCP section 忽略 external 源的 B 级条目 | 2026-06-02 实测：MCP Registry 有 11 个 B 级新 MCP server，Glama 有 10 个 B 级，但 MCP section 只显示了 2 个 reddit 条目。根因：generate_report.py 的 section 分配逻辑可能按 source 优先级排序，external 源被排在后面。修复：MCP section 应优先使用 MCP Registry/Glama 的条目 |
| P55 | Section quota 被单一源占满（GitHub 66.7%） | 2026-06-02 实测：GitHub 16条(66.7%) + Reddit 8条(33.3%) = 24条，其他9个源全部 Displayed=0。根因：section quota 无源分配限制，GitHub A/B 候选数量远超其他源。修复：增加 section quota 的源分配逻辑，每个 section 至少保留 1 个位置给非 GitHub 源，或按设计权重分配 |
| P56 | 用 Algolia 搜索标题找 HN 链接会匹配到旧 story | 2026-06-02 实测：搜索 "Zerostack" 匹配到 575pts 的旧 story（id=48164287），而实际采集的是 12pts 的新 story（id=48340468）。**原始数据已有 `hn_url` 字段（23/23 条都有）**，直接使用即可，不需要 Algolia 反查。如果需要 HN 讨论链接，从 raw 数据的 `hn_url` 字段读取 |
| P57 | HN 72h 过滤是开贴时间不是最后回复时间 | `created_at_i` 和 Firebase 的 `time` 字段都是 story 创建时间。一个 2 天前开的热帖（如 575pts Zerostack）即使今天还在活跃讨论，也会被 72h 过滤掉。Algolia 来源的 story 跳过代码中的 72h 过滤（`s.get("_source") == "algolia"`），但 Algolia API 自身有 `created_at_i>72h_ago` 参数 |
| P58 | Firebase newstories 无 points 门槛 | Firebase API 的 top/new/best stories 各取 50 条，不限 points。Algolia 有 `points>5` 过滤。因此 ≤5pts 的条目只能来自 Firebase newstories（新帖）。如果想过滤低质量条目，需给 Firebase 也加 points 门槛 |
| P65 | Growth gate 阈值过严 | 1k-5k 要求 rate>=20% 过严；<1k 直接不 reportable；archived 被跳过。修复：1k-5k delta>=100、<1k delta>=200 即 reportable。详见 references/growth-gate-fix.md |
| P74 | star_delta_24h 未归一化 | 当快照间隔不足24h时（如1.5h），delta_24h 用原始差值而非24h等效值。例：CodexPlusPlus 1.5h内+71，归一化后+1117。**已修复**：github_state.py calculate_historical_growth 中，interval<23h 时 delta_24h = round(delta_raw / interval_hours * 24)。metrics 新增 star_delta_24h_raw 保留原始值 |
| P75 | has_strong_agent_signal 漏判 Skill | 关键词匹配太僵硬：CodexPlusPlus（Agent增强器）、PaperSpine（Skill）、GordenPPTSkill（Skill）均未命中。**已修复**：增加 LLM 兜底判断，逐个读 README 判断是否与 Agent 生态相关。用户明确要求：Skill 和增强器无论内容主题都应纳入 |
| P76 | LLM 批量判断准确率下降 | 13个项目一起发给 LLM 时，长 prompt 导致注意力下降。**已确认**：逐个判断（每个项目独立 LLM 调用）更准确，13次调用约60秒可接受 |
| P66 | _find_growth_anomalies 跳过已进 candidates 的仓库 | L1008 `if rn in already: continue` 导致 discovery_candidate 不参与增长检测。同一仓库可同时有 discovery 和 growth 信号 |
| P62 | 候选池表未生成 | 2026-06-02 实测：用户要求日报末尾新增候选池表，包含所有候选项目。修复：在 report_layout 中添加 candidate_pool section
| P63 | HuggingFace 新模型直接放 A 级 | 2026-06-02 实测：用户要求提高 HuggingFace 判别标准，必须满足知名机构发布/star增长异常/社区热议才能放 A 级
| P64 | 异常增长项目规则不细化 | 2026-06-02 实测：用户要求细化规则，<24h 算百分比，1k+需要80+增长，<1k需要200+增长，10k+放watchlist
| P65 | 重复推荐同一项目 | 2026-06-02 实测：LangGraph/crewAI 昨天已推荐，今天又进正文。修复：昨天发过的只放 watchlist
| P66 | MCP 未验证就推荐 | 2026-06-02 实测：用户要求 GitHub MCP 必须验证 star>100、最近7天有更新、README完整、有实际代码
| P67 | Skill 来源不限制 | 2026-06-02 实测：用户要求 Skill 必须是 GitHub 上今日异常增长的，不能从 reddit/HN 随便找
| P68 | 模型与 API 变化范围过大 | 2026-06-02 实测：用户要求只关注 model_docs 和 framework_docs
| P69 | External Digests A 类未推送 | 2026-06-02 实测：用户要求 A 类且中文的推送到对应板块位置
| P70 | 过滤无关信息源 | 2026-06-02 实测：用户要求过滤与 Agent 生态无关的内容（如纯图像处理工具、纯安全事件） |
| P71 | batch_size 不一致 | 2026-06-04：用户要求所有 Agent batch_size=1。Trust Agent 原来 batch_size=5，改为 1 |
| P72 | timeout_seconds=0 导致网络请求失败 | 2026-06-05 实测确认：`timeout_seconds: 0` 导致 "Attempted to set connect timeout to 0" 错误。**影响范围**：所有 RSS 源全部返回 failed_network。**修复**：所有 timeout_seconds 改为 **60**。**必须检查的所有位置**（共 10 处）：`rss_feeds.request.timeout_seconds`、`developer_communities.linuxdo.request.timeout_seconds`、`developer_communities.nodeseek.request.timeout_seconds`、`hackernews.request.timeout_seconds`、`producthunt.request.timeout_seconds`、`reddit.request.timeout_seconds`、`agent_pipeline.agents.editor.timeout_seconds`、`agent_pipeline.agents.github_trust.timeout_seconds`、`agent_pipeline.agents.item_enrichment.timeout_seconds`、`agent_pipeline.source_verification.timeout_seconds`。**还需修复** `scripts/agent_llm_client.py` L49：`self.timeout = max(30, int(llm_config.get("timeout_seconds", 120)))`。**注意**：yaml.dump() 会丢失注释，修改 config.yaml 时用 execute_code + 逐行文本替换 |
| P80 | weak_agent_signal 误杀 Skill/Agent 项目 | 2026-06-05 实测：CodexPlusPlus（Agent增强器）、science-skills（Skill）、SkillOpt（Skill）均被标记为 weak_agent_signal 并排除。根因：`evaluate_github_growth_gate()` 在 `has_strong_agent_signal()` 返回 False 时直接 return，不检查项目是否为 Skill/Agent/Tool/Workflow。**修复**：添加 `_is_skill_or_agent_project(repo)` 函数检查 description/topics/name 中的 skill/agent/tool/workflow/mcp/codex 等关键词，匹配则跳过 weak_agent_signal 检查。**规则**：所有 Skill/Agent/Tool/Workflow 项目绝不应标记为 weak_agent_signal |
| P82 | 用户报告"项目未推送/等级错误"但实际数据正确 | 2026-06-05 实测：用户报告 `yetone/native-feel-skill` score=60 但 level=C 且未推送。**实际验证**：score=60 → level=B（正确），quality_flags=None（无 cap），项目已在报告中（`[B] 原生体验技能`）。**教训**：用户报告"未推送"或"等级错误"时，必须先验证实际数据再诊断 bug。验证步骤：(1) 用 `execute_code` 读取 `data/scored/{date}.json` 查找项目；(2) 检查 `score`、`importance_level`、`quality_flags`、`trust_score`、`trust_reason` 五个字段；(3) 用 `grep` 在报告文件中搜索项目名确认是否已推送。**常见原因**：(a) Trust Agent 降级——trust_score 30-60 之间会降一级（A→B, B→C）；(b) 数据刷新延迟；(c) 用户查看了旧版本报告。**不要假设用户报告准确**——2026-06-05 实测：9个项目被降级（Trust Agent 设计行为，非 bug）。详见 `references/trust-decision-mechanism.md` 和 `references/scoring-verification-pattern.md` |
| P83 | Trust Decision 降级逻辑过于宽泛 | 2026-06-05 实测：mastra-ai/mastra（score=78, A级）和 BigPizzaV3/CodexPlusPlus（score=73, A级）因"无多源共振证据"被降级到B。**用户要求**：仅对特定原因（Bug修复PR、缺乏独立价值）降级，"无多源共振证据"不应降级。**修复**：修改 `agent_pipeline.py` 的 `apply_trust_decisions()` 函数，添加降级关键词检查和多源共振升级逻辑。详见 `references/trust-decision-mechanism.md` |
| P86 | execute_code 300s 超时杀掉轮询循环 | execute_code 有 300s 硬超时，任何 polling loop（如每 10s 检查 pipeline 状态）在 300s 后被杀。**不要用 execute_code 内的 for+time.sleep 循环做长时间轮询**。正确做法：(1) 先用 `run_pipeline.py --background` 启动；(2) 立即返回，等用户追问时再用 `--status` 单次检查；(3) 不要在 execute_code 里写 36*10s 的循环——它永远到不了 360s |
| P84 | score_items.py 缺少 `import os` 导致静默失败 | `_calc_daily_avg_growth` 使用 `os.path.exists()` 但模块顶部未 `import os`。`except: return None` 吞掉异常导致函数静默返回 None。**调试**：改 `except Exception as e: print(f\"Error: {e}\")` 立即发现 `name 'os' is not defined`。**教训**：(1) 模块顶部 import 所有依赖；(2) `except: return None` 是最危险的错误处理模式；(3) 返回 None 需验证是否因异常 |
| P85 | 日均增长保底B级阈值过低 | 初始 `daily_avg > 0` 即保底B级，导致 118/264 项目被提升（含 0.2 stars/day）。**修复**：阈值改为 `daily_avg >= 20 stars/day`，提升数量降至 19 个。保底机制必须有合理下限，否则稀释高等级区分度 |
| P84 | score_items.py 缺少 `import os` 导致静默失败 | `_calc_daily_avg_growth` 使用 `os.path.exists()` 但模块顶部未 `import os`。`except: return None` 吞掉异常导致函数静默返回 None。**调试**：改 `except Exception as e: print(f"Error: {e}")` 立即发现 `name 'os' is not defined`。**教训**：(1) 模块顶部 import 所有依赖；(2) `except: return None` 是最危险的错误处理模式；(3) 返回 None 需验证是否因异常 |
| P85 | 日均增长保底B级阈值过低 | 初始 `daily_avg > 0` 即保底B级，导致 118/264 项目被提升（含 0.2 stars/day）。**修复**：阈值改为 `daily_avg >= 20 stars/day`，提升数量降至 19 个。保底机制必须有合理下限，否则稀释高等级区分度 |
| P81 | ai-news-radar 信源已移除 | 2026-06-05 用户要求从 external_digests 移除 ai-news-radar（LearnPrompt/ai-news-radar）。config.yaml 中 `external_sources` 列表已删除该条目 |
| P73 | max_items 限制处理数量 | 2026-06-04：用户要求解除 max_items 限制，Trust Agent 从 30 改为 0 |
| P74 | SkillOpt 目录名连字符导致 ModuleNotFoundError | Python 模块名不能有连字符，必须用下划线 |
| P75 | SkillOpt abstract method 签名不匹配 | rollout/reflect/get_task_types 必须匹配基类签名 |
| P62 | MCP Registry/Glama API 无 star 数据 | Official MCP Registry (`registry.modelcontextprotocol.io/v0.1/servers`) 和 Glama (`glama.ai/api/mcp/v1/servers`) 都返回 repo URL 但不返回 star/downloads。Popularity 固定 5 分。如需热度数据，需从 repo URL 反查 GitHub API 获取 stars。Official Registry 有 `status`（active/inactive）和 `publishedAt` 字段可判断维护状态 |
| P63 | HN _is_relevant text 匹配含 HTML 正文 | `_is_relevant` 的 text 字段包含 `story_text`（HTML），子串匹配会匹配到 HTML 标签内的内容。应先 strip HTML 再匹配 |
| P64 | MCP Registry 新 server 评分固定 60 分 | 11 个 Official + 10 个 Glama MCP server 全部 60 分（R=28 P=5 F=5 G=3 U=19），因为 Popularity 固定 5、Freshness 按发布时间可能只有 5。需要引入 GitHub stars 或下载量来差异化评分 |
| P65 | Growth gate 阈值过严导致异常增长全部缺失 | 2026-06-03 诊断：state 有 3 天快照（CodexPlusPlus +332、memory-os +309、loom +242），但报告输出"暂无"。根因：(1) 1k-5k 区间要求 rate>=20% 过于严格（SkillOpt +143/3.2% 被拒）；(2) <1k 区间直接 return 不 reportable（memory-os +309 被拒）；(3) archived 状态仓库被完全跳过。**已修复**：1k-5k 改为 delta>=100 即 reportable；<1k 改为 delta>=200 即 reportable。修改文件：collect_github.py evaluate_github_growth_gate()。清理所有 __pycache__ 后语法检查通过 |
| P66 | _find_growth_anomalies 跳过已在 candidates 中的仓库 | collect_github.py L1008 `if rn in already: continue` 导致已通过 Discovery Pool 进入 candidates 的仓库（如 CodexPlusPlus, discovery_type=discovery_candidate）不参与增长异常检测。同一仓库可能同时满足 discovery 和 growth 两种信号，不应互相排斥。**待修复** |
| P74 | star_delta_24h 未归一化 | 快照间隔不足24h时（如1.5h），delta_24h 用原始差值而非等效24h值。CodexPlusPlus: 原始+71→归一化+1117(rate=9.1%)。**已修复**：github_state.py calculate_historical_growth 添加 `delta_24h = round(delta_raw / interval_hours * 24)`，新增 `star_delta_24h_raw` 保留原始值 |
| P75 | watchlist 项目重复进入正文 | langchain-ai/langgraph 同时出现在 Watch List 表格和 Agent/Coding Agent 正文。根因：release 事件（`langgraph - 1.2.4`）和 repo 本体（`langgraph`）的 normalized_entity 不同，去重逻辑未合并。**已修复**：generate_report.py 添加 `_extract_repo_from_item` 函数，agent_items 排除已在 watchlist 的 repo |
| P76 | LLM Agent 相关性判断 | 用户要求用 LLM 读 README 判断 Agent 相关性，而非关键词匹配。方案：批量获取 README → 逐个调 LLM（批量会导致注意力下降）。返回 `{relevant, category, reason}`。用户明确要求：增强器、Skill 都要收录 |
| P77 | enrichment fallback 模板泛滥 | config.yaml `item_enrichment.max_items: 12` 导致42条中30条走离线模板（同一句话）。**已修复**：max_items 改为0（不限制）。注意：会增加 token 消耗和 pipeline 时间 |
| P67 | execute_code 300s 超时杀掉长 pipeline | execute_code 有 300s 硬超时，完整 pipeline（11源+Agent Pipeline）需 5-15 分钟。subprocess.run 会被连带终止。**已修复**：创建 `run_pipeline.py` wrapper 脚本，用 `subprocess.Popen + DETACHED_PROCESS` 启动独立后台进程，不受父进程超时限制。用法：`python run_pipeline.py --background` / `--status` / `--log` / `--kill`。psutil 轮询检查完成状态，最长等 30 分钟 |
| P66 | _find_growth_anomalies 跳过已在 candidates 中的仓库 | collect_github.py L1008 `if rn in already: continue` 导致已通过 Discovery Pool 进入 candidates 的仓库（如 CodexPlusPlus, discovery_type=discovery_candidate）不参与增长异常检测。同一仓库可能同时满足 discovery 和 growth 两种信号，不应互相排斥 |
| P71 | execute_code 300s 超时杀子进程 | 完整 pipeline 需要 5-15 分钟，execute_code 300s 硬超时会连带杀掉 subprocess 子进程。必须用 `run_pipeline.py --background` 启动独立后台进程（DETACHED_PROCESS），再用 `--status` 轮询，最长等 30 分钟 |
| P72 | GitHub API 限流导致 pipeline 超慢 | 采集 625 个仓库的 snapshot 时，每个 repo 都要 GET /repos/{name}，加上 search API，总计 300+ 请求。GitHub 未认证限流 60/h，即使有 token 也可能因并发被 403。pipeline 运行时间从 5min 膨胀到 20min+ |
| P73 | read_file 对 D: 盘路径返回 File not found 但文件存在 | 2026-06-04 实测：read_file("D:/openclaw-hermes/...") 返回 "File not found"，但 Python os.path.exists() 确认存在。terminal 的 stat 命令也因 WSL relay 失败。**必须用 execute_code + Python os/open 模块**读取 Windows D: 盘路径 |
| P74 | star_delta_24h 未归一化导致增长项目被误杀 | 2026-06-04 诊断：快照间隔只有1.5h时，delta_24h用原始差值（如71），而非24h等效值（1117）。**已修复**：github_state.py calculate_historical_growth() 中，当 interval_hours < 23 时，delta_24h = round(delta_raw / interval_hours * 24)。metrics 新增 star_delta_24h_raw 保留原始值 |
| P75 | watchlist 项目重复进入正文 | 2026-06-04 诊断：langchain-ai/langgraph（watchlist）和 langchain-ai/langgraph - 1.2.4（release事件）normalized_entity 不同，去重逻辑未捕获。**已修复**：generate_report.py select_display_items() 中，agent_items 过滤时用 _extract_repo_from_item() 提取 repo 全名，排除已在 watchlist 中的同一 repo 的 release/issue/PR 事件 |
| P76 | Enrichment max_items 限制导致大量离线模板 fallback | 2026-06-04 诊断：config.yaml 中 item_enrichment.max_items=12，42条中只有12条走LLM，30条用离线模板（全是同一句话"用途与最佳实践"）。**已修复**：max_items=0（不限制），batch_size=1（逐条调用） |
| P77 | External Digests 金融新闻与 Agent 生态无关 | 2026-06-04 诊断：9条金融新闻（美股异动、市值暴涨、IPO等）进入日报但与Agent生态无关。**已修复**：normalize_items.py negative_kws 添加金融关键词（美股异动、市值暴涨、IPO出现波折、私人信贷、基金创始人、桥水基金、高盛首席、Pimco等） |
| P78 | LLM Agent 相关性判断优于关键词匹配 | 2026-06-04 实测：has_strong_agent_signal 关键词匹配太僵硬，CodexPlusPlus（明显Agent工具）未命中。用 LLM 读 README 后判断，13个项目中11个正确通过。建议：关键词不通过的项目，用 LLM 读 README 做兜底判断 |
| P79 | MiMo API SSL 连接中断 | 2026-06-04 实测：batch 37-39 调用 token-plan-sgp.xiaomimimo.com 时 SSL EOF，导致 fallback。agent_llm_client.py 只重试1次。建议：增加重试次数或加 SSL keep-alive |
| P80 | Editor segments 超限走规则 fallback | 2026-06-04 实测：editable segments 32 > segment_max_segments=30，Editor 被跳过。建议：增大 segment_max_segments 或减少入选条目数 |
| P74 | star_delta_24h 未归一化 | 快照间隔不是精确24h时（如1.5h），raw delta 被直接当作24h值使用，导致增长项目被误杀。**修复**：`github_state.py` 的 `calculate_historical_growth` 中，当 `interval_hours < 23` 时归一化：`delta_24h = round(delta_raw / interval_hours * 24)`。metrics 新增 `star_delta_24h_raw` 保留原始值 |
| P75 | Watchlist 项目重复进入正文 | release/issue 事件（如 `langchain-ai/langgraph - 1.2.4`）与 repo 本体（`langchain-ai/langgraph`）的 normalized_entity 不同，去重逻辑未捕获。**修复**：`generate_report.py` 新增 `_extract_repo_from_item` 函数，`select_display_items` 中 agent_items 先排除已进 watchlist 的 repo |
| P76 | enrichment max_items 限制导致大量离线模板 | config.yaml 中 `item_enrichment.max_items=12`，超出部分走离线模板（30条全是同一句话"用途与最佳实践"）。**修复**：`max_items: 0`（不限制，全部走 LLM） |
| P77 | enrichment batch_size>1 导致质量下降 | batch=3 时 LLM 注意力分散，后面条目质量下降。**用户明确要求 batch_size=1**（逐条 LLM，最高质量）。42条约需3-5分钟 |
| P78 | 金融新闻未过滤 | external:ai-news-radar 中大量金融/投资/股市新闻（美股异动、IPO、市值暴涨等）与 Agent 生态无关。**修复**：normalize_items.py 的 negative_kws 添加金融关键词。**注意**：不要用过于宽泛的词（如"收购"、"估值"），会误杀有价值的条目（如"英伟达收购 Kumo AI"） |
| P79 | 关键词过滤不足以判断 Agent 相关性 | has_strong_agent_signal 的关键词匹配太僵硬（CodexPlusPlus 是 Agent 增强器但没命中任何模式词）。**方案**：用 LLM 读 README 逐个判断，batch_size=1 最准确。详见 `references/llm-relevance-check.md` |
| P74 | star_delta_24h 未归一化导致增长项目被误杀 | 2026-06-04 实测：pipeline 多次运行时快照间隔仅 1.5h，但 delta 被当作 24h 值。CodexPlusPlus raw=+71(1.5h) 归一化=+1117/day。修复：`github_state.py` 中当 interval<23h 时 `delta_24h = round(delta_raw / interval_hours * 24)`。详见 `references/growth-normalization-fix.md` |
| P74 | star_delta_24h 未做 24h 归一化 | 2026-06-04 实测：`calculate_historical_growth` 找昨天快照计算 delta，但不检查实际间隔是否 ~24h。CodexPlusPlus: 间隔仅 1.52h，delta=71 被当作 star_delta_24h，实际 24h 等效 = 71/1.52×24 = **1121**（rate=9.1%，应为 A 级）。MedSkillOS: 间隔 1.52h，delta=52，等效 821/day（应为 B 级 reportable）。**根因**：`github_state.py` 的 `calculate_historical_growth` 用 `stars_today - snap_1d["stars"]` 直接赋值给 `star_delta_24h`，未用 `interval_hours` 归一化。`evaluate_github_growth_gate` 也未检查 `is_full_24h` 字段。**修复方案**：当 `interval_hours < 23` 时，`star_delta_24h = delta / interval_hours * 24`；或在 growth gate 中跳过非完整 24h 快照。详见 `references/growth-gate-interval-bug.md` |
| P60 | HN _is_relevant 关键词匹配太宽松导致误匹配 | 2026-06-02 实测：_is_relevant 在 title+text+url 合并字符串中做子串匹配，导致 text 正文中顺带提及关键词的帖子被误收入。示例：(1) Expanse (GPU Capacity) 的 text 提到 coding agents → 匹配 coding agent；(2) Ask HN: ChatGPT recommends tools 的 text 提到 ai agents → 匹配 AI agent；(3) 768GB Optane 的 URL 包含 kimi-k2-5 → 匹配 Kimi。修复：title 匹配权重 > text 匹配；URL 匹配只针对特定域名；text 匹配加频率门槛 ≥2 |
| P66 | _find_growth_anomalies 跳过已在 candidates 中的仓库 | collect_github.py L1008 `if rn in already: continue` 导致已通过 Discovery Pool 进入 candidates 的仓库（如 CodexPlusPlus, discovery_type=discovery_candidate）不参与增长异常检测。同一仓库可能同时满足 discovery 和 growth 两种信号，不应互相排斥。待修复 |
| P85 | 日均增长保底B级阈值过低 | 初始 `daily_avg > 0` 即保底B级，导致 118/264 项目被提升（含 0.2 stars/day）。**修复**：阈值改为 `daily_avg >= 20 stars/day`，提升数量降至 19 个。保底机制必须有合理下限，否则稀释高等级区分度 |
| P86 | GitHub collector datetime 时区错误 | 2026-06-06 实测：`can't subtract offset-naive and offset-aware datetimes`，GitHub 源返回 failed_network，0 条数据。根因：collector 中混合使用了 aware（带时区）和 naive（不带时区）的 datetime 对象做减法。**修复**：所有 datetime 对象统一使用 aware（`datetime.now(timezone.utc)`）或在减法前用 `.replace(tzinfo=None)` 去掉时区信息 |
| P85 | 日均增长保底B级阈值过低 | 初始 `daily_avg > 0` 即保底B级，导致 118/264 项目被提升（含 0.2 stars/day）。**修复**：阈值改为 `daily_avg >= 20 stars/day`，提升数量降至 19 个。保底机制必须有合理下限，否则稀释高等级区分度 |
| P86 | `_parse_snapshot_time` 返回 naive datetime 导致 GitHub 整源失败 | 2026-06-06 实测：`github_state.py` L119 `_snapshot_interval_hours` 中 `(newer_at - older_at).total_seconds()` 报错 `can't subtract offset-naive and offset-aware datetimes`。根因：部分快照 `collected_at` 值无时区信息（如 `2026-06-06T14:54:08`），`datetime.fromisoformat()` 返回 naive datetime；而其他快照含 `+08:00` 或 `Z` 后缀返回 aware datetime。**修复**：`_parse_snapshot_time` 中对返回值强制检查 `dt.tzinfo is None`，若为 None 则 `dt.replace(tzinfo=JST)`。**影响**：此 bug 导致整个 GitHub 源返回 `failed_network`，raw=0。**调试方法**：在 `safe_collect` 的 except 块中添加 `import traceback; logger.error(traceback.format_exc())` 获取完整调用栈 |
| P87 | 用户说"report那个skill"指 agent-daily-report 不是 ai-daily-digest | 2026-06-06 实测：用户说"用report那个skill"，Agent 加载了 `ai-daily-digest`，用户纠正"我要用的是agent-daily-report"。**规则**：当用户说"report"、"日报"、"agent日报"时默认指 `agent-daily-report`；只有明确说"AI新闻日报"或"AI日报"时才用 `ai-daily-digest` |

## 日报诊断工具

当用户问"各源占比"或"为什么某源 Displayed=0"时，使用 **source-distribution-diagnostic** 诊断流程。详见 `references/source-distribution-diagnostic.md`。

## 微信手动推送规范 (WeChat Manual Push)

当用户要求手动推送日报到微信时，**必须严格遵守以下流程**：

### 铁律：先读后发，不得编造

1. **先读取实际报告文件** — 用 `execute_code` 读取 `data/reports/Agent_Daily_Report_YYYY-MM-DD.md`
2. **不得凭记忆或上下文重构内容** — 之前对话中出现过的片段可能已过时或不准确
3. **按文件实际内容拆分发送** — 不要自行编造摘要或省略

### 拆分策略

- 每条消息 ≤ 3500 字符（微信安全线）
- 按 `##` 一级标题作为拆分边界
- 每段标注 `[N/M]` 序号，方便用户确认完整性
- 最后一段标注 `✅ 推送完毕 (M/M)`
- P50 风险：拆分过多消息（>8条）可能触发 iLink 限流。合并小节为较少消息。

### 推送流程

```python
# 1. 读取报告
with open("D:/openclaw-hermes/agent-daily-report-skill/data/reports/Agent_Daily_Report_YYYY-MM-DD.md", "r", encoding="utf-8") as f:
    content = f.read()

# 2. 按 ## 标题拆分，每段 ≤ 3500 字符
chunks = []
current = ""
for line in content.split("\n"):
    if len(current) + len(line) + 1 > 3500 and current.strip():
        chunks.append(current)
        current = ""
    current += line + "\n"
if current.strip():
    chunks.append(current)

# 3. 逐段发送，标注序号
```

### 错误模式（已踩坑）

| 错误 | 后果 | 正确做法 |
|------|------|---------|
| 凭对话上下文编造"摘要版" | 数据与实际报告不一致，用户要求重发 | 先 read_file 再发 |
| 不标序号 | 用户不知道缺了哪段 | 每段 `[N/M]` 标注 |
| 按字符暴力截断 | 表格被截断、链接断裂 | 按 `##` 标题边界拆分 |
| 一次发完 | 超过微信单条消息限制，部分内容丢失 | 拆分后逐段发送 |
| 限流后每 15-60 秒重试 | 延长限流时间，2026-06-04 实测全部失败 | 收到 ret=-2 立即停止，等 2-6 小时 |
| read_file 读 D: 盘失败 | File not found 但文件存在 | 用 execute_code + Python os 模块读取 |

## 微信手动推送工作流

当用户要求手动推送日报到微信时，**必须**：

1. **先读取实际 .md 文件**，不要凭记忆或之前的内容拼凑
   ```python
   with open("D:/openclaw-hermes/agent-daily-report-skill/data/reports/Agent_Daily_Report_YYYY-MM-DD.md", "r", encoding="utf-8") as f:
       content = f.read()
   ```

2. **逐字原文发送**，不删减、不摘要、不精简。用户明确要求原始内容，不要"帮忙"缩短。

3. **按 ~3500 字符分段**（微信单条消息安全上限），在行边界切割，每段加 `[N/M]` 标签。

4. **每段间隔发送**，但注意 P50 限流：连续 3 条消息即触发 iLink rate limit (ret=-2)，限流后重试无效，持续数小时。建议：
   - 最多连续发 3 条，第 4 条前等 2 分钟
   - 一旦收到 ret=-2，**立即停止**，告知用户已发送的部分和剩余部分
   - 限流恢复（2-6 小时）后可重发剩余段，或用 cron job 延迟推送

| P55 | section quota 被单一源占满 | GitHub 16条(66.7%) + Reddit 8条(33.3%) = 24条，其他9个源全部 Displayed=0。增加源分配逻辑 |
| P56 | HN _format_story 硬编码 primary_category="Community" | collect_hackernews.py L168 硬编码。根据标题内容动态分类 |
| P57 | GitHub discovery penalty 封顶过低 | generic_github_discovery_candidate 封顶54分，导致高增长项目无法进日报。提高封顶到62 |
| P58 | HN 关键词匹配过于宽松 | text正文中顺带提及就匹配。title权重>text，URL加白名单 |
| P59 | HN Firebase newstories 无 points 门槛 | ≤5pts条目来自newstories。可加points门槛 |
| P60 | 重复推荐同一项目 | LangGraph/crewAI等昨天已展示的项目今天又出现在正文。修复：report_history.check_previous_days，昨日已展示→只放watchlist |
| P61 | HuggingFace新模型自动放A级 | 不是有新模型就放A级。修复：必须满足知名机构/star异常/社区热议之一，否则降B级或不收录 |
| P62 | Skill来源不是GitHub异常增长 | 从reddit/HN随便找的skill没有star数据。修复：skill来源必须是GitHub今日异常增长，无star数据不收录 |
| P63 | MCP未经GitHub验证 | GitHub上的MCP必须验证：star>100、7天内有更新、README完整、有实际代码。不符合→不推荐 |
| P64 | 增长项目不足24h未算百分比 | <24h项目需算百分比判断能否今日超100。能超100→必须放，>80但不能超→可以放 |
| P65 | External Digests A类中文未推送 | A类且中文的external digests条目应推送到对应板块位置，英文/B/C类不推送 |

## 定时推送 (Cron Job)

每天早上 6 点自动执行并推送到微信：
```
Job ID:    57e936ce4084
Schedule:  0 6 * * *
Deliver:   weixin:o9cq803R0Y4HMdI1VnJApgMyYGbo@im.wechat
Skill:     agent-daily-report
Workdir:   D:/openclaw-hermes/agent-daily-report-skill
```

Cron prompt 自包含：加载 skill → python main.py --debug → 读取日报 → 推送到微信。

### Obsidian 集成 (2026-06-02)
obsidian-second-brain skill 已安装，vault 在 `D:\ObsidianVault`。
日报可自动整理到 Obsidian vault 的 daily/ 目录。触发词："把今天的日报整理到 Obsidian"。

### 长 Pipeline 运行 (P67)

execute_code 有 300s 硬超时，完整 pipeline（11源 + Agent）通常需要 5-15 分钟。
**禁止**用 execute_code 内的 subprocess.run 运行完整 pipeline。

正确方式：用 `run_pipeline.py` wrapper（独立后台进程）：
```bash
cd D:/openclaw-hermes/agent-daily-report-skill
python run_pipeline.py --background   # 后台启动（不受超时限制）
python run_pipeline.py --status       # 查看运行状态
python run_pipeline.py --log          # 查看最新日志
python run_pipeline.py --kill         # 终止进程
```

或用 Popen + DETACHED_PROCESS 手动启动：
```python
proc = subprocess.Popen(
    [sys.executable, "main.py", "--debug"],
    cwd="D:/openclaw-hermes/agent-daily-report-skill",
    stdout=open(log_file, "w"),
    stderr=subprocess.STDOUT,
    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
    close_fds=True
)
```

然后用 psutil 轮询完成状态，最长等 30 分钟。

## 微信推送故障排查

如果 cron job 的 `last_delivery_error` 包含 `rate limited: ret=-2`：

**关键：必须用 `%USERPROFILE%\\.hermes\\gateway-service\\Hermes_Gateway.cmd`（全局），不能用项目级 `hermes.bat`，因为项目级 HERMES_HOME 缺少微信 accounts 配置。**

### 手动推送重试策略 (2026-06-02 验证, 2026-06-04 更新)

当需要手动分段推送长报告时：
1. **每段最大 2500 字符**（微信消息长度限制）
2. **最多连续发 3 条**，第 4 条前等待 2 分钟
3. **如果收到 ret=-2，立即停止重试** — 这是账户级限流，继续重试会延长限流时间
4. **等待 2-6 小时**后用 cron job 延迟推送，或直接查看报告文件
5. **绝对不要**在限流状态下每 15-60 秒重试 — 2026-06-04 实测：15s→30s→60s 递增等待全部失败，限流是 sticky 的
import os, json, subprocess, time

hermes_home = os.path.expanduser("~/.hermes")

# 1. 清理 stale context_token
ctx_file = os.path.join(hermes_home, "weixin", "accounts", "<account_id>@im.bot.context-tokens.json")
with open(ctx_file, "w") as f:
    json.dump({}, f)

# 2. 用全局 gateway-service 重启（不能用项目 hermes.bat，缺微信配置）
gateway_script = os.path.join(hermes_home, "gateway-service", "Hermes_Gateway.cmd")
subprocess.Popen(["cmd", "/c", "start", "Hermes Gateway", gateway_script],
                  shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

# 3. 等待 10s，检查 gateway_state.json 确认 weixin: connected
```

关键：必须用 `%USERPROFILE%\.hermes\gateway-service\Hermes_Gateway.cmd`（全局），不能用项目级 `hermes.bat`，因为项目级 HERMES_HOME 缺少微信 accounts 配置。

## 微信推送策略（2026-06-02 实测，2026-06-04 更新）

**铁律：合并为最少消息数，不要拆分发送。**

- iLink 账户级限流（ret=-2）：2026-06-04 实测，连续 4 条即触发（第1-3条成功，第4条失败），限流后 60 秒间隔重试仍失败，持续数小时
- **正确做法**：将报告压缩为 2-3 条长消息（每条 3000-4000 字符），最多连续发 3 条后等 2 分钟
- 如果限流了：**立即停止**，告知用户已发送部分和剩余部分，等 2-6 小时自动解除

## 输出

- 日报: `data/reports/Agent_Daily_Report_YYYY-MM-DD.md`
- 原始数据: `data/raw/YYYY-MM-DD.json`
- 评分数据: `data/scored/YYYY-MM-DD.json`
- 源状态: `data/source_status/YYYY-MM-DD.json`
- 运行日志: `logs/run.log`

## Agent Pipeline (v3.2 实现)

3 个 Agent 节点已实现，通过 config.yaml `agent_pipeline.enabled` 开关控制。

### Trust Decision 降级/升级机制

**关键发现（2026-06-05）**：Trust Agent 可以对项目进行降级（demote）或升级（promote），导致最终等级低于或高于评分对应的等级。
### 决策流程

1. **检查多源共振**：如果原因包含正面多源共振关键词（且无否定模式），则升级一级
2. **检查降级条件**：仅当原因包含特定关键词时才降级
3. **其他情况**：保持原级

**代码位置**：`scripts/agent_pipeline.py` → `apply_trust_decisions()` 函数

**降级逻辑**（仅对特定原因）：
```
原因包含 "bug修复" / "缺乏独立价值" 等 → 降一级
其他原因（如"无多源共振证据"）→ 保持原级
```

**升级逻辑**（多源共振）：
```
原因包含 "多源共振" / "cross-source verified" 等（且无否定模式）→ 升一级
```

**否定模式检测**（防止误升级）：
```python
negation_patterns = ["无多源", "无跨源", "no multi", "no cross", "缺乏多源", "lacks multi",
                   "无新增", "无.*共振", "缺乏.*共振", "无.*验证", "缺乏.*验证"]
```

**信任评分阈值**：
```
trust_score ≥ 60 → keep (保持原级)
trust_score ≥ 30 → demote (降一级，仅特定原因)
trust_score < 30 → drop (移除)
```

**降级映射**：
```
S → A
A → B
B → C
C → D
```

**升级映射**：
```
B → A
C → B
D → C
```

**实际案例**：
| 项目 | 评分 | 原始等级 | trust_score | 最终等级 | 原因 |
|------|------|----------|-------------|----------|------|
| mastra-ai/mastra | 78 | A | 50 | A | 星标数据缺失、无多源共振证据（不降级） |
| BigPizzaV3/CodexPlusPlus | 73 | A | 35 | A | Star增长异常(24h+941)、无描述（不降级） |
| pydantic/pydantic-ai | 68 | B | 58 | C | 评估的是Bug修复PR、缺乏独立价值（降级） |

**诊断要点**：
- 当用户报告"等级错误"时，检查 `trust_score` 和 `trust_reason` 字段
- `trust_score` 在 30-60 之间，但原因不包含特定降级关键词 → 不降级
- "无多源共振证据"不再导致降级（2026-06-05 修改）
- "Bug修复PR、缺乏独立价值"仍会导致降级
- `quality_flags: None` 不代表没有降级——降级由 Trust Agent 决定，不由 quality_flags 控制

详见 `references/trust-decision-mechanism.md`

### 节点概览

| Agent | 触发 | 有 LLM | 无 LLM | 参考 |
|-------|------|--------|--------|------|
| GitHub Trust Agent | score 后、select 前 | LLM 过滤+评分(0-100) | 跳过，保留原评分 | agents-radar |
| Item Enrichment Agent | select 后 | 中文摘要+工程价值 | 离线模板(已有字段) | ai-news-agent candidate→decision |
| Editor Agent | draft 生成后 | LLM 润色整篇报告 | 纯规则检查(去重/链接/格式) | ai-news-radar 无LLM模式 |

### 文件

| 文件 | 职责 |
|------|------|
| `scripts/agent_pipeline.py` | 管道控制器，调度 3 个 Agent + 多轮验证 |
| `scripts/agent_llm_client.py` | 统一 LLM 调用层 (OpenAI-compatible HTTP) |
| `scripts/agent_prompts.py` | 3 个 Agent 的 system/user prompt + 验证 prompt |

### 多轮验证 (v3.2)

每个 Agent 执行后自动验证：
```
Round 1: Agent 执行 → 输出结果
Round 2: 验证器检查 → 如有问题，带修正反馈重新执行
```
验证规则见 `scripts/agent_prompts.py` 中的 `*_VERIFY_SYSTEM` 常量。

### 用户偏好 (2026-06-04)

- **Enrichment 必须全部走 LLM**：`max_items: 0`（不限制），`batch_size: 1`（逐条最高质量）
- **金融新闻必须过滤**：美股异动、市值暴涨、IPO、私人信贷、桥水基金、Pimco 等，但不要用过于宽泛的词（如"收购"、"估值"）
- **增强器和 Skill 都要收录**：CodexPlusPlus（Agent 增强器）、ian-xiaohei-illustrations（插画 Skill）等，只要能增强 Agent 或是 Skill 就要收录
- **LLM 读 README 判断相关性**：替代关键词匹配，逐个判断最准确
- **用途与最佳实践不能是模板**：每条必须是 LLM 根据具体内容生成的，不能是同一句话

### batch_size=1 策略

**必须用 batch_size=1**（每个 item 独立一次 LLM 调用）。原因：
1. LLM 注意力有限：batch=5 时第 3-5 个 item 质量明显下降
2. 验证效率：单条失败只重跑 1 个，batch 失败重跑整批
3. 中文质量：单条有足够空间生成详细描述

每天 ~50 次 LLM 调用（12 item × 2 验证 + 1 editor × 2 验证）。

### 限制配置（2026-06-04 更新）

所有 Agent 的限制已解除：
- timeout_seconds: 0（无限制）
- Trust Agent max_items: 0（无限制）
- batch_size: 所有 Agent 均为 1
- max_input_chars: 30000（超出需分割输入）

详见 `AGENT_LIMITATIONS.md` 和 `LIMITATIONS.md`。

### SkillOpt 集成

SkillOpt 已集成用于优化 Agent 提示词。详见 `references/skillopt-integration.md`。

每天 ~84 次 LLM 调用（42 item × 2 验证 + 1 editor × 2 验证）。

### 中间产物 (data/intermediate/{date}/)

| 文件 | 来源 | 用途 |
|------|------|------|
| candidates.json | Phase 7a | 所有 scored items 的快照 |
| trust-decisions.json | Phase 7b | GitHub 信任评分决策 |
| enriched-decisions.json | Phase 7d | 中文摘要和工程价值 |
| draft.md | Phase 7e | 生成报告初稿 |
| final.md | Phase 7f | 最终报告 |

### 配置

```yaml
agent_pipeline:
  enabled: true           # false 则走原全脚本 pipeline
  intermediate_dir: data/intermediate
  agents:
    github_trust:
      enabled: true
      batch_size: 1       # 每次最多处理一个
      max_items: 0        # 无限制
  batch_size: 1       # 每次最多处理一个
      trust_threshold_keep: 60     # >= 60 keep
      trust_threshold_demote: 30   # 30-60 demote, < 30 drop
      max_items: 0        # 无限制
      timeout_seconds: 0  # 无限制
    item_enrichment:
      enabled: true
      max_items: 0        # 无限制
      batch_size: 1       # 每次最多处理一个
      timeout_seconds: 0  # 无限制
      max_retries: 0
      timeout_seconds: 0  # 无限制（P76：max_items=12导致30条走离线模板）
      max_items: 0         # 0=不限制，全部走LLM（P76修复）
    editor:
      enabled: true
      timeout_seconds: 0  # 无限制
      max_input_chars: 30000  # 超出需分割输入
      fallback_to_rules: true      # 无 LLM 时用纯规则
      timeout_seconds: 0  # 无限制
      max_input_chars: 30000  # 超出需分割输入
  llm:
    api_key_env: AGENT_PIPELINE_API_KEY
    base_url_env: AGENT_PIPELINE_BASE_URL
    default_model: mimo-v2.5-pro   # 小米 MiMo Token Plan
    temperature: 0.2
    max_retries: 3
    timeout_seconds: 0   # 无限制
```

### 降级策略

| Agent | 有 LLM | 无 LLM |
|-------|--------|--------|
| Trust | LLM 评估 trust_score | 跳过，保留原评分 |
| Enrichment | LLM 生成中文摘要 | 离线模板 (enrich_report_with_agent) |
| Editor | LLM 润色报告 | 纯规则 (去重+链接检查+格式) |

详见 `references/agent-architecture.md` 和 `references/competitor-analysis.md`。

| Agent | 验证规则 |
|-------|---------|
| Trust | decision 与 trust_score 一致、reason 有实质内容、无遗漏 repo |
| Enrichment | title_zh 是中文、不编造数据、engineering_value 不泛泛 |
| Editor | Source Status 表存在、不新增条目、不修改数值、链接完整 |

验证器用独立 system prompt，与 Agent 分离，避免自我确认偏差。

详见 `references/agent-architecture.md` 和 `references/competitor-analysis.md`。

## Obsidian 集成（2026-06-02）

obsidian-second-brain skill 已安装，vault 位于 `D:\ObsidianVault`。
日报可通过 obsidian-second-brain 的命令自动整理到 vault 的 daily/ 或 notes/ 目录。

## SkillOpt 调优

SkillOpt (Microsoft, ⭐4619) 可用于优化 agent_prompts.py 中的提示词。
详见 `references/skillopt-integration.md`。

关键注意：
- SkillOpt edit 格式：`op`/`content`/`target`（不是 `operation`/`new_text`/`old_text`）
- MiMo v2.5 Pro 对复杂英文 prompt 会返回空内容，必须用中文 prompt
- Python 模块名不能有连字符（`agent_daily_report` 不是 `agent-daily-report`）
- 必须预创建所有输出目录，否则训练中途崩溃

## References

- 实现位置：`D:/openclaw-hermes/agent-daily-report-skill/`
- 配置文件：`config.yaml`
- 提示词目录：`prompts/` — 9个Agent提示词的独立文件，详见 `references/prompts-extraction.md`
- SkillOpt集成：`references/skillopt-integration.md` — 用SkillOpt优化提示词的完整流程
- source_status 规范：`scripts/source_status.py`
- 采集器模式：各 `scripts/collect_*.py`
- **Timeout 配置：`references/timeout-configuration.md`** — timeout=0 导致的网络失败、限流、enrichment 问题及修复
- **Timeout 配置 Pitfall：`references/timeout-configuration-pitfall.md`** — 所有 timeout_seconds 位置清单、修复脚本、验证方法
- **Timeout 所有位置清单：`references/timeout-all-locations.md`** — 2026-06-05 实测确认的 9+ 处 timeout 位置及修复方法
- **GitHub 自动发现：`references/github-auto-discovery.md`** — 从 HackerNews/Reddit 等自动提取 GitHub 链接并添加到观察列表
- **SkillOpt 提示词优化：`references/skillopt-prompt-optimization.md`** — 使用 SkillOpt 优化提示词的工作流
- **实现模式：`references/implementation-patterns.md`** — safe_collect wrapper, RSS fallback, hash_diff, endpoint discovery, dual API
- **评分公式：`references/scoring-formulas.md`** — 唯一评分公式，不使用归一化
- **评分等级Bug：`references/scoring-level-assignment-bug.md`** — P82: score=60但level=C的不一致问题诊断（已解决：用户误判，实际等级正确）
- **评分验证模式：`references/scoring-verification-pattern.md`** — 用户报告"未推送/等级错误"时的验证步骤（先验证数据再诊断bug）
- **Trust Decision 降级机制：`references/trust-decision-mechanism.md`** — Trust Agent 降级逻辑、阈值、实际案例、诊断流程
- **日均增长计算：`references/daily-average-growth.md`** — 日均增长计算逻辑、保底B级机制、调试经验(P84)、阈值调优(P85)
- **Memory OS 集成：`references/memory-os-integration.md`** — 7层记忆架构、2026-06-05 实际集成状态（Qdrant+Redis+Icarus+memory_store.db 已部署）、Ground Truth 层级、未完成步骤
- **分类规则：`references/classification-rules.md`** — 内容实体优先
- **~~评分系统：`references/scoring-system.md`~~** — DEPRECATED，不得引用
- **Cost Signal 规则：`references/cost-signal-rules.md`** — 价格正则、单位标准化、禁止编造
- **成长门控修复：`references/growth-gate-fix.md`** — 2026-06-03 代码变更
- **成长门控归一化：`references/growth-gate-normalization.md`** — P74 快照间隔归一化修复
- **LLM Agent 相关性判断：`references/llm-agent-relevance-check.md`** — P75 逐个读 README 判断
- **长 Pipeline 运行：`references/long-pipeline-runner.md`** — run_pipeline.py 模式、Growth Gate 阈值调优、P65/P66 诊断
- **成长门控间隔Bug：`references/growth-gate-interval-bug.md`** — P74: star_delta_24h 未归一化到 24h，间隔 1.5h 的快照 delta 被严重低估
- **长时Pipeline运行：`references/long-running-pipeline.md`** — DETACHED_PROCESS + psutil
- **成长门控归一化：`references/growth-gate-normalization.md`** — delta_24h 归一化修复（interval<24h 时按比例换算）
- **Watchlist 去重：`references/watchlist-dedup-fix.md`** — 同一 repo 的 release/issue 事件与 watchlist 去重
- **报告结构更新：`references/report-structure-updates-2026-06-05.md`** — 待观察项目、更新信息、GitHub跟踪状态表
- **Enrichment 配置：`references/enrichment-config.md`** — batch_size/max_items 推荐值、金融过滤、SSL 错误处理
- **LLM 相关性判断：`references/llm-relevance-check.md`** — 用 LLM 读 README 判断 Agent 相关性（替代关键词匹配）
- **已知陷阱：`references/pitfalls.md`** — source_status 常量截断、execute_code 沙箱、--test import、HN 分类、discovery penalty
- **数据分析方法论：`references/data-analysis-methodology.md`** — 流水线追踪、评分验证、HN 分类验证、section quota 分析
- **GitHub 架构：`references/github-collector-architecture.md`** — 四池架构、Lifecycle、state 结构
- **竞品分析：`references/competitor-analysis.md`** — agents-radar / ai-news-agent / ai-news-radar 对比
- **Agent 架构：`references/agent-architecture.md`** — candidate→decision JSON 模式、3 个 Agent 节点设计
- **长 Pipeline 运行：`references/long-pipeline-runner.md`** — run_pipeline.py 模式、Growth Gate 阈值调优、P65/P66/P74/P75 诊断
- **Agent 实现：`references/agent-pipeline-implementation.md`** — v3.2 实现细节、配置、降级策略、评分标准
- **外部信源：`references/external-sources.md`** — 11 个子源的采集策略、API端点、字段映射
- **MCP Registry API：`references/mcp-registry-api.md`** — Official/Glama/Smithery 端点、字段结构、缺失 star 数据的解决方案
- **诊断方法论：`references/diagnostic-methodology.md`** — 日报诊断流程、分类bug排查、HN重新评分、链接反查
- **HN 采集逻辑：`references/hn-collection-logic.md`** — Firebase/Algolia 双源、72h 过滤、字段映射、重新评分
- **2026-06-02 诊断：`references/source-distribution-2026-06-02.md`** — 各源占比、Displayed=0 根因、HN 重新评分结果
- **提示词管理：`references/prompts-management.md`** — 9个Agent提示词文件位置、SkillOpt优化流程
- **Agent 限制条件：`references/agent-limitations.md`** — 执行时间、Trust/Enrichment/Editor 各 Agent 的具体限制
- **SkillOpt 优化：`references/skillopt-optimization.md`** — 使用 SkillOpt 优化提示词的完整工作流
- **Hermes 维护：`AGENTS.md`** — 自主诊断/修复操作/命令参考
- **源分布诊断：`references/source-distribution-diagnostic.md`** — 各源占比分析、Displayed=0 排查、已知分类/quota 问题模式
- **SkillOpt 提示词优化：`references/skillopt-prompt-optimization.md`** — 使用 SkillOpt 优化 agent prompts 的完整工作流
- **快照时间间隔：`references/snapshot-time-interval.md`** — 快照间隔约24.6小时，star_delta_24h 基于此计算
- **Datetime 时区Bug：`references/datetime-timezone-bug.md`** — P86: naive vs aware datetime 导致 GitHub 整源失败的诊断与修复
