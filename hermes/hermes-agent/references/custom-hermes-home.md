# Custom HERMES_HOME Directory Configuration

## Overview
Hermes supports running with a custom configuration directory instead of the default `%USERPROFILE%\.hermes`. This is useful for:
- Project-specific configurations
- Multiple isolated environments
- Running Hermes from a project directory

## Setting Custom HERMES_HOME

### Method 1: Environment Variable
Set `HERMES_HOME` environment variable to your desired directory:
```cmd
set HERMES_HOME=D:\your-project\.hermes
```

### Method 2: Using hermes.bat Script
If your project includes a `hermes.bat` script (like in D:\openclaw-hermes\scripts\hermes.bat), it automatically sets:
```cmd
set HERMES_HOME=D:\openclaw-hermes\hermes-home\.hermes
set PYTHONPATH=D:\openclaw-hermes\hermes-home;%PYTHONPATH%
```

## Required Files in Custom Directory
Your custom `.hermes` directory should contain:
1. `config.yaml` - Main configuration
2. `.env` - Environment variables (API keys, base URLs)
3. `auth.json` - Credential pool
4. `channel_directory.json` - Messaging channel bindings

If these files don't exist, Hermes may fall back to the default directory or create minimal defaults.

## Starting Gateway with Custom HERMES_HOME

### Using hermes.bat
```cmd
D:\openclaw-hermes\scripts\hermes.bat gateway restart
```

### Manual Start
```cmd
set HERMES_HOME=D:\openclaw-hermes\hermes-home\.hermes
python -m gateway.run
```

## Verification
After starting with custom HERMES_HOME:
1. Check gateway process is running
2. Send test message to verify connections
3. Verify configuration files are being read from custom directory

## Common Issues

### Configuration Not Loading
- Ensure `config.yaml` exists in custom `.hermes` directory
- Check `HERMES_HOME` path is correct
- Verify Python path includes project root if using custom modules

### WeChat Connection Issues
WeChat accounts, context-tokens.json, and iLink credentials live ONLY in the **global** config directory (`%USERPROFILE%\.hermes`), not in custom `HERMES_HOME` directories. The project `hermes.bat` sets `HERMES_HOME` to the project directory, which has no WeChat config.

**Fix**: Restart using the GLOBAL gateway-service instead of the project hermes.bat:
```python
import subprocess
gateway_script = r"C:\Users\<user>\.hermes\gateway-service\Hermes_Gateway.cmd"
subprocess.Popen(
    ["cmd", "/c", "start", "Hermes Gateway", gateway_script],
    shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE
)
```

**Why not copy weixin config to custom directory?** It's fragile — context-tokens expire frequently, and you'd need to keep two copies in sync. Using the global gateway-service is the reliable approach.

### Process Management
When using custom HERMES_HOME, gateway PID file is stored in custom directory:
```
D:\openclaw-hermes\hermes-home\.hermes\gateway.pid
```

## Example Project Structure
```
D:\openclaw-hermes\
├── hermes-home\
│   └── .hermes\
│       ├── config.yaml
│       ├── .env
│       ├── auth.json
│       └── channel_directory.json
├── scripts\
│   └── hermes.bat
└── ... (other project files)
```

## Best Practices
1. **Keep configurations separate**: Each project should have its own `.hermes` directory
2. **Use hermes.bat**: If provided, use the project's hermes.bat script for consistency
3. **Verify connections**: Always test WeChat/messaging after switching configurations
4. **Backup configurations**: Before switching, backup important configurations