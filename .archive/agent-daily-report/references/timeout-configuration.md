# Timeout Configuration Issues (2026-06-04)

## Problem

When `timeout_seconds: 0` is set in config.yaml, the LLM client fails with:
```
Attempted to set connect timeout to 0, but the timeout cannot be set to a value less than or equal to 0.
```

This affects:
- Trust Agent
- Enrichment Agent  
- Editor Agent
- RSS Feeds
- External Digests

## Root Cause

`agent_llm_client.py` passes timeout directly to requests library:
```python
self.timeout = int(llm_config.get("timeout_seconds", 120))
# When timeout=0, requests raises ValueError
```

## Fix

### Option 1: Fix in agent_llm_client.py (Recommended)

```python
# In __init__ method
self.timeout = max(30, int(llm_config.get("timeout_seconds", 120)))  # Minimum 30 seconds
```

### Option 2: Set environment variables

```bash
export AGENT_PIPELINE_TIMEOUT=300
export AGENT_PIPELINE_CONNECT_TIMEOUT=300
```

### Option 3: Update config.yaml

```yaml
agent_pipeline:
  llm:
    timeout_seconds: 300  # NOT 0!
```

## Rate Limiting (429)

MiMo v2.5 Pro Token Plan has rate limits. When processing 40+ items, batch processing hits 429 errors.

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

## Editor Segmented Mode Skipped

When report has too many segments (>30), editor falls back to rules:
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

LinuxDo, NodeSeek, HackerNews, Reddit, ProductHunt, RSS feeds all fail with network errors.

**Root Cause**: Timeout=0 causes immediate failure for all network requests.

**Fix**:
1. Fix timeout issue (see above)
2. Check network connectivity
3. Verify RSS feed URLs are accessible

## Enrichment Not Producing Final Version

Enrichment runs but no `.final.md` file is generated.

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
