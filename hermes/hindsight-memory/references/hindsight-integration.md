# Hindsight Integration Module

## Location
`~/.hermes/hindsight/client.py`

## Features
- Config loading from `~/.hermes/hindsight/config.yaml`
- Metadata sanitization (bool→string conversion)
- Convenience functions: `store_conversation_memory()`, `recall_relevant_memories()`
- User preference learning

## Usage

```python
from hindsight.client import HindsightMemory, store_conversation_memory, recall_relevant_memories

# Full API
memory = HindsightMemory()
memory.store_memory("content", metadata={"key": "value"})
results = memory.recall_memory("query", max_tokens=4096)

# Convenience
store_conversation_memory("content")
results = recall_relevant_memories("query")
```

## Key Implementation Details

1. **Metadata sanitization**: All metadata values converted to strings before API call
2. **Default bank**: Uses "hermes" from config
3. **Singleton pattern**: `get_hindsight_memory()` returns shared instance
4. **Error handling**: Prints errors, returns False/[] on failure

## Config File (`~/.hermes/hindsight/config.yaml`)

```yaml
hindsight:
  base_url: "http://localhost:8888"
  default_bank_id: "hermes"
  memory:
    recall_limit: 5
    store_threshold: 0.7
  learning:
    enabled: true
    frequency: 10
```

## Hermes Config Integration

In `~/.hermes/config.yaml`:
```yaml
hindsight:
  enabled: true
  base_url: "http://localhost:8888"
  default_bank_id: "hermes"
  auto_store: true
  auto_recall: true
  learning_enabled: true

memory:
  provider: "hindsight"
  hindsight_enabled: true
```

## File Structure

```
~/.hermes/hindsight/
├── client.py              # Integration module
├── config.yaml            # Configuration
├── test_integration.py    # Test script
├── USAGE_GUIDE.md         # Detailed guide
├── QUICK_REFERENCE.md     # Quick reference
└── README.md              # Overview
```
