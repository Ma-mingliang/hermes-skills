# Agent Daily Report × SkillOpt Integration — Pitfalls & Fixes

## Timeout Configuration Issue (2026-06-04)

**Problem**: When `timeout_seconds: 0` is set in config.yaml, the LLM client AND all RSS/HTTP collectors fail with:
```
Attempted to set connect timeout to 0, but the timeout cannot be set to a value less than or equal to 0.
```

**CRITICAL**: `timeout_seconds: 0` exists in MULTIPLE config sections. Fixing only one is not enough!

**All locations where timeout=0 must be fixed**:
```yaml
# 1. Agent pipeline LLM
agent_pipeline:
  llm:
    timeout_seconds: 0  # ← FIX

# 2. Agent pipeline agents
agent_pipeline:
  agents:
    github_trust:
      timeout_seconds: 0  # ← FIX
    item_enrichment:
      timeout_seconds: 0  # ← FIX
    editor:
      timeout_seconds: 0  # ← FIX

# 3. Source verification
agent_pipeline:
  source_verification:
    timeout_seconds: 0  # ← FIX

# 4. Developer communities
developer_communities:
  linuxdo:
    request:
      timeout_seconds: 0  # ← FIX
  nodeseek:
    request:
      timeout_seconds: 0  # ← FIX

# 5. Other sources
hackernews:
  request:
    timeout_seconds: 0  # ← FIX
reddit:
  request:
    timeout_seconds: 0  # ← FIX
producthunt:
  request:
    timeout_seconds: 0  # ← FIX
rss_feeds:
  request:
    timeout_seconds: 0  # ← FIX
```

**Fix ALL at once** with this Python script:
```python
import yaml

config_path = "config.yaml"
with open(config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

def fix_timeouts(obj, path=""):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'timeout_seconds' and value == 0:
                obj[key] = 60  # or 300 for LLM calls
                print(f"Fixed {path}.{key}: 0 -> 60")
            elif isinstance(value, dict):
                fix_timeouts(value, f"{path}.{key}")
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        fix_timeouts(item, f"{path}.{key}[{i}]")

fix_timeouts(config)

with open(config_path, "w", encoding="utf-8") as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
```

**Root Cause**: `agent_llm_client.py` passes timeout directly to requests library:
```python
self.timeout = int(llm_config.get("timeout_seconds", 120))
# When timeout=0, requests raises ValueError
```

**Fix**: Add minimum timeout in `agent_llm_client.py`:
```python
self.timeout = max(30, int(llm_config.get("timeout_seconds", 120)))  # Minimum 30 seconds
```

**Alternative**: Set environment variables before running:
```bash
export AGENT_PIPELINE_TIMEOUT=300
export AGENT_PIPELINE_CONNECT_TIMEOUT=300
```

**Symptom**: When timeout=0 affects RSS collectors, ALL these sources fail:
- LinuxDo: `failed_network, raw=0`
- NodeSeek: `failed_network, raw=0`
- HackerNews: `failed_network, raw=0`
- Reddit: `failed_network, raw=0`
- ProductHunt: `failed_network, raw=0`
- RSS Feeds: `failed_network, raw=0`

GitHub and External Digests still work because they use different HTTP clients.

## Rate Limiting (429) During Enrichment

**Problem**: MiMo v2.5 Pro Token Plan has rate limits. When processing 40+ items, batch processing hits 429 errors.

**Symptoms**:
```
LLM 429 rate limited, waiting 5s
Enrichment agent batch 26 failed: LLM call failed after 1 attempts: None, using offline
```

**Fix**: 
1. Set `batch_size: 1` in config.yaml (already done)
2. Add exponential backoff in `agent_llm_client.py`:
```python
if response.status_code == 429:
    wait_time = min(30, 5 * (2 ** attempt))  # Exponential backoff, max 30s
    time.sleep(wait_time)
    continue
```

**Note**: Rate limiting is expected behavior. The system handles it with retries. Final report will still be generated, just takes longer.

## Editor Segmented Mode Skipped

**Problem**: When report has too many segments (>30), editor falls back to rules:
```
Editor segmented mode skipped: editable segments 39 exceed segment_max_segments=30; using rules fallback
```

**Fix**: Increase `segment_max_segments` in config.yaml:
```yaml
agent_pipeline:
  agents:
    editor:
      segment_max_segments: 50  # Increase from 30
```

## Network Failures for Multiple Sources

**Problem**: LinuxDo, NodeSeek, HackerNews, Reddit, ProductHunt, RSS feeds all fail with network errors.

**Root Cause**: Timeout=0 causes immediate failure for all network requests.

**Fix**: 
1. Fix timeout issue (see above)
2. Check network connectivity
3. Verify RSS feed URLs are accessible

## Enrichment Not Producing Final Version

**Problem**: Enrichment runs but no `.final.md` file is generated.

**Root Cause**: 
1. Rate limiting causes some batches to fail
2. Failed batches use offline fallback (no enrichment)
3. Editor falls back to rules mode

**Fix**:
1. Fix timeout issue
2. Reduce batch_size to 1
3. Add retry logic for failed batches
4. Monitor enrichment progress in logs

## Key Configuration Settings

```yaml
# config.yaml - Recommended settings for stable operation
agent_pipeline:
  llm:
    timeout_seconds: 300  # NOT 0!
    max_retries: 3
    temperature: 0.2
  agents:
    github_trust:
      batch_size: 1
    item_enrichment:
      batch_size: 1
      max_retries: 3
    editor:
      segment_max_segments: 50
      fallback_to_rules: true
```

## Debugging Tips

1. **Check logs**: `tail -f logs/run.log`
2. **Monitor enrichment**: Look for "Enrichment agent batch N: 1 items" messages
3. **Check rate limiting**: Look for "429 rate limited" messages
4. **Verify timeout**: Look for "Attempted to set connect timeout to 0" errors
5. **Check final version**: Look for "Agent pipeline: N items selected" at the end
