---
name: daily-news-report
description: "Daily news aggregation system architecture — multi-source collection, classification, scoring, quality gates, and WeChat delivery. Covers both Agent Engineering Intelligence (agent-daily-report) and General AI News Digest (ai-daily-digest) workflows. Use when building, maintaining, or troubleshooting any daily news/report system."
version: "1.0.0"
tags: ["news", "daily-report", "data-collection", "classification", "scoring", "wechat", "quality-gates"]
---

# Daily News Report System

Class-level patterns for building daily news aggregation systems. Covers the full pipeline: multi-source collection → classification → scoring → quality check → delivery.

## When to Use

- Building or maintaining a daily news/report system
- User asks about "日报", "daily report", "news digest", "news aggregation"
- Troubleshooting data collection, classification, scoring, or delivery issues
- Extending an existing report system with new sources

## Two Production Implementations

| System | Audience | Sources | Complexity | Trigger |
|--------|----------|---------|------------|---------|
| **Agent Daily Report** | Agent developers | 11 sources, 4-pool GitHub, 3 Agent nodes | High (87 pitfalls) | "agent日报", "report", "agent情报" |
| **AI Daily Digest** | General AI readers | HN + GitHub + 36氪 + model sites | Medium (80+ pitfalls) | "AI日报", "AI news digest", "AI月报" |

**Routing rule**: When user says "日报"/"report" without specifying "AI新闻", default to Agent Daily Report.

## Shared Architecture

### Pipeline Stages

```
1. Data Collection     → Multi-source collectors with fallback strategies
2. Normalization       → Unified schema, deduplication, negative keyword filtering
3. Classification      → Content-entity-first categorization (not source-based)
4. Scoring/Ranking     → Multi-dimensional scoring (relevance, popularity, freshness, growth, utility)
5. Quality Gates       → Empty title/URL, low-signal posts, source quota limits
6. Report Generation   → Section-quota layout, source status table
7. Agent Pipeline      → Trust → Enrichment → Editor (optional LLM nodes)
8. Delivery            → WeChat segmented push, cron scheduling
```

### Unified Source Status

Every collector returns `(items, source_status)` tuple. 12 status enums:

| Status | Meaning |
|--------|---------|
| `success` | Data collected and keywords matched |
| `success_no_match` | Data collected but no keyword match |
| `checked_no_change` | Page unchanged (hash-diff) |
| `skipped_disabled` | Source disabled in config |
| `skipped_missing_auth` | Required env vars missing |
| `skipped_no_stable_api` | No stable public API |
| `skipped_requires_api_key` | Needs API key but not configured |
| `failed_network` | Connection/timeout/HTTP 5xx |
| `failed_parse` | Response unparseable |
| `failed_auth` | Auth rejected (401/403) |
| `failed_rate_limited` | HTTP 429 |

**Critical**: `skipped_missing_auth` is ONLY for sources with no fallback. If RSS exists, return `success` or `success_no_match` regardless of auth.

### Classification: Content-Entity-First

**Never** classify by source (e.g., "from HN → Community"). Classify by what the content IS:
- HN post about MCP → `MCP` category (not `Community`)
- Product Hunt AI IDE → `Coding Agent` (not `Product`)
- Reddit discussion of workflow tool → `Tool / Plugin / Connector`

Priority: MCP > Agent Framework > Coding Agent > Tool > Workflow > Skill > Research > Product > Community

### Scoring Formula

Total = relevance(30) + popularity(20) + freshness(15) + growth(15) + utility(20)

- No normalization — each item scored independently
- Grade bands: S(85-100), A(70-84), B(55-69), C(40-54), D(0-39)
- Community sources NOT penalized — score by content topic, not source

### Quality Gates

| Gate | Rule |
|------|------|
| Empty fields | title/URL/summary empty → filter out |
| Low signal | "求推荐"/"水一贴"/"闲聊"/"招聘" → drop |
| Source quota | Single source ≤ 45% of displayed items |
| Category quota | Single category ≤ 35% |
| Section quota | Per-section target/max counts |

### Cross-Source Deduplication

- **Same source**: URL exact match + title similarity ≥ 0.90 → keep most complete
- **Cross source**: title similarity ≥ 0.85 + entity match → merge as `related_items`, +3 score per source (max +10)

### WeChat Delivery

**Iron rule**: Merge into fewest messages. iLink rate limiting (ret=-2) triggers after 4+ consecutive messages.

| Strategy | Details |
|----------|---------|
| Max message size | 3500 chars (safe), 4000 chars (aggressive) |
| Split boundaries | At `##` headings, not mid-sentence |
| Sequential limit | Max 3 messages, then wait 2 minutes |
| Rate limit response | Stop immediately on ret=-2, wait 2-6 hours |
| Cron delivery | Use `final response` auto-delivery |

### Report Layout

Reports use section-quota layout, not flat sorted list:

| Section | Target | Max |
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

### Agent Pipeline (Optional LLM Nodes)

3 nodes with multi-round verification:

| Node | Purpose | No-LLM fallback |
|------|---------|-----------------|
| Trust Agent | Score credibility (0-100), apply trust decisions | Skip, keep original score |
| Enrichment Agent | Chinese summary + engineering value | Offline template |
| Editor Agent | Polish full report | Rule-based checks only |

**batch_size=1** for all agents — batch > 1 causes quality degradation (attention spread).

## Common Pitfalls (Cross-System)

| Pitfall | Applies to | Fix |
|---------|-----------|-----|
| Classify by source instead of content | Both | Content-entity-first classification |
| Single source dominates section | Both | Section quota with source allocation |
| Cross-source duplicates not merged | Both | Entity match + title similarity ≥ 0.85 |
| WeChat rate limiting on segmented push | Both | Max 3 consecutive, wait 2min, stop on ret=-2 |
| `timeout_seconds: 0` causes network failure | Both | Minimum 60s for all network timeouts |
| `__pycache__` stale bytecode after edits | Both | Clear ALL `__pycache__` dirs, not just scripts/ |
| YAML dump loses comments | Both | Use `execute_code` + line-by-line text replacement |
| execute_code 300s timeout kills subprocess | Both | Use `run_pipeline.py --background` for long jobs |
| `write_file` silently fails (WSL relay) | Both | Use `execute_code` + Python `open()` |
| read_file can't access D: drive | Both | Use `execute_code` + Python `os.path.exists()` + `open()` |
| Daily avg growth threshold too low | Agent Report | `daily_avg >= 20 stars/day` for B-level boost |
| star_delta_24h not normalized | Agent Report | `delta_24h = round(delta_raw / interval_hours * 24)` when < 23h |
| Subagent data fabrication | Both | Verify GitHub URLs, stars, model versions before writing |

## Implementation-Specific Details

### Agent Daily Report (Full Reference)

**Location**: `D:/openclaw-hermes/agent-daily-report-skill/`
**Architecture**: 11 collectors + 3 Agent nodes + 16 external sub-sources
**GitHub Intelligence**: 4-pool architecture (Watch/Discovery/Growth/Event)
**Scoring**: 5-dimension, 100-point scale with quality flag caps

For complete source list, GitHub growth gate rules, lifecycle management, and all 87 pitfalls, load the full reference:
- `references/agent-daily-report-workflow.md` — Complete workflow with all sources, scoring formulas, and pitfalls

### AI Daily Digest (Full Reference)

**Location**: `C:/Users/lenovo_mml/.hermes/skills/news/ai-daily-digest/`
**Architecture**: Script + Agent collaboration, 8-step workflow
**Classification**: 6-category system with decision tree
**Monthly digest**: Aggregates daily reports into 5-section monthly report

For complete checklist, classification decision tree, report template, and all pitfalls, load the full reference:
- `references/ai-daily-digest-workflow.md` — Complete 8-step workflow with checklists and templates

## References

- `references/shared-patterns.md` — Cross-system patterns: source_status, classification, scoring, delivery
- `references/agent-daily-report-workflow.md` — Full Agent Daily Report workflow and pitfalls
- `references/ai-daily-digest-workflow.md` — Full AI Daily Digest workflow and checklists
