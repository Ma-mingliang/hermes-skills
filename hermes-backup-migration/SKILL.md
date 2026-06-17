---
name: hermes-backup-migration
description: Backup complete Hermes installation (skills, config, memories, sessions, state DB, plugins) and restore on another machine. Covers Git LFS for large files, sensitive data masking, and Windows-specific pitfalls.
category: hermes
triggers:
  - "备份hermes"
  - "迁移hermes"
  - "hermes backup"
  - "hermes migration"
  - "打包hermes"
  - "transfer hermes to another computer"
---

# Hermes Backup & Migration

## When to Use

User wants to backup their Hermes installation, migrate to another machine, or create a reproducible snapshot of their entire setup.

## Prerequisites

- Git installed with LFS support (`git lfs install`)
- GitHub CLI authenticated (`gh auth status`) or SSH key configured
- Sufficient disk space (~500MB for full backup)

## Directory Inventory

```
~/.hermes/
├── config.yaml          # Main config (API keys inside)
├── auth.json            # Auth tokens (SENSITIVE)
├── .env                 # Environment vars (SENSITIVE)
├── SOUL.md              # Agent personality
├── memories/            # MEMORY.md, USER.md, CREATIVE.md
├── skills/              # All installed skills (~500MB)
├── sessions/            # Session history (~300MB, 700+ files)
├── state.db             # Main state DB (~250MB)
├── kanban.db            # Kanban board (~100KB)
├── memory_store.db      # Memory store (~50KB)
├── plugins/             # Icarus, reasoning-trace-hook, etc.
├── cron/                # Scheduled jobs
├── scripts/             # Utility scripts
├── references/          # Reference docs
├── monitoring/          # Monitoring config
├── hindsight/           # Memory OS (Hindsight+Qdrant) config
├── logs/                # Agent logs (~17MB)
└── Various state files  # gateway_state.json, .icarus-state.json, etc.
```

## Step-by-Step Workflow

### 1. Prepare Repo

```bash
git clone <target-repo-url>
cd <repo-dir>
git checkout -b hermes-full-backup-YYYY-MM-DD
git lfs install
git lfs track "*.zip"
git lfs track "*.db"
git lfs track "*.node"
```

### 2. Mask Sensitive Data

**config.yaml**: Replace all `api_key:` values with `'YOUR_API_KEY'`
**auth.json**: Replace all `api_key`/`token`/`secret`/`password` values
**.env**: Save as `.env.template`, replace values matching `=[\w\-]{20,}` with `=YOUR_KEY_HERE`

### 3. Copy Core Config

```
hermes-config/
  ├── config.yaml (masked)
  ├── auth.json (masked)
  ├── .env.template (masked)
  ├── SOUL.md
  ├── channel_directory.json
  ├── memories/ (all .md files)
  ├── plugins/ (copy entire tree)
  ├── cron/
  ├── scripts/
  ├── references/
  ├── monitoring/
  ├── hindsight/
  └── state files (gateway_state.json, .icarus-state.json, etc.)
```

### 4. Compress Large Directories

```python
import zipfile

# Skills (~500MB → ~215MB compressed)
with zipfile.ZipFile('hermes-skills.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(skills_dir):
        for f in files:
            zf.write(os.path.join(root, f), os.path.relpath(...))

# Sessions (~300MB → ~73MB)
# State DB (~250MB → ~104MB)
# Logs (~17MB → ~1.6MB)
```

### 5. Write MIGRATION.md

Must include:
- Complete directory structure explanation
- 10+ step restoration guide with exact commands
- API key configuration instructions
- Memory OS (Docker) setup
- Ollama embedding setup
- Troubleshooting FAQ

### 6. Push to GitHub

```bash
git add .
git commit -m "feat: 完整Hermes Agent配置备份 (YYYY-MM-DD)"
git lfs push origin <branch> --all    # MUST push LFS first
git push -u origin <branch>
```

## Pitfalls

### PITFALL: Git LFS push must come BEFORE git push

GitHub rejects pushes with LFS pointers that haven't been uploaded.
Always run `git lfs push origin <branch> --all` before `git push`.

### PITFALL: SSL/TLS timeouts on Windows

Windows Git uses Schannel SSL backend which can fail with large uploads.
Fix: `git config --global http.sslBackend schannel`
If still failing: `git config --local http.sslVerify false` (temporary)
Set large buffer: `git config --local http.postBuffer 524288000`

### PITFALL: Push timeout for 400MB+ uploads

Subprocess timeout of 300s is NOT enough for 400MB+ LFS uploads.
Solutions:
1. Create a .bat script and ask user to run it manually
2. Use `notify_on_complete=True` with background terminal
3. Split into smaller pushes (push skills separately)

### PITFALL: Windows permission errors deleting large copied dirs

`shutil.rmtree()` fails on `.git` directories inside copied skill repos
(permission denied on pack files). Don't copy `.git` dirs from skills,
or use `git rm -r --cached` after the fact.

### PITFALL: WSL relay failures on Windows

The terminal tool may fail with `CreateProcessCommon:798: execvpe(/bin/bash)`.
Use `execute_code` with `subprocess.run(..., shell=True)` as fallback.
Never assume terminal tool works on Windows.

### PITFALL: Skills directory has internal .git repos

Some skills (like `gorden-ppt-skill`) are cloned repos with their own `.git/`.
Size can bloat significantly. Consider adding `*/.git/` to `.gitignore`.

### PITFALL: auth.json contains Ollama SSH keys

The `~/.hermes/ollama/` directory may contain SSH private keys.
Always mask these or exclude from backup.

## File Size Reference

| Component | Raw | Compressed |
|-----------|-----|-----------|
| Skills (77) | 492 MB | 215 MB |
| Sessions (722) | 316 MB | 73 MB |
| state.db | 248 MB | 104 MB |
| openclaw-hermes/ | ~1.5 GB | 38 MB (excluding node_modules) |
| logs | 17 MB | 1.6 MB |
| Config files | ~100 KB | ~100 KB |
| **Total** | **~2.6 GB** | **~431 MB** |

## Restoration Checklist

1. Install Hermes (`npm install -g hermes-agent` or `pip install hermes-agent`)
2. Clone repo, checkout backup branch
3. Create `~/.hermes/` directory structure
4. Copy core config files
5. Unzip skills into `~/.hermes/skills/`
6. Unzip state.db (optional, for session continuity)
7. Unzip sessions (optional, for history)
8. Edit `.env` with real API keys
9. Edit `auth.json` with real API keys
10. Setup Memory OS Docker containers (optional)
11. Install Ollama + nomic-embed-text (optional)
12. Verify with `hermes config show` and `hermes skills list`
