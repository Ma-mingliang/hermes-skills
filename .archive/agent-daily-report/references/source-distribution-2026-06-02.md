# Source Distribution Diagnostic — 2026-06-02

## 流水线数据

Raw 709 → Matched 844 → Scored 389 → A/B候选 186 → Displayed 24

## 各源 Displayed 占比

| Source | Raw | Matched | A/B候选 | Displayed | 占比 |
|---|---:|---:|---:|---:|---:|
| github | 385 | 385 | 117 | 16 | 66.7% |
| reddit | 262 | 54 | 30 | 8 | 33.3% |
| hackernews | 180 | 23 | 1 | 0 | 0% |
| external_digests | 134 | 134 | 33 | 0 | 0% |
| rss_feeds | 491 | 37 | 2 | 0 | 0% |
| huggingface | 143 | 95 | 2 | 0 | 0% |
| linuxdo | 30 | 12 | 0 | 0 | 0% |
| nodeseek | 20 | 2 | 0 | 0 | 0% |
| producthunt | 50 | 1 | 0 | 0 | 0% |
| model_docs | 8 | 1 | 1 | 0 | 0% |
| framework_docs | 5 | 0 | 0 | 0 | 0% |

## Bug 发现

### Bug 1: HN 全部归类为 Community (P50/P52)
- 23条HN条目全部 primary_category="Community"
- 实际内容：Coding Agent 10+, MCP 2, Tool 1, Workflow 3, General Agent 3
- 根因：collect_hackernews.py `_format_story` 硬编码 `"primary_category": "Community"`
- 重新评分后：1A + 17B = 18条优质内容（原始仅1B）

### Bug 2: RSS primary_category 为空 (P51/P53)
- 37条RSS matched条目 primary_category 字段为空
- 导致无法分配到对应板块

### Bug 3: MCP section 忽略 external 源 (P52/P54)
- MCP Registry 11个B级 + Glama 10个B级 = 21条B级MCP条目
- MCP section 只显示了2个reddit条目
- 根因：section 填充逻辑未优先使用专用源

### Bug 4: Section quota 无源分配限制 (P53/P55)
- GitHub 独占 66.7%，Reddit 33.3%，其他9个源全部0%
- 设计权重：GitHub 35%, HN 15%, Reddit 8%...

### Bug 5: Discovery 项目被 quality flag 封顶 (P61)
- CodexPlusPlus: +918/24h, 评分明细83分 → 实际54分（C级）
- GordenPPTSkill: +242/24h, 评分明细73分 → 实际54分（C级）

## HN 重新评分结果

原始（全部Community）：A:0, B:1, C:2, D:1（仅4条评分）
重新（按内容实体）：A:1, B:17, C:4, D:1（23条全部评分）

### A级
- AI Agent Guidelines for CS336 at Stanford: 77分 (458pts/140c)

### B级 Top 5
- Komi-learn: 67分 (25pts)
- MCP is definitely not dead: 65分 (3pts)
- Voice control coding agents: 65分 (7pts)
- HarnessKit: 65分 (82pts)
- Zerostack v1.3.4: 65分 (575pts - 旧story，不在72h内)

## GitHub 增长率分析

24h增长≥100 Stars 的项目共9条：

| 增长率 | 24h增长 | 总Stars | 级别 | 项目 |
|---:|---:|---:|---|---|
| 28.21% | +101 | 358 | B | DannyMac180/skills |
| 24.26% | +115 | 474 | C🔒 | female-portrait-director |
| 17.58% | +150 | 853 | B | google-deepmind/science-skills |
| 15.91% | +242 | 1,521 | C🔒 | GordenPPTSkill |
| 8.20% | +918 | 11,197 | C🔒 | CodexPlusPlus |
| 7.56% | +327 | 4,323 | B | microsoft/SkillOpt |
| 7.13% | +180 | 2,523 | B | guizang-social-card-skill |
| 6.52% | +117 | 1,794 | C🔒 | PaperSpine |
| 0.17% | +165 | 96,674 | A | browser-use |

🔒 = generic_github_discovery_candidate 质量标记封顶

## 诊断方法论

当用户问"各源占比"或"为什么某源 Displayed=0"时：

1. 读取 `data/scored/YYYY-MM-DD.json`，按 source 分组统计
2. 检查 A/B 候选数量 vs Displayed 数量
3. 检查 primary_category 是否正确设置
4. 检查 section quota 分配逻辑
5. 检查 quality_flags 是否有惩罚
6. 对比设计权重 vs 实际占比
