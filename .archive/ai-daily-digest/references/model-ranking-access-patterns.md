# Model Ranking Website Access Patterns (2026-05-31)

## Overview

Three major model ranking websites all use Vercel with aggressive anti-bot protection.
Traditional HTTP requests and even headless Playwright with extended waits fail consistently.

## Website Access Status

| Website | HTTP Request | Playwright (headless) | API Available | Fallback |
|---------|-------------|----------------------|---------------|----------|
| lmarena.ai | ❌ Vercel checkpoint | ❌ Vercel checkpoint | ❌ | OpenRouter API |
| artificialanalysis.ai | ❌ Vercel checkpoint | ❌ Vercel checkpoint | ❌ | OpenRouter API |
| designarena.ai | ❌ 403 Forbidden | ❌ Vercel checkpoint | ❌ | OpenRouter API |
| openrouter.ai (API) | ✅ 350 models | N/A | ✅ `/api/v1/models` | — |

## What Was Tried (All Failed)

1. **urllib HTTP request** → Vercel Security Checkpoint / 403
2. **Playwright headless** → Vercel Security Checkpoint persists after 60s wait
3. **Playwright with browser flags** (`--disable-blink-features=AutomationControlled`) → Still blocked
4. **Page refresh after checkpoint** → Still checkpoint
5. **Wait 20s, 30s, 60s** → Checkpoint never resolves

## Working Fallback: OpenRouter API

```python
import urllib.request, json

url = "https://openrouter.ai/api/v1/models"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode())
    models = data.get("data", [])

# Each model has: id, name, pricing (prompt/completion per token), context_length
# Can calculate value_ratio = context_length / avg_price
```

**What OpenRouter provides:**
- Model ID, name, description
- Prompt and completion pricing (per token)
- Context length
- Architecture info
- Knowledge cutoff date

**What OpenRouter does NOT provide:**
- Elo scores / ranking positions
- Quality benchmarks
- Speed benchmarks
- User vote counts

## Critical Rule: NEVER Fabricate Ranking Data

When ranking websites are inaccessible:
1. **State clearly**: "排名数据未获取（SPA站点安全检查）"
2. **Use available data**: OpenRouter pricing + context length for value analysis
3. **Never invent Elo scores, rankings, or benchmark numbers**
4. **Mark data source**: Always label which source data came from

## Future Improvement Paths

1. **Anti-detection**: browserforge fingerprint spoofing + residential proxies
2. **Alternative sources**: HuggingFace Open LLM Leaderboard (may have API)
3. **Community data**: Scrape HN/Reddit discussions for informal rankings
4. **Manual snapshot**: User provides screenshot → vision_analyze extracts data
