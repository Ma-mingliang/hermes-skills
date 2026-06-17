# WeChat iLink Rate Limiting Fixes (2026-06-02 updated)

## Symptom
WeChat shows "暂时无法连接" or messages not responding. Gateway state shows
"connected" but logs show `ret=-2 rate limited`.

## Root Cause
iLink API's context_token becomes stale after frequent rate limiting. Gateway
shows "connected" but can't actually send/receive.

## Fix Procedure

### 1. Clear the stale context_token
```python
import json, os

ctx_dir = os.path.expanduser(r"~\.hermes\weixin\accounts")
for f in os.listdir(ctx_dir):
    if f.endswith("@im.bot.context-tokens.json"):
        ctx_file = os.path.join(ctx_dir, f)
        with open(ctx_file, "w") as fh:
            json.dump({}, fh)
        print(f"Cleared: {ctx_file}")
```

### 2. Restart the gateway (use GLOBAL gateway, not project hermes.bat)
```python
import subprocess, os
gateway_script = os.path.join(os.path.expanduser("~/.hermes"), "gateway-service", "Hermes_Gateway.cmd")
subprocess.Popen(["cmd", "/c", "start", "Hermes Gateway", gateway_script],
                  shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
```

### 3. Verify
Gateway_state.json should show `weixin: connected` after ~10s.

## Rate Limit Thresholds (2026-06-02 verified)

| Parameter | Value |
|-----------|-------|
| Scope | **Account-level** (iLink throttles the entire account, not per-chat) |
| Trigger | ~4-5 messages in a session, regardless of interval |
| Interval impact | **None** — even 2-5 minute waits between messages still trigger once 3+ sent |
| Recovery | 2-6 hours for auto-unthrottle |
| Context token refresh | Helps but doesn't instantly lift account-level throttle |

## Safe Messaging Rules

1. **Max 2-3 messages per session** — merge content into fewer, longer messages (3000-4000 chars each)
2. **Long content → cron job** — for reports needing >3 messages, use cron job with self-contained prompt
3. **Rate limit detected → stop immediately** — don't retry; wait 2+ hours or use cron
4. **Daily push (cron)**: Uses final response auto-delivery, usually bypasses send_message limits
5. **Cron job model override**: If cron gets HTTP 402, explicitly set `model` and `provider` on the job

## When Rate Limited (ret=-2)

1. Stop sending immediately — retries waste time and context
2. Option A: Wait 2-6 hours for auto-unthrottle
3. Option B: Clear context_token + restart with GLOBAL gateway (may help, not guaranteed)
4. Option C: Set a cron job to deliver content later

## Pitfall: Gateway Source for WeChat

WeChat config (accounts, context-tokens, iLink credentials) lives ONLY in the **global** `~/.hermes`, NOT in project-level `.hermes` directories.

| Method | Config Source | Use When |
|--------|--------------|----------|
| Project `hermes.bat` | Project-local `.hermes` | Provider/model changes, non-WeChat work |
| Global `Hermes_Gateway.cmd` | Global `~/.hermes` | WeChat connection issues, channel binding changes |

## Related Files
- Context tokens: `~/.hermes/weixin/accounts/<account_id>@im.bot.context-tokens.json`
- Gateway service: `~/.hermes/gateway-service/Hermes_Gateway.cmd`
- Gateway state: `~/.hermes/gateway_state.json`
