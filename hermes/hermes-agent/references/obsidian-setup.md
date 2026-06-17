# Obsidian 集成配置

## 安装信息
- Obsidian v1.8.10 安装包：`D:\Obsidian-Setup.exe`
- obsidian-second-brain skill：`~/.hermes/skills/obsidian-second-brain/`（⭐1931）

## Vault 配置
- 路径：`D:\ObsidianVault`
- 环境变量：`OBSIDIAN_VAULT_PATH=D:\ObsidianVault`（在 `~/.hermes/.env`）

## Vault 结构
```
D:\ObsidianVault\
├── .obsidian/          # 配置
├── Boards/             # 看板（Work/Personal）
├── daily/              # 每日笔记
├── notes/              # 笔记
├── templates/          # 模板（Daily Note, Project, Person, Task 等）
├── Projects/           # 项目
├── People/             # 人物
├── Tasks/              # 任务
├── Knowledge/          # 知识库
├── Goals/              # 目标
├── Mentions/           # 提及记录
├── _CLAUDE.md          # AI 配置文件
└── Home.md             # 首页
```

## 使用方法
- "把今天的日报整理到 Obsidian"
- "在 Obsidian 中创建一个新笔记"
- "搜索 Obsidian vault 中的内容"

## Skill 功能（43 个命令）
- /obsidian-init — 初始化 vault
- /obsidian-architect — 扫描代码库生成架构笔记
- /research — AI 研究并保存到 vault
- /daily — 创建每日笔记
- 详见 obsidian-second-brain 的 SKILL.md
