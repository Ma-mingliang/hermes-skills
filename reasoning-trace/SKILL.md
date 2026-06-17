---
name: reasoning-trace
description: "记录AI推理过程，用于skill修改调整，支持任务→skill流程，添加思维验证功能"
version: 4.0.0
category: hermes
tags: [reasoning, trace, skill, debugging, improvement, verification]
---

# Reasoning Trace Skill

记录AI推理过程，用于skill修改调整，支持任务→skill流程，添加思维验证功能。

## 🎯 核心定位

**用途**：用于skill的修改调整  
**目标**：以任务导向的更新skill  
**范围**：压缩到skill修改调整这个领域内

## 🔄 核心流程

```
执行任务 → 记录推理过程 → 思维验证 → 用户发现问题 → 用户给出修改意见 → 更新skill
    ↓
hermes-skill-factory捕获工作流 → 自动生成skill
    ↓
用户审查skill → 给出修改意见 → 更新skill
    ↓
后续任务 → 使用更新后的skill → 执行任务
```

## 🔧 核心功能

### 1. 记录推理过程（不输出token）
```python
task_id = start_trace("task_001", "执行某个任务")
trace_step("reasoning", "我需要先检查...")
trace_step("decision", "我决定使用...")
end_trace("success")
```

### 2. 思维验证（新增）
```python
# 在做决策前进行验证
verify_decision(
    decision="ARIS是Agent",
    verification_questions=[
        "有没有反例？",
        "一定是对的吗？",
        "如果错了会怎样？"
    ]
)

# 检查是否与之前的分析一致
check_consistency(
    current_decision="ARIS是Agent",
    previous_analysis="ARIS = Skills"
)
```

### 3. 关联任务和skill
```python
# 任务执行后，关联到生成的skill
link_task_to_skill(task_id, skill_name)

# 查看skill的生成过程
skill_traces = get_skill_traces(skill_name)
```

### 4. 保存skill修改意见
```python
# 对skill给出修改意见
save_skill_modification(
    skill_name="my_skill",
    user_feedback="这个skill应该先检查X",
    related_task_id="task_001"
)

# 获取skill的修改意见
modifications = get_skill_modifications(skill_name)
```

### 5. skill版本管理
```python
# 保存skill版本
save_skill_version(skill_name, version="1.0")

# 回滚到之前的版本
rollback_skill(skill_name, version="1.0")

# 查看修改差异
diff = get_skill_diff(skill_name, "1.0", "1.1")
```

### 7. 轨迹进化（2026-05-31新增，来自SE-Agent）

**问题**：每次执行任务都犯同样的错误，不从历史执行中学习
**解决方案**：轨迹级进化（trajectory-level evolution）

**核心思想**：
- 记录每次执行的完整轨迹（步骤、决策、结果）
- 从多个轨迹中学习，找到更好的执行路径
- 通过修订、重组、精炼三个阶段进化

**三个阶段**：
1. **Revision（修订）**：检查当前轨迹，找出错误和改进点
2. **Recombination（重组）**：从多个轨迹中提取最佳部分，组合成新轨迹
3. **Refinement（精炼）**：优化新轨迹，确保逻辑一致

**使用示例**：
```python
# 记录执行轨迹
trace_id = record_trajectory(
    task="AI日报生成",
    steps=[
        {"step": "数据收集", "result": "只收集了5个源", "issue": "RSS解析失败"},
        {"step": "分类", "result": "分类不准确", "issue": "没有执行Step 1-6流程"},
        {"step": "报告生成", "result": "内容不完整", "issue": "缺少前辈对比"}
    ]
)

# 从历史轨迹学习
learned_patterns = analyze_trajectories(
    task="AI日报生成",
    patterns_to_find=["RSS解析失败", "分类不准确", "内容不完整"]
)

# 生成改进轨迹
improved_trace = evolve_trajectory(
    current_trace=trace_id,
    learned_patterns=learned_patterns,
    evolution_stages=["revision", "recombination", "refinement"]
)

# 应用改进
apply_learned_patterns(task="AI日报生成", patterns=learned_patterns)
```

**关键价值**：
- 避免重复犯同样的错误
- 从多个执行路径中找到最优解
- 持续改进执行质量

**参考项目**：[SE-Agent](https://github.com/JARVIS-Xs/SE-Agent) (⭐273)

### 6. 清理功能
```python
# ⚠️ cleanup_traces() 包装函数缺少 keep_with_modifications，只传 keep_days + keep_important
# 用实例方法以支持完整功能：
from client import get_trace_client
client = get_trace_client()
result = client.cleanup(keep_days=30, keep_important=True, keep_with_modifications=True)
```

⚠️ Cron 定期清理必须手动补充 `.jsonl` 处理，完整实现见 `references/cron-cleanup-pattern.md`
**清理脚本**: `scripts/cleanup-traces.py` — 可直接运行的完整清理脚本，处理 .json + .jsonl + 空目录

**⚠️ Pitfall: cleanup() 和 get_storage_stats() 仅处理 `.json` 文件**（2026-06-01 发现，2026-06-06 确认仍未修复）：
- Plugin hook 自动生成的 session trace 使用 `.jsonl` 格式（存储于 `traces/YYYY-MM-DD/session_*.jsonl`）
- `cleanup()` 第 173 行 `if not filename.endswith('.json'): continue` 会跳过所有 `.jsonl` 文件
- `get_storage_stats()` 同样只统计 `.json` 文件，遗漏 `.jsonl` 的实际存储占用
- 后果：`.jsonl` 文件会无限累积，永远不会被清理
- **实际影响**（2026-06-06实测）：`get_storage_stats()` 报告 5 个文件/5.83KB，实际有 522 个文件/1.33MB — 差距 **228倍**
- 修复方案：详见 `references/cleanup-jsonl-fix.md` — `.jsonl` 按日期清理（无 important/modification 标记），`.json` 保留现逻辑
- **⚠️ 修复方案仅为文档，尚未应用到 client.py** — 执行 cron 清理时需手动补充 `.jsonl` 清理逻辑

**⚠️ Pitfall: `cleanup_traces()` 包装函数丢弃 `keep_with_modifications`**（2026-06-09 实测确认）：
- `cleanup_traces()` (line 1094) 只传 `keep_days` 和 `keep_important`，不传 `keep_with_modifications`
- 结果：通过包装函数调用时，有修改意见的旧 trace 可能被误删
- 正确做法：`get_trace_client().cleanup(keep_days, keep_important, keep_with_modifications)`

**⚠️ Pitfall: `get_storage_stats()` 抛 datetime 序列化异常**（2026-06-09 实测确认）：
- 直接调用 `get_storage_stats()` 并 JSON 序列化会抛 `Object of type datetime is not JSON serializable`
- Cron 清理统计应手动遍历 `traces/` 目录，不要依赖 `get_storage_stats()`

**⚠️ Pitfall: Cron 清理时 .jsonl 需要单独处理**
- `cleanup_traces()` API 不处理 `.jsonl`，cron job 必须额外扫描并删除过期的 `.jsonl` 文件
- 正确的 cron 清理流程：调用 `cleanup_traces()` → 手动遍历 `traces/` 删除过期 `.jsonl` → 清理空目录
- 示例代码见 `references/cron-cleanup-pattern.md`

## 📝 使用场景

### 场景1: 思维验证
```
AI准备生成回答："ARIS有CLI但是Agent"
    ↓
思维验证：检查是否与分析一致
    ↓
发现不一致：分析说ARIS=Skills，但回答说ARIS=Agent
    ↓
调整回答："ARIS有CLI但是Skills"
    ↓
记录验证过程到Reasoning Trace
```

### 场景2: 任务→skill优化
```
用户: "执行这个任务"
AI: [执行任务，记录推理过程]
AI: [hermes-skill-factory生成skill]
用户: "这个skill有问题，应该先检查X"
AI: [保存修改意见，更新skill]
用户: "下次执行类似任务时，使用更新后的skill"
AI: [使用更新后的skill执行任务]
```

### 场景3: skill迭代优化
```
用户: "这个skill的推理过程怎么样？"
AI: [回放skill的生成过程]
用户: "第3步有问题，应该先检查Y"
AI: [保存修改意见，更新skill]
用户: "查看修改历史"
AI: [展示skill的修改历史]
```

## 📊 存储结构

```
~/.hermes/
├── traces/                          # 推理过程存储
│   ├── YYYY-MM-DD/                  # 按日期组织
│   │   ├── task_XXX.json           # 手动trace（.json，含important/modifications标记）
│   │   ├── session_XXXXX.jsonl     # Plugin自动trace（.jsonl，原始事件日志）
│   │   └── ...
│   └── index.json                  # 索引文件（仅索引.json文件）
├── skills/
│   ├── reasoning-trace/
│   │   ├── SKILL.md                # 技能说明
│   │   ├── client.py               # 客户端模块（含cleanup/get_storage_stats）
│   │   ├── cleanup.py              # 清理脚本（CLI入口）
│   │   └── modifications/          # 修改意见
│   │       ├── YYYY-MM-DD.json     # 任务修改意见
│   │       └── skill_YYYY-MM-DD.json  # skill修改意见
│   └── <skill_name>/
│       ├── SKILL.md                # skill内容
│       └── versions/               # 版本历史
│           ├── 1.0/
│           ├── 1.0.json
│           └── ...
```

## 💡 关键价值

1. **完整闭环**：任务→skill→修改→更新→任务
2. **可追溯**：记录skill的生成过程和修改历史
3. **可改进**：用户可以参与skill的优化过程
4. **可回滚**：支持回滚到之前的版本
5. **思维验证**：在做决策前进行验证，避免错误
6. **高效**：不输出token，节省成本

## ⚡ 自动启用（Plugin Hook，推荐）

**问题**：reasoning-trace是skill，按需加载，执行任务时容易"忘记"启用。

**解决方案**：创建Hermes Plugin，用 `pre_llm_call` 钩子在每个LLM turn自动注入推理追踪指令。

**Plugin位置**：`~/.hermes/plugins/reasoning-trace-hook/`

```
reasoning-trace-hook/
├── plugin.yaml      ← 插件配置，声明使用pre_llm_call hook
├── hooks.py         ← 钩子实现，每个turn注入推理追踪指令
└── __init__.py      ← 注册入口
```

**工作原理**：
```
用户发送消息 → Hermes触发pre_llm_call → plugin注入指令到user message末尾 → LLM看到指令并记录推理
```

**关键特性**：
- **ephemeral**：注入内容不污染system prompt，不影响prompt cache
- **自动发现**：Hermes自动扫描 `~/.hermes/plugins/` 目录
- **可配置**：修改 `hooks.py` 中的 `TRACE_INSTRUCTION` 调整指令
- **可禁用**：删除plugin目录即可

**生效**：重启Gateway `hermes gateway restart`

**参考**：`gejifeng/hermes-time-perception-extension` 用了相同的 `pre_llm_call` hook机制注入时间标签。

---

## 🚀 快速开始
## 🚀 快速开始

### 方式1：Plugin自动记录（推荐，v2.0）

**位置**：`~/.hermes/plugins/reasoning-trace-hook/`

Plugin通过Hermes的hook机制，在每个LLM turn自动记录Agent的全过程：
- `pre_llm_call` — 记录Agent开始思考（模型、输入、历史长度）
- `pre_tool_call` — 记录即将调用的工具+参数（skill加载、文件读取、API搜索等）
- `post_tool_call` — 记录工具调用结果（成功/失败、耗时、输出摘要）

**存储格式**：JSONL（每行一条JSON记录），实时追加到 `~/.hermes/traces/YYYY-MM-DD/session_XXXXX.jsonl`

**查看trace**：
```bash
python ~/.hermes/plugins/reasoning-trace-hook/view_trace.py              # 今天
python ~/.hermes/plugins/reasoning-trace-hook/view_trace.py 2026-05-31   # 指定日期
```

**记录内容示例**：
```json
{"event": "llm_call_start", "session_id": "xxx", "model": "mimo-v2.5-pro", "ts": "..."}
{"event": "tool_call_start", "tool": "skill_view", "params": {"name": "ai-daily-digest"}, "ts": "..."}
{"event": "tool_call_end", "tool": "skill_view", "duration_ms": 150, "result_preview": "...", "ts": "..."}
{"event": "tool_call_start", "tool": "execute_code", "params": {"code": "import requests..."}, "ts": "..."}
{"event": "tool_call_end", "tool": "execute_code", "duration_ms": 31000, "result_preview": "...", "ts": "..."}
```

**生效**：
1. 启用plugin → `hermes plugins enable reasoning-trace-hook`（⚠️ Plugin默认opt-in，必须手动启用！）
2. 重启Gateway → `hermes gateway restart`
3. 新session才生效（当前session连接的是旧Gateway）

**⚠️ 关键Pitfall：Plugin默认不启用**
- `hermes plugins list` 查看状态，新plugin显示 `not enabled`
- 必须运行 `hermes plugins enable <name>` 才能激活
- 仅创建plugin文件不够，启用+重启+新session三步缺一不可
- 验证：`hermes plugins list` 确认状态为 `enabled`

### 方式2：手动记录（skill API）

适用于需要精细控制记录内容的场景：
```python
from client import (
    start_trace, trace_step, end_trace,
    verify_decision, check_consistency,
    link_task_to_skill, save_skill_modification,
    save_skill_version, rollback_skill
)

# 记录推理过程
task_id = start_trace("my_task", "执行某个任务")
trace_step("reasoning", "我需要先检查...")
end_trace("success")

# 思维验证
verify_decision(
    decision="ARIS是Agent",
    verification_questions=["有没有反例？"]
)
```

## 💡 与mimo-v2.5-pro的集成机会

mimo-v2.5-pro模型原生返回`reasoning_content`字段，包含详细的推理过程。这个字段：
- 不计入输出token（节省成本）
- 自动记录推理步骤
- 可以被捕获并存储到Reasoning Trace

**未来优化方向**：直接捕获mimo-v2.5-pro的reasoning_content，替代手动调用trace_step()。

详见 `~/.hermes/skills/hermes-agent/references/mimo-v25pro-reasoning-model.md`

## 📚 相关文件

- **SKILL.md**: 本文件
- **client.py**: Python客户端模块（含cleanup/get_storage_stats）
- **cleanup.py**: 清理脚本（CLI入口）
- **README.md**: 详细使用文档
- **references/cleanup-jsonl-fix.md**: cleanup() 对 .jsonl 文件的修复方案（2026-06-01）
- **references/mimo-reasoning-model.md**: mimo-v2.5-pro reasoning_content 集成说明

## 📖 方法论参考

思维验证方法论详见 `hermes-agent` skill 的 `references/thinking-verification.md`，包含：
- Chain of Verification (CoVe) - Meta AI
- Socratic Questioning - Mirror Agent
- Constitutional AI 自我批评
- Red Team / Blue Team 对抗测试

**核心原则**：在做决策前，问自己"有没有反例？"、"一定是对的吗？"、"如果错了会怎样？"

**ARIS分类案例**（2026-05-30）：
- 决策："ARIS是Agent"
- 验证：ARIS有CLI（tools/目录有.py和.sh文件）
- 反例：ARIS描述说"Markdown-only skills"，核心是81个.md文件
- 结论：ARIS是Skills，不是Agent → CLI不能作为判定标准
- 修正：分类流程从6步精简为5步
