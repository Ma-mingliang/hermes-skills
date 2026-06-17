# Timeout Configuration - All Locations (2026-06-05 Confirmed)

## Problem

`timeout_seconds: 0` causes Python requests library to reject with:
`Attempted to set connect timeout to 0, but the timeout cannot be set to a value less than or equal to 0`

This affects ALL RSS-based sources: LinuxDo, NodeSeek, HackerNews, Reddit, ProductHunt, RSS Feeds.

## All Locations (10 places in config.yaml)

```yaml
# RSS/Community sources
rss_feeds.request.timeout_seconds: 60
developer_communities.linuxdo.request.timeout_seconds: 60
developer_communities.nodeseek.request.timeout_seconds: 60
hackernews.request.timeout_seconds: 60
producthunt.request.timeout_seconds: 60
reddit.request.timeout_seconds: 60

# Agent Pipeline
agent_pipeline.agents.editor.timeout_seconds: 60
agent_pipeline.agents.github_trust.timeout_seconds: 60
agent_pipeline.agents.item_enrichment.timeout_seconds: 60
agent_pipeline.source_verification.timeout_seconds: 60
```

## Additional Fix: agent_llm_client.py

Line 49 in `scripts/agent_llm_client.py`:
```python
# Old:
self.timeout = int(llm_config.get("timeout_seconds", 120))
# New:
self.timeout = max(30, int(llm_config.get("timeout_seconds", 120)))
```

This prevents the LLM client from using timeout=0 even if config says 0.

## Verification

After running the report, check logs for:
- No "Attempted to set connect timeout to 0" errors
- All sources show success/success_no_match (not failed_network)

## Config Change Method

**Do NOT use yaml.dump()** - it loses comments and formatting.

Use execute_code + text replacement:
```python
with open("config.yaml", "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace("timeout_seconds: 0", "timeout_seconds: 60")
with open("config.yaml", "w", encoding="utf-8") as f:
    f.write(content)
```

Or use the recursive fix_timeouts function that traverses the entire config tree.
