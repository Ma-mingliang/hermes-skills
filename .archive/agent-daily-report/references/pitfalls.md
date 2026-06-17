# Pitfalls Reference (v3.3)

## P1-P37: 见 SKILL.md

## P38-P59: Agent Pipeline + External Sources + HN 诊断

| ID | 问题 | 解决 |
|----|------|------|
| P38 | ai-news-radar 端点错误 | 旧端点 `/data/latest.json` 返回 0。正确: `/data/latest-24h.json`，fallback 到 raw.githubusercontent.com |
| P39 | source_status 常量截断 | STATUS_SKIPPED_MISSING_AUTH 和 STATUS_FAILED_AUTH 被 patch 截断。必须整个文件重写 |
| P40 | smithery 返回 success_no_match 而非 skipped | collector 返回空列表时被覆盖。用 _pending_skip 哨兵机制 |
| P41 | mcp.so 无稳定 API 每天报错 | enabled=false 降级为 skipped_disabled |
| P42 | YAML config 替换边界错误 | external_sources 嵌套在 external_digests 内，替换脚本找错边界 |
| P43 | Agent batch_size>1 导致中文质量下降 | 必须 batch_size=1，每个 item 独立 LLM 调用 |
| P44 | Agent 多轮验证不通过时整批重跑 | batch_size=1 时只重跑单个 item，成本可控 |
| P45 | WeChat context_token 过期导致推送失败 | 清理 context-tokens.json + 用全局 Hermes_Gateway.cmd 重启 |
| P46 | 完整 pipeline 超时 | 11 源采集 + agent pipeline 超过 5 分钟。用 terminal(background=True) 或 cron job |
| P47 | WeChat context_token 过期 | iLink rate limiting (ret=-2) 后 token 变 stale。清理 + 全局 Hermes_Gateway.cmd 重启 |
| P48 | agent_pipeline enabled 但 LLM 未配置 | 走降级模式（Trust 跳过，Enrichment 离线模板，Editor 规则）|
| P49 | YAML dump 破坏注释 | 用 execute_code + 逐行文本替换，不要 yaml.safe_load + yaml.dump |
| P50 | 日报过长分段推送触发限流 | 合并为 2-3 条长消息(3000-4000字符/条)，不要逐段 send_message |
| P51 | 凭记忆编造日报内容 | 必须先 read_file 读取实际 .md 文件，不得凭上下文重构 |
| P52 | HN collector 不存储 story ID | 原始数据已有 hn_url 字段（23/23 条都有），直接使用。不需要 Algolia 反查 |
| P53 | RSS 条目 primary_category 为空 | 37条 RSS matched 条目的 primary_category 为空字符串。修复：RSS collector 应根据 feed 名称设置默认 category |
| P54 | MCP section 忽略 external 源 | MCP Registry 有 11 个 B 级新 MCP server，但 MCP section 只显示了 2 个 reddit 条目。修复：MCP section 应优先使用 MCP Registry/Glama 的条目 |
| P55 | Section quota 被单一源占满 | GitHub 16条(66.7%) + Reddit 8条(33.3%) = 24条，其他9个源全部 Displayed=0。修复：增加源分配逻辑 |
| P56 | HN _format_story 硬编码 primary_category="Community" | collect_hackernews.py L168 硬编码。23条HN全部归类为Community，但实际包含Coding Agent、MCP、Tool等。修复：根据标题内容动态分类，或留空让 classify_items.py 处理 |
| P57 | GitHub discovery penalty 封顶过低 | generic_github_discovery_candidate 标记强制封顶54分（C级上限），导致 CodexPlusPlus（+918/24h，评分明细83分）无法进日报。修复：提高封顶到62（B级下限），或对高增长项目（+100/24h）降低惩罚系数 |
| P58 | HN 关键词匹配过于宽松 | _is_relevant 只检查关键词存在性，不区分title/text/URL权重。text正文中顺带提及"coding agent"或URL中包含"kimi"就匹配。修复：title匹配权重>text，URL匹配加白名单，text匹配加频率门槛 |
| P59 | HN Firebase newstories 无 points 门槛 | ≤5pts条目只能来自Firebase newstories（新帖，不限points）。Algolia有points>5过滤，但Firebase没有。如需过滤低质量条目，可给Firebase加points门槛 |

## P60-P70: Growth Gate + Pipeline Execution + Push

| ID | 问题 | 解决 |
|----|------|------|
| P60 | HN _is_relevant 关键词匹配太宽松导致误匹配 | title权重>text，URL加白名单，text匹配加频率门槛≥2 |
| P61 | Discovery penalty 封顶54分导致高增长项目无法进日报 | 提高封顶到62，或对高增长项目降低惩罚系数 |
| P62 | MCP Registry/Glama API 无 star 数据 | 需从 repo URL 反查 GitHub API 获取 stars |
| P63 | HN _is_relevant text 匹配含 HTML 正文 | 先 strip HTML 再匹配 |
| P64 | MCP Registry 新 server 评分固定60分 | 需引入 GitHub stars 或下载量来差异化评分 |
| P65 | Growth gate 阈值过严 | 1k-5k 改为 delta>=100；<1k 改为 delta>=200。修改 collect_github.py evaluate_github_growth_gate() |
| P66 | _find_growth_anomalies 跳过已在 candidates 的仓库 | L1008 `if rn in already: continue` 导致 discovery_candidate 不参与增长检测，待修复 |
| P67 | execute_code 300s 超时杀掉长 pipeline | 用 `run_pipeline.py --background`（DETACHED_PROCESS），再用 `--status` 轮询，最长等30分钟 |
| P68 | 修改 .py 后 __pycache__ 未清理导致旧代码运行 | 批量修改后清除所有 `__pycache__`（主目录+scripts/+tests/）。2026-06-03实测：growth gate代码已改但pipeline仍输出旧reason，根因是.pyc缓存 |
| P69 | Growth gate过滤漏斗导致大量仓库被拒 | 23个日均>=100仓库仅4个通过：5个archived被跳过、4个weak_signal被拒、10个__pycache__旧代码被拒。详见references/growth-gate-diagnosis.md |
| P70 | 手动分段推送只发了2/17段就暂停 | 微信推送容易触发限流(P50)。建议：合并为2-3条长消息；用cron job自动推送 |

## P71-P78: Growth Normalization + Enrichment Coverage + Finance Filter

| ID | 问题 | 解决 |
|----|------|------|
| P71 | 列出仓库时缺少描述 | 用户要求列出仓库时必须附带功能描述。来源：candidates.json → GitHub API GET /repos/{name} → 标注"(无描述)" |
| P72 | has_strong_agent_signal 误拒高增长仓库 | CodexPlusPlus(+1066/24h)因description不含agent关键词被weak_agent_signal拒绝。需检查signal检测是否过于保守 |
| P73 | read_file 对 D: 盘路径返回 File not found | Python os.path.exists() 确认存在但 read_file 返回 File not found。**必须用 execute_code + Python os/open 模块**读取 Windows D: 盘路径 |
| P74 | Growth Gate delta 未归一化到24h | 快照间隔只有1.5h（cron凌晨00:37跑），delta_raw=71 但24h等效=1117。**已修复**：当 interval_hours<23 时，delta_24h = round(delta_raw / interval_hours * 24)。metrics 新增 `star_delta_24h_raw` 保留原始值。修改文件：`github_state.py` |
| P75 | Watchlist release 事件重复进入正文 | `langchain-ai/langgraph`(watchlist) 在 Watch List 表格，`langchain-ai/langgraph - 1.2.4`(release) 又在 Agent 正文。根因：normalized_entity 不同，_item_key 基于 URL 无法去重。**已修复**：`generate_report.py` 新增 `_extract_repo_from_item`，agent_items 排除已在 watchlist 的同一 repo |
| P76 | Enrichment max_items 限制导致大量条目走离线模板 | 42个条目只有12个走 LLM，30个走离线模板。根因：`item_enrichment.max_items=12`。**已修复**：`max_items=0`（全部走 LLM），`batch_size=1`（逐条最高质量） |
| P77 | External Digests 金融新闻混入日报 | 9条金融新闻（美股异动、IPO、市值暴涨等）进入 enrichment 但走离线模板。**已修复**：`normalize_items.py` 的 `negative_kws` 新增金融关键词 |
| P78 | has_strong_agent_signal 关键词匹配漏掉 Skill/增强器项目 | CodexPlusPlus（Codex增强器）、PaperSpine（Skill）、GordenPPTSkill（Skill）未命中 GITHUB_STRONG_AGENT_PATTERNS。**解决方案**：对关键词不通过的候选，用 LLM 读取 README 逐个判断。用户要求：只要是 Skill 或能增强 Agent 的工具都收录 |

## P79-P81: Finance Filter + weak_agent_signal + ai-news-radar Removal

| ID | 问题 | 解决 |
|----|------|------|
| P79 | 金融/投资/股市新闻混入日报 | external:ai-news-radar 采集的金融新闻（美股异动、IPO、市值暴涨、基金、信贷等）与 Agent 生态无关但进入 enrichment。**已修复**：`normalize_items.py` 的 `negative_kws` 新增 16 个金融关键词。注意：finance关键词需要精确匹配（如"美股异动"而非"美股"），避免误杀含"AI"的金融Agent新闻 |
| P80 | weak_agent_signal 误杀 Skill/Agent 项目 | CodexPlusPlus（Agent增强器）、science-skills（Skill）、SkillOpt（Skill）均被标记为 weak_agent_signal 并排除。根因：`evaluate_github_growth_gate()` 不检查项目是否为 Skill/Agent/Tool/Workflow。**修复**：添加 `_is_skill_or_agent_project()` 函数，匹配则跳过 weak_agent_signal 检查 |
| P81 | ai-news-radar 信源已移除 | 2026-06-05 用户要求从 external_digests 移除 ai-news-radar（LearnPrompt/ai-news-radar）。config.yaml 中 `external_sources` 列表已删除该条目 |

## P82-P85: Trust Decision + Scoring + Daily Avg Growth (2026-06-05)

| ID | 问题 | 解决 |
|----|------|------|
| P82 | 用户报告"项目未推送/等级错误"但实际数据正确 | 2026-06-05 实测：用户报告 `yetone/native-feel-skill` score=60 但 level=C 且未推送。**实际验证**：score=60 → level=B（正确），项目已在报告中。**教训**：必须先验证实际数据再诊断 bug。验证步骤：(1) 读取 `data/scored/{date}.json`；(2) 检查 score/importance_level/quality_flags/trust_score/trust_reason 五字段；(3) 在报告文件中搜索项目名。详见 `references/scoring-verification-pattern.md` |
| P83 | Trust Decision 降级逻辑过于宽泛 | mastra-ai/mastra（score=78）和 BigPizzaV3/CodexPlusPlus（score=73）因"无多源共振证据"被降级到B。**用户要求**：仅对特定原因（Bug修复PR、缺乏独立价值）降级。**修复**：修改 `apply_trust_decisions()`，添加降级关键词检查和多源共振升级逻辑。详见 `references/trust-decision-mechanism.md` |
| P84 | score_items.py 缺少 `import os` 导致静默失败 | `_calc_daily_avg_growth` 使用 `os.path.exists()` 但模块顶部未 `import os`。`except: return None` 吞掉异常。**调试**：改 `except Exception as e: print(f"Error: {e}")` 立即发现。**教训**：(1) 模块顶部 import 所有依赖；(2) `except: return None` 是最危险的错误处理；(3) 返回 None 需验证是否因异常 |
| P85 | 日均增长保底B级阈值过低 | 初始 `daily_avg > 0` 即保底B级，导致 118/264 项目被提升（含 0.2 stars/day）。**修复**：阈值改为 `daily_avg >= 20 stars/day`，提升数量降至 19 个。保底机制必须有合理下限 |
