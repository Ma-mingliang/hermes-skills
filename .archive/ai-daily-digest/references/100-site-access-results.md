# 100-Site Access Results (2026-05-28)

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total sites | 100 |
| Successful | 66 (66.0%) |
| Failed | 34 (34.0%) |
| Total data items | 1,451 |

## Success Rate by Tier

| Tier | Name | Success/Total | Rate |
|------|------|---------------|------|
| 1 | Top AI News Sources | 31/35 | 88.6% |
| 2 | Quality AI News | 6/9 | 66.7% |
| 3 | AI Professional Media | 6/10 | 60.0% |
| 4 | Chinese AI Media | 8/15 | 53.3% |
| 5 | Developer Communities | 8/16 | 50.0% |
| 6 | Video Platforms | 2/5 | 40.0% |
| 7 | Forums/Communities | 5/10 | 50.0% |

## Top 20 Data Sources by Volume

1. AI Plus Info: 501 items (Tier 3)
2. DeepMind Blog: 101 items (Tier 1)
3. IT之家: 61 items (Tier 4)
4. Wired AI: 51 items (Tier 2)
5. V2EX: 51 items (Tier 5)
6. Product Hunt: 51 items (Tier 5)
7. Hacker News: 50 items (Tier 1)
8. 36氪: 31 items (Tier 4)
9. Linux.do: 31 items (Tier 5)
10. Analytics Insight: 30 items (Tier 3)
11-14. HN Algolia (Claude/OpenClaw/DeepSeek/Skill): 30 each (Tier 1)
15. BBC Tech: 23 items (Tier 2)
16. TechCrunch AI: 22 items (Tier 2)
17. Ars Technica: 22 items (Tier 2)
18. 雷锋网: 22 items (Tier 4)
19. 爱范儿: 21 items (Tier 4)
20. AI Weekly: 21 items (Tier 3)

## Failure Analysis

| Failure Type | Count | % |
|--------------|-------|---|
| HTTP 403 (Forbidden) | 15 | 44% |
| HTTP 404 (Not Found) | 8 | 24% |
| SSL/Connection errors | 6 | 18% |
| HTTP 401 (Unauthorized) | 2 | 6% |
| Other errors | 3 | 8% |

## Consistently Unreliable Sites (skip immediately)

- **B站/抖音 RSSHub**: Always returns 403, needs authenticated API
- **知乎/微博/头条 RSSHub**: Always returns 403
- **财联社/少数派 RSSHub**: Always returns 403
- **OpenAI Blog**: Returns 403 (blocks scraping)
- **Lobste.rs**: SSL errors
- **DZone/InfoQ**: Returns 403/405

## Consistently Reliable Sites (prioritize)

- **HN Algolia API**: 100% success, best data quality
- **GitHub API**: 100% success, essential for Agent/Skill data
- **36氪 RSS**: 100% success, best Chinese source
- **BBC Tech RSS**: 100% success
- **Wired/Ars Technica/TechCrunch RSS**: 100% success
- **V2EX/Linux.do RSS**: 100% success, good Chinese forum data
