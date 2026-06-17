# Agent Daily Report — Full Workflow Reference

Source skill: `agent-daily-report` (archived to `.archive/`)
Project location: `D:/openclaw-hermes/agent-daily-report-skill/`

## Run Commands

```bash
cd D:/openclaw-hermes/agent-daily-report-skill
python run_pipeline.py --background  # Run pipeline (independent process, no timeout)
python run_pipeline.py --status      # Check status
python run_pipeline.py --log         # View logs
python run_pipeline.py --kill        # Kill running process
```

**Iron rule**: Never use `execute_code + subprocess.run` for full pipeline (300s timeout kills it). Use `run_pipeline.py --background`.

## Sources (11)

| Source | Weight | Strategy | Auth |
|--------|--------|----------|------|
| GitHub | 35% | api (4-pool architecture) | token_optional |
| Hacker News | 15% | Firebase + Algolia (72h limit) | none |
| LinuxDo | 10% | RSS → JSON → HTML fallback | none |
| Model Docs | 10% | hash_diff (with baseline) | none |
| Reddit | 8% | RSS first + OAuth optional | OAuth optional |
| V2EX | 6% | API | none |
| Product Hunt | 5% | RSS first + GraphQL optional | token optional |
| NodeSeek | 4% | RSS only (rss.nodeseek.com) | none |
| Hugging Face | 4% | API | HF_TOKEN optional |
| Framework Docs | 3% | hash_diff | none |
| External Digests | 3% | GitHub Issues/Pages | token_optional |

## GitHub 4-Pool Architecture

| Pool | Purpose | Display Rule |
|------|---------|--------------|
| Watch Pool | Fixed core projects (10) | Only show changes |
| Discovery Pool | GitHub Search new projects | Only spike/strong-relevance after lifecycle filter |
| Growth Pool | Historical snapshot growth | Star delta + realtime spike |
| Event Pool | Release/issue/PR events | Important events only |

### Growth Gate Rules

| Stars | Reportable Condition | Grade |
|-------|---------------------|-------|
| < 100 | Not eligible | — |
| < 1k | delta >= 200 | S≥500 / A≥300 / B≥200 |
| 1k-5k | delta >= 100 | S≥500 / A≥300 / B≥100 |
| ≥5k | daily_rate >= 1% | B / A≥10% |

### Lifecycle
discovered → spike_hold → probation_7d → candidate_30d → watchlist → archived/dropped

## Scoring (5 dimensions, 100 points)

Total = relevance(30) + popularity(20) + freshness(15) + growth(15) + utility(20)

- **Daily avg growth boost**: `daily_avg ≥ 20 stars/day` → min B-level (55 points)
- **Quality flag cap**: Discovery Pool candidates capped at 54 points (C-level)
- **Trust decision**: Trust Agent can demote/promote based on multi-source resonance

## Agent Pipeline (3 nodes)

1. **Trust Agent** (post-score, pre-select): LLM evaluates trust_score (0-100)
   - ≥60: keep | 30-60: demote (specific reasons only) | <30: drop
   - Demotion keywords: "bug修复", "缺乏独立价值"
   - Promotion keywords: "多源共振", "cross-source verified"
2. **Enrichment Agent** (post-select): Chinese summary + engineering value
   - Must use batch_size=1, max_items=0 (all items, one-by-one)
3. **Editor Agent** (post-draft): LLM polishes full report
   - Fallback: rule-based checks (dedup, link validation, format)

## Cron

```
Job: 57e936ce4084
Schedule: 0 6 * * *
Delivery: weixin:o9cq803R0Y4HMdI1VnJApgMyYGbo@im.wechat
Skill: agent-daily-report
Workdir: D:/openclaw-hermes/agent-daily-report-skill
```

## Key Pitfalls (Top 20)

| ID | Issue | Fix |
|----|-------|-----|
| P28 | `__pycache__` stale bytecode | Clear ALL dirs after .py edits |
| P46 | Pipeline timeout | Use run_pipeline.py --background |
| P50 | WeChat segmented push rate limit | Max 3 consecutive, wait 2min |
| P65 | Growth gate too strict | 1k-5k: delta≥100, <1k: delta≥200 |
| P72 | timeout_seconds=0 breaks RSS | Set minimum 60s everywhere |
| P74 | star_delta_24h not normalized | delta_24h = round(raw / hours * 24) when <23h |
| P75 | weak_agent_signal kills Skills | LLM README check as fallback |
| P80 | Skill/Agent projects filtered out | _is_skill_or_agent_project() bypass |
| P84 | Missing import os → silent failure | Module-top imports, no bare except |
| P86 | Naive vs aware datetime crash | Force timezone-aware in _parse_snapshot_time |
| P87 | "report" ambiguity | "report" → agent-daily-report unless "AI新闻" |

For complete pitfalls list, see archived skill at `.archive/agent-daily-report/`.
