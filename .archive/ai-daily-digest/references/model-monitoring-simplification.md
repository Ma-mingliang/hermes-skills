# 模型监控简化方案（2026-05-31用户确认）

## 背景

原方案要求日报自动抓取三个层级的模型数据：
1. 模型官网（9个厂商）
2. 排名网站（artificialanalysis.ai、lmarena.ai等）
3. 调用网站（openrouter.ai、together.ai等）

**问题**：
- 排名网站多为SPA站点，有Vercel安全检查，无法自动抓取
- 尝试了多种方案（crawlee、playwright、反检测）均失败
- 自动抓取消耗大量时间且不可靠

## 用户确认的简化方案

### 日报自动收集（必须）
- **模型官网信息**：Claude/GPT/Gemini/GLM/MiMo/DeepSeek/Kimi/MiniMax/Qwen
- **关注内容**：新模型发布、API定价变化、Token Plan变化、Coding Plan变化

### 用户自行收集（只提供链接）
- **OpenRouter** (openrouter.ai/models) — 200+模型统一API，可观察模型热度和价格
- **DesignArena** (designarena.ai) — 设计能力对比，用户投票排名
- **ArtificialAnalysis** (artificialanalysis.ai) — 综合能力排名、速度、价格对比
- **OpenCode** (opencode.ai) — 编程能力对比，代码生成质量评估
- **ChatbotArena** (lmarena.ai) — 用户投票排名，最权威的模型对比

## 关键原则

1. **不尝试抓取SPA站点**：浪费时间且不可靠
2. **只提供链接和说明**：用户自行收集详细信息
3. **模型官网信息必须推送**：这是日报的核心价值
4. **对比网站链接必须提供**：方便用户快速访问