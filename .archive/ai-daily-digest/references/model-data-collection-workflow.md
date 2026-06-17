# Model Data Collection Workflow (2026-05-31)

## Three-Source Strategy

Collect model capability AND cost data from three sites, then compute value ratios.

### Source 1: lmarena.ai (Chatbot Arena) — Rankings
- **URL**: https://lmarena.ai/leaderboard
- **Data**: Elo scores, Overall/Coding/Math/Creative/Vision rankings
- **Access method**: crawlee/playwright (SPA site)
- **Status (2026-05-31)**: ⚠️ Vercel Security Checkpoint blocks headless browsers
  - crawlee with PlaywrightCrawler: page loads but content is security checkpoint
  - playwright direct: same issue, even with 40-second waits
  - **Workaround**: None found yet. Try: (1) non-headless mode, (2) proxy, (3) cookie injection
- **Fallback**: Report "排名数据未获取" — do NOT fabricate rankings

### Source 2: openrouter.ai — Pricing
- **URL**: https://openrouter.ai/api/v1/models
- **Data**: 350+ models with prompt/completion pricing, context_length
- **Access method**: urllib REST API (no JS rendering needed)
- **Status (2026-05-31)**: ✅ Works reliably
- **Key fields**:
  - `id`: model identifier
  - `name`: display name
  - `pricing.prompt`: cost per input token
  - `pricing.completion`: cost per output token
  - `context_length`: max context window
  - `top_provider`: provider details
- **API**: `GET https://openrouter.ai/api/v1/models` — no auth needed

### Source 3: artificialanalysis.ai — Quality + Speed
- **URL**: https://artificialanalysis.ai/leaderboards/models
- **Data**: Quality index, speed (tokens/sec), pricing comparison
- **Access method**: crawlee/playwright (SPA site)
- **Status (2026-05-31)**: ⚠️ Vercel Security Checkpoint blocks headless browsers
- **Fallback**: Use OpenRouter data only

## Value Ratio Calculation

```python
# For each model:
prompt_price = float(model["pricing"]["prompt"])
completion_price = float(model["pricing"]["completion"])
avg_price = (prompt_price + completion_price) / 2
context_length = model["context_length"]

if avg_price > 0:
    value_ratio = context_length / avg_price  # tokens per dollar
else:
    value_ratio = float('inf')  # free model
```

## Categories for Selection

1. **Free models** (value_ratio = inf):
   - Owl Alpha, NVIDIA Nemotron, Poolside Laguna, IBM Granite
   - Best for: experimentation, high-volume tasks

2. **Budget models** (prompt < $0.000002/token):
   - StepFun Step 3.7 Flash, Google Gemini 3.1 Flash Lite
   - Best for: routine tasks, summarization

3. **Mid-range models** (prompt $0.000002-0.00001/token):
   - Qwen3.7 Max, xAI Grok 4.3
   - Best for: complex reasoning, coding

4. **Premium models** (prompt > $0.00001/token):
   - Claude Opus 4.8, GPT-5.5
   - Best for: critical tasks, highest quality needed

## Saved Data Format

```json
{
  "lmarena": {
    "overall_top10": [...],
    "coding_top10": [...]
  },
  "openrouter": {
    "all_models": [...],  // 350+ models
    "free_models": [...],
    "best_value": [...]
  },
  "artificialanalysis": {
    "quality_ranking": [...],
    "speed_ranking": [...]
  }
}
```

Save to: `D:/openclaw-hermes/data/daily/YYYY-MM-DD/model_ranking_data.json`
Analysis to: `D:/openclaw-hermes/data/daily/YYYY-MM-DD/model_value_analysis.json`

## Lessons Learned (2026-05-31)

1. **OpenRouter API does NOT provide rankings** — only pricing/specs
2. **lmarena.ai has Vercel Security Checkpoint** — blocks all headless browsers
3. **artificialanalysis.ai has same issue** — Vercel checkpoint
4. **Never fabricate rankings** — report "未获取" instead
5. **OpenRouter pricing API is reliable** — use as primary data source
6. **crawlee needs browserforge** — `pip install crawlee browserforge` then `playwright install`
