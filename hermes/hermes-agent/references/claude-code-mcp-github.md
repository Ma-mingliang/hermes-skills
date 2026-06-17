# Claude Code GitHub MCP Configuration

## Overview

Claude Code (the CLI tool) has its own MCP server configuration in `~/.claude.json`, separate from Hermes's `config.yaml`. To give Claude Code GitHub access, configure the GitHub MCP server in `.claude.json`'s `mcpServers` section.

## Recommended Approach: GitHub Official Remote HTTP Server

Source: `github/github-mcp-server` (GitHub's official MCP server)

**Why Remote HTTP over npm/Docker/binary:**
- Zero local dependencies (no Docker, no npx, no binary download)
- Always up-to-date (hosted by GitHub)
- `@modelcontextprotocol/server-github` npm package is **deprecated** (April 2025)
- The official replacement is the Remote HTTP server at `https://api.githubcopilot.com/mcp/`

## Configuration

### Step 1: Get GitHub PAT

Either:
- Reuse the existing Hermes token from `~/.hermes/.env` (`GITHUB_PERSONAL_ACCESS_TOKEN`)
- Create a new Fine-grained PAT at https://github.com/settings/personal-access-tokens/new

Minimum scopes: `repo`, `read:org`, `workflow`

### Step 2: Add to `~/.claude.json`

```python
import os, json

# Read token from Hermes .env
env_path = os.path.expanduser("~/.hermes/.env")
github_token = None
with open(env_path, 'r') as f:
    for line in f:
        if line.startswith('GITHUB_PERSONAL_ACCESS_TOKEN='):
            github_token = line.split('=', 1)[1].strip()
            break

# Update .claude.json
claude_json = os.path.expanduser("~/.claude.json")
with open(claude_json, 'r') as f:
    config = json.load(f)

config.setdefault('mcpServers', {})['github'] = {
    "type": "http",
    "url": "https://api.githubcopilot.com/mcp/",
    "headers": {
        "Authorization": f"Bearer {github_token}"
    }
}

with open(claude_json, 'w') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
```

### Step 3: Restart Claude Code

Verify with `/mcp` command inside Claude Code.

## Alternative Approaches

### Docker (local server)
```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<token>"
      }
    }
  }
}
```

### Binary (no Docker)
Download from https://github.com/github/github-mcp-server/releases
```json
{
  "mcpServers": {
    "github": {
      "command": "github-mcp-server",
      "args": ["stdio"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<token>"
      }
    }
  }
}
```

### npx (deprecated, but works)
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<token>"
      }
    }
  }
}
```

## Available Toolsets

The GitHub MCP server provides: repos, issues, pull_requests, actions, code_security, discussions, gists, notifications, orgs, projects, labels, stargazers, users, and more.

Default toolsets (auto-enabled): context, repos, issues, pull_requests, users.

To enable all: set `GITHUB_TOOLSETS=all` in env.

## Pitfalls

1. **npx not in PATH on Windows**: Node.js may be installed but `npx` not in PATH for subprocess. Full path: `C:\Program Files\nodejs\npx.cmd`. Use Remote HTTP to avoid this entirely.

2. **Token in .env uses `${VAR}` syntax**: Hermes config.yaml uses `${GITHUB_PERSONAL_ACCESS_TOKEN}` which resolves at gateway runtime. Claude Code's `.claude.json` needs the actual token value, not a variable reference.

3. **`.claude.json` vs `settings.json`**: MCP servers go in `~/.claude.json` (under `mcpServers`), NOT in `~/.claude/settings.json` (which has `env`, `hooks`, `customProviders`).

4. **Scope**: Use `--scope user` with `claude mcp add` to make the server available across all projects. Default is `local` (current project only).

5. **PAT permissions**: Fine-grained PATs need explicit repository access. Classic PATs with `repo` scope work for all your repos.

## References

- Official repo: https://github.com/github/github-mcp-server
- Claude Code install guide: https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md
- Remote server docs: https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md
