# WeChat Gateway Configuration & Working Directory

## Problem
Gateway may connect to wrong working directory (e.g., E:\Code\bike instead of D:\openclaw-hermes).

## Root Cause
`config.yaml` has `terminal.cwd: .` which uses the launch directory, not the intended project directory.

## Fix Steps

1. **Edit config file**:
   ```
   C:\Users\lenovo_mml\.hermes\config.yaml
   ```

2. **Set terminal.cwd explicitly**:
   ```yaml
   terminal:
     cwd: D:\openclaw-hermes
   ```

3. **Restart gateway**:
   ```bash
   hermes gateway restart
   ```
   Or use global service script:
   ```
   C:\Users\lenovo_mml\.hermes\gateway-service\Hermes_Gateway.cmd
   ```

## Verification
After restart, read a known file from the target directory to confirm connection:
```
read_file("D:/openclaw-hermes/CLAUDE.md")
```

## Key Paths
| Item | Path |
|------|------|
| Config file | `C:\Users\lenovo_mml\.hermes\config.yaml` |
| Gateway service | `C:\Users\lenovo_mml\.hermes\gateway-service\Hermes_Gateway.cmd` |
| Local scripts | `D:\openclaw-hermes\scripts\hermes.bat` |
| .env credentials | `C:\Users\lenovo_mml\.hermes\.env` |
| WeChat context tokens | `C:\Users\lenovo_mml\.hermes\weixin\accounts\84620941bcd5@im.bot.context-tokens.json` |
| Working directory (correct) | `D:\openclaw-hermes` |

## WeChat Connection Fix
If WeChat stops responding:
1. Clear stale context-tokens: write `{}` to the context-tokens.json file
2. Restart gateway
3. Send test message via send_message

## MCP GitHub Server
If `github-mcp-server` fails with JSON parse errors:
- Root cause: `GITHUB_PERSONAL_ACCESS_TOKEN` not loaded in gateway process
- Fix: Set env var from `.env` file before gateway start
- Token format: 40-char `ghp_` prefix
