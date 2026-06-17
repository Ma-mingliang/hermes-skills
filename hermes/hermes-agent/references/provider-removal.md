# Removing a Provider from Hermes

To completely remove a provider (e.g., DeepSeek) from Hermes model call chain, clean all 3 config files.

## Files to Clean

| File | What to Remove |
|------|---------------|
| `~/.hermes/config.yaml` | Model/provider lines under `model:` and any `fallback_providers` entries |
| `~/.hermes/auth.json` | Entry in `credential_pool.<provider_name>` |
| `~/.hermes/.env` | API key and base URL env vars (e.g., `DEEPSEEK_API_KEY`, `DEEPSEEK_BASE_URL`) |

## Procedure

```python
import os, json

# 1. config.yaml - remove model/provider lines
config_file = os.path.expanduser("~/.hermes/config.yaml")
with open(config_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if '<provider_name>' in line.lower():
        print(f"Removed: {line.rstrip()}")
        continue
    new_lines.append(line)

with open(config_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

# 2. auth.json - remove credential_pool entry
auth_file = os.path.expanduser("~/.hermes/auth.json")
with open(auth_file, 'r', encoding='utf-8') as f:
    auth = json.load(f)

pool = auth.get("credential_pool", {})
if "<provider_name>" in pool:
    del pool["<provider_name>"]

with open(auth_file, 'w', encoding='utf-8') as f:
    json.dump(auth, f, indent=2, ensure_ascii=False)

# 3. .env - remove API key and base URL
env_file = os.path.expanduser("~/.hermes/.env")
with open(env_file, 'r', encoding='utf-8') as f:
    env_lines = f.readlines()

new_env = []
for line in env_lines:
    if '<provider_name>' in line.lower():
        print(f".env removed: {line.rstrip()}")
    else:
        new_env.append(line)

with open(env_file, 'w', encoding='utf-8') as f:
    f.writelines(new_env)

# 4. Verify - count remaining references
for fname, path in [("config.yaml", config_file), ("auth.json", auth_file), (".env", env_file)]:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    count = content.lower().count('<provider_name>')
    print(f"{fname}: {count} remaining references")
```

## Verification
All 3 files should show 0 remaining references for the provider name.
Restart gateway after removal for changes to take effect.

## Example: DeepSeek Removal (2026-06-02)
- Removed `deepseek-v4-pro` model/provider from config.yaml (was already commented out due to HTTP 402)
- Removed `deepseek` entry from auth.json credential_pool (had API key + base_url)
- Removed `DEEPSEEK_API_KEY`, `DEEPSEEK_BASE_URL`, and comment lines from .env
- Verified: 0 remaining references in all 3 files
