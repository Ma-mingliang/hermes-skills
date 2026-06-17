# Shared Patterns — Cross-System Reference

Patterns common to both Agent Daily Report and AI Daily Digest.

## 1. Multi-Source Collection Pattern

### safe_collect Wrapper
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
Never let one collector crash the pipeline.

### Fallback Strategies
| Strategy | Use When | Examples |
|----------|----------|---------|
| RSS-first + API optional | Source has RSS + API | Reddit, Product Hunt |
| Hash-diff change detection | Monitoring doc pages | Model docs, Framework docs |
| RSS endpoint auto-discovery | RSS URL may change | NodeSeek |

## 2. Classification Rules

**Content-entity-first, never source-based:**
- HN post about MCP → `MCP` (not `Community`)
- Product Hunt AI IDE → `Coding Agent` (not `Product`)
- Reddit workflow tool → `Tool / Plugin / Connector`

**Negative keywords** (filter non-AI content):
- English: real estate agent, travel agent, insurance agent, sales agent, hiring, job, recruiting
- Chinese: 美股异动, 市值暴涨, IPO出现波折, 私人信贷, 桥水基金, 高盛首席
- Don't use overly broad terms (e.g., "收购" kills valuable items like "英伟达收购 Kumo AI")

## 3. Scoring Patterns

### No Normalization
Each item scored independently. No cross-item normalization, no min-max scaling.

### Grade Bands
| Grade | Score | Action |
|-------|-------|--------|
| S | 85-100 | Must push |
| A | 70-84 | Key attention |
| B | 55-69 | Normal inclusion |
| C | 40-54 | Backup |
| D | 0-39 | Ignore |

### Community Sources
NOT automatically low-scored. Score by content topic: MCP/Coding Agent/Workflow/Model API discussions get high relevance + utility.

## 4. Deduplication

### Same Source
- URL exact match → keep most complete
- Title similarity ≥ 0.90 → merge

### Cross Source
- Title similarity ≥ 0.85 + entity match → merge as `related_items`
- Score boost: +3 per related source, max +10

## 5. WeChat Delivery

### Rate Limiting (ret=-2)
- iLink account-level throttle after 4+ consecutive messages
- Recovery: 2-6 hours (auto-unthrottle)
- **Stop immediately** on ret=-2, do NOT retry

### Strategy
| Rule | Value |
|------|-------|
| Max message size | 3500 chars safe, 4000 chars aggressive |
| Split at | `##` headings (not mid-sentence) |
| Sequential limit | Max 3 messages, wait 2 min |
| Label format | `[1/N]...[N/N]`, last: `✅ 推送完毕 (N/N)` |
| Read first | Always `read_file` actual report, never from memory |

### Context Token Refresh
When WeChat shows "暂时无法连接":
1. Clear stale token: `~/.hermes/weixin/accounts/<id>@im.bot.context-tokens.json` → `{}`
2. Restart with GLOBAL gateway: `%USERPROFILE%\.hermes\gateway-service\Hermes_Gateway.cmd`
3. NOT project hermes.bat (lacks WeChat config)

## 6. Windows/WSL Workarounds

### File Writing
- `write_file` tool fails silently (WSL relay)
- Use `execute_code + open(path, 'w').write(content)` instead
- Post-write verification MANDATORY: `assert os.path.exists(path)`

### Long-Running Pipelines
- `execute_code` has 300s hard timeout → kills subprocess
- Use `run_pipeline.py --background` (DETACHED_PROCESS)
- Or `subprocess.Popen(..., creationflags=DETACHED_PROCESS)`

### Path Access
- `read_file` can't access D: drive paths
- Use `execute_code + Python open()` for Windows paths

### HTTP Requests (No Shell)
```python
import urllib.request, json
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode())
```
Works for: HN Algolia API, GitHub REST API. Does NOT work for SPA sites (need browser).

## 7. Configuration Patterns

### YAML Config Editing
- `yaml.dump()` loses comments and custom formatting
- Use `execute_code` + line-by-line text replacement instead

### Environment Variables
- `.env` may have `GITHUB_PERSONAL_ACCESS_TOKEN` while code expects `GITHUB_TOKEN`
- Fallback chain: check both names

### Timeout Settings
- `timeout_seconds: 0` causes "Attempted to set connect timeout to 0" error
- Minimum 60s for all network timeouts
- Check ALL config sections (10+ locations in agent-daily-report)

## 8. Data Verification

### Subagent Fabrication
delegate_task subagents may return fabricated data (fake GitHub repos, invented star counts).
- GitHub project → verify URL exists (404 check)
- Star count → GitHub API confirms
- Model version → browser visit ranking site

### SPA Sites
SPA sites (artificialanalysis.ai, lmarena.ai, openrouter.ai) return static skeleton via web_fetch.
- Must use browser for full render
- If browser unavailable: skip source, label "今日未能获取"
- NEVER use old web_fetch data to "correct" user-provided new information
