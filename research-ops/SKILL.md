---
name: research-ops
description: Evidence-first current-state research workflow for ECC. Use when the user wants fresh facts, comparisons, enrichment, or a recommendation built from current public evidence and any supplied local context.
origin: ECC
---

# Research Ops

Use this when the user asks to research something current, compare options, enrich people or companies, or turn repeated lookups into a monitored workflow.

This is the operator wrapper around the repo's research stack. It is not a replacement for `deep-research`, `exa-search`, or `market-research`; it tells you when and how to use them together.

## Skill Stack

Pull these ECC-native skills into the workflow when relevant:

- `exa-search` for fast current-web discovery
- `deep-research` for multi-source synthesis with citations
- `market-research` when the end result should be a recommendation or ranked decision
- `lead-intelligence` when the task is people/company targeting instead of generic research
- `knowledge-ops` when the result should be stored in durable context afterward

## When to Use

- user says "research", "look up", "compare", "who should I talk to", or "what's the latest"
- the answer depends on current public information
- the user already supplied evidence and wants it factored into a fresh recommendation
- the task may be recurring enough that it should become a monitor instead of a one-off lookup

## Guardrails

- do not answer current questions from stale memory when fresh search is cheap
- separate:
  - sourced fact
  - user-provided evidence
  - inference
  - recommendation
- do not spin up a heavyweight research pass if the answer is already in local code or docs

## Workflow

### 1. Start from what the user already gave you

Normalize any supplied material into:

- already-evidenced facts
- needs verification
- open questions

Do not restart the analysis from zero if the user already built part of the model.

### 2. Classify the ask

Choose the right lane before searching:

- quick factual answer
- comparison or decision memo
- lead/enrichment pass
- recurring monitoring candidate

### 3. Take the lightest useful evidence path first

- use `exa-search` for fast discovery
- escalate to `deep-research` when synthesis or multiple sources matter
- use `market-research` when the outcome should end in a recommendation
- hand off to `lead-intelligence` when the real ask is target ranking or warm-path discovery

### 4. Report with explicit evidence boundaries

For important claims, say whether they are:

- sourced facts
- user-supplied context
- inference
- recommendation

Freshness-sensitive answers should include concrete dates.

### 5. Decide whether the task should stay manual

If the user is likely to ask the same research question repeatedly, say so explicitly and recommend a monitoring or workflow layer instead of repeating the same manual search forever.

## Output Format

```text
QUESTION TYPE
- factual / comparison / enrichment / monitoring

EVIDENCE
- sourced facts
- user-provided context

INFERENCE
- what follows from the evidence

RECOMMENDATION
- answer or next move
- whether this should become a monitor
```

## Tool Integration Evaluation

When the user asks "can I use tool X to solve problem Y in my system?", use this framework:

### 1. Ecosystem Discovery
- Search GitHub for the tool AND its ecosystem (not just single repo)
- Check npm/pypi for related packages
- Look for companion tools (e.g., caveman → cavemem → cavekit → cavegemma)

### 2. Architecture Analysis
- Read README for: design intent, supported platforms, integration model
- Identify: hooks-based vs native, coding-assistant vs general-purpose
- Check: does it need npm/pip install? MCP? API keys?

### 3. Platform Compatibility
- Check open issues for platform-specific bugs (especially Windows)
- Look for: path handling, shell compatibility, dependency issues
- Search issues for your OS/environment keywords

### 4. Feasibility Matrix

| Dimension | Question | Weight |
|-----------|----------|--------|
| Architecture match | Does its design model match your system? | High |
| Platform support | Does it work on your OS/environment? | High |
| Integration complexity | How much setup/config/migration? | Medium |
| Existing solution | Do you already have something that works? | High |
| Maintenance burden | Active development? Known issues? | Medium |

### 5. Recommendation
- Clear YES/NO with reasoning
- If NO: what's the better alternative?
- If YES: what's the integration path?

## Reference Files

- `references/caveman-ecosystem.md` — Analysis of caveman/cavemem ecosystem (66k⭐), architecture, Windows issues, and integration assessment for Hermes

## Pitfalls

- do not mix inference into sourced facts without labeling it
- do not ignore user-provided evidence
- do not use a heavy research lane for a question local repo context can answer
- do not give freshness-sensitive answers without dates
- do not recommend tools without checking platform-specific issues
- do not assume a tool works for your use case just because it's popular

## Verification

- important claims are labeled by evidence type
- freshness-sensitive outputs include dates
- the final recommendation matches the actual research mode used
- tool recommendations include platform compatibility check
