# Report Structure Updates (2026-06-05)

## New Sections Added

### 1. GitHub 跟踪状态表

**Before**: "详见 Source Status 表的 lifecycle_summary" (no actual data)

**After**: Full markdown table with Top 20 tracked repos

```markdown
### GitHub 跟踪状态

| 项目 | Stars | 24h增长 | 状态 | 分类 | 最近更新 |
|------|------:|--------:|------|------|----------|
| browser-use/browser-use | 97,202 | +168 | watchlist | Tool / Plugin / Connector | 2026-06-01 |
| ... | ... | ... | ... | ... | ... |

> 状态说明：watchlist=持续跟踪, probation_7d=7天观察期, archived=已归档
```

**Data source**: `state/github_repo_state.json` → repos → sorted by stars descending → Top 20

### 2. 待观察项目 (Pending Observation)

**Purpose**: Track GitHub projects mentioned in community sources (HN/Reddit/LinuxDo) before recommending.

**Trigger**: Any GitHub link found in community/news content.

**Workflow**:
1. Extract GitHub repo from mention
2. Get current stars via GitHub API
3. Add to `state/github_repo_state.json` with tracking_status=candidate_30d
4. Set next_check_date = tomorrow
5. Add to report's "待观察项目" section

**Format**:
```markdown
### 待观察项目

> 从社区/新闻中发现的GitHub项目，需观察24h star变化后再决定是否推荐。

| 项目 | 来源 | Stars | 发现日期 | 状态 | 说明 |
|------|------|------:|----------|------|------|
| [getpaseo/paseo](https://github.com/getpaseo/paseo) | HackerNews | 7,771 | 2026-06-05 | 待观察 | Coding agents from your phone, desktop and CLI |

> 观察规则：发现后记录初始star数，24h后再次检查，若增长≥50则纳入推荐。
```

**Rule**: 24h后复查，增长≥50则纳入推荐。

### 3. 更新信息 (Update Information)

**Purpose**: Track version updates, important PRs, architecture changes for already-tracked projects.

**Trigger**: Watch List project has new release, important PR, or architecture change.

**Format**:
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

**Position**: After Watch List changes, before 待观察项目.

## Updated Section Order

1. 今日关键事件
2. GitHub 项目动态
   - GitHub 跟踪状态表 (Top 20)
   - 今日实时爆发项目
   - 今日新发现项目
   - 每日异常增长项目
   - Watch List 重要变化
   - **更新信息** (NEW)
   - **待观察项目** (NEW)
3. Agent / Coding Agent 动态
4. MCP 生态
5. ...
