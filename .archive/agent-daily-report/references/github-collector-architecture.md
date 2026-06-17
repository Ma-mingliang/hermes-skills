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
