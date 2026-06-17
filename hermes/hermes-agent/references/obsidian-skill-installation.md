# Obsidian Second Brain Skill Installation (2026-06-02)

## Overview

Installed `eugeniughelbur/obsidian-second-brain` (⭐1931) — cross-CLI skill for Obsidian vault management via AI agents.

## Installation Steps (Hermes-specific, no Claude Code setup.sh)

The skill's `scripts/setup.sh` is designed for Claude Code (`~/.claude/settings.json`). For Hermes, manual setup is required:

### 1. Search & Clone

```python
# Search GitHub
url = "https://api.github.com/search/repositories?q=obsidian+claude+code+skill&sort=stars&order=desc&per_page=20"

# Clone highest-starred match
git clone https://github.com/eugeniughelbur/obsidian-second-brain.git D:\openclaw-hermes\obsidian-second-brain
```

### 2. Install Obsidian Application

```python
# Download installer (version pattern)
url = "https://github.com/obsidianmd/obsidian-releases/releases/download/v1.8.10/Obsidian-1.8.10.exe"
# Save to D:\Obsidian-Setup.exe, run with /S for silent install
```

### 3. Create Vault

```python
vault_path = r"D:\ObsidianVault"
os.makedirs(vault_path, exist_ok=True)
# Create .obsidian/app.json with basic config
```

### 4. Copy Skill to Hermes

```python
source = r"D:\openclaw-hermes\obsidian-second-brain"
dest = os.path.expanduser("~/.hermes/skills/obsidian-second-brain")
# Copy: SKILL.md, commands/, references/, scripts/, hooks/, adapters/
```

### 5. Configure Vault Path

```python
# Add to ~/.hermes/.env
# OBSIDIAN_VAULT_PATH=D:\ObsidianVault

# Create skill config
config = {"vault_path": "D:\\ObsidianVault", "auto_sync": True}
# Write to ~/.hermes/skills/obsidian-second-brain/config.json
```

### 6. Bootstrap Vault

```python
# Run bootstrap script (pipe 'y' to confirm if vault exists)
proc = subprocess.Popen(
    ["python", bootstrap_script, "--path", vault_path, "--name", "Hermes User"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
)
stdout, stderr = proc.communicate(input='y\n', timeout=60)
```

### 7. Post-Install

- Restart Hermes Gateway to load the new skill
- Open Obsidian → Open vault → Select `D:\ObsidianVault`
- Recommended plugins: Dataview, Templater, Kanban, Calendar

## Pitfalls

- `setup.sh` fails on Windows/WSL — must do manual copy
- `bootstrap_vault.py` prompts for confirmation if vault exists — pipe 'y' via stdin
- No `--force` flag on bootstrap — use stdin confirmation instead
- GitHub API may hit SSL/rate limits — use browser fallback or direct URL pattern
- MCP tools may fail if GitHub token not in gateway environment — reconnect needed

## Skill Features

- 43 commands for vault management
- AI-first vault rule: self-contained context, rich frontmatter, cross-links mandatory
- Bi-temporal facts: never overwrite, always append with timeline
- Auto-synthesis: sources rewrite existing pages instead of appending
- Research toolkit: /x-read, /x-pulse, /research, /research-deep, /notebooklm, /youtube, /podcast
