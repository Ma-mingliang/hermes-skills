# MCP Server 安装模式

## 概述

安装自定义 MCP Server 到 Hermes 的标准流程。

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/<owner>/<repo>.git D:\openclaw-hermes\<repo>
```

### 2. 配置 Hermes

在 `~/.hermes/config.yaml` 的 `mcp_servers` 部分添加：

```yaml
mcp_servers:
  <server-name>:
    command: python
    args:
    - "D:\\openclaw-hermes\\<repo>\\server.py"
    env:
      API_KEY: ${API_KEY}
      BASE_URL: https://api.example.com/v1
```

### 3. 配置环境变量

在 `~/.hermes/.env` 中添加：

```bash
API_KEY=your_api_key_here
```

### 4. 重启 Gateway

```bash
hermes gateway restart
```

## 示例：mcp-image-reader

```yaml
mcp_servers:
  image-reader:
    command: python
    args:
    - "D:\\openclaw-hermes\\mcp-image-reader\\server.py"
    env:
      MIMO_API_KEY: ${MIMO_API_KEY}
      MIMO_BASE_URL: https://token-plan-sgp.xiaomimimo.com/v1
```

## 注意事项

1. 确保 Python 路径正确
2. 确保环境变量已配置
3. 重启 Gateway 后生效
4. 在新的会话中测试 MCP Server
