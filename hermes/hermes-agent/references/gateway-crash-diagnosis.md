# Gateway Crash Diagnosis (Windows)

## Architecture: Why Claude Code Loses API When Gateway Crashes

```
Claude Code CLI
    ↓ HTTP
http://127.0.0.1:34567/anthropic  ← mimo-claude-proxy.py (Python, port 34567)
    ↓ HTTPS
Xiaomi MiMo API (token-plan-sgp.xiaomimimo.com)
```

The anthropic proxy (port 34567) is a **separate Python process** launched by the gateway startup script. When the gateway main process crashes, the proxy may also die (depending on how it was launched). Claude Code's `ANTHROPIC_BASE_URL` points to this proxy — no proxy = no API.

**Key ports**:
| Port | Process | Purpose |
|------|---------|---------|
| 34567 | python (mimo-claude-proxy) | Anthropic-compatible proxy for Claude Code |
| 4820 | hermes gateway | Main gateway HTTP (messaging, cron, kanban) |

## Diagnostic Checklist (execute_code based, no shell needed)

```python
import os, subprocess, json

# 1. Check key ports
for port in [34567, 4820]:
    result = subprocess.run(["powershell", "-Command",
        f"Get-NetTCPConnection -LocalPort {port} -ErrorAction SilentlyContinue "
        f"| Select-Object LocalPort, State, OwningProcess | Format-Table"],
        capture_output=True, text=True)
    status = "LISTENING" if "Listen" in result.stdout else "NOT IN USE"
    print(f"Port {port}: {status}")
    if "Listen" in result.stdout:
        # Extract PID and check process
        for line in result.stdout.strip().split('\n'):
            if str(port) in line and 'Listen' in line:
                pid = line.split()[2]
                p = subprocess.run(["powershell", "-Command",
                    f"Get-Process -Id {pid} -ErrorAction SilentlyContinue "
                    f"| Select-Object ProcessName, Path | Format-List"],
                    capture_output=True, text=True)
                print(f"  PID {pid}: {p.stdout.strip()}")

# 2. Check system memory
result = subprocess.run(["powershell", "-Command",
    "Get-CimInstance Win32_OperatingSystem "
    "| Select-Object TotalVisibleMemorySize, FreePhysicalMemory | Format-List"],
    capture_output=True, text=True)
print(f"\n=== System Memory ===\n{result.stdout}")

# 3. Check all python processes (memory usage)
result = subprocess.run(["powershell", "-Command",
    "Get-Process python* -ErrorAction SilentlyContinue "
    "| Select-Object ProcessName, Id, @{N='MemMB';E={[math]::Round($_.WorkingSet64/1MB)}}, Path "
    "| Format-Table"],
    capture_output=True, text=True)
print(f"=== Python Processes ===\n{result.stdout}")

# 4. Read gateway state
state_file = os.path.expanduser("~/.hermes/gateway_state.json")
if os.path.exists(state_file):
    with open(state_file, 'r') as f:
        state = json.load(f)
    print(f"=== Gateway State ===")
    print(f"State: {state.get('gateway_state')}, PID: {state.get('pid')}")
    for name, info in state.get('platforms', {}).items():
        print(f"  {name}: {info.get('state')}")

# 5. Read last 30 lines of errors.log
errors_log = os.path.expanduser("~/.hermes/logs/errors.log")
if os.path.exists(errors_log):
    with open(errors_log, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    print(f"\n=== errors.log (last 30 of {len(lines)}) ===")
    for line in lines[-30:]:
        print(line.rstrip())
```

## Common Crash Causes (by frequency)

### 1. MCP Server Failure Loop
**Symptom**: errors.log filled with `MCP server 'xxx' initial connection failed (attempt N/3)`
**Impact**: Repeated connection retries consume resources, may destabilize asyncio event loop.
**Fix**: Disable the failing MCP server in config.yaml (`enabled: false` or remove from `mcp_servers`), restart gateway.
**Example**: image-reader failing with "unhandled errors in a TaskGroup" — Python subprocess can't start.

### 2. Memory Pressure (OOM)
**Symptom**: System free memory < 1GB, gateway process disappears from task list.
**Diagnosis**: Check `FreePhysicalMemory` in Win32_OperatingSystem. If < 1GB with 16GB total, Windows may kill processes.
**Fix**: Close memory-heavy apps, reduce number of concurrent python/node processes.
**Note**: Hermes gateway + anthropic proxy + MCP servers + node processes can easily consume 2-3GB.

### 3. Network Disruption Propagation
**Symptom**: `Cannot connect to host xxx:443 ssl:default [指定的网络名不再可用]` in gateway.log
**Impact**: If platform connection handler doesn't gracefully handle network loss, exception may propagate to main event loop.
**Mitigation**: Disable unused platforms (e.g., WeChat) to reduce exposure to network failures.

### 4. API Timeout Blocking Event Loop
**Symptom**: `RemoteProtocolError: peer closed connection without sending complete message body` after 120-240s.
**Impact**: Long-blocking HTTP requests can starve the event loop, especially if many concurrent requests.
**Note**: MiMo Token Plan API occasionally has 240s+ response times.

### 5. SystemExit: 75 (Known Bug)
**Symptom**: Gateway exits with code 75 (EX_TEMPFAIL), auto-restarts within 1-2s.
**Status**: Known issue (#45454), not a real crash — gateway recovers automatically.

## Prevention

1. **Disable unused MCP servers**: If image-reader keeps failing, disable it until the underlying issue is fixed.
2. **Disable unused platforms**: If WeChat is not needed, remove or disable the weixin platform to avoid network-related crashes.
3. **Monitor memory**: Keep > 2GB free. Close unnecessary python/node processes.
4. **Set gateway_timeout**: In config.yaml, `agent.gateway_timeout: 1800` prevents runaway sessions.
5. **Use `--replace` flag**: Gateway started with `--replace` kills old instance before starting new one, preventing port conflicts.

## Restart After Crash

```python
import subprocess, os, time

# Option A: hermes.bat (project-local)
subprocess.run([r"D:\openclaw-hermes\scripts\hermes.bat", "gateway", "restart"],
               capture_output=True, text=True, shell=True)

# Option B: Global gateway-service (includes WeChat config)
gateway_script = os.path.expanduser("~/.hermes/gateway-service/Hermes_Gateway.cmd")
subprocess.Popen(["cmd", "/c", "start", "Hermes Gateway", gateway_script],
                  shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

# Wait and verify
time.sleep(10)
# Run diagnostic checklist above to confirm ports are listening
```
