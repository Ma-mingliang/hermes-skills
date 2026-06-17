## Pattern: Long Pipeline Runner (run_pipeline.py)

When a pipeline exceeds execute_code's 300s timeout, use a detached subprocess wrapper:

```python
# run_pipeline.py
import subprocess, sys, os, time
from pathlib import Path

SKILL_DIR = Path(__file__).parent
PID_FILE = SKILL_DIR / "logs" / "pipeline.pid"
LOG_FILE = SKILL_DIR / "logs" / "pipeline_latest.log"
PYTHON = sys.executable

def start_background():
    log_f = open(LOG_FILE, "w", encoding="utf-8")
    proc = subprocess.Popen(
        [PYTHON, "main.py", "--debug"],
        cwd=str(SKILL_DIR),
        stdout=log_f,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0,
        close_fds=True
    )
    PID_FILE.write_text(str(proc.pid))

def show_status():
    # Use psutil to check PID, report file mtime, log tail
    ...

def kill_process():
    # Terminate PID, clean up PID file
    ...
```

**Key rules:**
- `DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP` on Windows — survives parent exit
- `close_fds=True` — no inherited file handles
- PID file for status tracking
- Log file for progress monitoring
- psutil for process status checking
- Agent should use `--background` then poll `--status` every 30s until done
- Max wait: 30 minutes

**Usage from agent:**
```python
import subprocess, sys, time, psutil
# Start
subprocess.run([sys.executable, "run_pipeline.py", "--background"], cwd=SKILL_DIR)
# Poll
while True:
    result = subprocess.run([sys.executable, "run_pipeline.py", "--status"], cwd=SKILL_DIR, capture_output=True, text=True)
    if "已退出" in result.stdout:
        break
    time.sleep(30)
```

## Pattern: Growth Gate Threshold Tuning (P65-P66)

`evaluate_github_growth_gate()` in collect_github.py controls which growth signals enter the report.

**Current thresholds (P65 fix):**
| Stars Range | Reportable Condition | Level |
|---|---|---|
| < 100 | Never eligible | — |
| 100-999 | delta_24h >= 200 | S≥500 / A≥300 / B≥200 |
| 1k-5k | delta_24h >= 100 | S≥500 / A≥300 / B≥100 |
| ≥ 5k | daily_rate >= 1% | B / A≥10% |

**Known issue (P66):** `_find_growth_anomalies()` skips repos already in candidates (`if rn in already: continue`). A repo discovered via Discovery Pool (discovery_type=discovery_candidate) won't be checked for growth anomalies, even if it has +1000/24h growth. Same repo can satisfy both signals — they shouldn't be mutually exclusive.

**Diagnostic flow when "暂无" but data exists:**
```python
import json
state = json.load(open("state/github_repo_state.json"))
for rn, rs in state["repos"].items():
    snaps = rs.get("snapshots", {})
    if len(snaps) >= 2:
        dates = sorted(snaps.keys())
        delta = snaps[dates[-1]]["stars"] - snaps[dates[-2]]["stars"]
        if delta >= 100:
            print(f"{rn}: +{delta} tracking={rs.get('tracking_status')}")
            # Check: is it in candidates? is it archived? is gate reportable?
```
