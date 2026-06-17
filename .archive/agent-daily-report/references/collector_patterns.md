# Collector Patterns (v3.1)

## make_source_status Never Takes items

Signature: source, enabled, status, auth, strategy_used, raw_count, matched_count, selected_count, errors, warnings.

**Does NOT accept `items`**. Items returned as first tuple element: `return items, status_dict`.

Bug: `return matched, make_source_status(..., items=matched)` — delete `items=matched`.

## Collector --test .env Loading

Every `__main__` block must load .env before running:
```python
from pathlib import Path as _Path
for _ep in [_Path.home() / ".hermes" / ".env", _Path(__file__).parent.parent / ".env"]:
    if _ep.exists():
        with open(_ep, "r", encoding="utf-8") as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    if _k.strip() not in os.environ:
                        os.environ[_k.strip()] = _v.strip()
```

## selected_items Pipeline

main.py must filter before generate_report:
```python
selected_items = [i for i in scored if i.get("importance_level") in ("S","A","B")]
report = generate_report(selected_items, config, ...)
```

## HN final_age_filter

Firebase stories may be older than 72h. After dedup, before keyword filter:
```python
_cutoff = int(time.time()) - 72 * 3600
unique = [s for s in unique if int(s.get("time", 0)) >= _cutoff or s.get("_source") == "algolia"]
```

## V2EX _is_relevant Full Match

Must match title+content+node+url, not just title. Node via `topic.get("node",{}).get("name","")`.

## Clear __pycache__ After Batch Edits

```python
import shutil
for d in ["__pycache__", os.path.join("scripts", "__pycache__")]:
    if os.path.exists(d): shutil.rmtree(d)
```

## External Digest Collection

Collect digests from peer projects (agents-radar, ai-news-agent, ai-news-radar):
- GitHub Issues API: `/repos/{owner}/{repo}/issues?labels=...&state=open`
- GitHub Pages JSON: `https://{user}.github.io/{repo}/data/*.json`
- Parse issue body for linked stories
- Only take recent issues (last 3 days)

## Source Health Trend Tracking

Record daily source_status to `state/source_health_history.json`:
```python
from source_health import record_daily_health
record_daily_health(statuses)
```
Track: success_rate, failure_rate, signal_density, streak, last_success, last_failure.

## RSS-first + API optional (Reddit, PH)

Missing auth + successful RSS = success, not skip.

## token_optional (GitHub)

Missing token = api_limited, not skipped_missing_auth.

## hash_diff (Model/Framework Docs)

First run = save baseline, status=checked_no_change.

## Dual API (HN)

Firebase + Algolia merge → dedup → keyword filter → 72h age filter.

## GitHub --test Lightweight Mode

Don't call `collect_github(config)` (runs all 4 pools, 100+ API calls). Instead:
1. Load .env
2. Create GitHubClient
3. Check auth_mode
4. Fetch ONE watch repo as sample
5. Return JSON
