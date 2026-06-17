# Memory OS Integration Guide

Integrated: 2026-06-06
Components: Ollama + Qdrant + Redis + Icarus Plugin

## Architecture

```
Ollama (nomic-embed-text, 768d) → Qdrant (vector DB) → Icarus Plugin (Hermes)
                                      ↑
Redis (job queue) ←───────────────────┘
```

## Setup Steps

### 1. Install Ollama
```bash
# Download from https://ollama.com/download
# Install, then:
ollama pull nomic-embed-text  # 274MB, 768 dimensions
```

### 2. Start Qdrant + Redis (Docker)
```yaml
# docker-compose-simple.yml
services:
  redis:
    image: redis:7-alpine
    ports: ["127.0.0.1:6379:6379"]
  qdrant:
    image: qdrant/qdrant:v1.17.1
    ports: ["127.0.0.1:6333:6333"]
    volumes: [qdrant_data:/qdrant/storage]
```

### 3. Create Qdrant Collection
```python
import requests
requests.put("http://localhost:6333/collections/knowledge_base", json={
    "vectors": {"dense": {"size": 768, "distance": "Cosine"}},
    "sparse_vectors": {"sparse": {}}
})
```

### 4. Install Icarus Plugin
```bash
cp -r memory-os/icarus/ ~/.hermes/plugins/icarus/
```

### 4b. Enable Icarus Plugin (CRITICAL — often missed)
Plugin files in `~/.hermes/plugins/icarus/` are NOT auto-discovered. Must explicitly enable:
```yaml
# config.yaml
plugins:
  enabled:
    - icarus
```
Then restart gateway for changes to take effect.

**Pitfall**: Installing plugin files alone does nothing. Without `plugins.enabled: [icarus]`, the plugin is invisible to Hermes.

### 5. Add Ground Truth Hierarchy to SOUL.md
```markdown
## Ground Truth Hierarchy
1. Terminal output → Ground Truth for system state
2. Injected memory [qdrant, fabric, sessions, facts] → Ground Truth for documented knowledge
3. Official documentation → Authoritative
4. Training knowledge → Reference only
```

### 6. Create memory_store.db
```bash
python memory-os/setup/setup_db.py
```

### 7. Configure .env
```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
EMBEDDING_DIMS=768
```

## Verification
```python
import requests
# Test embedding
resp = requests.post("http://localhost:11434/api/embeddings",
    json={"model": "nomic-embed-text", "prompt": "test"})
assert resp.status_code == 200
assert len(resp.json()["embedding"]) == 768

# Test Qdrant
resp = requests.get("http://localhost:6333/collections/knowledge_base")
assert resp.status_code == 200
```

## Running Docker Stack (Verified 2026-06-16)

All Memory OS services run as Docker containers managed by Docker Desktop (`com.docker.backend`):

| Container | Image | Ports | Purpose |
|-----------|-------|-------|---------|
| `hindsight` | `ghcr.io/vectorize-io/hindsight:latest` | 8888 (API), 9999 (UI) | Memory engine (Hindsight) |
| `docker-redis-1` | `redis:7-alpine` | 127.0.0.1:6379 | Job queue / cache |
| `docker-qdrant-1` | `qdrant/qdrant:v1.17.1` | 127.0.0.1:6333 | Vector DB (768d Cosine) |

**GitHub**: https://github.com/vectorize-io/hindsight

**Actual deployment config** (`~/.hindsight/docker-compose.yml`):
```yaml
version: '3.8'
services:
  hindsight:
    image: ghcr.io/vectorize-io/hindsight:latest
    container_name: hindsight
    restart: unless-stopped
    ports:
      - "8888:8888"
      - "9999:9999"
    environment:
      - HINDSIGHT_API_LLM_API_KEY=<MiMo API key>
      - HINDSIGHT_API_LLM_BASE_URL=https://token-plan-sgp.xiaomimimo.com/v1
    volumes:
      - ./data:/home/hindsight/.pg0
```

**Key**: Hindsight uses MiMo API as its LLM backend (for memory extraction/consolidation), NOT Ollama. Ollama is only used for embeddings (nomic-embed-text, 768d).

**Diagnosis command** (use `execute_code`, not terminal — WSL relay may be broken):
```python
import subprocess
result = subprocess.run(['powershell', '-Command',
    'docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"'],
    capture_output=True, text=True, shell=True)
print(result.stdout)
```

**Port check** (pure Python, no shell needed):
```python
import socket
for port, name in [(8888,'Hindsight'), (6379,'Redis'), (6333,'Qdrant')]:
    s = socket.socket(); s.settimeout(2)
    try: s.connect(('127.0.0.1', port)); print(f"✅ {name}:{port}")
    except: print(f"❌ {name}:{port}")
    finally: s.close()
```

**Pitfall**: Port 8888 shows TWO listeners — PID 8000 (Docker Desktop) and PID 24412 (wslrelay). This is normal; Docker Desktop proxies container ports through wslrelay.

**Hindsight API health check**:
```python
import requests
resp = requests.get("http://localhost:8888/health", timeout=5)
print(resp.json())  # {"status": "healthy", "database": "connected"}
resp = requests.get("http://localhost:8888/version", timeout=5)
print(resp.json())  # API version, features list
```

**Hindsight UI**: http://localhost:9999/zh-CN/dashboard (Control Plane)

## MCP Server (GitHub)

The local MCP server for GitHub runs as node processes:
```
PID 15964: npx -y @modelcontextprotocol/server-github
PID 39956: node @modelcontextprotocol/server-github/dist/index.js
```
Configured in `~/.hermes/config.yaml` under `mcp_servers`.

## Pitfalls
- EMBEDDING_DIMS must match actual model output (768 for nomic-embed-text, not 4096)
- Qdrant collection must be recreated if dimension changes
- Ollama service must be running before embedding calls
- Windows: Ollama installs to C:/Users/<user>/AppData/Local/Programs/Ollama by default
- **Icarus not loaded**: Files in plugins dir are not auto-discovered. Must add to `plugins.enabled` in config.yaml
- **Docker Desktop not running**: All 3 containers (Hindsight, Redis, Qdrant) require Docker Desktop. Start it and wait 30-60s for daemon before `docker-compose up -d`

## Full Verification Checklist

After setup, run this to verify all components:
```python
import requests, socket, os, sys

# 1. Qdrant
resp = requests.get("http://localhost:6333/collections/knowledge_base", timeout=5)
assert resp.status_code == 200, f"Qdrant: {resp.status_code}"
vectors = resp.json().get("result", {}).get("vectors_count", 0)
print(f"✅ Qdrant: collection exists, {vectors} vectors")

# 2. Ollama embedding
resp = requests.post("http://localhost:11434/api/embeddings",
    json={"model": "nomic-embed-text", "prompt": "test"}, timeout=30)
assert resp.status_code == 200
dims = len(resp.json().get("embedding", []))
assert dims == 768, f"Expected 768d, got {dims}d"
print(f"✅ Ollama: nomic-embed-text, {dims}d")

# 3. Redis
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1', 6379))
sock.close()
assert result == 0, "Redis port 6379 closed"
print("✅ Redis: port 6379 open")

# 4. Icarus Plugin importable + all tools present
sys.path.insert(0, os.path.expanduser("~/.hermes/plugins"))
import icarus
expected = ['fabric_recall','fabric_write','fabric_search','fabric_pending',
            'fabric_curate','fabric_export','fabric_train','fabric_train_status',
            'fabric_models','fabric_eval','fabric_switch_model','fabric_rollback_model',
            'fabric_brief','fabric_telemetry','fabric_init_obsidian','fabric_report']
available = [t for t in expected if hasattr(icarus.tools, t)]
assert len(available) == 16, f"Icarus: {len(available)}/16 tools"
print(f"✅ Icarus: {len(available)} tools available")

# 5. SOUL.md has Ground Truth
soul_path = os.path.expanduser("~/.hermes/SOUL.md")
with open(soul_path, 'r', encoding='utf-8') as f:
    assert "Ground Truth" in f.read(), "SOUL.md missing Ground Truth"
print("✅ SOUL.md: Ground Truth hierarchy present")
```
