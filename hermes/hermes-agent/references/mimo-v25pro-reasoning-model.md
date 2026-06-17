# mimo-v2.5-pro Reasoning Model Behavior

**Discovered**: 2026-05-30 during API connection diagnosis

## Key Behavior

mimo-v2.5-pro is a **reasoning model** that returns two fields:
- `content`: The final answer (may be empty or short)
- `reasoning_content`: The model's internal reasoning process (always populated)

## Symptom: "Connection error" is actually reasoning timeout

**Error message**:
```
APIConnectionError: Connection error.
Provider: xiaomi  Model: mimo-v2.5-pro
Endpoint: https://token-plan-sgp.xiaomimimo.com/v1
Elapsed: 0.08s
```

**Root cause**: NOT a connection issue. The model starts reasoning immediately but the reasoning process is long. If the timeout is too short (e.g., 30s), it appears as a connection error.

**Fix**: Increase timeout to 120s+ for mimo-v2.5-pro.

## API Test Results (2026-05-30)

| Model | content | reasoning_content | Notes |
|-------|---------|-------------------|-------|
| mimo-v2.5-pro | ✅ (82 chars) | ✅ (237 chars) | Default: reasoning enabled |
| mimo-v2.5-pro (enable_reasoning=False) | ❌ (empty) | ✅ (178 chars) | Disabling reasoning doesn't work as expected |
| mimo-v2-pro | ✅ (59 chars) | ✅ (62 chars) | Balanced, faster |
| mimo-v2-omni | ✅ (10 chars) | ✅ (170 chars) | Multimodal |

## Available Models

```
mimo-v2-omni
mimo-v2-pro
mimo-v2-tts
mimo-v2.5
mimo-v2.5-pro
mimo-v2.5-tts
mimo-v2.5-tts-voiceclone
mimo-v2.5-tts-voicedesign
```

## Reasoning Trace Opportunity

mimo-v2.5-pro's `reasoning_content` field is a natural fit for Reasoning Trace:
- The reasoning is recorded automatically by the model
- It does NOT count as output tokens (cost savings)
- It can be captured and stored for later analysis
- It provides detailed step-by-step thinking

## Configuration Recommendations

For daily use: `mimo-v2-pro` (fast, reliable)
For complex reasoning: `mimo-v2.5-pro` (slow but deep reasoning)
For multimodal: `mimo-v2-omni`

In config.yaml:
```yaml
model:
  provider: xiaomi
  model: mimo-v2-pro  # daily use

fallback_providers:
  - provider: xiaomi
    model: mimo-v2.5-pro  # complex tasks
  - provider: deepseek
    model: deepseek-v4-pro  # backup
```
