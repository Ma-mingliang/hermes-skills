# 分类修正：专精Agent搜索策略 (2026-05-31 最终版)

## 核心教训

专精Agent的问题不是分类逻辑，而是**搜索策略**。

## 错误过程

1. **第一次错误**：把MetaGPT/agency-agents/lobehub分类为agent_specialized
   - 这些是Agent框架/平台，不是垂直领域Agent
   - 应该分类为component

2. **第二次错误**：用通用搜索关键词("ai agent")搜不到专精Agent
   - 通用搜索返回的都是全能Agent和框架
   - 需要专门搜索垂直领域关键词

## 正确做法

### 搜索策略

数据收集阶段**必须**增加垂直领域搜索关键词：

```python
queries_specialized = [
    "DB-GPT",           # 数据
    "HolmesGPT",        # SRE
    "html-anything",    # 设计
    "TradingAgents",    # 金融
    "security+agent",   # 安全
    "data+agent",       # 数据Agent
    "sre+agent",        # SREAgent
    "medical+agent",    # 医学Agent
]
```

### 分类规则

- **专精Agent** = 功能限定在某个垂直领域
  - 示例：DB-GPT=数据、HolmesGPT=SRE、TradingAgents=金融
  - 判断标准：描述含垂直领域关键词(data/research/security/finance)

- **Agent框架/平台** = component
  - 示例：MetaGPT、agency-agents、lobehub、AutoGen、CrewAI
  - 判断标准：描述含"framework/SDK/library/platform/operator"

### 如果没有新专精Agent

按skill规则："如果当日没有新的专精agent，推荐5个高星的专精agent（含详细描述+前辈对比）"

搜索skill中已定义的专精Agent示例即可。

## 验证结果 (2026-05-31)

搜索垂直领域关键词后，找到5个专精Agent：
- TradingAgents ⭐81K — 金融
- AutoResearch ⭐84K — 科研
- DB-GPT ⭐18K — 数据
- html-anything ⭐5K — 设计
- HolmesGPT ⭐2K — SRE

## 验证清单

- [ ] 是否搜索了垂直领域关键词
- [ ] agent_specialized是否包含真正的垂直领域Agent
- [ ] MetaGPT/agency-agents/lobehub是否分类为component
- [ ] 如果没有新专精Agent，是否推荐了5个高星的
