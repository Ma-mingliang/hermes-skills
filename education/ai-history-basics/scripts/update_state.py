#!/usr/bin/env python3
"""Update AI History progress state file.

Usage: python update_state.py <day> <topic>

Reads ~/.hermes/ai-history-state.json, increments current_day,
appends to history, writes back with correct Chinese field names.

Exit codes: 0=success, 1=error
"""
import sys
import os
import json
from datetime import datetime

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <day> <topic>", file=sys.stderr)
        sys.exit(1)

    day = int(sys.argv[1])
    topic = sys.argv[2]
    state_file = os.path.expanduser("~/.hermes/ai-history-state.json")

    if not os.path.exists(state_file):
        # Initialize fresh state
        data = {
            "current_day": 1,
            "last推送_date": None,
            "total推送": 0,
            "history": []
        }
    else:
        with open(state_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

    # Normalize field names to canonical Chinese format
    if "last_push_date" in data:
        print("INFO: Normalizing 'last_push_date' → 'last推送_date'", file=sys.stderr)
        data["last推送_date"] = data.pop("last_push_date")
    if "total_pushes" in data:
        print("INFO: Normalizing 'total_pushes' → 'total推送'", file=sys.stderr)
        data["total推送"] = data.pop("total_pushes")

    today = datetime.now().strftime('%Y-%m-%d')

    # Update state
    data["current_day"] = day + 1
    data["last推送_date"] = today
    data["total推送"] = data.get("total推送", 0) + 1

    # Append to history
    if "history" not in data:
        data["history"] = []
    data["history"].append({
        "day": day,
        "topic": topic,
        "date": today
    })

    # Write back
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"State updated: Day {day} ({topic}) → next Day {data['current_day']}")
    print(f"Total pushes: {data['total推送']}")

if __name__ == "__main__":
    main()
