# 2026-06-03 工具安装记录

## Obsidian 集成

### obsidian-second-brain (⭐1931)
- 仓库：`D:\openclaw-hermes\obsidian-second-brain`
- Skill位置：`~/.hermes/skills/obsidian-second-brain/`
- Vault位置：`D:\ObsidianVault`
- 功能：将 Obsidian vault 变成自进化的"第二大脑"，43 个命令
- 安装：git clone + 手动复制到 skills 目录
- 配置：`~/.hermes/.env` 中添加 `OBSIDIAN_VAULT_PATH=D:\ObsidianVault`
- 使用：vault 已 bootstrap，包含 Boards/daily/notes/templates 等目录

### Obsidian 应用
- 安装包：`D:\Obsidian-Setup.exe`（v1.8.10，51MB）
- 需要手动运行安装

## SkillOpt (Microsoft, ⭐4619)
- 仓库：`D:\openclaw-hermes\SkillOpt`
- PyPI：`pip install skillopt`（v0.1.0）
- 功能：优化自然语言 skill 文档（SKILL.md），不优化代码
- CLI：`skillopt-train`、`skillopt-eval`
- 配置：`D:\openclaw-hermes\SkillOpt\.env` 已配置使用 mimo-v2.5-pro
- 核心效果：GPT-5.5 上准确率提升 +23.5（直接聊天）、+24.8（Codex CLI）、+19.1（Claude Code）

## mcp-image-reader
- 仓库：`D:\openclaw-hermes\mcp-image-reader`
- 功能：将 mimo-v2.5 的图片理解能力封装为 MCP Tool
- 技术栈：Python 3.9，零外部依赖
- 配置：已添加到 `~/.hermes/config.yaml` 的 `mcp_servers` 部分
- API：使用 MIMO_API_KEY（从 XIAOMI_API_KEY 复制）
- 工具：`describe_image`（参数：image_path, prompt）

## 微信限流经验（2026-06-02-03）
- iLink 账户级限流（ret=-2）：连续 3+ 条消息触发，需等 2-6 小时
- 正确做法：合并为 2-3 条长消息（3000-4000 字符/条），不要拆分 10+ 条短消息
- 限流后不要每 30 秒重试，会加剧限流
- 解决方案：等 2 小时后用 cron job 定时重发

## GitHub Issue 解决方案
### mimo-v2.5-pro "selected model" 错误
- 根因：OpenGateway 中间件剥离 Authorization header（当请求包含图片时）
- 触发条件：在对话中使用了图片（Read 工具、mcp-chrome-tool 截图等）
- 解决方案：
  1. 避免在 mimo-v2.5-pro 下读取图片
  2. 新开一个不带图片历史的对话
  3. 使用 mimo-v2.5（非 pro 版本）
  4. 直接调用小米 API（绕过 OpenGateway）— Hermes 已配置为直连
- 关联 issue：Gitlawb/openclaude#1343, #1362; anthropics/claude-code#62487
