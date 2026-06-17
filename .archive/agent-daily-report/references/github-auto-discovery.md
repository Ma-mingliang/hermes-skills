# GitHub Auto-Discovery from Community Sources (2026-06-05)

## Overview

Automatically extract GitHub repository links from HackerNews, Reddit, LinuxDo, NodeSeek, ProductHunt and add them to the watch list for 24h observation.

## Implementation

### 1. collect_hackernews.py - Extract GitHub links

In `_format_story()` method, extract GitHub repo URL from story URL or text:

```python
import re
github_pattern = r'https?://github\.com/([^/]+/[^/]+)'
match = re.search(github_pattern, url)
if match:
    github_repo = match.group(1)
else:
    text = story.get("text") or ""
    match = re.search(github_pattern, text)
    if match:
        github_repo = match.group(1)

if github_repo:
    result["github_repo"] = github_repo
    result["github_url"] = f"https://github.com/{github_repo}"
```

### 2. github_link_enricher.py - Add to watch list

New function `add_to_watch_list()`:

```python
def add_to_watch_list(repo, repo_data, source, config, log=None):
    """Add a GitHub project to the watch list for observation."""
    state_file = config.get("state", {}).get("github_repo_state", "state/github_repo_state.json")
    
    # Load existing state
    state = {"repos": {}}
    if os.path.exists(state_file):
        with open(state_file, "r", encoding="utf-8") as f:
            state = json.load(f)
    
    # Skip if already tracked
    if repo in state.get("repos", {}):
        return False
    
    # Add with candidate_30d status
    today = datetime.now().strftime("%Y-%m-%d")
    repo_entry = {
        "repo": repo,
        "url": f"https://github.com/{repo}",
        "first_seen_date": today,
        "tracking_status": "candidate_30d",
        "source_origin": source,
        "snapshots": {
            today: {
                "stars": repo_data.get("stargazers_count", 0),
                "collected_at": datetime.now().isoformat()
            }
        },
        # ... other fields
    }
    
    state.setdefault("repos", {})[repo] = repo_entry
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
```

### 3. generate_report.py - New report sections

Added "待观察项目" sub-section in `_generate_github_project_dynamics()`:

```python
# Sub-section 7: Pending Observation
pending_items = [i for i in github_items 
                 if i.get("tracking_status") == "candidate_30d" 
                 and i.get("source_origin") in ("hackernews", "reddit", "producthunt", "linuxdo", "nodeseek")]
sections.append("### 待观察项目")
if pending_items:
    sections.append("| 项目 | 来源 | Stars | 发现日期 | 状态 | 说明 |")
    sections.append("|------|------|------:|----------|------|------|")
    for item in pending_items[:10]:
        # ... format row
    sections.append("> 观察规则：发现后记录初始star数，24h后再次检查，若增长≥50则纳入推荐。")
```

## Trigger Conditions

- `item.source in ("hackernews", "reddit", "producthunt", "linuxdo", "nodeseek")`
- `github_repo` field is non-empty
- Repo not already in `state/github_repo_state.json`

## Observation Rules

1. Record initial star count when discovered
2. Check again after 24h
3. If growth >= 50 stars → recommend
4. If growth < 50 → keep observing or archive
