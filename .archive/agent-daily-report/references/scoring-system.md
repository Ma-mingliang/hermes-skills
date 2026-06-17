# ⚠️ DEPRECATED — Scoring System (5 Dimensions, 0-100)

> **This file is DEPRECATED as of v2.0.**
> The only valid scoring formula is: relevance(30) + popularity(20) + freshness(15) + growth(15) + utility(20) = 100.
> Do NOT reference this file in code. Use `references/scoring-formulas.md` instead.

---

# Scoring System (5 Dimensions, 0-100)

## Dimension 1: Relevance Score (0-30)

| Level | Score | Criteria |
|-------|-------|---------|
| 强相关 | 25-30 | Agent Framework, General Agent, Specialized Agent, Coding Agent, MCP, Workflow, Skill |
| 中相关 | 15-24 | Tool/Plugin/Connector, Model, Research |
| 弱相关 | 5-14 | AI 工具、LLM、模型 |
| 无关 | 0-4 | 非 AI 内容 |

## Dimension 2: Popularity Score (0-25)

### GitHub (Stars)
| Stars | Score |
|-------|-------|
| > 50,000 | 25 |
| > 10,000 | 20 |
| > 3,000 | 15 |
| > 1,000 | 10 |
| > 100 | 5 |

### Hacker News (Score)
| HN Score | Score |
|----------|-------|
| > 500 | 25 |
| > 200 | 20 |
| > 100 | 15 |
| > 50 | 10 |

### Hugging Face (Likes)
| Likes | Score |
|-------|-------|
| > 1,000 | 20 |
| > 500 | 15 |
| > 100 | 10 |
| > 50 | 5 |

### arXiv
默认 5-15，若作者/机构/Benchmark 强则更高

## Dimension 3: Freshness Score (0-15)

| Age | Score |
|-----|-------|
| < 24 hours | 15 |
| < 3 days | 10 |
| < 7 days | 5 |
| > 7 days | 0 |

## Dimension 4: Growth Score (0-20)

### GitHub (star_delta_24h)
| 24h Stars | Score |
|-----------|-------|
| > 1,000 | 20 |
| > 500 | 16 |
| > 200 | 12 |
| > 100 | 8 |
| > 50 | 5 |

### HN (comments/讨论热度)
| Comments | Score |
|----------|-------|
| > 200 | 15 |
| > 100 | 10 |
| > 50 | 5 |

## Dimension 5: Utility Score (0-10)

| Level | Score | Criteria |
|-------|-------|---------|
| 高 | 8-10 | 可直接用于 Hermes/OpenClaw/Claude Code |
| 中 | 5-7 | 可用于 Agent 开发 |
| 低 | 2-4 | 仅理论相关 |
| 无 | 0-1 | 无直接价值 |

## Importance Levels

| Level | Score Range | Action |
|-------|------------|--------|
| S | 85-100 | 必须推送，关键事件 |
| A | 70-84 | 值得重点关注 |
| B | 55-69 | 普通收录 |
| C | 40-54 | 备选 |
| D | 0-39 | 忽略 |

## Current Implementation Notes

v1.0.0 使用规则评分，部分维度实现简化：
- growth_score: GitHub 暂用 stars 代替 star_delta_24h（需 state 文件积累）
- utility_score: 基于 category 和关键词推断
- arXiv: 固定分值
