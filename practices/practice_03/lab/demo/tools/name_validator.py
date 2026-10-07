#!/usr/bin/env python3

"""
Simple standalone validator tool (mock MCP tool) for demonstration:
- Input (stdin JSON): {"name": "Ann", "max_len": 255, "current": 0, "capacity": 100}
- Output (stdout JSON): {"ok": true, "message": "valid"} or error details

No external deps; intended to demonstrate a useful tool and error handling.
"""

import sys, json

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        print(json.dumps({"ok": False, "error": "invalid_json"}))
        return 0

    name = str(data.get("name", ""))
    max_len = int(data.get("max_len", 255))
    capacity = int(data.get("capacity", 100))
    current = int(data.get("current", 0))

    if not name.strip():
        print(json.dumps({"ok": False, "error": "empty_name"}))
        return 0
    if len(name) > max_len:
        print(json.dumps({"ok": False, "error": "name_too_long", "limit": max_len}))
        return 0
    # capacity check simulating unique insert
    will_add_unique = bool(data.get("unique", True))
    if will_add_unique and current >= capacity:
        print(json.dumps({"ok": False, "error": "capacity_exceeded", "capacity": capacity}))
        return 0

    print(json.dumps({"ok": True, "message": "valid"}))
    return 0

if __name__ == '__main__':
    sys.exit(main())
