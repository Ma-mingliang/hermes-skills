# ai-daily-digest vs agent-daily-report

两个系统定位不同，不互相替代。

## 对比

| 维度 | ai-daily-digest | agent-daily-report |
|------|-----------------|-------------------|
| **定位** | AI 综合新闻日报 | Agent 生态技术情报 |
| **受众** | 通用 AI 读者 | Agent 开发者 |
| **分类** | 5 类粗分类 | 14 类严格分类 |
| **评分** | 无量化评分 | 5 维度 0-100 + S/A/B/C/D |
| **数据源** | HN/GitHub/36氪/模型官网/HuggingFace | GitHub/HN/arXiv/HuggingFace |
| **特色** | 模型动态、行业应用、AI教育 | Agent 生态深度、MCP、论文 |
| **输出** | 中文报告 | 英文报告 |
| **位置** | ~/.hermes/skills/news/ai-daily-digest/ | D:/openclaw-hermes/agent-daily-report-skill/ |

## 何时用哪个

- **ai-daily-digest**: 用户说"AI日报"、"今日AI新闻"、"生成日报"
- **agent-daily-report**: 用户说"agent情报"、"agent日报"、"agent生态"

## 可以合并吗？

理论上可以，但当前保持独立：
- ai-daily-digest 侧重推送格式（微信分段）和中文输出
- agent-daily-report 侧重分类深度和评分体系
- 未来可考虑将 agent-daily-report 的分类/评分能力整合进 ai-daily-digest
