# Supplement Data Collection Patterns

> When script doesn't cover all sources, use `execute_code` with `urllib.request` to collect supplement data.
> Do NOT use `delegate_task` for web scraping — subagents lack web access tools.

## 36kr RSS

```python
import urllib.request, re

req = urllib.request.Request("https://36kr.com/feed", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=30) as resp:
    content = resp.read().decode('utf-8', errors='replace')

items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
for item in items[:20]:
    title = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
    link = re.search(r'<link>(.*?)</link>', item, re.DOTALL)
    desc = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
    # Filter for AI keywords
    ai_keywords = ['AI', '人工智能', '大模型', 'GPT', 'LLM', 'AIGC', '智能', '机器人']
```

## HuggingFace Daily Papers

```python
import urllib.request, json

req = urllib.request.Request("https://huggingface.co/api/daily_papers", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=30) as resp:
    papers = json.loads(resp.read().decode('utf-8'))

for paper in papers[:10]:
    paper_data = paper.get('paper', {})
    title = paper_data.get('title', '')
    paper_id = paper_data.get('id', '')
    url = f"https://huggingface.co/papers/{paper_id}"
```

## Important Notes

- Use `execute_code` tool, NOT `delegate_task` (subagents lack web tools)
- Set `timeout=30` for each request
- Always set `User-Agent` header
- Filter for AI-related keywords for 36kr
- Save to `D:/openclaw-hermes/data/daily/YYYY-MM-DD/supplement_data.json`
