# Logic Chain Skills Installation (2026-05-30)

## Installed Skills

### 1. Skills for Humanity (⭐99) - 171 skills
**Repository**: https://github.com/human-avatar/skills-for-humanity
**Location**: `~/.hermes/skills/hermes/skills-for-humanity/`
**Description**: Structured reasoning methodologies from history's most rigorous thinkers

**Categories (27 total)**:
| Category | Skills | Purpose |
|----------|--------|---------|
| Think Sharper | logic, probability, decision, constraint, game-theory, epistemology, investigation | 逻辑推理、概率分析 |
| Think Differently | creativity, analogy, play | 创造性思维、类比推理 |
| Think About People | communication, social, emotional, ethics, identity, narrative, psychology, mindset, writing | 人际智能、情感分析 |
| Think in Time & Systems | systems, temporal, historical, resource, strategy | 系统思维、历史分析 |
| See More Clearly | aesthetic, sensory | 美学判断、感官观察 |

**Key Skills (most useful for reasoning)**:
- `/logic-check` - Fast logic report
- `/logic-argument-validation` - Validate arguments
- `/logic-consistency-check` - Find contradictions
- `/creativity-brainstorm` - Multi-method creative sprint
- `/creativity-six-hats` - Six Thinking Hats
- `/decision-criteria-weighting` - Weighted decision matrix
- `/investigation-claim-decomposition` - Break claims into parts

### 2. Future Tokens (⭐61)
**Repository**: https://github.com/jordanrubin/FUTURE_TOKENS
**Location**: `~/.hermes/skills/hermes/future-tokens/`
**Description**: Composable reasoning skills targeting AI output blind spots

**Operations**:
- `antithesize` - Generate counter-arguments
- `excavate` - Surface hidden assumptions
- `metaphorize` - Find analogies
- `synthesize` - Combine perspectives
- `dimensionalize` - Multi-dimensional analysis
- `handlize` - Practical action steps
- `inductify` - Pattern generalization

### 3. Prompt Decorators (⭐469)
**Repository**: https://github.com/smkalami/prompt-decorators
**Location**: `~/.hermes/skills/hermes/prompt-decorators/`
**Description**: Structured prefixes to enhance AI reasoning

**Key Decorators**:
- `+++Reasoning` - Detailed reasoning explanation
- `+++StepByStep` - Structured step-by-step response
- `+++Socratic` - Socratic questioning approach
- `+++Debate` - Multi-perspective analysis
- `+++Critique` - Constructive criticism
- `+++FactCheck` - Fact verification

## Installation Pattern

```python
import subprocess, os

skills_to_install = [
    {"name": "skills-for-humanity", "url": "https://github.com/human-avatar/skills-for-humanity.git"},
    {"name": "future-tokens", "url": "https://github.com/jordanrubin/FUTURE_TOKENS.git"},
    {"name": "prompt-decorators", "url": "https://github.com/smkalami/prompt-decorators.git"},
]

skills_base_dir = r"C:\Users\lenovo_mml\.hermes\skills\hermes"
for skill in skills_to_install:
    skill_dir = os.path.join(skills_base_dir, skill["name"])
    if not os.path.exists(skill_dir):
        subprocess.run(["git", "clone", "--depth", "1", skill["url"], skill_dir], timeout=120)
```

## Impact

- **Before**: 172 skills
- **After**: 306 skills (+134)
- **New capability**: Complete logical reasoning framework, creative thinking, decision analysis

## Usage Tips

1. **For logic checks**: Use `/logic-check` or `/logic-argument-validation`
2. **For creative thinking**: Use `/creativity-brainstorm` or `/creativity-six-hats`
3. **For decisions**: Use `/decision-criteria-weighting` or `/decision-premortem-analysis`
4. **For investigations**: Use `/investigation-claim-decomposition` or `/investigation-evidence-audit`
