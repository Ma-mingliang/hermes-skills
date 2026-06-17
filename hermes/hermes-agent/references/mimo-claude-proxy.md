# MiMo Claude Code Proxy

## Architecture

Local HTTP proxy (Python `ThreadingHTTPServer`) that sits between Claude Code CLI and MiMo's Anthropic-compatible API.

```
Claude Code CLI
  ↓ (all requests to ANTHROPIC_BASE_URL)
http://127.0.0.1:34567/anthropic
  ↓ (mimo-claude-proxy.py)
https://token-plan-sgp.xiaomimimo.com/anthropic
```

## File Locations

| File | Path |
|------|------|
| Entry script | `D:\Claude Code\scripts\Start-Claude-Mimo.ps1` |
| Proxy launcher | `D:\Claude Code\scripts\Start-MimoClaudeProxy.ps1` |
| Proxy logic | `C:\Users\<user>\.claude\scripts\mimo-claude-proxy.py` |
| Proxy log | `C:\Users\<user>\.claude\logs\mimo-claude-proxy.log` |
| Proxy stderr | `C:\Users\<user>\.claude\logs\mimo-claude-proxy.stderr.log` |
| Claude settings | `C:\Users\<user>\.claude\settings.json` |

## Claude Code Settings (settings.json)

```json
{
  "model": "mimo-v2.5-pro",
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:34567/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "<mimo-api-key>",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "mimo-v2.5-pro",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "mimo-v2.5-pro",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "mimo-v2.5"
  }
}
```

## Model Routing

The proxy intercepts every `/v1/messages` request and checks the JSON body:

```python
def contains_image(value):
    # Recursively checks for:
    # - media_type starting with "image/"
    # - type in {"image", "image_url", "input_image"}
    # - source.type == "base64" with image media_type
    ...

def route_body(raw_body, path):
    if contains_image(payload):
        payload["model"] = "mimo-v2.5"      # vision model
    else:
        payload["model"] = "mimo-v2.5-pro"  # reasoning model (unchanged)
```

## Dry-Run Mode

Add header `X-Mimo-Proxy-Dry-Run: 1` to test routing without making actual API calls:

```python
import http.client, json

conn = http.client.HTTPConnection("127.0.0.1", 34567, timeout=5)

# Test image routing
body = json.dumps({
    "model": "mimo-v2.5-pro",
    "messages": [{"role": "user", "content": [
        {"type": "text", "text": "describe"},
        {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": "iVBORw0KGgo="}}
    ]}]
}).encode()
conn.request("POST", "/anthropic/v1/messages?beta=true", body=body,
    headers={"Content-Type": "application/json", "X-Mimo-Proxy-Dry-Run": "1"})
r = json.loads(conn.getresponse().read().decode())
# Expected: {"ok": true, "model": "mimo-v2.5", "changed": true, ...}
```

## Known Bug: Query String Breaks Path Matching (2026-06-04)

### Symptom
Image requests fail with: "There's an issue with the selected model (mimo-v2.5-pro). It may not exist or you may not have access to it."

### Root Cause
Claude Code appends `?beta=true` to the endpoint. The proxy's path check:
```python
path.rstrip("/").endswith("/v1/messages")
```
evaluates to False for `/anthropic/v1/messages?beta=true` because the query string is part of the string being checked.

### Fix (Applied)
```python
from urllib.parse import urlsplit as _urlsplit
_clean_path = _urlsplit(path).path
if not raw_body or not _clean_path.rstrip("/").endswith("/v1/messages"):
    return raw_body, "", False
```

### How to Verify
```python
import http.client, json
conn = http.client.HTTPConnection("127.0.0.1", 34567, timeout=5)
body = json.dumps({"model": "mimo-v2.5-pro", "max_tokens": 10,
    "messages": [{"role": "user", "content": [
        {"type": "text", "text": "describe"},
        {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": "iVBORw0KGgo="}}
    ]}]}).encode()
conn.request("POST", "/anthropic/v1/messages?beta=true", body=body,
    headers={"Content-Type": "application/json", "X-Mimo-Proxy-Dry-Run": "1"})
r = json.loads(conn.getresponse().read().decode())
assert r["model"] == "mimo-v2.5" and r["changed"] is True
```

## Restarting the Proxy

```python
import subprocess, time, http.client

# Kill existing proxy
subprocess.run(['powershell.exe', '-Command',
    'Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort 34567 -State Listen -EA SilentlyContinue | % { Stop-Process -Id $_.OwningProcess -Force -EA SilentlyContinue }'],
    capture_output=True, timeout=5)
time.sleep(1)

# Start new proxy (background, no window)
subprocess.Popen(['powershell.exe', '-ExecutionPolicy', 'Bypass', '-Command',
    r'& "D:\Claude Code\scripts\Start-MimoClaudeProxy.ps1"'],
    creationflags=0x08000000)  # CREATE_NO_WINDOW
time.sleep(2)

# Verify
conn = http.client.HTTPConnection("127.0.0.1", 34567, timeout=5)
conn.request("GET", "/anthropic/health")
print(conn.getresponse().read().decode())  # {"ok": true, "proxy": "mimo-claude-proxy"}
```

## Launching Claude Code

```python
import subprocess
subprocess.run(
    ['powershell.exe', '-Command',
     r'Start-Process -FilePath "D:\Claude Code\tools\claude\v2.1.150\claude.exe" -WorkingDirectory "E:\Code"'],
    capture_output=True, timeout=10)
```

## Debugging Checklist

1. **Check proxy is running**: `http://127.0.0.1:34567/anthropic/health` → 200
2. **Check settings.json has `model` field**: `"model": "mimo-v2.5-pro"` must exist at top level. Without it, Claude Code may not select the correct default model even when env vars are configured. Use `json.load()` to verify — the field is easy to miss since Claude Code works without it (falls back to env vars) but image routing depends on it being set explicitly.
3. **Check dry-run routing**: Send image request with `X-Mimo-Proxy-Dry-Run: 1` header
4. **Check proxy log**: `~/.claude/logs/mimo-claude-proxy.log` for route decisions and errors
5. **Check DNS**: `socket.getaddrinfo("token-plan-sgp.xiaomimimo.com", 443)` — intermittent DNS failures happen
6. **Check API key**: Direct request to MiMo API with `x-api-key` header → 401 means key invalid

## Startup Script Flow

```
Start-Claude-Mimo.ps1
  ├─ Start-MimoClaudeProxy.ps1
  │   ├─ Check port 34567 (skip if already listening)
  │   └─ Start python.exe mimo-claude-proxy.py (background)
  └─ claude.exe (with args)
```
