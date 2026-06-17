# MiMo v2.5 Pro 图片处理问题

## 问题描述

使用 mimo-v2.5-pro 时，如果对话中包含图片（Read 工具读取图片、mcp-chrome-tool 截图等），会报错：

```
There's an issue with the selected model (mimo-v2.5-pro). It may not exist or you may not have access to it. Run /model to pick a different model.
```

## 根本原因

OpenGateway 中间件 bug（Gitlawb/openclaude#1362）：当请求包含图片内容时，中间件会**剥离 Authorization header**，导致 401 认证失败。

## 触发条件

1. 在 mimo-v2.5 下读取图片
2. 切换到 mimo-v2.5-pro
3. 发送任何内容 → 报错

## 解决方案

| 方案 | 操作 | 适用场景 |
|------|------|---------|
| **临时修复** | `/model` 切回 mimo-v2.5 | 纯文本模型不受影响 |
| **临时修复** | 新开一个对话（不带图片历史） | 已触发 bug 后 |
| **临时修复** | 避免在 mimo-v2.5 下读取图片 | 用其他模型处理图片 |
| **根本修复** | 直接调用小米 API（绕过 OpenGateway） | 有小米 API key 时 |

## Hermes 配置（已解决）

Hermes 直接调用小米 API（`https://token-plan-sgp.xiaomimimo.com/v1`），不经过 OpenGateway，所以这个 bug 不影响。

## 关联 Issue

- Gitlawb/openclaude#1362 — OpenGateway 中间件剥离 Authorization header（根因）
- Gitlawb/openclaude#1345 — OpenGateway 撤回了免费模型 mimo-v2.5
- Gitlawb/openclaude#1344 — OpenGateway 仍拒绝 ogw_live key
- anthropics/claude-code#62487 — claude-code 仓库的相同 bug 报告

## mcp-image-reader 解决方案

已安装 `D:\openclaw-hermes\mcp-image-reader`，将 mimo-v2.5 的图片理解能力封装为 MCP Tool。

配置：
- 命令：`python D:\openclaw-hermes\mcp-image-reader\server.py`
- 环境变量：`MIMO_API_KEY`, `MIMO_BASE_URL`

使用方法：
```
请读取 C:\path\to\image.png 的内容
```
