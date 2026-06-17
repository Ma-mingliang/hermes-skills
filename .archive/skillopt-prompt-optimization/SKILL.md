---
name: skillopt-prompt-optimization
description: "Use SkillOpt to iteratively optimize any Hermes skill's prompts (SKILL.md, agent_prompts.py). Covers environment setup, training data preparation, MiMo v2.5 Pro compatibility fixes, 13-dimension 3-prompt serial evaluation, and .env override pitfalls."
version: "1.3.0"
tags: ["skillopt", "prompt-optimization", "skill-development", "mimo", "training"]
---

# SkillOpt Prompt Optimization

Use SkillOpt (Microsoft, ⭐4600+) to iteratively optimize Hermes skill prompts through rollout → reflect → evaluate loops.

## When to Use

- User says "optimize prompts", "SkillOpt training", "improve skill prompts"
- A skill's prompts are underperforming and need systematic improvement
- Want to test prompt variations against real data

## Prerequisites

- SkillOpt installed: `pip install skillopt` (v0.1.0+)
- MiMo v2.5 Pro API key configured in `~/.hermes/.env`
- Target skill has historical data (reports, outputs, etc.)

## Quick Start

```bash
cd D:/openclaw-hermes/SkillOpt
# Set up environment
set -a; source .env; set +a
# Run training
python scripts/train.py --config configs/<skill-name>/default.yaml
```

## Architecture

```
SkillOpt/
├── configs/<skill>/default.yaml    # Training config
├── skillopt/envs/<skill>/
│   ├── adapter.py                  # Environment adapter
│   ├── dataloader.py               # Data loader
│   ├── rollout.py                  # Rollout + Reflect logic
│   ├── evaluator.py                # Evaluation logic
│   └── skills/initial.md           # Initial skill prompt
├── data/<skill>/
│   ├── train/items.json
│   ├── val/items.json
│   └── test/items.json
└── outputs/<skill>/                # Training results
    ├── best_skill.md               # Optimized prompt
    ├── history.json                # Training history
    └── steps/                      # Per-step records
```

## CRITICAL: Edit Format

SkillOpt expects edits with these exact field names:

```json
{
  "op": "append" | "insert_after" | "replace" | "delete",
  "content": "new content to add/replace with",
  "target": "existing text to find (for replace/delete/insert_after)"
}
```

**NOT** these (common mistake):
```json
{
  "operation": "add",     ← WRONG field name
  "old_text": "",          ← WRONG field name  
  "new_text": "..."        ← WRONG field name
}
```

Operation mapping:
- `add` → `append` (append to end of skill)
- `replace` → `replace` (find target, replace with content)
- `delete` → `delete` (find target, remove it)

## CRITICAL: MiMo v2.5 Pro Compatibility

MiMo has intermittent empty responses for complex English prompts.

**Fixes applied in rollout.py:**
1. All prompts in Chinese (MiMo handles Chinese more reliably)
2. Retry logic: 3 attempts with temperature increment (0.2 → 0.3 → 0.4)
3. Simplified prompt structure with examples
4. Empty response check before returning

```python
def _call_llm(system_prompt, user_prompt, max_tokens=4096, max_retries=3):
    for attempt in range(max_retries):
        # temperature increases with retries
        payload["temperature"] = 0.2 + attempt * 0.1
        # ... call API ...
        if content and content.strip():
            return content
        # empty response → retry
    return ""
```

## CRITICAL: Evaluation — MiMo 评估修复

**根本原因**：MiMo v2.5 Pro 的 thinking 模式（默认开启）导致评估类 prompt 返回空。不是 prompt 复杂度问题。

**修复方案（v2.0）**：`thinking: {"type": "disabled"}` + 3-prompt 串行评估

```python
payload = {
    "model": model,
    "messages": [...],
    "thinking": {"type": "disabled"},  # 关键修复
}
```

**3-prompt 串行评估设计**（evaluator.py v2, 13维度）：

| Prompt | 维度 | 权重 |
|--------|------|------|
| 1 — 核心维度 | relevance(15%), completeness(15%), accuracy(15%), specificity(15%) | 60% |
| 2 — 执行维度 | actionability(10%), clarity(10%), coverage(10%), consistency(10%) | 40% |
| 3 — 质量维度 | robustness(10%), verifiability(10%), examples(5%), safety(5%), maintainability(5%) | 35% |

总权重135%，`_weighted_score()`自动归一化。每个prompt只评估4-5个维度，失败时独立重试。`_retry_call()`包装每个调用，最多重试2次。

**为什么拆分有效**：
- thinking 修复后 MiMo 能正常响应评估 prompt
- 每个 prompt 更聚焦（2维度 vs 5维度），降低空响应概率
- 单个维度失败不影响其他维度，可独立重试

**备用方案：规则评估**（不依赖 LLM，用于 LLM 完全不可用时）：

```python
def _evaluate_rule_based(skill_md):
    score = 30  # baseline
    numbers = re.findall(r'(?:star|阈值|threshold|>=|<=|>|<)\s*[>=]?\s*(\d+)', skill_md, re.IGNORECASE)
    rules = re.findall(r'(?:必须|不得|禁止|应该|规则|要求)', skill_md)
    sections = re.findall(r'^##\s+', skill_md, re.MULTILINE)
    examples = re.findall(r'(?:示例|例如|example)', skill_md, re.IGNORECASE)
    # 数值阈值>=3→+20, 规则>=5→+15, sections>=8→+15, 示例>=2→+10, 长度>4000→+10
    return {"overall": score, "method": "rule_based"}
```

**文件位置**：`D:\openclaw-hermes\SkillOpt\skillopt\envs\agent_daily_report\evaluator.py`

## Key Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Edit format wrong | `status: "skipped_unknown_op"` in edit_apply_report.json | Use `op`/`content`/`target` not `operation`/`old_text`/`new_text` |
| MiMo returns empty | `rollout_soft=0.50` (default) for all steps | Use Chinese prompts + retry logic |
| MiMo evaluation returns empty | All evaluation scores are 0.50 | Add `thinking: {"type": "disabled"}` to payload + use 3-prompt serial eval |
| `~/.hermes/.env` overrides SkillOpt `.env` | 401 Unauthorized despite correct key in SkillOpt/.env | `_load_env()` in rollout.py loads `~/.hermes/.env` first and breaks; see pitfall section below |
| `api.xiaomimimo.com` returns 401 | API key works on `token-plan-sgp` but not `api` endpoint | Force `token-plan-sgp.xiaomimimo.com/v1` in `_call_llm` when existing key detected |
| Missing directories | `FileNotFoundError` for steps/skills/slow_update | Pre-create all directories before training |
| .env not loaded | `HTTP 401 Unauthorized` | Remove `export` prefix from .env lines |
| patches=0 | reflect function called but no patches | Check LLM response content, add fallback |
| Timeout=0 in config | `Attempted to set connect timeout to 0` error | Fix in `agent_llm_client.py`: `self.timeout = max(30, int(...))` AND fix ALL config sections (see pitfalls) |
| Rate limiting (429) | LLM calls fail with 429 status | Add retry with exponential backoff, or reduce batch_size to 1 |
| Over-optimization | Scores drop when adding verbose structure | Make minimal targeted changes, don't add ## 目录 or ### 核心职责 headers |

## Training Data Format

```json
[
  {
    "id": "scenario_1",
    "input": {
      "date": "2026-06-04",
      "task": "optimize_prompts",
      "report_content": "...",
      "constraints": ["constraint 1", "constraint 2"]
    },
    "output": {
      "expected_quality": "high",
      "expected_improvements": ["improvement 1"],
      "evaluation_criteria": {
        "completeness": 80,
        "specificity": 90,
        "clarity": 85,
        "consistency": 80
      }
    }
  }
]
```

## References

- SkillOpt repo: https://github.com/microsoft/SkillOpt
- Edit application logic: `skillopt/optimizer/skill.py` → `_edit_fields()` extracts `op`, `content`, `target`
- Patch normalization: `skillopt/engine/trainer.py` → `_normalise_patches()` expects `edits` key
- See `references/agent-daily-report-integration.md` for complete working example
- See `references/agent-daily-report-pitfalls.md` for timeout, rate limiting, and network issues
- See `references/evaluator-v2-3prompt.md` for 3-prompt serial evaluator design
- See `references/manual-optimization-technique.md` for targeted dimension improvement

## Verify-First-Then-Optimize Pattern (CRITICAL)

When optimizing skills that contain factual claims (history, science, technical explanations), **always verify facts before optimizing prompts**. Optimizing an incorrect causal chain makes it more "convincing" but not more "correct."

### Workflow

1. **Extract all causal claims** from the skill content
2. **Delegate verification** to subagents (parallel, one per era/topic)
3. **Fix inaccurate claims** before running SkillOpt
4. **Then optimize** prompts, structure, examples

### Causal Chain Verification (for historical/educational skills)

```python
delegate_task(tasks=[
    {"goal": "Verify causal chains for Era 1...", "toolsets": ["web", "search"]},
    {"goal": "Verify causal chains for Era 2...", "toolsets": ["web", "search"]},
    {"goal": "Verify causal chains for Era 3...", "toolsets": ["web", "search"]},
])
```

**Verification checklist per claim**:
- [ ] Is the historical fact accurate? (dates, people, events)
- [ ] Is the causal direction correct? (A caused B, not just A preceded B)
- [ ] Are there multiple causes being oversimplified to one?
- [ ] Are there parallel developments being mistaken for sequential?
- [ ] Is the key paper/figure correctly attributed?

**Common pitfalls found in AI history**:
- "Neural networks failed → SVM replaced them" (actually coexisted)
- "Expert systems failed → Backpropagation revived" (parallel, not causal)
- "RNN couldn't parallel → Transformer invented" (accurate, paper confirms)
- "Word2Vec replaced BOW" (Word2Vec solved semantic capture, not BOW directly)

### Patch Pattern After Verification

After verification, patch the skill with:
1. Corrected causal chains
2. Key paper citations (author, year, title)
3. Nuance notes ("X and Y coexisted" / "Z was one of several causes")
4. Updated version number

Then run SkillOpt optimization rounds on the verified content.

---

## Manual Optimization Technique

When automated training stalls (score stuck at 0.0) or produces suboptimal results, manual targeted optimization is more effective.

### Workflow

1. **Run evaluation** to identify low-scoring dimensions (<80)
2. **Analyze root cause** for each low dimension
3. **Apply targeted fixes** based on dimension type:
   - `examples` (30→60): Add good/bad examples per section
   - `safety` (50→90): Add explicit safety checks with "必须执行" prefix
   - `robustness` (65→85): Add boundary handling rules
   - `coverage` (75→95): Add "边界处理" section for edge cases
   - `verifiability` (30→80): Add "输出格式（必须遵守）" section
   - `consistency` (80→95): Use "必须执行/遵守" prefix on all rules
4. **Re-evaluate** to verify improvements

### Dimension-Specific Patterns

**Improving consistency (80→90+)**:
- Add "必须执行" or "必须遵守" prefix to all rules
- Unify rule language across sections
- Ensure no contradictions between new and existing rules

**Improving safety (50→90+)**:
```markdown
安全检查（必须执行）:
- 不得编造版本号除非原始数据明确提供
- 不得编造Stars数除非原始数据明确提供
- 如果原始数据为空或不足，必须标注 "⚠️ 信息不足"
```

**Improving robustness (65→85+)**:
```markdown
边界处理（必须执行）:
- 如果 title 为空，使用 repo name 作为替代
- 如果 description 为空，使用 README 的第一段
- 如果两者都为空，标注 "⚠️ 信息不足，建议查看原文"
```

**Improving verifiability (75→90+)**:
```markdown
输出格式（必须遵守）:
- 每个条目必须包含: id, title_zh, description_zh, engineering_value
- title_zh 必须是中文
- description_zh 必须是中文，2-3句话
- engineering_value 不能是泛泛而谈（如"值得关注"）
```

**Improving examples (30→70+)**:
```markdown
示例（必须参考）:
好的示例: title_zh="Claude Code", description_zh="Anthropic 官方的 AI 编程助手"
坏的示例: title_zh="AI Project", description_zh="一个很棒的项目"
```

### CRITICAL: Over-Optimization Pitfall

**DO NOT** add verbose structure (## 目录, ### 核心职责, ### 执行步骤, etc.) to skills. The evaluator penalizes excessive length and complexity. A 6000-char skill scores higher than an 8000-char skill with the same content.

**What HURTS scores** (learned the hard way):
- Adding `## 目录` section → coverage drops 35 points
- Adding `### 核心职责` / `### 执行步骤` headers → actionability drops 20 points
- Adding too many examples (4+ per section) → examples drops 30 points
- Rewriting entire sections → consistency drops 15-20 points
- Adding verbose explanations → clarity drops 20 points

**What HELPS scores** (minimal targeted changes):
- Add "必须执行/遵守" prefix to existing rules → consistency +10
- Add 2-3 examples (not more) → examples +10-20
- Add "验证规则（必须遵守）" section → verifiability +20
- Add "安全检查（必须执行）" section → safety +15-40
- Add "边界处理（必须执行）" section → robustness +20
- Add version header `# Version: 2.0 | Updated: 2026-06-04` → maintainability +5

**Rule of thumb**: Make the SMALLEST possible change to target ONE dimension at a time. Don't touch sections that are already scoring well.

### Evaluator Non-Determinism

MiMo v2.5 Pro evaluation scores vary ±2-3 points between runs. Always run 3 evaluations and average:

```python
scores = []
for i in range(3):
    result = _evaluate_output(skill, item, output)
    scores.append(result['details']['overall'])
avg = sum(scores) / len(scores)  # Use this as the true score
```

This is expected behavior — the LLM's scoring has inherent randomness. Don't chase single-run improvements; look for consistent improvements across multiple runs.

### Results (Manual Optimization)

| Dimension | Initial | Auto v9 | Manual v1 | Final |
|-----------|---------|---------|-----------|-------|
| accuracy | 90 | 90 | 90 | 90 |
| actionability | 85 | 85 | 85 | 85 |
| clarity | 90 | 90 | 90 | 90 |
| completeness | 85 | 85 | 85 | 85 |
| consistency | 80 | 95 | 90 | 80-90 |
| coverage | 75 | 75 | 95 | 95 |
| examples | 30 | 30 | 70 | 60-70 |
| maintainability | 60 | 75 | 80 | 75-80 |
| relevance | 95 | 95 | 95 | 95 |
| robustness | 40 | 65 | 85 | 85 |
| safety | 20 | 50 | 95 | 90-95 |
| specificity | 80 | 95 | 95 | 80-95 |
| verifiability | 30 | 80 | 90 | 70-90 |
| **overall** | **71** | **82** | **88** | **86-88** |

## Weight Tuning Strategy

When targeting specific low-scoring dimensions, increase their weights in the evaluator:

```python
# Original weights (balanced)
weights = {
    "relevance": 0.15, "completeness": 0.15, "accuracy": 0.15, "specificity": 0.15,
    "actionability": 0.10, "clarity": 0.10, "coverage": 0.10, "consistency": 0.10,
    "robustness": 0.10, "verifiability": 0.10, "examples": 0.05,
    "safety": 0.05, "maintainability": 0.05,
}

# Tuned weights (emphasize weak dimensions)
weights = {
    "relevance": 0.10, "completeness": 0.10, "accuracy": 0.10, "specificity": 0.10,
    "actionability": 0.08, "clarity": 0.08, "coverage": 0.10, "consistency": 0.08,
    "robustness": 0.12, "verifiability": 0.12, "examples": 0.10,
    "safety": 0.10, "maintainability": 0.08,
}
```

**Key insight**: Weight tuning guides the optimizer to focus on weak areas, but manual optimization is often more effective for targeted improvements.
