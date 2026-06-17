# Installing Claude Code Skills into Hermes

Skills designed for Claude Code can be adapted to work with Hermes. The obsidian-second-brain (⭐1931) installation serves as the reference pattern.

## General Pattern

### 1. Clone the repo
```python
import subprocess, os
target_dir = r"D:\openclaw-hermes\<skill-name>"
subprocess.run(["git", "clone", "<repo-url>", target_dir], timeout=60)
```

### 2. Copy essential files to Hermes skills directory
```python
import shutil
source = r"D:\openclaw-hermes\<skill-name>"
dest = os.path.expanduser("~/.hermes/skills/<skill-name>")
os.makedirs(dest, exist_ok=True)

# Files to copy
for f in ["SKILL.md", "README.md", "LICENSE"]:
    src = os.path.join(source, f)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(dest, f))

# Directories to copy
for d in ["commands", "references", "scripts", "hooks", "adapters"]:
    src_dir = os.path.join(source, d)
    dst_dir = os.path.join(dest, d)
    if os.path.exists(src_dir):
        if os.path.exists(dst_dir):
            shutil.rmtree(dst_dir)
        shutil.copytree(src_dir, dst_dir)
```

### 3. Configure for Hermes
- Add env vars to `~/.hermes/.env` if the skill needs them
- Create `config.json` in the skill directory if it needs paths/settings
- Run any bootstrap scripts (pipe 'y' to stdin if they ask for confirmation)

### 4. Restart Gateway
The gateway needs restart to pick up new skills.

## Key Differences: Claude Code vs Hermes

| Aspect | Claude Code | Hermes Adaptation |
|--------|-------------|-------------------|
| Settings | `~/.claude/settings.json` | `~/.hermes/.env` or `config.json` |
| Commands | `~/.claude/commands/` | Skill commands dir |
| MCP config | In settings.json | `config.yaml` mcp_servers section |
| Hooks | `~/.claude/settings.json` hooks | `~/.hermes/plugins/` |
| Setup scripts | Target `~/.claude/` | Need manual path adaptation |

## Example: obsidian-second-brain (⭐1931)

**Repo**: https://github.com/eugeniughelbur/obsidian-second-brain
**What it does**: 43 commands for operating Obsidian vault as AI second brain
**Hermes installation**:
1. Clone to `D:\openclaw-hermes\obsidian-second-brain`
2. Copy to `~/.hermes/skills/obsidian-second-brain/`
3. Create vault: `D:\ObsidianVault/`
4. Run bootstrap: `python scripts/bootstrap_vault.py --path D:\ObsidianVault --name "User"` (pipe 'y')
5. Add to `.env`: `OBSIDIAN_VAULT_PATH=D:\ObsidianVault`
6. Create `config.json` with vault path

## Pitfalls

| Issue | Fix |
|-------|-----|
| setup.sh targets `~/.claude/` | Don't run it directly; copy files manually instead |
| Bootstrap asks for confirmation | Pipe 'y' via `subprocess.communicate(input='y\n')` |
| Skill has no Hermes adapter | Use Claude Code adapter as reference; adapt paths |
| Commands reference `~/.claude/` paths | Update to `~/.hermes/` equivalents |
| WSL not available | Use `execute_code` + Python for all file operations |
