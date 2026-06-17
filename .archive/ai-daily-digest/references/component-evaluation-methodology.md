# Component Evaluation Methodology

When evaluating whether to add a new tool/skill/component to Hermes, follow this framework:

## Decision Matrix

| Criteria | Weight | Questions |
|----------|--------|-----------|
| **Overlap** | High | Does Hermes already have this capability? |
| **Marginal gain** | High | What % improvement over existing? |
| **Token cost** | Medium | How much does it add to system prompt per API call? |
| **Maintenance** | Medium | How often does it need updates? |
| **Complexity** | Medium | MCP server vs pure skill? Dependencies? |
| **Verification** | Low | Stars, community, production use? |

## Token Impact Calculation

```
Extra tokens per API call = new_skills_count × avg_chars_per_skill_entry / 4
Extra tokens per session = extra_per_call × calls_per_session
Extra monthly cost = extra_per_session × sessions_per_month × price_per_token
```

Each skill entry in system prompt ≈ 60 chars ≈ 15 tokens.

## Categories of "Not Needed"

1. **Full overlap**: Hermes already does this (e.g., Browser-use when Hermes has browser)
2. **Overkill**: Too complex for the use case (e.g., GraphRAG for daily digest)
3. **Paid dependency**: Requires external paid service (e.g., Tavily, Apify)
4. **Wrong platform**: Designed for a different agent framework

## Categories of "Worth Installing"

1. **Large marginal gain**: >50% improvement (e.g., context-mode: 98% reduction)
2. **Fills real gap**: Hermes genuinely lacks this (e.g., cache-audit)
3. **Proven at scale**: Used by major companies or >1K stars
4. **Low integration cost**: Pure skill or simple MCP

## Evaluated This Session (2026-05-29)

| Component | Stars | Decision | Reason |
|-----------|-------|----------|--------|
| ECC | ⭐197K | Partial (25 skills) | Most skills are coding-specific |
| Browser-use | ⭐96K | Skip | Hermes has browser |
| Mem0 | ⭐57K | Skip (for now) | Memory is sufficient |
| context-mode | ⭐16K | Install | 98% tool output reduction |
| cache-audit | ⭐53 | Install | Diagnoses cache issues |
| token-saver | ⭐5 | Install | Context compression |
| prompt-cache-skills | ⭐69 | Install | 14 caching fixes |
| open-webSearch | ⭐1.3K | Skip | Overlaps firecrawl/duckduckgo |
| Tavily | ⭐1.3K | Skip | Paid API key |
| Composio | ⭐28K | Skip | Too heavy |
