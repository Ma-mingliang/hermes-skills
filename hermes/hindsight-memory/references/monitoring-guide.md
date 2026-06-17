# Hindsight Monitoring Guide

End-to-end health-check recipe for cron or manual inspection.

## Quick Health Check (HTTP only)

```bash
# 1. Service alive?
curl -s http://localhost:8888/health
# → {"status":"healthy","database":"connected"}

# 1b. Version & features
curl -s http://localhost:8888/version
# → {"api_version":"0.7.1","features":{"observations":true,"mcp":true,...}}

# 2. Bank stats
curl -s http://localhost:8888/v1/default/banks/hermes/stats | jq '{nodes: .total_nodes, docs: .total_documents, failed: .failed_operations, pending: .pending_operations}'

# 3. Memory recall
curl -s -X POST http://localhost:8888/v1/default/banks/hermes/memories/recall \
  -H "Content-Type: application/json" \
  -d '{"query": "monitoring status", "max_tokens": 500}' | jq '.results | length'
```

## Full Python Script Pattern

```python
"""Hindsight health monitor — test all 4 dimensions."""
import json, os, urllib.request, urllib.error

BASE = "http://localhost:8888"
BANK = "hermes"

def api_get(path, timeout=10):
    req = urllib.request.Request(f"{BASE}{path}")
    req.add_header("User-Agent", "Hindsight-Monitor/1.0")
    resp = urllib.request.urlopen(req, timeout=timeout)
    return json.loads(resp.read().decode())

def api_post(path, data, timeout=60):
    js = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(f"{BASE}{path}", data=js, method="POST")
    req.add_header("Content-Type", "application/json")
    resp = urllib.request.urlopen(req, timeout=timeout)
    return json.loads(resp.read().decode())

# 1. Service check
health = api_get("/health")
assert health["status"] == "healthy", f"Health check failed: {health}"

# 2. API surface (discover endpoints)
spec = api_get("/openapi.json")
endpoints = list(spec.get("paths", {}).keys())
assert f"/v1/default/banks/{BANK}/memories" in str(endpoints), "Memory endpoint missing"

# 3. Storage test
store = api_post(f"/v1/default/banks/{BANK}/memories", {
    "items": [{
        "content": "Health check test — auto-generated",
        "tags": ["monitor", "health-check"],
        "metadata": {"source": "monitor_cron"}
    }]
}, timeout=60)
print(f"Store: {store}")

# 4. Retrieval test
recall = api_post(f"/v1/default/banks/{BANK}/memories/recall", {
    "query": "health check monitoring",
    "max_tokens": 500,
    "budget": "low"
})
print(f"Recall: {len(recall.get('results', []))} results")

# 5. LLM backend (reflect requires LLM)
reflect = api_post(f"/v1/default/banks/{BANK}/reflect", {
    "query": "What is the current system status?",
    "budget": "low"
}, timeout=60)
print(f"Reflect: {len(reflect.get('text', ''))} chars")

# 6. Stats summary
stats = api_get(f"/v1/default/banks/{BANK}/stats")
print(f"Stats: {stats['total_nodes']} nodes, {stats['total_documents']} docs, "
      f"{stats.get('failed_operations', 0)} failed, {stats.get('pending_operations', 0)} pending")
```

## LLM Backend Verification (direct MiMo call)

```python
import json, urllib.request

# Read credentials from ~/.hindsight/.env
env = {}
with open(os.path.expanduser("~/.hindsight/.env")) as f:
    for line in f:
        if "=" in line and not line.startswith("#"):
            k, v = line.strip().split("=", 1)
            env[k] = v

data = json.dumps({
    "model": "mimo-v2.5-pro",
    "messages": [{"role": "user", "content": "Reply OK"}],
    "max_tokens": 10
}).encode()

req = urllib.request.Request(f"{env['HINDSIGHT_API_LLM_BASE_URL']}/chat/completions", data=data)
req.add_header("Authorization", f"Bearer {env['HINDSIGHT_API_LLM_API_KEY']}")
req.add_header("Content-Type", "application/json")
resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
print(f"Model: {resp['model']}, tokens: {resp['usage']['total_tokens']}")
```

## Key Metrics to Watch

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| `failed_operations` | 0 | 1-3 | >3 |
| `pending_operations` | 0 | 1-5 | >5 |
| `total_nodes` growth | steady ↑ | flat >24h | declining |
| `last_consolidated_at` | <1h ago | 1-6h | >6h |
| Port response | 200 | >500ms | timeout |
| LLM API latency | <5s | 5-15s | >15s |

## Windows: execute_code as terminal fallback

On Windows hosts where bash/WSL is broken (common errors: `execvpe(/bin/bash) failed`,
WSL NAT relay errors), use `execute_code` with Python `urllib` for all HTTP checks:

```python
import urllib.request, urllib.error, json, socket

# Port check
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3)
port_open = s.connect_ex(('127.0.0.1', 8888)) == 0
s.close()

# Health check
resp = urllib.request.urlopen('http://localhost:8888/health', timeout=5)
health = json.loads(resp.read().decode('utf-8'))

# Read .env for API key testing
import os
env = {}
with open(os.path.expanduser('~/.hindsight/.env')) as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            env[k] = v
```

This pattern works inside Hermes `execute_code` blocks and avoids all shell/WSL issues.

### Windows: browser_navigate as last-resort fallback

When both terminal and execute_code fail (WSL relay errors, Python not on PATH), use
`browser_navigate` to hit endpoints directly. The browser renders JSON endpoints in an
HTML wrapper with a "美观输出" (pretty-print) checkbox.

**Preferred**: Use `browser_console` to extract parsed JSON directly — returns a native dict:

```
browser_navigate(url="http://localhost:8888/health")
browser_console(expression="document.body.innerText")
# → {"status": "healthy", "database": "connected"}  (dict, not string)
```

**Fallback**: If `browser_console` fails, use `browser_snapshot(full=True)` to read
the JSON from `StaticText` nodes (returns raw string, needs manual parsing).

Slower than urllib but works when everything else is down. For incident triage only.

### Prometheus metrics filtering

`GET /metrics` returns ~75KB of Prometheus text. To extract Hindsight-specific metrics:

```
browser_console(expression="document.body.innerText.substring(3000, 8000)")
```

Key metric families to look for:
- `hindsight_http_requests_in_progress_requests` — active requests by endpoint
- `hindsight_http_duration_seconds` — request latency histogram by endpoint/status
- `hindsight_llm_*` — LLM call counts and timing (if present)
- `process_resident_memory_bytes`, `process_cpu_seconds_total` — host resource usage

### Windows: `read_file` path resolution also fails — use `execute_code` for file reads

The `read_file` tool may fail to find files under `~/.hindsight/` on Windows even with
explicit paths like `C:/Users/<user>/.hindsight/.env`. Use `execute_code` with
`os.path.expanduser` and `os.listdir` for all config file reads:

```python
import os
env_path = os.path.expanduser('~/.hindsight/.env')
with open(env_path) as f:
    content = f.read()
```

Also useful: list the hindsight directory to detect stale config files:
```python
for f in os.listdir(os.path.expanduser('~/.hindsight')):
    print(f)
```

This catches `config.env`, `settings.env`, or other files that could cause config drift.

## Diagnostic Workflow (when LLM-backed endpoints fail)

When `reflect` or `store` time out but `/health` and `recall` work fine:

1. **Check Docker logs** for the exact error:
   ```bash
   docker logs --tail 50 hindsight 2>&1 | grep -iE 'error|fail|timeout'
   ```
   Common pattern: `APIStatusError: HTTP 400: "Not supported model gpt-4o-mini"`

2. **Verify model availability** against the provider's catalog:
   ```python
   import json, os, urllib.request
   env = {}
   with open(os.path.expanduser('~/.hindsight/.env')) as f:
       for line in f:
           if '=' in line and not line.startswith('#'):
               k, v = line.strip().split('=', 1)
               env[k] = v
   req = urllib.request.Request(f"{env['HINDSIGHT_API_LLM_BASE_URL']}/models")
   req.add_header('Authorization', f"Bearer {env['HINDSIGHT_API_LLM_API_KEY']}")
   models = [m['id'] for m in json.loads(urllib.request.urlopen(req, timeout=10).read())['data']]
   configured = env.get('HINDSIGHT_API_LLM_MODEL', 'gpt-4o-mini (default)')
   print(f"Configured: {configured}")
   print(f"Available: {models}")
   print(f"Match: {configured in models}")
   ```

3. **Fix**: Set `HINDSIGHT_API_LLM_MODEL` to a model that exists on the provider, restart container.

> **Why health checks can miss this**: `/health` only checks DB connection. `recall` uses embeddings (separate model/route). Only `reflect` and `store` exercise the chat/completion LLM — they silently retry 6 times then timeout with no error body to the client.

## Common Pitfalls

- **POST /memories timeout**: Storage needs LLM extraction. Use 60s+ timeout or check operations endpoint for completion.
- **422 on store**: Request body must be `{"items": [{"content": "...", ...}]}` — the `content` field inside `items[]` is mandatory.
- **Endpoint guessing**: Never guess API paths. Always fetch `/openapi.json` first — Hindsight version upgrades can shift endpoints.
- **read_file on Windows**: The `read_file` tool may fail with `~` or Windows-style paths. Always use `execute_code` with `os.path.expanduser` for config file access.
- **Config drift detection**: When diagnosing LLM failures, compare `BASE_URL` across `.env`, `config.env`, and `docker-compose.yml` — stale files with wrong URLs are a common root cause.
