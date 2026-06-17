# Hindsight Memory System Docker Setup

**Date**: 2026-05-30  
**Status**: Working configuration with mimo-v2.5-pro

## Docker Container

```bash
docker run -d --name hindsight \
  -e HINDSIGHT_API_LLM_PROVIDER=openai \
  -e HINDSIGHT_API_LLM_API_KEY=tp-s48...drjv \
  -e HINDSIGHT_API_LLM_BASE_URL=https://token-plan-sgp.xiaomimimo.com/v1 \
  -e HINDSIGHT_API_LLM_MODEL=mimo-v2.5-pro \
  -e HINDSIGHT_API_HOST=0.0.0.0 \
  -e HINDSIGHT_API_PORT=8888 \
  -e HINDSIGHT_API_LOG_LEVEL=info \
  -e HINDSIGHT_ENABLE_API=true \
  -e HINDSIGHT_ENABLE_CP=true \
  -e HINDSIGHT_CP_DATAPLANE_API_URL=http://localhost:8888 \
  -p 8888:8888 -p 9999:9999 \
  ghcr.io/vectorize-io/hindsight:latest
```

## Key Configuration Notes

1. **Provider**: Must be `openai` (OpenAI-compatible mode)
2. **Model**: Must match an available model in the provider's list
3. **Port 8888**: API service
4. **Port 9999**: Control plane (web UI)

## Python SDK

```python
from hindsight_client import Hindsight

client = Hindsight(base_url="http://localhost:8888")

# Store memory
client.retain(bank_id="hermes", content="用户喜欢简洁的中文回答")

# Recall memory
results = client.recall(bank_id="hermes", query="用户偏好")
```

## API Endpoints

- `GET /health` — Health check
- `GET /version` — Version info
- `POST /v1/default/banks/{bank_id}/memories` — Store memory
- `POST /v1/default/banks/{bank_id}/memories/recall` — Recall memory
- `GET /docs` — API documentation

## Common Issues

### 1. Model not supported
**Error**: `Not supported model gpt-4o-mini`  
**Fix**: Set `HINDSIGHT_API_LLM_MODEL` to a model supported by your provider

### 2. Connection timeout
**Error**: `Read timed out`  
**Fix**: Increase timeout in Python SDK or use async client

### 3. Memory store format
**Error**: `Field required: items`  
**Fix**: Use `items` array format:
```python
{"items": [{"content": "...", "metadata": {...}}]}
```

## Integration with Hermes

The Hindsight client is integrated into `~/.hermes/hindsight/client.py`:
- `store_conversation_memory(content)` — Store conversation
- `recall_relevant_memories(query)` — Recall memories
- `learn_user_preferences(conversation)` — Learn from conversation
