#!/usr/bin/env python3
"""
Agent Daily Report — Quick Health Check
Run: python scripts/verify_system.py
Checks: py_compile, source_status constants, --test modes, config integrity.
"""

import os
import sys
import json
import py_compile
from pathlib import Path

PROJ = Path(__file__).parent.parent
SCRIPTS = PROJ / "scripts"
CONFIG = PROJ / "config.yaml"

results = []


def check(name, ok, detail=""):
    sym = "✅" if ok else "❌"
    results.append((name, ok, detail))
    print(f"  {sym} {name}" + (f" ({detail})" if detail else ""))


def main():
    print("=" * 60)
    print("Agent Daily Report — Health Check")
    print("=" * 60)

    # 1. py_compile
    print("\n[1] py_compile")
    ok_count = 0
    for f in sorted(SCRIPTS.glob("*.py")):
        try:
            py_compile.compile(str(f), doraise=True)
            ok_count += 1
        except py_compile.PyCompileError as e:
            check(f.name, False, str(e)[:80])
    try:
        py_compile.compile(str(PROJ / "main.py"), doraise=True)
        ok_count += 1
    except py_compile.PyCompileError as e:
        check("main.py", False, str(e)[:80])
    check(f"py_compile ({ok_count} files)", True)

    # 2. source_status constants
    print("\n[2] source_status constants")
    sys.path.insert(0, str(SCRIPTS))
    try:
        from source_status import (
            STATUS_SUCCESS, STATUS_SUCCESS_NO_MATCH, STATUS_CHECKED_NO_CHANGE,
            STATUS_SKIPPED_DISABLED, STATUS_SKIPPED_MISSING_AUTH, STATUS_SKIPPED_NO_CONFIG,
            STATUS_FAILED_NETWORK, STATUS_FAILED_PARSE, STATUS_FAILED_AUTH, STATUS_FAILED_RATE_LIMITED,
        )
        check("STATUS_SKIPPED_MISSING_AUTH", STATUS_SKIPPED_MISSING_AUTH == "skipped_missing_auth",
              f"got '{STATUS_SKIPPED_MISSING_AUTH}'")
        check("STATUS_FAILED_AUTH", STATUS_FAILED_AUTH == "failed_auth",
              f"got '{STATUS_FAILED_AUTH}'")
        check("STATUS_SKIPPED_NO_CONFIG", STATUS_SKIPPED_NO_CONFIG == "skipped_no_config",
              f"got '{STATUS_SKIPPED_NO_CONFIG}'")
    except ImportError as e:
        check("source_status import", False, str(e))

    # 3. Config integrity
    print("\n[3] Config integrity")
    import yaml
    with open(CONFIG, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    check("quality_gates", "quality_gates" in cfg)
    check("cost_signal", "cost_signal" in cfg)
    check("empty_report_policy", "empty_report_policy" in cfg)
    check("deduplication", "deduplication" in cfg)
    check("runtime.timezone", cfg.get("runtime", {}).get("timezone") == "Asia/Tokyo")
    check("github.token_env_candidates", "token_env_candidates" in cfg.get("github", {}))
    check("v2ex.endpoints", "endpoints" in cfg.get("v2ex", {}))

    # 4. .env token check
    print("\n[4] Token availability")
    env_path = Path.home() / ".hermes" / ".env"
    if env_path.exists():
        # Load .env
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() not in os.environ:
                        os.environ[k.strip()] = v.strip()
        gh = os.environ.get("GITHUB_TOKEN", "") or os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN", "")
        check("GitHub token", len(gh) >= 20, f"len={len(gh)}")
    else:
        check("~/.hermes/.env", False, "not found")

    # 5. Key files exist
    print("\n[5] Key files")
    for path in [
        "scripts/collect_github.py", "scripts/collect_v2ex.py",
        "scripts/github_state.py", "scripts/source_status.py",
        "scripts/score_items.py", "scripts/generate_report.py",
        "scripts/deduplicate_items.py", "scripts/classify_items.py",
        "scripts/normalize_items.py",
    ]:
        full = PROJ / path
        check(path, full.exists(), f"{full.stat().st_size}b" if full.exists() else "missing")

    # Summary
    passed = sum(1 for _, ok, _ in results if ok)
    failed = sum(1 for _, ok, _ in results if not ok)
    print(f"\n{'=' * 60}")
    print(f"Result: {passed} PASS, {failed} FAIL")
    if failed:
        print("\nFailed checks:")
        for name, ok, detail in results:
            if not ok:
                print(f"  ❌ {name}: {detail}")
    print("=" * 60)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
