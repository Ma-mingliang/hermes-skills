# Hermes Ecosystem - Skill Discovery Guide

## High-Star Skill Repositories (2026-05-29)

### Tier 1: Essential (1000+ stars)
| Repository | Stars | Description |
|------------|-------|-------------|
| nexu-io/open-design | 55,495 | Design tool with 259+ skills |
| OthmanAdi/planning-with-files | 22,329 | Manus-style persistent planning |
| MemTensor/MemOS | 9,453 | Self-evolving memory OS for LLMs |
| outsourc-e/hermes-workspace | 5,045 | Native web workspace for Hermes |
| jnMetaCode/superpowers-zh | 4,261 | AI programming superpowers (Chinese) |
| NousResearch/hermes-agent-self-evolution | 3,698 | Evolutionary self-improvement |
| 0xNyk/awesome-hermes-agent | 3,563 | Curated skills list |
| codejunkie99/agentic-stack | 2,052 | Portable .agent/ folder framework |
| anysearch-ai/anysearch-skill | 1,730 | Unified real-time search engine |
| conorbronsdon/avoid-ai-writing | 1,606 | Remove AI writing patterns |
| prompt-security/clawsec | 1,016 | Security skill suite |
| ksimback/hermes-ecosystem | 912 | Hermes Atlas community map |

### Tier 2: Notable (100-999 stars)
| Repository | Stars | Description |
|------------|-------|-------------|
| Varnan-Tech/opendirectory | 395 | AI Agent Skills for founders |
| OnlyTerp/hermes-optimization-guide | 363 | Setup and optimization guide |

## Popular Skills from awesome-hermes-agent

### Development Tools
- **hermes-skill-factory** - Meta-skill that auto-generates reusable skills
- **litprog-skill** - Literate programming across platforms
- **oh-my-hermes** - Multi-agent orchestration skills

### Life & Entertainment
- **hermes-spotify-skill** - Spotify playback control (Linux/Raspberry Pi)
- **hermes-life-os** - Personal OS agent for daily pattern detection
- **acca-tracker** - Multi-sport accumulator betting tracking

### Security & Operations
- **clawsec** - Complete security skill suite (1016 stars)
- **hermes-incident-commander** - Autonomous SRE incident detection

### Intelligence Enhancement
- **super-hermes** - Meta-reasoning layer for better prompts
- **hermes-dojo** - Self-improvement system for weak skills
- **personal-api** - Turn Obsidian vault into identity layer

### Integration & Connectivity
- **hermes-nextcloud** - Self-hosted Nextcloud bridge
- **hermes-plugins** - Goal management, agent bridge, model selection

## GitHub API Search Patterns

### Search for high-star skills
```python
import requests

search_url = "https://api.github.com/search/repositories"
params = {
    "q": "hermes-agent skill stars:>50",
    "sort": "stars",
    "order": "desc",
    "per_page": 20
}
headers = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Hermes-Agent"
}

response = requests.get(search_url, params=params, headers=headers, timeout=10)
data = response.json()

for repo in data['items'][:10]:
    print(f"{repo['full_name']} - ⭐{repo['stargazers_count']}")
    print(f"  {repo['description'][:100]}")
    print(f"  {repo['html_url']}")
```

### Search queries to try
- `hermes-agent skill`
- `hermes skill stars:>50`
- `hermes-agent skill stars:>100`
- `hermes skill marketplace`
- `hermes skill framework`

### Skill Generator Comparison

| Tool | Stars | Function | Platform Support |
|------|-------|----------|-----------------|
| **agent-skill-creator** | ⭐1,242 | Workflow → Skill (any input) | 14+ tools (Claude Code, Copilot, Cursor, etc.) |
| skill-generator | ⭐340 | Idea → Skill | Antigravity, Claude Code, Cursor, Windsurf |
| hermes-skill-factory | ⭐339 | Auto-capture workflows → Skill | Hermes Agent |
| skill-ten-prompt-generator | ⭐65 | Prompt → Skill | Claude Code |

**Recommendation**: Use `agent-skill-creator` (⭐1,242) as the primary skill generation tool. It accepts any input (messy docs, links, code, PDFs, transcripts) and produces validated, security-scanned skills.

## Current Skill Inventory (2026-05-30)

Total: 171+ skills installed (2026-05-30)

### Categories
- **ARIS (Academic Research)**: 77 skills
- **ECC (Development Framework)**: 25 skills
- **Hermes (Agent Self)**: 6 skills
- **News**: 2 skills
- **Research**: 1 skill
- **Data Research**: 1 skill
- **General Tools**: 30+ skills

### Key Skill Areas
1. **Paper Writing**: paper-write, paper-compile, paper-figure, paper-plan
2. **Literature Search**: arxiv, semantic-scholar, openalex, deepxiv, alphaxiv
3. **Research Workflow**: idea-discovery, research-refine, experiment-plan, auto-review-loop
4. **Patent**: patent-pipeline, claims-drafting, specification-writing
5. **Presentation**: paper-slides, paper-poster, paper-talk
6. **Quality Check**: citation-audit, paper-claim-audit, proof-checker

## References

- [Hermes Atlas](https://github.com/ksimback/hermes-ecosystem) - Community ecosystem map
- [awesome-hermes-agent](https://github.com/0xNyk/awesome-hermes-agent) - Curated skills list
- [hermes-agent-self-evolution](https://github.com/NousResearch/hermes-agent-self-evolution) - Self-improvement system
