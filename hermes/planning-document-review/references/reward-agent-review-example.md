# Example: Reward Research Agent V1.0 Planning Document Review

## Input

Planning document: `D:\openclaw-hermes\Reward_Research_Agent_V1.0_Plan.md`
Size: 1995 chars, 129 lines
Type: High-level planning spec for a CLI tool

## Section-by-Section Findings

### Section 1: 当前范围（仅 V1.0）

**Well-defined:** Clear "不做" and "仅允许" lists with specific items.

**Findings:**

[严重] "仅允许"列表缺少 Reward Function Rewrite（整体重写奖励函数）。
  只列了"权重调整"和"Shaping"，但如果当前reward函数设计本身有缺陷
  （比如没有fall penalty），LLM应该能添加全新的reward项。
  修复：补充 - 新增Reward项（如fall_penalty、smoothness_penalty）

[重要] 缺少对环境包装层（wrapper）的权限定义。
  有些RL项目的reward是在wrapper里计算的，而非环境step内部。
  修复：明确wrapper中的reward修改是否允许。

[重要] "小规模训练验证"没有量化定义。
  修复：补充默认步数（如20000步）。

### Section 2: 核心目标

**Well-defined:** Main/aux agent roles are clear. Workflow is listed.

**Findings:**

[严重] 缺少"主Agent如何调用辅Agent"的具体机制。
  是terminal执行CLI？MCP server？Python API？
  修复：明确调用方式。

[严重] 工作流缺少 baseline 采集步骤。
  第8步"指标比较"需要baseline数据，但流程中没有baseline训练。
  修复：在propose前增加baseline训练步骤。

[重要] 工作流缺少迭代机制。
  只描述单次迭代，没有"效果不好→换方案→再试"的循环。
  修复：末尾加条件循环。

### Section 3: 指标

**Well-defined:** Primary and secondary metrics listed.

**Findings:**

[严重] 缺少指标的优化方向定义。
  fall_rate是越低越好还是越高？不定义方向，比较模块无法工作。
  修复：每个指标标注优化方向。

[严重] 缺少"improved"的量化判定标准。
  多大算"改善"？5%？10%？
  修复：定义阈值，如"主指标任一改善>=5%且其他不恶化超过10%"。

[重要] 缺少 baseline 记录机制。
  指标需要对比对象，文档没有说明baseline如何采集存储。

### Section 4: 技术路线

**Well-defined:** CLI-first approach, MiMo model selection.

**Findings:**

[严重] CLI命令列表缺少 init 和 rollback 命令。
  用户需要初始化项目和回滚修改。
  修复：补充 init --project <path> 和 rollback --to-checkpoint。

[重要] 缺少命令间的状态传递机制。
  scan结果存哪里？find-reward怎么读取？
  修复：定义state文件（如logs/current_state.json）。

### Section 5: 安全策略

**Well-defined:** Forbidden modification targets listed.

**Findings:**

[严重] 禁止列表不完整。
  缺少 scheduler, backward, gradient, loss, advantage, GAE,
  value function, policy function 等常见RL组件。
  修复：扩展禁止关键词列表。

[重要] 缺少白名单机制。
  只有黑名单不够。reward_locator定位的文件应自动加入白名单。

### Section 6: Git策略

**Well-defined:** Before/after commit, no auto-reset.

**Findings:**

[严重] 缺少脏工作区处理策略。
  dirty working tree会导致git apply失败。
  修复：检测dirty state → 警告 → stash → apply。

[严重] 缺少patch冲突处理。
  git apply可能因上下文不匹配失败。
  修复：先git apply --check，失败则--3way。

### Section 7: 论文来源

**Well-defined:** arXiv as source, query directions listed.

**Findings:**

[重要] 缺少arXiv API速率限制说明（每3秒1请求）。
[重要] 缺少论文缓存和去重策略。

### Section 8: 项目结构

**Well-defined:** Module list provided.

**Findings:**

[重要] 缺少 __init__.py, config.py, llm_client.py, state.py,
  configs/, logs/, reports/, tests/, .env.example, pyproject.toml。
[重要] 缺少 hermes_skill_writer.py（验收标准要求"能生成Hermes Skill"）。

## Cross-Cutting Issues

[严重] LLM调用的重试和错误处理策略完全没有提及。
[严重] 多seed实验：seeds配置为[0]，单seed无法判断稳定性。
[重要] 错误恢复状态机：任何一步失败后的恢复路径未定义。
[重要] 配置文件和文档中的列表需要同步（arXiv queries, 禁止关键词）。

## Prioritized Action List

P0:
  1. 补充baseline训练步骤到工作流
  2. 定义指标优化方向和improved判定标准
  3. 补充init和rollback命令
  4. 定义命令间状态传递机制
  5. 补充项目结构中缺失的模块文件
  6. 扩展禁止关键词列表

P1:
  7. 脏工作区和patch冲突处理策略
  8. LLM重试和错误处理策略
  9. 论文缓存和去重策略
  10. 量化验收标准
  11. 多seed实验支持
  12. 错误恢复状态机

P2:
  13. 迭代机制
  14. arXiv API速率限制
  15. V1.0/V2.0范围精简
  16. 配置文件与文档同步
  17. 集成验收测试方案
  18. 日志结构定义

## Verdict

Needs P0 fixes first. The document covers 8 of ~15 necessary topics,
with 6 critical gaps in baseline collection, metric definition,
command completeness, state management, safety keywords, and
error handling.
