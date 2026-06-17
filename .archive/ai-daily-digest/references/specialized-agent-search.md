# 专精Agent搜索策略

## 搜索关键词（必须在数据收集阶段执行）

### 垂直领域Agent搜索
```python
specialized_queries = [
    "DB-GPT",           # 数据
    "HolmesGPT",        # SRE
    "html-anything",    # 设计
    "TradingAgents",    # 金融
    "security+agent",   # 安全Agent
    "data+agent",       # 数据Agent
    "sre+agent",        # SREAgent
]
```

### 已验证的搜索结果（2026-05-31）
| Agent | Stars | 领域 | GitHub |
|-------|-------|------|--------|
| TradingAgents | 81K | 金融交易 | TauricResearch/TradingAgents |
| TradingAgents-CN | 27K | 金融交易(中文) | hsliuping/TradingAgents-CN |
| DB-GPT | 18K | 数据库 | eosphoros-ai/DB-GPT |
| OpenSRE | 6K | SRE运维 | Tracer-Cloud/opensre |
| html-anything | 5K | 设计 | nexu-io/html-anything |
| HolmesGPT | 2K | SRE运维 | HolmesGPT/holmesgpt |

## 分类规则

### 专精Agent vs 组件的区别
- **专精Agent**：面向特定垂直领域的Agent（数据/SRE/设计/金融/安全）
  - 判断标准：功能限定在某个垂直领域，能独立执行该领域任务
  - 示例：DB-GPT(数据)、HolmesGPT(SRE)、TradingAgents(金融)
- **组件**：Agent框架/平台/SDK，不是垂直领域Agent
  - 示例：MetaGPT(多Agent框架)、agency-agents(AI agency平台)、lobehub(Agent operator)

### 常见误判
| 项目 | 错误分类 | 正确分类 | 原因 |
|------|---------|---------|------|
| MetaGPT | agent_specialized | component | 多Agent协作框架，不是垂直领域Agent |
| agency-agents | agent_specialized | component | AI agency平台，不是垂直领域Agent |
| lobehub | agent_specialized | component | Agent operator平台，不是垂直领域Agent |

## 自动化脚本

```python
def collect_specialized_agents():
    """搜索skill中定义的专精Agent（垂直领域）"""
    gh_headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"}
    
    specialized_queries = [
        "DB-GPT", "HolmesGPT", "html-anything",
        "TradingAgents", "security+agent", "data+agent", "sre+agent",
    ]
    
    all_repos = []
    for q in specialized_queries:
        try:
            url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}&sort=stars&per_page=5"
            data = fetch_json(url, headers=gh_headers)
            all_repos.extend(data.get("items", []))
        except Exception as e:
            print(f"  专精Agent '{q}': FAIL {e}")
    
    seen = set()
    deduped = []
    for r in all_repos:
        rid = r.get("id")
        if rid and rid not in seen:
            seen.add(rid)
            deduped.append(r)
    
    return sorted(deduped, key=lambda x: x.get("stargazers_count",0), reverse=True)
```
