# Classification Flow Fix — 2026-05-30

**User Correction**: CLI cannot be used as a condition for Agent classification

## Problem

The old classification flow incorrectly used CLI as a condition:
```
Step 5: 有API/Web UI/CLI？ → 有 → 🤖 Agent
```

This caused misclassification:
- Claude Code has CLI → correctly classified as Agent (but for wrong reason)
- ECC has CLI → correctly classified as Component (but for wrong reason)

## Corrected Flow

```
Step 1: 描述含"skill(s)" → 📚 Skills
Step 2: 主要是.md文件（.md > .py） → 📚 Skills
Step 3: 需要其他Agent平台才能运行？→ 需要 → 🧩 Agent组件
Step 4: 能独立运行 + 有API/Web UI？ → 有 → 🤖 Agent（CLI不算）
Step 5: 以上都不满足 → 🧩 Agent组件
```

## Key Principle

**CLI is an interface format, not a classification criterion.**
- Agent can have CLI (Claude Code has `claude` CLI)
- Component can have CLI (ECC has `ecc` CLI)
- The real question: Can it run independently? Does it depend on other Agent platforms?

## Files Modified

1. `SKILL-full.md` — Main classification flow
2. `SKILL.md` — Compressed version
3. `references/classification-decision-tree.md` — Decision tree
4. `references/agent-classification-guide.md` — Guide
5. `references/classification-correction-2026-05-29.md` — Correction log
6. `references/classification-flow-v2.md` — Flow v2
7. `references/SKILL-balanced.md` — Balanced version

## Verification

After fix, all files should contain:
- `CLI不能作为判定Agent的条件`
- `能独立运行 + 有API/Web UI（CLI不算）`
- `需要其他Agent平台才能运行`

## Examples

| Project | CLI | Independent | Needs Platform | Classification |
|---------|-----|-------------|----------------|----------------|
| Claude Code | ✅ | ✅ | ❌ | 🤖 Agent |
| ECC | ✅ | ❌ | ✅ (Claude Code) | 🧩 Component |
| ARIS | ❌ | ❌ | ❌ | 📚 Skills |
| n8n | ❌ | ✅ | ❌ | 🤖 Agent |
