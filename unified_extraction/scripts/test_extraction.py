from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.execution_engine import ExecutionEngine


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a manual extraction test")
    parser.add_argument("--config", default="config/processes.json", help="Path to config")
    parser.add_argument("--project", help="Project id")
    parser.add_argument("--list", action="store_true", help="List enabled projects and exit")
    parser.add_argument("--param", action="append", default=[], help="key=value parameter")
    args = parser.parse_args()

    engine = ExecutionEngine(Path(args.config))

    if args.list:
        print("Enabled projects")
        for item in engine.list_projects():
            print(f" - {item.get('id')}: {item.get('name')}")
        return 0

    if not args.project:
        parser.error("--project is required unless --list is used")

    params = {}
    for entry in args.param:
        if "=" not in entry:
            raise ValueError(f"Invalid --param '{entry}', expected key=value")
        key, value = entry.split("=", 1)
        params[key.strip()] = value.strip()

    result = engine.execute(args.project, params)

    print("Execution finished")
    print(f"  id: {result['execution_id']}")
    print(f"  project: {result['project_id']}")
    print(f"  status: {result['status']}")
    print(f"  duration_seconds: {result['duration_seconds']}")
    return 0 if result["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
