# WeChat (iLink) Troubleshooting Guide

## Problem: "暂时无法连接" / Messages Not Sending

### Root Cause
iLink API context_token becomes stale after rate limiting (ret=-2). The gateway shows "connected" but messages silently fail or the WeChat client shows "temporarily unable to connect."

### Diagnosis
1. Check `gateway_state.json` — if `weixin.state` = "connected" but user reports issues, token is likely stale
2. Check `gateway.log` for recent `ret=-2` rate limit errors
3. Check `weixin/accounts/<id>.im.bot.context-tokens.json` — if token exists but old, it may be invalid

### Fix: Clear Context Token + Restart Gateway
```python
import json, subprocess, time

# 1. Clear stale context token
ctx_file = r"C:\Users\<user>\.hermes\weixin\accounts\<account_id>.im.bot.context-tokens.json"
with open(ctx_file, "w") as f:
    json.dump({}, f)

# 2. Kill gateway
with open(r"C:\Users\<user>\.hermes\gateway.pid") as f:
    pid = json.load(f)["pid"]
subprocess.run(["taskkill", "/PID", str(pid), "/F"], creationflags=subprocess.CREATE_NO_WINDOW)
time.sleep(3)

# 3. Restart gateway
subprocess.Popen(
    ["cmd", "/c", "start", "Hermes Gateway", r"C:\Users\<user>\.hermes\gateway-service\Hermes_Gateway.cmd"],
    shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE
)
```

### Why It Works
- Gateway restart forces fresh authentication with iLink API
- New context_token is obtained on reconnect
- Old stale token was causing silent message drops

### GitHub References
- Issue #31131: Messages silently dropped under rate limiting
- Issue #26828: Rate-limit retry storm causes OOM
- Issue #21011: ret=-2 with no built-in retry
- PR #20797: Treat ret=-2 as stale context_token

### Alternative Solutions
- wechat-acp (⭐629): https://github.com/formulahendry/wechat-acp
- wechatbot SDK (⭐451): https://github.com/corespeed-io/wechatbot
- hermes-wechat (⭐32): https://github.com/RongleCat/hermes-wechat
- LangBot (⭐16K): https://github.com/langbot-app/LangBot

## Rate Limiting Prevention
- Send messages with 10-second intervals (verified stable for 5 segments)
- Keep report to 5-6 segments max
- If ret=-2 occurs, wait 60s before retry
