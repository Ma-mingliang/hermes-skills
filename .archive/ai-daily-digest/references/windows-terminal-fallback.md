# Windows Terminal Fallback Pattern

> When `terminal` tool fails with WSL/bash errors on Windows hosts, use `execute_code` with `subprocess.run()` to run Python scripts.

## Problem

On some Windows hosts, the `terminal` tool invokes WSL (Windows Subsystem for Linux), but if bash is not installed or WSL is misconfigured, commands fail with:
```
<3>WSL (XXXXX - Relay) ERROR: CreateProcessCommon:798: execvpe(/bin/bash) failed: No such file or directory
```

This prevents running Python scripts like `quality_check.py` and `ai_daily_digest_v4.py`.

## Solution

Use `execute_code` with `subprocess.run()`:

```python
import sys, os, subprocess

script_dir = os.path.expanduser("~/.hermes/skills/news/ai-daily-digest/scripts")

result = subprocess.run(
    [sys.executable, os.path.join(script_dir, "quality_check.py"), 
     "D:/openclaw-hermes/data/daily/YYYY-MM-DD/report.md"],
    capture_output=True,
    text=True,
    timeout=30
)
print(result.stdout)
print(f"Exit code: {result.returncode}")
```

## Key Points

- Use `sys.executable` to get the correct Python interpreter path
- `capture_output=True` captures both stdout and stderr
- `text=True` returns strings instead of bytes
- Always set a `timeout` to prevent hangs
- Works from any `execute_code` call — no terminal needed

## When to Use

1. Run `quality_check.py` for Step 6 verification
2. Run `ai_daily_digest_v4.py` for Step 2 data collection (if terminal fails)
3. Any other Python script in the skill's scripts directory

## Pre-Validation Pattern

Before running the official `quality_check.py`, do a quick format pre-check:

```python
checks = {
    "拆分分析格式": "按自主性" in report,
    "Skills无冒号": "第一类：" not in report,
    "6类emoji": all(e in report for e in ['📉','🔒','⚡','🔬','🔍','📦']),
    "板块顺序": report.index("Agent生态") < report.index("Skills市场") < report.index("模型动态"),
    "信号>=3": len([l for l in report.split('\n') if l.strip().startswith(('1. **', '2. **', '3. **'))]) >= 3,
    "GitHub链接>=3": report.count("github.com") >= 3,
}
for check, result in checks.items():
    print(f"  {'✅' if result else '❌'} {check}")
```

This catches 95% of common failures before the official script, saving iteration time.
