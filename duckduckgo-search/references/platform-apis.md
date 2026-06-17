# Platform API Fallback Patterns

When DuckDuckGo is rate-limited (returns 0 results), fall back to direct platform APIs. These are the
APIs used successfully in research sessions — each includes a working Python snippet.

## Reddit JSON API

No auth required. Add `.json` to any Reddit URL.

```python
import requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Subreddit search
r = requests.get(
    "https://www.reddit.com/r/OpenAI/search.json?q=KEYWORD&sort=new&restrict_sr=on&limit=10",
    headers=headers, timeout=15
)
data = r.json()
for p in data['data']['children']:
    d = p['data']
    print(f"{d['title']} | {d['permalink']} | created_utc={d['created_utc']}")

# Specific post + comments
r = requests.get("https://www.reddit.com/r/OpenAI/comments/POST_ID/.json", headers=headers)
post = r.json()[0]['data']['children'][0]['data']
comments = r.json()[1]['data']['children']
```

## GitHub Issues API (public repos)

No auth needed for public repos. Rate limit: 60 req/hour unauthenticated.

```python
# List issues (sorted by update time)
r = requests.get(
    "https://api.github.com/repos/openai/codex/issues?state=all&per_page=20&sort=updated&direction=desc",
    headers={'User-Agent': 'Mozilla/5.0'}, timeout=15
)
issues = r.json()

# Filter by keyword in title/body
relevant = [i for i in issues if 'quota' in (i.get('title','') + (i.get('body','') or '')).lower()]

# Get issue comments
r = requests.get(issue['comments_url'], headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
comments = r.json()
```

## OpenAI Developer Community (Discourse API)

Base URL: `https://community.openai.com`. Append `.json` to any topic URL.

```python
# Search topics
r = requests.get(
    "https://community.openai.com/search.json?q=KEYWORD&page=1",
    headers={'User-Agent': 'Mozilla/5.0'}, timeout=15
)
data = r.json()
for t in data.get('topics', []):
    print(f"ID:{t['id']} | {t['title']} | slug={t['slug']}")

# Get full topic with all posts
r = requests.get("https://community.openai.com/t/SLUG/TOPIC_ID.json", headers=headers)
data = r.json()
posts = data['post_stream']['posts']
for p in posts:
    # cooked is HTML, strip tags for readability
    import re
    text = re.sub(r'<[^>]+>', ' ', p['cooked'])
    text = re.sub(r'\s+', ' ', text).strip()
    print(f"[{p['username']}]: {text[:500]}")
```

## Tips

- Reddit: use `restrict_sr=on` to limit to one subreddit, `sort=new` for recency
- GitHub: `sort=updated&direction=desc` for latest activity; keyword-filter in Python (no server-side text search on issues list)
- Discourse: `search.json` returns `topics` + `posts` arrays; `.json` on a topic URL returns the full `post_stream`
- All three: always set a `User-Agent` header to avoid being blocked
