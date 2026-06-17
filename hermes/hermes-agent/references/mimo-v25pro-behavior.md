# MiMo v2.5 Pro Behavior Notes

## Empty Response Bug (2026-06-02)

MiMo v2.5 Pro intermittently returns **empty content** for certain prompts.

### Test Results

| Prompt Type | Result |
|-------------|--------|
| Simple Chinese ("请回复 OK") | ✅ Always works |
| Simple English ("Output OK") | ❌ Sometimes empty |
| Chinese with instructions | ✅ Always works |
| Complex English (system + user, JSON output) | ❌ Often empty |
| Chinese with examples | ✅ Always works |
| English "你好" | ❌ Empty |

### Root Cause

Unknown. Likely model-specific behavior with English prompts containing:
- Complex JSON formatting instructions
- Multiple output constraints
- Long system prompts

### Workaround

1. **Use Chinese prompts** — MiMo handles Chinese more reliably
2. **Add retry logic** — 3 retries with temperature 0.2 → 0.3 → 0.4
3. **Add examples** — Include expected output format in the prompt
4. **Keep prompts short** — Reduce complexity

### Retry Pattern

```python
def call_mimo(system_prompt, user_prompt, max_retries=3):
    for attempt in range(max_retries):
        response = call_api(system_prompt, user_prompt, temperature=0.2 + attempt * 0.1)
        if response and response.strip():
            return response
        if attempt < max_retries - 1:
            time.sleep(2)
    return ""
```

## API Key Format

MiMo v2.5 Pro API key format: `tp-s48...` (51 chars)
Base URL: `https://token-plan-sgp.xiaomimimo.com/v1`
Auth: `Authorization: Bearer {key}`

## Token Plan vs Custom Provider

- **Token Plan**: `https://token-plan-sgp.xiaomimimo.com/v1` (main provider)
- **Custom Provider**: `https://api.xiaomimimo.com/v1` (backup, different API key)

Both use the same model name `mimo-v2.5-pro` but are separate accounts.
