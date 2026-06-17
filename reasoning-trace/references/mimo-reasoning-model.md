# MiMo v2.5 Pro Reasoning Model Discovery

**Date**: 2026-05-30  
**Context**: API connection diagnosis revealed mimo-v2.5-pro is a reasoning model

## Key Finding

MiMo v2.5 Pro returns **two fields** in chat completions:
- `content`: Final answer (short)
- `reasoning_content`: Full reasoning process (long)

This is the native "Reasoning Trace" — the model already records its thinking process internally.

## API Response Structure

```json
{
  "choices": [{
    "message": {
      "content": "你好！很高兴见到你！",
      "reasoning_content": "The user has greeted me with a simple '你好'..."
    }
  }]
}
```

## Available Models (as of 2026-05-30)

- `mimo-v2-omni` — Multimodal
- `mimo-v2-pro` — Standard (fast, no reasoning)
- `mimo-v2-tts` — Text-to-speech
- `mimo-v2.5` — Base reasoning
- `mimo-v2.5-pro` — Full reasoning (slow, expensive)
- `mimo-v2.5-tts` — TTS v2.5
- `mimo-v2.5-tts-voiceclone` — Voice cloning
- `mimo-v2.5-tts-voicedesign` — Voice design

## Implications for Reasoning Trace

1. **Native support**: mimo-v2.5-pro already has reasoning built-in
2. **Token cost**: reasoning_content tokens are NOT counted as output (cheaper)
3. **Latency**: reasoning takes time → may cause timeout on complex tasks
4. **Fallback**: use mimo-v2-pro for speed, mimo-v2.5-pro for quality

## Configuration Recommendations

```yaml
# For speed (no reasoning)
model:
  provider: xiaomi
  model: mimo-v2-pro

# For quality (with reasoning)
model:
  provider: xiaomi
  model: mimo-v2.5-pro
```

## Connection Error Root Cause

The "APIConnectionError" was NOT a network issue — it was the model's reasoning process taking too long. Solutions:
1. Increase timeout to 120s
2. Use mimo-v2-pro for routine tasks
3. Use mimo-v2.5-pro only when reasoning quality matters
