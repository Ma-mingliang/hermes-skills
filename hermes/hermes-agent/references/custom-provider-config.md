# 自定义 Provider 配置

## 概述

配置自定义 OpenAI-compatible provider 到 Hermes。

## 配置步骤

### 1. 在 config.yaml 中添加 provider

```yaml
providers:
  custom-provider-name:
    base_url: https://api.example.com/v1
    api_key_env: CUSTOM_API_KEY
    api_mode: openai
```

### 2. 在 .env 中添加 API Key

```bash
CUSTOM_API_KEY=your_api_key_here
```

### 3. 重启 Gateway

```bash
hermes gateway restart
```

## 示例：MiMo v2.5 Pro 备用配置

```yaml
providers:
  mimo-backup:
    base_url: https://api.xiaomimimo.com/v1
    api_key_env: MIMO_BACKUP_API_KEY
    api_mode: openai
```

```bash
# .env
MIMO_BACKUP_API_KEY=sk-c8e3k25tk32gghhnzl723as518o3wf21loaqzfke8q4py3do
```

## 注意事项

1. base_url 必须是 OpenAI-compatible API
2. api_mode 通常为 `openai`
3. 重启 Gateway 后生效
4. 可以配置多个备用 provider
