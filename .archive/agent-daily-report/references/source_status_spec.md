# Source Status 统一规范 v3.1

## 12 种状态枚举

| Status | 含义 | 何时使用 |
|---|---|---|
| `success` | 正常采集，有匹配数据 | raw_count > 0, matched_count > 0 |
| `success_no_match` | 采集成功但无关键词命中 | raw_count > 0, matched_count = 0 |
| `checked_no_change` | 文档类源：hash 未变或首次 baseline | 仅用于 hash_diff 变更检测 |
| `skipped_disabled` | config 中 enabled=false | 配置禁用 |
| `skipped_missing_auth` | 缺少 token/client_id/secret | 仅限纯 API 源（不能降级） |
| `skipped_no_config` | enabled=true 但缺少 URL/pages/nodes | 配置不完整 |
| `skipped_no_stable_api` | 无稳定公开JSON API | 源本身限制，不是失败（v3.1新增） |
| `skipped_requires_api_key` | 需要API key但未配置 | 可选源缺 key 时降级跳过（v3.1新增） |
| `failed_network` | 网络失败/DNS/超时/5xx | 连接层错误 |
| `failed_parse` | 响应无法解析 | RSS/JSON/HTML/GraphQL 解析失败 |
| `failed_auth` | 认证信息存在但认证失败 | 401, 403 |
| `failed_rate_limited` | 被限流 | 429 |

## 统一返回结构（无 items 字段）

```python
{
    "source": "reddit",
    "enabled": True,
    "status": "success",
    "auth": "missing",          # ok / missing / failed / n/a / none
    "strategy_used": "rss",     # api / rss / rss_fallback / api_and_search / hash_diff / scrape / api_degraded
    "raw_count": 257,
    "matched_count": 48,
    "selected_count": 0,        # main.py 在评分后回填
    "errors": [],
    "warnings": ["OAuth missing, used RSS fallback"]
}
```

**source_status 中不包含 items。** items 由 collector 直接返回。

**selected_count 由 main.py 在评分筛选后回填**，collector 初始返回 0。

### auth 字段取值
| 值 | 含义 |
|---|---|
| `ok` | 认证正常 |
| `missing` | 缺少认证环境变量（但可能有降级策略） |
| `failed` | 认证信息存在但认证失败 |
| `n/a` | 该源不需要认证 |
| `none` | 明确标注无认证需求 |

### strategy_used 字段取值
| 值 | 含义 |
|---|---|
| `api` | 纯 API 调用（有认证） |
| `api_degraded` | API 调用（无认证，降级模式） |
| `rss` | RSS 采集 |
| `rss_fallback` | 原计划用 API，降级为 RSS |
| `api_and_search` | Firebase API + Algolia Search 组合 |
| `hash_diff` | 文档 hash 变更检测 |
| `scrape` | HTML 页面关键词检测 |
| `rss+json+html` | 多级 fallback（LinuxDo） |
| `multi_api` | 多子源聚合（External Digests） |
| `skipped` | 源被跳过（requires_api_key / no_stable_api） |

## Collector 返回签名

所有 collector 必须返回 `Tuple[List[Dict], Dict]`：

```python
def collect_xxx(config: Dict[str, Any]) -> Tuple[List[Dict], Dict]:
    return items, source_status
```

## main.py 安全调用模式

```python
def safe_collect(name, collect_fn, config, logger):
    try:
        items, source_status = collect_fn(config)
        return items, source_status
    except Exception as e:
        return [], make_source_status(
            source=name, status="failed_network",
            errors=[f"Collector exception: {e}"],
        )
```

关键规则：单个 collector 异常不能中断日报生成。

## selected_count 回填

main.py 在评分筛选后回填 selected_count：

```python
# After scoring
selected_per_source = {}
for item in scored_items:
    if item.get("importance_level") in ["S", "A", "B"]:
        src = item.get("source", "unknown")
        selected_per_source[src] = selected_per_source.get(src, 0) + 1
for name, st in all_statuses.items():
    st["selected_count"] = selected_per_source.get(name, 0)
```

## source_status.py 工厂函数

提供快捷函数避免重复代码：
- `skipped_disabled(source)` → `([], status)`
- `skipped_missing_auth(source, missing_vars)` → `([], status)`
- `skipped_no_config(source, missing_fields)` → `([], status)`
- `skipped_no_stable_api(source)` → `([], status)` — v3.1: for sources with no stable public API
- `skipped_requires_api_key(source, env_key)` → `([], status)` — v3.1: for optional API sources without key
- `failed_network(source, error)` → `([], status)`
- `failed_parse(source, error)` → `([], status)`
- `failed_auth(source, error)` → `([], status)`
- `failed_rate_limited(source, error)` → `([], status)`

## 日报 Source Status 表格

日报开头必须展示：

```
| Source | Auth | Strategy Used | Status | Raw | Matched | Selected | Notes |
|---|---|---|---|---:|---:|---:|---|
| GitHub | missing | api_degraded | ✅ success | 15 | 15 | 8 | Data collected successfully |
| LinuxDo | n/a | rss | ✅ success | 52 | 7 | 4 | Data collected successfully |
| Model Docs | n/a | hash_diff | ⚪ checked_no_change | 8 | 0 | 0 | All pages checked, no hash change |
| Model Docs | n/a | hash_diff | ⚪ checked_no_change | 6 | 0 | 0 | baseline initialized (first run) |
```

Notes 生成规则按12种状态分别处理。新增状态的 Notes:
- `skipped_no_stable_api` → "No stable public JSON API"
- `skipped_requires_api_key` → "Requires {env_key}"
