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

## Pattern: Collector --test .env Loading

Collectors run standalone must load .env themselves. Insert at the top of `if _args.test:` block:

```python
from pathlib import Path as _Path
for _ep in [_Path.home() / ".hermes" / ".env", _Path(__file__).parent.parent / ".env"]:
    if _ep.exists():
        with open(_ep, "r", encoding="utf-8") as _ef:
            for _eline in _ef:
                _eline = _eline.strip()
                if _eline and not _eline.startswith("#") and "=" in _eline:
                    _ek, _ev = _eline.split("=", 1)
                    if _ek.strip() not in os.environ:
                        os.environ[_ek.strip()] = _ev.strip()
```

This ensures GITHUB_TOKEN, REDDIT_CLIENT_ID, etc. are available when testing collectors independently.

## Pattern: GitHub --test Lightweight Mode

GitHub --test should NOT call `collect_github(config)` (runs all 4 pools, 100+ API calls). Instead:
1. Load .env
2. Create GitHubClient
3. Check auth_mode (api vs api_limited)
4. Fetch ONE watch repo as sample
5. Return JSON

This keeps --test under 10 seconds instead of timing out at 120+.

## Pattern: Collector Skip Status Sentinel

When a sub-collector needs to return a "skipped" status but the parent collect() loop expects a plain list, use a `_pending_skip` sentinel attribute:

```python
class ExternalDigestCollector:
    def __init__(self, ...):
        self._pending_skip = None

    def collect(self):
        for src_cfg in self.sources:
            self._pending_skip = None
            items = self._dispatch(src_cfg)

            # Check sentinel BEFORE processing items
            if self._pending_skip:
                skip_status = self._pending_skip
                self._pending_skip = None
                sub_statuses.append(skip_status)
                continue

            # Normal processing...

    def _dispatch_mcp_registry(self, src_cfg):
        if name == "smithery":
            result = self._collect_smithery(src_cfg)
            if isinstance(result, tuple):
                items, skip_status = result
                if skip_status:
                    skip_status["name"] = name  # MUST include name
                    self._pending_skip = skip_status
                return items
            return result

    def _collect_smithery(self, src_cfg) -> Tuple[List[Dict], Optional[Dict]]:
        if not api_key:
            _, skip_status = skipped_requires_api_key(name, "SMITHERY_API_KEY")
            return [], skip_status
        # ... normal collection
```

Key rules:
- Skip status dict MUST have "name" field (source_status helpers use "source" not "name")
- Reset `_pending_skip = None` at the start of each iteration
- Only check sentinel AFTER _dispatch returns
- This pattern avoids changing the collect() return type (still Tuple[List, Dict])

## Pattern: MCP Registry Collection

Multiple MCP registry sites exist with different API shapes. Pattern for collecting:

1. **Official MCP Registry** (`registry.modelcontextprotocol.io`):
   - `/v0.1/servers?limit=100` with cursor pagination
   - Supports `updated_since` for incremental fetch
   - Fallback: `/v0/servers` if v0.1 fails

2. **Glama** (`glama.ai`):
   - `/api/mcp/v1/servers` — public, no auth
   - Response may be list or dict with servers/items/data/results keys

3. **Smithery** (`api.smithery.ai`):
   - `/servers` with pagination (page, pageSize)
   - Requires `SMITHERY_API_KEY` env var
   - Return skipped_requires_api_key when key missing (not failed)

4. **mcp.so**: No stable public JSON API → `enabled: false`

Common field mapping:
```python
title = entry.get("displayName") or entry.get("name") or ""
desc = entry.get("description") or ""
url = entry.get("webpage_url") or entry.get("repository_url") or entry.get("url") or ""
repo = entry.get("repository", {}).get("url") if isinstance(entry.get("repository"), dict) else ""
```

All MCP registry items get `source_type: "mcp_server"` and `primary_category: "MCP"`.

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
