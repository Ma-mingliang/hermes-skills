# Hindsight Agent记忆系统集成指南

## 概述

Hindsight是一个Agent记忆系统，专注于"学习而非记忆"。它能让Agent从经验中学习，而不仅仅是记住对话历史。

**Stars**: ⭐15,147  
**License**: MIT  
**URL**: https://github.com/vectorize-io/hindsight

## 核心特点

| 特点 | 说明 |
|------|------|
| **学习而非记忆** | 不仅回忆对话历史，还能从经验中学习 |
| **超越RAG和知识图谱** | 消除了传统技术的局限性 |
| **最先进的性能** | 在LongMemEval基准测试中达到SOTA |
| **生产级** | 已在财富500强企业中使用 |

## 安装方式

### 方式1：Python客户端（推荐）

```bash
pip install hindsight-client -U
```

### 方式2：Docker（推荐用于服务端）

```bash
docker run --rm -it --pull always -p 8888:8888 -p 9999:9999 \
  -e HINDSIGHT_API_LLM_API_KEY=your-api-key \
  -e HINDSIGHT_API_LLM_BASE_URL=https://api.xiaomi.com/v1 \
  -v $HOME/.hindsight-docker:/home/hindsight/.pg0 \
  ghcr.io/vectorize-io/hindsight:latest
```

### 方式3：本地安装

```bash
pip install hindsight-api
hindsight serve --port 8888
```

## 支持的LLM Provider

Hindsight支持以下LLM Provider：
- openai（OpenAI兼容接口）
- anthropic
- gemini
- groq
- ollama
- lmstudio
- minimax

## MiMo v2.5 Pro集成

MiMo使用OpenAI兼容接口，配置如下：

```bash
export HINDSIGHT_API_LLM_PROVIDER=openai
export HINDSIGHT_API_LLM_API_KEY=your-mimo-api-key
export HINDSIGHT_API_LLM_BASE_URL=https://api.xiaomi.com/v1
```

## 与Hermes集成

### 方案1：使用hermes-memory-installer

```bash
git clone https://github.com/mage0535/hermes-memory-installer.git
cd hermes-memory-installer
python3 installer/install.py
```

### 方案2：手动集成

1. 安装hindsight-client
2. 配置Hindsight服务
3. 在Hermes配置中添加Hindsight端点

### 方案3：LLM Wrapper（最简单）

```python
from hindsight_client import Hindsight

client = Hindsight(base_url="http://localhost:8888")
client.retain(bank_id="my-bank", content="Alice works at Google")
```

## 代价分析

| 使用方式 | 代价 | 适用场景 |
|----------|------|----------|
| **开源版本** | 免费，需要技术能力 | 开发者、技术团队 |
| **Hindsight Cloud** | 付费，具体价格未知 | 企业用户、快速部署 |
| **自托管部署** | 免费，但需要服务器资源 | 数据敏感用户 |

## 相关项目

- [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) - 主仓库
- [mage0535/hermes-memory-installer](https://github.com/mage0535/hermes-memory-installer) - Hermes一键安装器
- [hi-ogawa/gbrain](https://github.com/hi-ogawa/gbrain) - 大脑记忆存储

## 注意事项

1. **API Key安全**：不要在代码中硬编码API Key
2. **服务端口**：默认8888（API）和9999（UI）
3. **数据持久化**：使用Docker时挂载卷以持久化数据
4. **模型选择**：MiMo v2.5 Pro适合中文场景
