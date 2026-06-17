# Memory OS - Hermes Agent Memory Operating System (2026-06-05 集成)

## 概述

Memory OS 是一个专门为 Hermes Agent 设计的 7 层记忆操作系统，提供持久化记忆、结构化事实存储、智能上下文注入等功能。

**项目信息**：
- Stars: 829 (+195 stars/day)
- 语言: Python
- 许可证: MIT
- URL: https://github.com/ClaudioDrews/memory-os

## 7 层记忆架构

| 层级 | 名称 | 存储 | 功能 |
|------|------|------|------|
| 1 | Workspace | MEMORY.md, USER.md, CREATIVE.md | 每轮注入系统提示词 |
| 2 | Sessions | SQLite + FTS5 | 全文搜索对话历史 |
| 3 | Structured Facts | SQLite + HRR + FTS5 | 事实存储 + 信任评分 |
| 4 | Fabric | Icarus Plugin (fork) | 跨会话召回 + 多源注入 |
| 5 | Vector DB | Qdrant (768d Cosine) | 混合搜索 + 4级降级 |
| 6 | LLM Wiki | 自动策展 Wiki | 概念/实体/对比 |
| 7 | Ground Truth | SOUL.md, rulebook.md | 确保注入的记忆被使用 |

## 当前 Hermes 状态

```
✓ MEMORY.md: 3,673 bytes
✓ USER.md: 2,698 bytes
✓ CREATIVE.md: 738 bytes
✓ state.db: 173.2 MB (FTS5 enabled)
✓ memory_store.db: 52.0 KB
✓ SOUL.md: 1,636 bytes (Ground Truth hierarchy)
✓ Icarus Plugin: 13 files
✓ Redis: Running (docker-redis-1, port 6379)
✓ Qdrant: Running (docker-qdrant-1, port 6333)
✓ Qdrant Collection: knowledge_base (768d Cosine)
✓ Ollama: Running (nomic-embed-text, 768d, 262MB)
✓ Wiki: ~/vault/wiki/ (created)
```

## 当前集成状态 (2026-06-05 最终)

| 步骤 | 状态 | 说明 |
|------|------|------|
| 创建 CREATIVE.md | ✓ | `~/.hermes/memories/CREATIVE.md` |
| 检查 state.db FTS5 | ✓ | FTS5 已启用 |
| Ground Truth 层级 | ✓ | 已添加到 `~/.hermes/SOUL.md` |
| 克隆 Memory OS | ✓ | `~/memory-os/` |
| 部署 Qdrant + Redis | ✓ | Docker: port 6379 + 6333 |
| 集成 Icarus Plugin | ✓ | `~/.hermes/plugins/icarus/` (13 files) |
| 结构化事实存储 | ✓ | `~/.hermes/memory_store.db` (52 KB) |
| 配置 Qdrant 集合 | ✓ | `knowledge_base` (768d Cosine) |
| 配置嵌入后端 | ✓ | Ollama + nomic-embed-text (768d) |
| 创建 Wiki 目录结构 | ✓ | `~/vault/wiki/{raw,concepts,entities,...}` |
| Worker 容器 | ✗ | Docker build 失败（需解决 registry 认证） |

## 嵌入后端: Ollama

**已配置**：Ollama + nomic-embed-text (768维，262MB)

```
# ~/memory-os/.env 配置
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
EMBEDDING_DIMS=768
```

**安装**：
1. 下载 Ollama: https://ollama.com/download (~627MB)
2. `ollama pull nomic-embed-text` (~262MB)
3. 更新 Qdrant 集合维度为 768（不是 4096！）

**关键 Pitfall**: Qdrant 向量维度必须匹配嵌入模型输出。nomic-embed-text 输出 768d，不是 4096d。创建集合时维度错误会导致所有插入失败。

## 未完成步骤

1. **Worker 容器** — Docker build 失败（Python 镜像拉取 401），当前只用 Qdrant + Redis
2. **Vault Curator** — 未安装（可选，用于自动策展 Wiki）
3. **Wiki cron 任务** — 未配置（可选，用于自动摄入 Wiki 到 Qdrant）

## 关键文件位置

```
~/.hermes/
├── memories/
│   ├── MEMORY.md          # Agent 持久记忆 (§ 分隔)
│   ├── USER.md            # 用户档案
│   └── CREATIVE.md        # Agent 创造性状态 (新增)
├── plugins/
│   └── icarus/            # Icarus Plugin fork (新增)
├── state.db               # 会话数据库 (FTS5)
├── memory_store.db        # 结构化事实存储 (新增)
└── SOUL.md                # 含 Ground Truth 层级 (已修改)

~/memory-os/               # Memory OS 仓库 (新增)
├── docker/
│   └── docker-compose-simple.yml  # 简化版 (仅 Qdrant + Redis)
└── setup/
    └── setup_db.py        # 数据库初始化脚本
```

## Ground Truth 层级内容

已添加到 SOUL.md 的内容：
```markdown
## Ground Truth Hierarchy (Memory Authority)

1. Terminal output → Ground Truth for system state (runtime)
2. Injected memory [qdrant, fabric, sessions, facts] → Ground Truth for documented knowledge
3. Official documentation → Authoritative for APIs, configs, version-specifics
4. Training knowledge → Reference only; always verify against 1-3
```

## memory_store.db 表结构

```
entities          # 实体存储
facts             # 事实存储
facts_fts         # FTS5 全文搜索索引
fact_entities     # 事实-实体关联
memory_banks      # 记忆库
```

## 安装命令参考

```bash
# 克隆仓库
git clone https://github.com/ClaudioDrews/memory-os.git ~/memory-os

# 复制 Icarus Plugin
cp -r ~/memory-os/icarus/ ~/.hermes/plugins/icarus/

# 初始化数据库
cd ~/memory-os && python setup/setup_db.py

# 启动 Docker 服务 (简化版)
cd ~/memory-os/docker && docker-compose -f docker-compose-simple.yml up -d
```

## Pitfalls

| 问题 | 解决 |
|------|------|
| Docker Python 镜像拉取 401 | 使用简化 docker-compose（仅 Qdrant + Redis），跳过 Worker |
| .env.example 不存在 | 手动创建 .env，使用 `secrets.token_urlsafe(32)` 生成 Redis 密码 |
| python:3.12-slim 拉取失败 | 改用 python:3.11-slim |
| Qdrant 维度不匹配 | nomic-embed-text 输出 768d，不是 4096d。必须创建正确维度的集合 |
| Ollama 安装后不在 PATH | 完整路径: `C:/Users/<user>/AppData/Local/Programs/Ollama/ollama.exe` |
| Agent 忽略注入的记忆 | 必须添加 Layer 7 (Ground Truth) 到 SOUL.md |
| Icarus 覆盖 MEMORY.md | Icarus 现在写入 CREATIVE.md（fork 已修复） |
| `import os` 缺失 | `_calc_daily_avg_growth` 使用 `os.path.exists()` 但模块顶部未 import |

## References

- GitHub: https://github.com/ClaudioDrews/memory-os
- Layer 7 文档: https://github.com/ClaudioDrews/memory-os/blob/main/layers/07-ground-truth.md
- 安装指南: https://github.com/ClaudioDrews/memory-os/blob/main/setup/install.md
