# AI Daily Digest — Full Workflow Reference

Source skill: `ai-daily-digest` (archived to `.archive/`)
Project location: `C:/Users/lenovo_mml/.hermes/skills/news/ai-daily-digest/`

## 8-Step Workflow

### Step 1: Load Config & Prepare (Agent)
- Read `checklists/01-data-collection.md`
- Confirm date, output path: `D:/openclaw-hermes/data/daily/YYYY-MM-DD/report.md`
- Read past 3 days' report titles for dedup baseline

### Step 2: Multi-Source Data Collection (Script + Agent)
**Run script**:
```bash
python "C:/Users/lenovo_mml/.hermes/skills/news/ai-daily-digest/scripts/ai_daily_digest_v4.py"
```
Script handles: HN Algolia (9 keywords × 15 items), GitHub API (Agent/Skills/MCP), classification.

**Agent supplement** (script can't cover):
- 36氪 RSS, 量子位, 机器之心
- Model official sites (9): Claude/GPT/Gemini/GLM/MiMo/DeepSeek/Kimi/MiniMax/Qwen
- HuggingFace Daily Papers

**Pitfall**: delegate_task subagents have NO web tools. Use `execute_code + urllib` for supplement collection.

### Step 3: Data Verification (Script + Agent)
- Cross-reference: ≥5 sources → 🔴 extremely important, 3-4 → 🟡 important, 1-2 → ⚪ low confidence
- Confirm today/this week/history classification correct

### Step 4: Classification (Script + Agent)
**Decision tree** (priority order):
1. Description contains "skill(s)" → 📚 Skills
2. Mainly .md files → 📚 Skills
3. Description contains "mcp server"/"model context protocol" → 🔌 MCP
4. Description contains "for ai agents"/"for claude" → 🧩 Agent Components
5. Description contains "ai agent"/"agent for" → 🤖 Agent
6. Default → 🧩 Agent Components

### Step 5: Generate Report (Agent)
**Report structure** (8 sections, DO NOT add/remove):
1. 🤖 Agent Ecosystem (with predecessor comparison tables)
2. 🛠️ Skills Market (6 categories: reduce tokens / constrain behavior / add features / research / verification / supplementary)
3. 📊 Model Dynamics (3-layer monitoring)
4. 📰 Industry Hotspots + 🏭 Industry Applications (≥3 industries)
5. 🔌 MCP Dynamics (7 categories, multi-dimension evaluation)
6. 📊 Data Dashboard
7. 🔮 Core Signals (3-7 evidence-based)
8. 📖 AI Basics (daily educational content)

**9 Pain Point Framework**: 能力缺失/使用不便/成本过高/安全风险/效率低下/知识壁垒/协作困难/数据孤岛/行业落地

### Step 6: Quality Check (Script + Agent)
```bash
python "C:/Users/lenovo_mml/.hermes/skills/news/ai-daily-digest/scripts/quality_check.py" D:/openclaw-hermes/data/daily/YYYY-MM-DD/report.md
```
**Script precision rules**: "拆分分析" must contain "按自主性"/"按成本"/"对比分析". Skills titles must be `### 📉 第一类` (no colon).

### Step 7: Push (Agent)
- Chat: output full report in reply
- WeChat: [1/N]...[N/N] format, ~2000 chars per segment
- Local: write to `D:/openclaw-hermes/data/daily/YYYY-MM-DD/report.md`

### Step 8: Archive & Review (Agent)
- Save raw data, record issues, update skill if new pitfalls found

## Monthly Digest

Trigger: "AI月报"/"上月AI合订本"/"monthly AI digest"
- Aggregates daily reports from previous month
- Output: `D:/openclaw-hermes/data/monthly/YYYY-MM/monthly_report.md` + `.docx`
- Uses python-docx (微软雅黑 11pt, Table Grid style)

## Scripts

| Script | Purpose | When |
|--------|---------|------|
| `scripts/ai_daily_digest_v4.py` | Data collection + classification + verification | Step 2 |
| `scripts/quality_check.py` | Report format validation | Step 6 |
| `scripts/data_verification.py` | Data time verification | Step 3 |

## Key Pitfalls (Top 15)

| ID | Issue | Fix |
|----|-------|-----|
| P24 | Classification must use decision tree | Follow Step 1-6 decision tree |
| P43 | Must follow checklist step by step | Use todo tool for Step 1-8 |
| P48 | Data must distinguish today/this week/history | Script handles automatically |
| P50 | DDG max 1 query, fail → HN+GitHub | Don't rely on DDG |
| P57 | Must run quality check before push | Run quality_check.py, fix all FAIL |
| P58 | Every item must come from data collection | No writing from memory |
| P60 | Subagent has no web access | Use execute_code + urllib in main task |
| P61 | Skills title format: no colon | `### 📉 第一类` not `### 第一类：减少token消耗` |
| P62 | Split analysis uses "按自主性" not "按Stars" | quality_check.py exact string match |
| P63 | v4 script categories are [name,details] list pairs | Not a dict |
| P64 | No data today → no "today" section | Use "this week" data instead |
| P65 | terminal(WSL) broken → use execute_code | subprocess.run() for Python scripts |
| P66 | Pre-check format before quality check | Reduces feedback loops |

For complete pitfalls and checklists, see archived skill at `.archive/ai-daily-digest/`.
