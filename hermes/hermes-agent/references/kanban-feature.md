# Hermes Kanban Multi-Agent Board

## Overview
SQLite-backed task board for multi-agent collaboration (v0.12.0+). Tasks are claimed atomically, can depend on other tasks, and execute in isolated workspaces.

Source: https://x.com/NousResearch/status/2050997692977844324

## Setup
```bash
hermes kanban init              # Create kanban.db (idempotent)
hermes kanban boards            # Verify board exists
hermes gateway start            # Required for auto-dispatch
```

## Task Lifecycle
```
created → ready → claimed → running → completed
                    ↓          ↓
                  blocked    failed (≤failure_limit)
                    ↓
                  unblocked → ready
```

## Full Command Reference

### Board Management
```bash
hermes kanban boards                          # List all boards
hermes kanban init                            # Initialize DB
hermes kanban gc                              # Garbage collect old data
```

### Task CRUD
```bash
hermes kanban create "标题" --board default   # Create
hermes kanban list                            # List all
hermes kanban list --assignee default         # Filter by assignee
hermes kanban show <id>                       # Details + comments + events
hermes kanban edit <id>                       # Edit fields
hermes kanban archive <id>                    # Archive
```

### Task Execution
```bash
hermes kanban claim                           # Atomically claim a ready task
hermes kanban reclaim                         # Release active claim
hermes kanban assign <id> --to <profile>      # Manual assign
hermes kanban reassign <id> --to <profile>    # Reassign
hermes kanban complete <id>                   # Mark done
hermes kanban comment <id> -m "note"          # Add comment
```

### Dependencies
```bash
hermes kanban link <parent> <child>           # Add dependency
hermes kanban unlink <parent> <child>         # Remove dependency
hermes kanban block <id> --reason "..."       # Block task
hermes kanban unblock <id>                    # Unblock task
```

### Monitoring
```bash
hermes kanban watch                           # Live event stream
hermes kanban watch --interval 2              # Custom poll interval
hermes kanban stats                           # Board statistics
hermes kanban tail                            # Recent events
hermes kanban runs                            # Run history
hermes kanban heartbeat                       # Worker health
hermes kanban assignees                       # List workers
hermes kanban diagnostics                     # Active diagnostics
```

### Gateway Dispatch
```bash
hermes kanban dispatch                        # Manual dispatch tick
hermes kanban daemon                          # Run dispatcher foreground
hermes kanban notify-subscribe                # Subscribe to notifications
hermes kanban notify-list                     # List subscriptions
hermes kanban notify-unsubscribe              # Unsubscribe
```

## Dashboard
```bash
hermes dashboard --port 9119                  # Web UI with Kanban view
hermes dashboard --tui                        # Include terminal chat tab
hermes dashboard --status                     # Check if running
hermes dashboard --stop                       # Stop dashboard
```

## Quick-Start Script
Location: `~/.hermes/scripts/kanban-quickstart.bat`
```bat
@echo off
title Hermes Kanban Quick Start
echo ========================================
echo   Hermes Kanban Multi-Agent Dashboard
echo ========================================
hermes dashboard --port 9119
pause
```

## Pitfalls
- Gateway MUST be running for auto-dispatch (tasks stay 'ready' forever without it)
- `claim` is atomic — only one agent gets each task
- failure_limit (default 2) stops retrying after N failures
- Each profile gets isolated workspace path on claim
- WSL broken on Windows: use `execute_code` + Python subprocess for all hermes CLI calls
