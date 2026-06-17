# Subagent Data Fabrication — 2026-05-29 Lesson

## Problem
delegate_task subagents return plausible but fabricated data.

## Confirmed Fabrications

### 1. GitHub Repos (all 404)
| Claimed URL | Status |
|------------|--------|
| hindsight-memory/hindsight | ❌ 404 |
| hindsight-ai/hindsight-framework | ❌ 404 |
| hindsight-agent/hindsight | ❌ 404 |
| hindsight-ai/context-window | ❌ 404 |
| hindsight-memory-claude | ❌ User exists, no repos |

### 2. Fabricated Star Counts
- Subagent claimed "1.8k stars" for nonexistent repo
- Subagent claimed "1.2k stars" for nonexistent repo
- Different subagent calls returned DIFFERENT star counts for same claimed project

### 3. Model Version — Correct but for Wrong Reasons
- Subagent reported Claude Opus 4.8, GPT-5.5, Gemini 3.1
- These were CONFIRMED REAL via user's phone screenshot of artificialanalysis.ai
- BUT subagent was using training data inference, not live API data
- Lesson: even "correct" subagent data needs verification — right answer, wrong method

## Root Cause
LLMs generate plausible-sounding information based on:
- Naming patterns (hindsight + memory = plausible repo name)
- Common star count ranges (1.2k, 1.8k sound realistic)
- Domain knowledge extrapolation (HER paper exists → "hindsight memory" project must exist)

## Verification Protocol
1. GitHub URLs → web_fetch check for 404
2. Star counts → GitHub API `curl https://api.github.com/repos/OWNER/REPO`
3. Model versions → browser access to ranking sites
4. **Never trust subagent data without verification**
