# Newly Installed Skills — 2026-05-30

## Batch Installation Summary

Installed 6 high-star skills from GitHub, bringing total from 142 to 171.

### Skills Installed

| Skill | Category | Source | Stars |
|-------|----------|--------|-------|
| superpowers-zh | hermes | jnMetaCode/superpowers-zh | 4,261 |
| anysearch-skill | hermes | anysearch-ai/anysearch-skill | 1,730 |
| hermes-skill-factory | hermes | Romanescu11/hermes-skill-factory | - |
| super-hermes | hermes | Cranot/super-hermes | - |
| hermes-dojo | hermes | Yonkoo11/hermes-dojo | - |
| personal-api | hermes | beiyuii/personal-api-skill | - |
| hermes-incident-commander | hermes | Lethe044/hermes-incident-commander | - |
| agent-skill-creator | hermes | FrancyJGLisboa/agent-skill-creator | 1,242 |

### Custom Skills Created (2026-05-30)

| Skill | Version | Purpose | Status |
|-------|---------|---------|--------|
| reasoning-trace | v4.0.0 | 记录推理过程，用于skill修改调整 | ✅ 测试通过 |
| process-thinking | v1.1.0 | 拆分任务为环节 | ✅ 测试通过 |

### Installation Pattern

```python
import subprocess, os

skills_to_install = [
    {"name": "skill-name", "url": "https://github.com/user/repo", "category": "hermes"},
]

skills_base = r"C:\Users\lenovo_mml\.hermes\skills"

for skill in skills_to_install:
    skill_dir = os.path.join(skills_base, skill["category"], skill["name"])
    if os.path.exists(skill_dir):
        continue  # Skip existing
    os.makedirs(os.path.dirname(skill_dir), exist_ok=True)
    subprocess.run(["git", "clone", "--depth", "1", skill["url"], skill_dir],
                   capture_output=True, text=True, timeout=60)
```

### Post-Install

After batch installation, restart gateway to load new skills:
```python
subprocess.run([r"D:\openclaw-hermes\scripts\hermes.bat", "gateway", "restart"],
               capture_output=True, text=True, shell=True)
```

Verify with `skills_list` tool — count should increase.

### Skill Generator Discovery

**agent-skill-creator** (⭐1,242) was discovered as a superior alternative to skill-generator (⭐340):
- Accepts any input: messy docs, links, code, PDFs, transcripts
- Produces validated, security-scanned skills
- Supports 14+ tools: Claude Code, Copilot, Cursor, Windsurf, Codex, Gemini, Kiro, etc.
- Installed to: `~/.hermes/skills/hermes/agent-skill-creator/`

**URL**: https://github.com/FrancyJGLisboa/agent-skill-creator

### Logic Chain Skills Discovered (2026-05-30)

| Project | Stars | Function | Integration |
|---------|-------|----------|-------------|
| OpenSPG/KAG | ⭐8,795 | Knowledge Augmented Generation | 逻辑形式引导推理 |
| smkalami/prompt-decorators | ⭐469 | `+++Reasoning`, `+++StepByStep` | Agent Skill格式 |
| human-avatar/skills-for-humanity | ⭐99 | 171 skills, 27 categories | 结构化推理方法论 |
| jordanrubin/FUTURE_TOKENS | ⭐61 | antithesize, excavate, synthesize | 可组合推理skills |
| flight505/mcp-think-tank | ⭐62 | MCP增强推理 | MCP服务器 |

### Skill Discovery via GitHub API

When user asks about popular/high-star skills, search GitHub:

```python
import requests
search_url = "https://api.github.com/search/repositories"
params = {"q": "hermes-agent skill", "sort": "stars", "order": "desc", "per_page": 20}
headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "Hermes-Agent"}
response = requests.get(search_url, params=params, headers=headers, timeout=10)
```

Also check `0xNyk/awesome-hermes-agent` README for curated list.
