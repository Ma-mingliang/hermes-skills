# ai_daily_digest_v4.py Output Format

> Documents the exact JSON structure of the script output file.
> Path: `D:/openclaw-hermes/data/daily/YYYY-MM-DD/raw_data_v4.json`

## Top-level Keys

```json
{
  "date": "2026-05-31",
  "hn": [...],           // HN items (list of dicts)
  "github": [...],       // GitHub items (list of dicts)
  "industry": [...],     // Industry HN items (list of dicts)
  "classified": {...},   // All projects classified (dict)
  "categories": {...},   // Grouped by category (dict)
  "verification": {...}  // Time verification results (dict)
}
```

## `hn` — Hacker News Items

List of dicts, each with:
```json
{
  "title": "DeepSeek reasonix...",
  "url": "https://...",
  "points": 729,
  "time": "2026-05-31T..."
}
```

## `github` — GitHub Projects

List of dicts with project info (name, stars, description, url, etc).

## `industry` — Industry HN Items

Same structure as `hn`, filtered for industry-related topics.

## `classified` — Per-Project Classification

Dict keyed by project name (e.g. `"obra/superpowers"`):
```json
{
  "obra/superpowers": {
    "category": "skills",
    "reason": "Superpowers",
    "stars": 213492,
    "desc": "An agentic skills framework...",
    "url": "https://github.com/obra/superpowers"
  }
}
```

## `categories` — Grouped by Category

Dict keyed by category name, each value is a **list of [name, details] pairs**:
```json
{
  "skills": [
    ["obra/superpowers", {
      "category": "skills",
      "reason": "Superpowers",
      "stars": 213492,
      "desc": "...",
      "url": "https://github.com/obra/superpowers"
    }],
    ...
  ],
  "component": [...],
  "agent_allround": [...],
  "agent_specialized": [...],
  "mcp": [...]
}
```

⚠️ **Important**: `categories` values are lists of `[name, details]` pairs (NOT dicts).
Access: `item[0]` for name, `item[1]` for details dict.

## `verification` — Time Verification

```json
{
  "hn_today": 0,
  "hn_week": 0,
  "gh_today": 0,
  "gh_week": 2,
  "gh_old": 105
}
```

## Typical Counts (2026-05-31 run)

| Category | Count |
|----------|-------|
| HN total | 158 |
| GitHub total | 107 |
| Industry HN | 18 |
| agent_allround | 11 |
| agent_specialized | 5 |
| skills | 16 |
| component | 61 |
| mcp | 14 |

## Known Issues

- Some HN/GitHub queries may fail with SSL errors (still produces partial data)
- When `hn_today=0` and `gh_today=0`, report must NOT have "今日新闻" section
- Use `gh_week` data when today data is empty
