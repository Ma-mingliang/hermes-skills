# weak_agent_signal Fix (2026-06-05)

## Problem

Projects categorized as Skill, Agent, Tool, or Workflow were being marked as `weak_agent_signal` and excluded from reports.

Examples:
- BigPizzaV3/CodexPlusPlus (Agent增强器, 13k stars, +877/day) → excluded
- google-deepmind/science-skills (Skill, 1.5k stars, +264/day) → excluded
- microsoft/SkillOpt (Skill, 4.9k stars, +220/day) → excluded
- op7418/guizang-social-card-skill (Skill, 2.8k stars, +126/day) → excluded

## Root Cause

`evaluate_github_growth_gate()` in `collect_github.py` line 201-203:

```python
if not has_strong_agent_signal(repo):
    result["reason"] = "weak_agent_signal"
    return result
```

This returns early with `weak_agent_signal` if `has_strong_agent_signal()` returns False. The function checks `GITHUB_STRONG_AGENT_PATTERNS` which didn't cover all Skill/Agent/Tool/Workflow projects.

## Fix

Added `_is_skill_or_agent_project()` function and modified the gate logic:

```python
def _is_skill_or_agent_project(repo: Dict[str, Any]) -> bool:
    """Check if a project is a Skill, Agent, Tool, or Workflow project."""
    desc = (repo.get("description", "") or "").lower()
    topics = [t.lower() for t in (repo.get("topics", []) or [])]
    name = (repo.get("name", "") or "").lower()
    full_name = (repo.get("full_name", "") or "").lower()
    
    skill_indicators = [
        "skill", "agent", "tool", "plugin", "connector", "workflow",
        "pipeline", "mcp", "codex", "copilot", "cursor", "aider",
        "openhands", "swe-agent", "langgraph", "crewai", "autogen"
    ]
    
    for indicator in skill_indicators:
        if indicator in desc:
            return True
        if any(indicator in t for t in topics):
            return True
        if indicator in name or indicator in full_name:
            return True
    return False
```

In `evaluate_github_growth_gate()`:
```python
is_skill_or_agent = _is_skill_or_agent_project(repo)
if not has_strong_agent_signal(repo) and not is_skill_or_agent:
    result["reason"] = "weak_agent_signal"
    return result
```

## Rule

ALL Skill/Agent/Tool/Workflow projects should be eligible for reports. They should NEVER be marked as `weak_agent_signal`.

## Verification

After fix, the report shows:
- microsoft/SkillOpt → "Skill", reason "one_k_to_5k_delta_100plus" ✓
- nexu-io/html-anything → "Coding Agent", reason "one_k_plus_delta_50_observation" ✓
- No `weak_agent_signal` in report ✓
