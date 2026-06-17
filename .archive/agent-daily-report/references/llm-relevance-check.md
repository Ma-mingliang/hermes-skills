# LLM-Based Agent Relevance Check

## 背景

`has_strong_agent_signal` 的关键词匹配太僵硬：
- `CodexPlusPlus` 是 Agent 增强器，但描述里没命中任何模式词
- `PaperSpine` 是 Skill，但没匹配到 "skill"
- 误匹配风险也高

## 方案：LLM 读 README 逐个判断

### 为什么不用批量

- 批量(13个)：prompt~30K字符，LLM对后面的项目注意力下降
- 逐个替换：每个项目获得LLM全部注意力，最准
- 13次调用总共也就25秒，可接受

### 实现代码

```python
import json, os, time
import urllib.request

def fetch_readme(repo, github_token, max_chars=3000):
    """获取 README 前 max_chars 字符"""
    try:
        url = f"https://api.github.com/repos/{repo}/readme"
        headers = {
            "Accept": "application/vnd.github.v3.raw",
            "User-Agent": "agent-daily-report"
        }
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode("utf-8", errors="replace")[:max_chars]
    except Exception as e:
        return f"[README获取失败: {e}]"

def judge_agent_relevance(repo, readme, api_key, base_url):
    """逐个判断项目是否与 Agent 生态相关"""
    system_prompt = """你是 Agent 生态情报分析专家。根据 README 判断该项目是否与 Agent 生态相关。

Agent 生态包括：AI Agent 框架/运行时、Coding Agent/代码生成、MCP 服务器/工具、Agent Skill/可复用能力包、Agent 工作流编排、Agent 浏览器/终端自动化、多智能体协作、Agent 记忆/上下文管理。

重要：增强器（enhancer）和 Skill 都算 Agent 生态相关：
- 增强 Agent 能力的工具（如 Codex 增强器）→ relevant=true
- 可复用能力包（如 PPT 生成 Skill、插画 Skill）→ relevant=true
- 内容主题不影响判断（生成插画的 Skill 仍然是 Skill）

返回 JSON：{"relevant": true/false, "category": "分类", "reason": "一句话原因"}"""

    user_prompt = f"项目：{repo}\n\nREADME：\n{readme}"

    endpoint = f"{base_url.rstrip('/')}/chat/completions"
    payload = {
        "model": "mimo-v2.5-pro",
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    req = urllib.request.Request(endpoint, data=json.dumps(payload).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())

    content = result["choices"][0]["message"]["content"]
    return json.loads(content)

# 使用示例
def check_relevance_batch(repos, api_key, base_url, github_token):
    """逐个检查项目的 Agent 相关性"""
    results = []
    for repo in repos:
        readme = fetch_readme(repo, github_token)
        try:
            judgment = judge_agent_relevance(repo, readme, api_key, base_url)
            relevant = judgment.get("relevant", False)
            category = judgment.get("category", "?")
            reason = judgment.get("reason", "?")
        except Exception as e:
            relevant = False
            category = "?"
            reason = f"LLM调用失败: {e}"

        results.append({
            "repo": repo,
            "relevant": relevant,
            "category": category,
            "reason": reason
        })
        time.sleep(0.5)

    return results
```

### 2026-06-04 实测结果

13个项目逐个判断，11个通过，2个不通过：

| 项目 | LLM 判断 | 原因 |
|------|---------|------|
| CodexPlusPlus | ❌ → 应为 ✅ | "Codex 外部增强启动器，不是 AI Agent 核心组件" |
| ian-xiaohei-illustrations | ❌ → 应为 ✅ | "内容创作工具，而非 Agent 生态框架" |

**用户修正**：增强器和 Skill 都要收录。已更新 system prompt 强调这一点。

### 注意事项

1. system prompt 必须明确"增强器和 Skill 都算相关"，否则 LLM 会误判
2. README 获取限制 3000 字符，避免 prompt 过长
3. 逐个调用约 0.5s/项目，13个项目约 7 秒
4. 失败时默认 relevant=False（保守策略）
