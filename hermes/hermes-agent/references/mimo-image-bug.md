# mimo-v2.5-pro 图片输入 Bug

## 问题描述
当对话中包含图片时，mimo-v2.5-pro 会报错：
"There's an issue with the selected model (mimo-v2.5-pro). It may not exist or you may not have access to it. Run /model to pick a different model."

## 根因
OpenGateway 中间件在请求包含图片内容时剥离 Authorization header，导致 401 认证失败。

## 触发条件
- 在对话中使用了图片（Read 工具读取图片、mcp-chrome-tool 截图等）
- 切换到 mimo-v2.5-pro 后，即使发纯文本也会报错（因为对话历史中包含图片数据）

## 解决方案

| 方案 | 操作 | 说明 |
|------|------|------|
| 避免图片 | 不在 mimo-v2.5-pro 下读取图片/截图 | 所有场景 |
| 新开对话 | 新开一个不带图片历史的对话 | 已触发 bug 后 |
| 用 mimo-v2.5 | 使用非 pro 版本（不支持图片但不会报错） | 不需要图片时 |
| mcp-image-reader | 用 mimo-v2.5（非 pro）处理图片 | 需要图片能力时 |
| 绕过 OpenGateway | 直接调用小米 API | Hermes 已配置此方式 |

## 相关 Issue
- Gitlawb/openclaude#1343 — 同样的错误报告
- Gitlawb/openclaude#1362 — OpenGateway 中间件 bug（根因）
- anthropics/claude-code#62487 — Claude Code 仓库的相同 bug

## Hermes 的情况
Hermes 直接调用小米 API（`https://token-plan-sgp.xiaomimimo.com/v1`），不经过 OpenGateway，所以这个 bug 不影响 Hermes。
但如果使用 CC Switch 等第三方工具通过 OpenGateway 调用，则会遇到此问题。
