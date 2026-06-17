---
name: hindsight-memory
description: "Hindsight Agent记忆系统 - 为Hermes提供长期记忆和学习能力"
version: "1.2.0"
stars: 15147
url: "https://github.com/vectorize-io/hindsight"
---

# Hindsight Memory Skill

为 Hermes Agent 提供长期记忆和学习能力的记忆系统。

## Stars: ⭐15,147

## URL: https://github.com/vectorize-io/hindsight

## 功能特点

- **学习而非记忆**：不仅回忆对话历史，还能从经验中学习
- **超越RAG和知识图谱**：消除传统技术的局限性
- **最先进的性能**：在LongMemEval基准测试中达到SOTA
- **生产级**：已在财富500强企业中使用

## Docker 部署（推荐）

### 启动容器

```bash
docker run -d --name hindsight \
  -e HINDSIGHT_API_LLM_PROVIDER=openai \
  -e HINDSIGHT_API_LLM_API_KEY=<your-api-key> \
  -e HINDSIGHT_API_LLM_BASE_URL=<your-base-url> \
  -e HINDSIGHT_API_LLM_MODEL=<your-model-name> \
  -e HINDSIGHT_API_HOST=0.0.0.0 \
  -e HINDSIGHT_API_PORT=8888 \
  -e HINDSIGHT_API_LOG_LEVEL=info \
  -e HINDSIGHT_ENABLE_API=true \
  -e HINDSIGHT_ENABLE_CP=true \
  -e HINDSIGHT_CP_DATAPLANE_API_URL=http://localhost:8888 \
  -p 8888:8888 -p 9999:9999 \
  ghcr.io/vectorize-io/hindsight:latest
```

### Pitfall: Storage timeout — POST /memories needs 60s+ timeout
The `POST /memories` endpoint runs LLM-powered retain/extraction inline before returning.
On first-generation runs it can exceed 30s. Set client-side timeout to **60s or higher**,
or check `/v1/default/banks/{bank_id}/operations` for async completion status.

### Pitfall: LLM_MODEL environment variable is REQUIRED
Without `HINDSIGHT_API_LLM_MODEL`, Hindsight defaults to `gpt-4o-mini` which
fails on non-OpenAI providers. Always set the model name explicitly.

**Symptom**: Reflect endpoint (`POST /reflect`) times out (60s+) with no error body.
The LLM call silently fails because the default model name doesn't match the provider's
catalog. Store/recall still work (they don't need LLM), making this easy to miss in
health checks that skip the reflect step. Fix: set `HINDSIGHT_API_LLM_MODEL=mimo-v2.5-pro`
(or appropriate model) in `.env` and restart the container.

### Pitfall: Provider must be "openai" for compatible APIs
For Xiaomi MiMo, DeepSeek, or any OpenAI-compatible API, set
`HINDSIGHT_API_LLM_PROVIDER=openai` (not "xiaomi" or "deepseek").

### Pitfall: Metadata values must be strings
All metadata values in the `items` array MUST be strings. Booleans like `true`
cause Pydantic validation error: "Input should be a valid string". Use `"true"` instead.
```json
{"items": [{"content": "...", "metadata": {"test": "true"}}]}
```

### Pitfall: Multiple .env files cause config drift
If both `.env` and `config.env` exist in `~/.hindsight/`, they may contain
different `HINDSIGHT_API_LLM_BASE_URL` values. Hindsight loads whichever the
Docker invocation sources — the dormant file silently rots. Keep a single
`.env` and delete any stale `config.env` / `config.yaml` / `settings.env`.

### Pitfall: read_file tool fails on Windows for ~/.hindsight paths
On Windows, the `read_file` tool may not resolve `~/.hindsight/.env` correctly.
Use `execute_code` with `os.path.expanduser('~/.hindsight/.env')` for all
config file reads. This also applies to listing directory contents — use
`os.listdir(os.path.expanduser('~/.hindsight'))` instead of `search_files`.

### Pitfall: Docker compose/run MUST include HINDSIGHT_API_LLM_MODEL
Even though the container may default to a model that happens to work,
`HINDSIGHT_API_LLM_MODEL` is mandatory per Hindsight docs. Without it,
version upgrades can break silently when the default changes. Always set:
```yaml
environment:
  - HINDSIGHT_API_LLM_MODEL=mimo-v2.5-pro  # required
```

### Prometheus metrics for deep inspection
`GET /metrics` exposes full operational telemetry (~75KB) — LLM call counts/timing
by scope (`retain_extract_facts`, `consolidation`, `reflect_tool_call`),
HTTP request totals by endpoint and status class, DB pool stats, process
memory/CPU. Use it to confirm the LLM backend is live without making a
direct provider call. A reusable monitoring script is at `scripts/monitor.py`.

### Pitfall: Python SDK recall() uses max_tokens, NOT limit
The `recall()` method accepts `max_tokens` (default 4096) and `budget` ("low"/"mid"/"high").
Passing `limit=` raises "unexpected keyword argument 'limit'". HTTP API uses `max_tokens` too.

## API Endpoints (v0.7.1+)

The documented `/retain` and `/recall` endpoints are WRONG for current versions.
Actual endpoints use `/v1/default/banks/{bank_id}/memories`:

| Action | Method | Endpoint |
|--------|--------|----------|
| Store memories | POST | `/v1/default/banks/{bank_id}/memories` |
| Recall memories | POST | `/v1/default/banks/{bank_id}/memories/recall` |
| List memories | GET | `/v1/default/banks/{bank_id}/memories/list` |
| Get memory | GET | `/v1/default/banks/{bank_id}/memories/{memory_id}` |
| Health check | GET | `/health` |
| Version info | GET | `/version` — returns `api_version` and `features` dict |
| API docs | GET | `/docs` |
| OpenAPI spec | GET | `/openapi.json` |
| Bank stats | GET | `/v1/default/banks/{bank_id}/stats` |
| Reflect (deep query) | POST | `/v1/default/banks/{bank_id}/reflect` |
| List banks | GET | `/v1/default/banks` |
| Bank config | GET | `/v1/default/banks/{bank_id}/config` |

> **Endpoint discovery**: `/openapi.json` is the canonical source of truth. When in doubt, fetch it —
> Hindsight's API surface evolves across versions and the spec lists every available path and method.

### Reflect — LLM-driven deep memory query

The `reflect` endpoint runs a full LLM-powered analysis over relevant memories. It returns a
synthesized report, not just a ranked list. Use it for status checks, summaries, and complex
questions that require reasoning over stored facts.

```bash
curl -X POST http://localhost:8888/v1/default/banks/hermes/reflect \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the current status of the system?", "budget": "low"}'
```

### Stats — bank-level metrics for monitoring

```bash
curl http://localhost:8888/v1/default/banks/hermes/stats
# Returns: total_nodes, total_links, total_documents, operations_by_status,
#          pending_operations, failed_operations, last_consolidated_at, etc.
```

### Store memory (HTTP)
```bash
curl -X POST http://localhost:8888/v1/default/banks/hermes/memories \
  -H "Content-Type: application/json" \
  -d '{"items": [{"content": "用户喜欢简洁的中文回答"}]}'
```
Note: request body MUST use `items` array format, not bare `content`/`metadata`.

### Recall memories (HTTP)
```bash
curl -X POST http://localhost:8888/v1/default/banks/hermes/memories/recall \
  -H "Content-Type: application/json" \
  -d '{"query": "用户偏好", "limit": 5}'
```

## Python SDK

```bash
pip install hindsight-client
```

```python
from hindsight_client import Hindsight

client = Hindsight(base_url="http://localhost:8888")

# Store - uses retain()
result = client.retain(bank_id="hermes", content="用户喜欢简洁的中文回答")
# result.success == True, result.bank_id == "hermes"

# Recall - uses max_tokens, NOT limit
results = client.recall(bank_id="hermes", query="用户偏好", max_tokens=4096, budget="mid")
# results.results is list of RecallResult(id, text, type)
for r in results.results:
    print(r.text, r.type)  # type: "experience", "world", "opinion", "observation"
```

The Python SDK handles the correct endpoint format automatically — prefer it over raw HTTP.

## Integration with Hermes

### Environment variables for Hermes config
Add to `~/.hermes/.env`:
```
HINDSIGHT_URL=http://localhost:8888
HINDSIGHT_BANK_ID=hermes
```

### Hermes config.yaml integration
To enable Hindsight as the memory provider in Hermes:
```yaml
memory:
  provider: hindsight
  hindsight_enabled: true

hindsight:
  enabled: true
  base_url: "http://localhost:8888"
  default_bank_id: "hermes"
  auto_store: true
  auto_recall: true
  learning_enabled: true
```
Then restart the gateway for changes to take effect.

### Session lifecycle integration
```python
from hindsight_client import Hindsight

client = Hindsight(base_url="http://localhost:8888")

# On session start: recall relevant memories
def on_session_start(query):
    return client.recall(bank_id="hermes", query=query)

# On session end: store conversation summary
def on_session_end(summary):
    client.retain(bank_id="hermes", content=summary)
```

## System Health Monitoring

Run this 4-point check to verify the full Hindsight stack:

1. **Service liveness** — `GET /health` (expect 200), `GET /docs` (Swagger UI)
2. **API surface** — `GET /openapi.json` → extract endpoints, confirm expected paths exist
3. **Storage + retrieval** — `POST /memories` (store test), `POST /memories/recall` (semantic search), `POST /reflect` (LLM query)
4. **LLM backend** — Check `/metrics` for LLM call success counters (fast, no auth needed) or direct provider chat/completions call

> **Critical**: Health checks 1-3 can all pass while the LLM is misconfigured. Only `reflect` and `store` exercise the chat/completion model. If they timeout, verify the model exists on the provider via `GET {BASE_URL}/models` — see `references/monitoring-guide.md` for the full diagnostic workflow.

A reusable monitoring script is at `scripts/monitor.py` — run it directly or as a cron job:
```bash
python scripts/monitor.py          # human-readable report
python scripts/monitor.py --json   # machine-readable
python scripts/monitor.py --store --reflect  # full 7-point check
```
A complete monitoring recipe is in `references/monitoring-guide.md`.

## References

- [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) - 主仓库
- [mage0535/hermes-memory-installer](https://github.com/mage0535/hermes-memory-installer) - Hermes记忆安装器
- `references/hindsight-integration.md` - Full integration module details, config, and file structure
- `references/monitoring-guide.md` - Health-check recipe, Python monitor script, metrics thresholds
