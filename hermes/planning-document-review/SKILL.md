---
name: planning-document-review
description: "Analyze planning/architecture documents for implementation readiness. Section-by-section review with severity ratings, gap analysis, inconsistency detection, and prioritized action lists. Use when user says 'review this plan', 'analyze this spec', 'check this document for completeness', 'is this ready to implement', or provides a planning document and asks for assessment."
version: 1.0.0
tags: [review, planning, architecture, analysis, document, gap-analysis]
---

# Planning Document Review

Analyzes planning/architecture documents for **implementation readiness** — not logical soundness (use `logic`), not production readiness (use `production-audit`), but "does this document contain enough detail to be correctly implemented?"

## When to Use

- User says "review this plan", "analyze this spec", "check this document"
- User says "is this ready to implement", "what's missing from this design"
- User provides a planning/design document and asks for assessment
- Before handing a spec to a coding agent (Claude Code, Codex, etc.)

## When NOT to Use

- Reviewing code (use `security-review` or `code-review`)
- Checking logical soundness of an argument (use `logic` toolkit)
- Production readiness of shipped app (use `production-audit`)
- Reviewing a research paper (use `research-review`)

## Review Method

### Step 1: Document Inventory

Before analyzing content:
- Record file path, size, line count
- Identify document type: planning spec / architecture doc / RFC / design brief
- Note what it claims to cover (title, scope section, goals)

### Step 2: Section-by-Section Analysis

For EACH section of the document, evaluate:

1. **Clarity**: Can a developer implement this without guessing?
2. **Completeness**: Are all necessary details present?
3. **Consistency**: Does it agree with other sections?
4. **Feasibility**: Can this actually be built as described?
5. **Testability**: Can you verify this section's requirements?

Mark each finding with a severity:

```
[严重] = Must fix before implementation starts (blocks development)
[重要] = Should fix (causes rework or quality issues if skipped)
[建议] = Nice to have (improves quality but not blocking)
```

### Step 3: Cross-Cutting Issues

After reviewing all sections, look for issues that span multiple sections:
- **Missing design**: Entire topics not addressed by any section
- **Contradictions**: Sections that conflict with each other
- **Implicit assumptions**: Things the author assumed but didn't state
- **Missing error handling**: Happy path only, no failure modes
- **Missing quantification**: Vague criteria that can't be measured
- **Scope creep items**: Things included that shouldn't be in this version
- **Missing prerequisites**: Dependencies not accounted for

### Step 4: Gap Classification

Group all findings by type:

| Gap Type | Description | Example |
|----------|-------------|---------|
| Missing section | Entire topic not covered | No error handling strategy |
| Missing detail | Section exists but is vague | "Handle errors appropriately" |
| Ambiguity | Could be interpreted multiple ways | "Small scale training" |
| Inconsistency | Two sections contradict | List in doc A ≠ list in doc B |
| Missing quantification | No numbers or thresholds | "Improve performance" |
| Missing mechanism | How is never specified | "Agent calls CLI" (how?) |
| Missing fallback | No plan B | What if API is down? |
| Scope issue | Too broad or too narrow for stated goals | V1.0 includes V3.0 features |

### Step 5: Prioritized Action List

Produce a single ranked list:

```
P0 (must fix, blocks implementation):
  1. [finding with specific fix suggestion]
  2. ...

P1 (should fix, causes rework):
  3. ...

P2 (nice to have):
  ...
```

Each item must include:
- What's wrong (one sentence)
- Where in the document (section name or line reference)
- Specific fix suggestion (not just "add more detail")

### Step 6: One-Line Verdict

End with a single sentence:

```
Verdict: [Ready to implement / Needs P0 fixes first / Needs major revision]
The document covers [X] of [Y] necessary topics, with [N] critical gaps
in [specific areas].
```

## Output Format

```
================================================================
  [Document Title] — Implementation Readiness Review
================================================================

File: [path]
Size: [chars/lines]
Type: [planning spec / architecture doc / RFC]

## Section [N]: [Title]

[What's well-defined]
[What's missing or ambiguous]
[Specific findings with severity tags]

[... repeat for each section ...]

## Cross-Cutting Issues

[Issues that span multiple sections]

## Summary: Prioritized Action List

P0: [items]
P1: [items]
P2: [items]

## Verdict

[One-line assessment]
```

## Execution Feasibility Review (Agent-Executable Plans)

When reviewing a plan that will be **executed by an AI agent** (Claude Code, Hermes, Codex, etc.), apply a stricter lens than general implementation readiness. Agent-executable plans have unique failure modes:

### Agent-Specific Red Flags

1. **Core value deferred behind infrastructure.** If the plan spends 80%+ of tasks on plumbing (state machines, protocols, guards) and pushes the actual value-producing work to the last task, the agent will exhaust its budget on scaffolding. Check: what is the deliverable? How many tasks until first deliverable?

2. **Missing "engine" definitions.** The plan defines lifecycle, guards, cleanup — but never defines HOW the core artifact is created. E.g., a reward optimization plan that defines candidate states but never shows the LLM prompt that generates candidates. An agent will reach that task and freeze.

3. **Over-engineered state machines for V1.** Count the states. If V1 has 10+ states and 10+ transitions, question whether a 5-state version would work. State machine complexity is the #1 cause of agent implementation getting stuck.

4. **Contradictions between process model and actual requirements.** E.g., "single process" stated but "parallel execution" needed. Agent will implement one and break the other.

5. **Cross-platform implementation assumptions.** `fcntl.flock` on Windows, `SIGTERM` handling, atomic file operations — these have platform-specific failure modes that agents often miss.

6. **Vague scoring/formula mechanisms.** "improve_score" referenced 20 times but formula never given. Agent will invent a formula that may be wrong.

7. **No incremental delivery path.** If the plan has 12 sequential tasks and no "demo after task 3", the agent has no way to validate its work until very late.

8. **Implicit process management.** Assumes the caller can send SIGTERM, track PIDs, handle timeouts — but the actual caller (Claude Code/Hermes subprocess) may not support this.

### Severity for Agent Plans

- **[致命]** = Agent cannot start or will get stuck mid-implementation (missing engine, missing core mechanism)
- **[严重]** = Will cause rework or implementation divergence (contradictions, over-engineering)
- **[中等]** = Affects quality but won't block progress (missing validation, vague thresholds)

### Verdict for Agent Plans

End with:
```
Verdict: Agent can execute / Agent will likely get stuck at Task [N] / Needs major revision before agent execution
The plan's core value is [deferred to Task N / adequately front-loaded].
The [engine/mechanism/generator] is [defined / missing / underspecified].
```

## Pitfalls

- **Don't rewrite the document.** Review it. The output is findings + suggestions, not a new document.
- **Don't expand scope.** If the document says "V1.0 only", review V1.0 scope. Don't suggest adding V2.0 features.
- **Be specific.** "Missing error handling" is weak. "Section 5 (Experiment Runner) has no handling for training crash (exit code ≠ 0)" is strong.
- **Distinguish 'nice to have' from 'must have'.** Not every gap is critical. Use severity tags honestly.
- **Check cross-references.** If section A references section B's list, verify they match.
- **Don't assume implementation details.** If the document says "use CLI commands", don't assume they know which commands. Verify the commands are defined.
- **Quantify when possible.** "Small training" → "How many steps? Define default." "Improve metrics" → "By how much? Define threshold."
- **For agent-executable plans: check if the "engine" is defined.** A plan that defines everything except the core mechanism (LLM prompt, generator, transformer) is a skeleton without muscles.
- **Check for "core value deferred" anti-pattern.** Count tasks before first deliverable. If > 60% of tasks are infrastructure before any value, flag it.
