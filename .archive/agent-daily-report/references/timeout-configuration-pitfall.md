# Timeout Configuration Pitfall

## Problem

`timeout_seconds: 0` in config.yaml causes Python requests library to raise:
```
Attempted to set connect timeout to 0, but the timeout cannot be set to a value less than or equal to 0.
```

This affects ALL HTTP-based collectors, not just the agent pipeline.

## Affected Locations in config.yaml

All these locations must have timeout_seconds > 0 (recommended: 60):

```yaml
# Agent Pipeline
agent_pipeline:
  agents:
    editor:
      timeout_seconds: 60
    github_trust:
      timeout_seconds: 60
    item_enrichment:
      timeout_seconds: 60
  source_verification:
    timeout_seconds: 60
  llm:
    timeout_seconds: 60

# Developer Communities
developer_communities:
  linuxdo:
    request:
      timeout_seconds: 60
  nodeseek:
    request:
      timeout_seconds: 60

# Other collectors
hackernews:
  request:
    timeout_seconds: 60

producthunt:
  request:
    timeout_seconds: 60

reddit:
  request:
    timeout_seconds: 60

rss_feeds:
  request:
    timeout_seconds: 60
```

## Fix Script

Use this to find and fix all timeout_seconds: 0 in config.yaml:

```python
import yaml

config_path = "D:/openclaw-hermes/agent-daily-report-skill/config.yaml"
with open(config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

def fix_timeouts(obj, path=""):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'timeout_seconds' and value == 0:
                obj[key] = 60
                print(f"Fixed {path}.{key}: 0 -> 60")
            elif isinstance(value, dict):
                fix_timeouts(value, f"{path}.{key}")

fix_timeouts(config)

with open(config_path, "w", encoding="utf-8") as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
```

## Verification

After fixing, verify with:
```bash
grep -n "timeout_seconds: 0" config.yaml
```
Should return no results.

## Why 60 and not 0

- Python requests library requires timeout > 0
- 60 seconds is sufficient for most API calls
- 0 means "no timeout" in some contexts but "invalid" in requests library
- For truly unlimited timeout, use a large value like 300 or 600

## Related Pits

- P72: timeout=0导致网络请求失败
- P46: execute_code 300s超时杀子进程（用run_pipeline.py解决）
