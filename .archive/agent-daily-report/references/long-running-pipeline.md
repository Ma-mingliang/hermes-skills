# Long-Running Pipeline Execution Pattern

## Problem

`execute_code` has a 300s hard timeout that kills the entire process group including child subprocesses. The agent-daily-report full pipeline (11 sources + Agent pipeline) typically takes 5-15 minutes, well beyond this limit.

`terminal(background=True)` fails on Windows when WSL is unavailable.

## Solution: DETACHED_PROCESS

```python
import subprocess, sys, os, time, psutil
from datetime import datetime

python_path = sys.executable
log_file = 'D:/openclaw-hermes/agent-daily-report-skill/logs/pipeline_run.log'
cwd = 'D:/openclaw-hermes/agent-daily-report-skill'

# 1. Launch detached process (survives parent timeout)
os.makedirs(os.path.dirname(log_file), exist_ok=True)
with open(log_file, 'w', encoding='utf-8') as f:
    process = subprocess.Popen(
        [python_path, 'main.py', '--debug'],
        cwd=cwd,
        stdout=f,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0,
        close_fds=True
    )

print(f"PID: {process.pid}")

# 2. Poll for completion (in a new execute_code call)
while True:
    try:
        p = psutil.Process(process.pid)
        status = p.status()
        # Check log progress
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        last = lines[-1].strip()[:80] if lines else "empty"
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {status} | {last}")
        time.sleep(15)
    except psutil.NoSuchProcess:
        print("Pipeline completed")
        break

# 3. Check report
report = 'D:/openclaw-hermes/agent-daily-report-skill/data/reports/Agent_Daily_Report_2026-06-03.md'
dt = datetime.fromtimestamp(os.path.getmtime(report))
print(f"Report updated: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
```

## Process Control

```python
p = psutil.Process(pid)
p.suspend()   # pause
p.resume()    # resume
p.terminate() # kill
```

## Key Rules

1. **Never** use `execute_code` + `subprocess.run` for full pipeline — 300s timeout kills it
2. **Never** use `terminal(background=True)` on Windows — WSL errors
3. **Always** use `Popen` + `DETACHED_PROCESS` + `CREATE_NEW_PROCESS_GROUP`
4. **Always** redirect stdout to log file (not pipe — pipe blocks on buffer full)
5. Poll with `psutil` in a **separate** `execute_code` call (don't block in the same call)
6. Max wait: 30 minutes. If still running after 30min, something is wrong.
