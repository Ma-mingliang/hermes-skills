# Thinking Verification Patterns

Self-critique and verification patterns for AI decision-making.

## Core Concept

Before executing a decision, verify it by:
1. Generating verification questions ("Is there a counterexample?", "Is this always true?")
2. Answering the questions
3. Checking if counterexamples hold
4. Adjusting the decision if needed

## Example: Classification Flow Verification

**Original flow**: 6 steps for classifying Agent/Skills/Components

**Verification questions**:
- "Is there a counterexample to Step 4 (CLI = component)?"
- "Does ARIS have CLI? Is it a component?"

**Counterexample found**:
- ARIS has CLI tools (tools/ directory with .py and .sh files)
- But ARIS is Skills (core is 81 .md files, described as "Markdown-only skills")
- ECC has CLI but is Agent Component (depends on other Agent platforms)

**Conclusion**: CLI cannot be used as a classification criterion

**Adjusted flow**:
```
Step 1: Description contains "skill(s)" → Skills
Step 2: Mainly .md files → Skills
Step 3: Needs other Agent platform? → Yes → Agent Component
Step 4: Can run independently + has API/Web UI? → Yes → Agent
Step 5: None of the above → Agent Component
```

## Methods

### 1. Chain of Verification (CoVe) - Meta AI (⭐204)
- Generate initial answer
- Generate verification questions
- Answer verification questions
- Revise answer based on verification results

**Reference**: https://github.com/ritun16/chain-of-verification

### 2. Socratic Questioning (Mirror Agent ⭐67)
- Self-questioning before decisions
- "Is there a counterexample?"
- "Is this always true?"
- "What if I'm wrong?"

**Reference**: https://github.com/DannyMac180/mirror-agent

### 3. Constitutional AI
- Self-criticism before decisions
- "Does this comply with principles?"
- Check against defined principles
- Revise if non-compliant

### 4. Red Team / Blue Team
- Blue Team: maintains the system
- Red Team: tries to find counterexamples
- If counterexample found → fix the system

## Implementation in Reasoning Trace

The Reasoning Trace skill supports this workflow:

```python
from client import start_trace, trace_step, end_trace

# Start recording
task_id = start_trace("classification", "Classify ARIS")

# Record reasoning
trace_step("reasoning", "ARIS has CLI tools in tools/ directory")
trace_step("verification", "Is there a counterexample? ARIS has CLI but is Skills")
trace_step("decision", "CLI cannot be used as classification criterion")

# End recording
end_trace("success")
```

## Key Lessons

1. **Self-verification**: Verify answers before generating them
2. **Counterexample check**: Check for counterexamples before making judgments
3. **Consistency check**: Ensure answers are consistent with prior analysis
4. **Thinking monitoring**: Record thinking process for replay and correction

## Common Pitfalls

1. **Verbal slip**: Saying "Agent" when meaning "Skills" (思维跳跃)
2. **Missing verification**: Not checking if answer is consistent with analysis
3. **Missing counterexamples**: Not checking for counterexamples
4. **Attention drift**: Losing focus during comparison tasks

## Integration Points

- **Reasoning Trace**: Record verification process
- **Skill Classification**: Apply verification to classification decisions
- **AI Daily Report**: Verify before publishing
- **Research**: Verify findings before claiming results
