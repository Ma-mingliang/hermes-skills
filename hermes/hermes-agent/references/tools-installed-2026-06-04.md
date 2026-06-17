# 2026-06-04 工具安装记录

## 1. Obsidian + obsidian-second-brain

**安装内容：**
- Obsidian v1.8.10 安装包：`D:\Obsidian-Setup.exe`
- obsidian-second-brain skill：`~/.hermes/skills/obsidian-second-brain/`
- Obsidian Vault：`D:\ObsidianVault`

**Vault 结构：**
```
D:\ObsidianVault\
├── .obsidian/
├── Boards/
├── daily/
├── notes/
├── templates/
├── Projects/
├── People/
├── Tasks/
├── Knowledge/
├── Goals/
├── Mentions/
├── _CLAUDE.md
└── Home.md
```

**配置：**
- OBSIDIAN_VAULT_PATH=D:\ObsidianVault（已添加到 .env）

## 2. SkillOpt（Microsoft）

**安装内容：**
- 仓库：`D:\openclaw-hermes\SkillOpt`（4619 ⭐）
- PyPI 包：`skillopt 0.1.0`

**CLI 命令：**
- `skillopt-train` — 训练优化 skill
- `skillopt-eval` — 评估 skill 效果

**配置：**
- 使用 mimo-v2.5-pro 作为优化器和目标模型
- .env 已配置 AZURE_OPENAI_ENDPOINT、AZURE_OPENAI_API_KEY、AZURE_OPENAI_AUTH_MODE

**用途：** 优化 agent-daily-report 的 9 个 Agent 提示词

## 3. mcp-image-reader

**安装内容：**
- 仓库：`D:\openclaw-hermes\mcp-image-reader`
- MCP server 配置已添加到 config.yaml

**配置：**
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

**功能：** 将 mimo-v2.5 的图片理解能力封装为 MCP Tool

## 4. DeepSeek V4 Pro 移除

**移除内容：**
- config.yaml：删除了注释掉的 model/provider 行
- auth.json：删除了 credential_pool 中的 deepseek 条目
- .env：删除了 DEEPSEEK_API_KEY、DEEPSEEK_BASE_URL

**原因：** 用户明确要求从模型调用列表中移除（余额不足 402）

## 5. mimo-v2.5-pro 图片处理问题

**问题：** 使用图片时出现 "model not found" 错误
**根因：** OpenGateway 中间件剥离 Authorization header
**解决方案：** 直接调用小米 API（不经过 OpenGateway）
**Hermes 配置已是最优：** https://token-plan-sgp.xiaomimimo.com/v1

**关联 issue：**
- Gitlawb/openclaude#1343
- Gitlawb/openclaude#1362
- anthropics/claude-code#62487
