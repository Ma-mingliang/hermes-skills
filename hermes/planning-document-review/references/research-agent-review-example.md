# Example: Research Optimization Agent Platform V1.0 — Execution Feasibility Review

## Input

Document: `newplan.executable.md`
Size: 121,818 chars, 3,684 lines
Type: Agent-executable plan (product spec + API contract + implementation plan)
Target executor: AI Agent (Claude Code / Hermes)

## Review Angle

Ruthless execution feasibility — can an agent actually build this? Where will it get stuck?

## Fatal Issues (Agent Cannot Start or Will Freeze)

### 1. Core Value Deferred

12 tasks defined. Tasks 1-11 are infrastructure. Task 12 is the first to touch core value. Agent will spend 80% budget on scaffolding.

### 2. LLM Call Layer Undefined

`llm_client.py` appears in directory structure but entire document has zero detail on: model selection, prompt templates, token budget, rate limiting, retry strategy, error handling. This is the engine of the system — every other component depends on it.

### 3. Candidate Patch Generation Mechanism Missing

12 candidate states defined, guard rules, cleanup strategy — but HOW to generate a patch is never stated. What prompts? What format (unified diff? AST?)? How to validate syntax? Agent will manage candidate lifecycle without being able to create candidates.

### 4. `improve_score` Formula Never Given

Referenced throughout as acceptance/rejection criterion. Only described as "按 primary weights 和 safety penalty 计算". No formula, no weighting scheme, no threshold.

## Severe Issues (Will Cause Rework)

### 5. Document Triple-Role Failure

Claims to be product spec + API contract + implementation plan. Fails at all three:
- No user stories or success criteria (product spec)
- JSON schemas scattered, no versioning (API contract)
- No time estimates, dependencies, milestones (implementation plan)

### 6. Over-Complex State Machine for V1

12 phase states, 11 candidate states, 11 stop_reasons. V1 needs ~5 states. Implementation + testing of state machine alone could consume 40% of project budget.

### 7. Cross-Platform Lock Unreliable

`open(path, 'x')` has TOCTOU race on Windows. PID detection can false-positive on PID reuse. No heartbeat for 336-hour runs.

### 8. `run-plan` Claims Single Process but Needs Parallelism

Document says "single process" but execution scheduler section describes parallel screening with multiple seeds. Contradiction.

## Medium Issues (Quality Impact)

- Paper pipeline has no quality guarantee (LLM-based classification without defined labels)
- Reward hacking detection is post-hoc, not preventive
- No intermediate artifact validation timing defined
- Front-agent contract assumes capabilities (SIGTERM, timeout detection) that callers may not have
- No LLM prompt regression tests in test strategy
- Log rotation design has race conditions

## Verdict

Agent will likely get stuck at Task 4 (project understanding) because LLM call layer is undefined. Even if bypassed, Task 11 (executor lifecycle) will stall because candidate patch generation mechanism is missing. The plan's core value (reward optimization) is deferred to the last task. Needs major revision before agent execution: define the LLM layer, define patch generation, simplify state machine to 5 states, front-load one optimizer to demonstrate value.
