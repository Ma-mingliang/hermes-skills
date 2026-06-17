# last30days-skill GITHUB_TOKEN Pitfall

## Problem
`last30days` v3.3.2's `get_config()` in `scripts/lib/env.py` does NOT include `GITHUB_TOKEN` in its keys list. Even with `GITHUB_TOKEN` set as an environment variable, the pipeline's `available_sources()` check (`config.get("GITHUB_TOKEN") or which("gh")`) returns False for GITHUB_TOKEN because it's not in the config dict.

## Symptom
- stderr shows `sources=[reddit,hackernews]` — GitHub is missing
- `Sources: 2 active (Hacker News, Reddit)` — no GitHub

## Fix
Patch `scripts/lib/env.py` — add `GITHUB_TOKEN` to the keys list:

```python
# In get_config(), find the keys list and add:
('GITHUB_TOKEN', None),
```

After patching, stderr should show `sources=[reddit,hackernews,github]` and `Sources: 3 active (GitHub, Hacker News, Reddit)`.

## Verification
```python
import subprocess, os
env = os.environ.copy()
env['GITHUB_TOKEN'] = '<your-token>'
r = subprocess.run(
    ['python', 'last30days.py', 'test query', '--emit=compact'],
    capture_output=True, text=True, timeout=60, env=env
)
assert 'GitHub' in r.stderr  # Should appear in source list
```

## Location
- Repo: `~/last30days-skill/`
- Installed to: `~/.hermes/skills/last30days/`
- Patch file: `~/last30days-skill/skills/last30days/scripts/lib/env.py` (also at `~/.hermes/skills/last30days/scripts/lib/env.py`)
