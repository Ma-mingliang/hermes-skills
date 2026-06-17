# ECC Skills Installation (2026-05-29)

## Installed Skills (25 total, in ~/.hermes/skills/ecc/)

### Information Collection & Content (8)
- article-writing: Article writing standards
- content-engine: Content generation engine
- deep-research: Multi-source deep research
- data-scraper-agent: Data scraping agent
- market-research: Market research
- social-publisher: Social media publishing
- social-graph-ranker: Social graph ranking
- email-ops: Email operations

### Security (3)
- security-review: Security review
- security-scan: Security scanning
- safety-guard: Safety protection

### Agent Optimization (6)
- continuous-learning-v2: Automatic learning from sessions
- agent-eval: Agent evaluation
- agent-introspection-debugging: Agent debugging
- verification-loop: Verification loop
- skill-stocktake: Skill audit
- skill-scout: Skill discovery

### Automation & Audit (3)
- automation-audit-ops: Automation audit
- production-audit: Production environment audit
- workspace-surface-audit: Workspace audit

### Tool Efficiency (5)
- content-hash-cache-pattern: Content hash caching
- documentation-lookup: Documentation lookup
- ecc-tools-cost-audit: Cost audit
- hookify-rules: Rules hookification
- benchmark-optimization-loop: Benchmark optimization

## Not Installed (from ECC, potentially useful)
- nutrient-document-processing (5.9KB): Document processing
- click-path-audit (8.0KB): Click path audit
- database-migrations (11.8KB): Database migration
- scientific-db-pubmed-database (4.7KB): PubMed scientific database
- scientific-db-uspto-database (6.2KB): US patent database

## Key ECC Repos
- ECC main: https://github.com/affaan-m/ECC (⭐197K)
- ECC v2.0.0-rc.1 has Hermes setup guide
- 348 total skills, 63 agents, 135 rules, 199 security items

## Token Impact of Full ECC Install
- 348 skills × ~60 chars in list = ~20,880 chars per API call
- Extra tokens per call: ~4,890
- Monthly cost (30 sessions × 10 calls): ~44M tokens, ~¥27
- Recommendation: cherry-pick only relevant skills (done)
