from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.config_loader import ConfigLoader


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate processes configuration")
    parser.add_argument("--config", default="config/processes.json", help="Path to processes.json")
    args = parser.parse_args()

    loader = ConfigLoader(args.config)
    config = loader.get_config()

    projects = loader.get_all_projects(enabled_only=False)
    enabled = loader.get_all_projects(enabled_only=True)

    print(f"OK config loaded: {Path(args.config).resolve()}")
    print(f"Version: {config.get('version', 'n/a')}")
    print(f"Projects: total={len(projects)} enabled={len(enabled)}")

    for project in projects:
        print(f" - {project.get('id')}: {project.get('name')} (enabled={project.get('enabled', True)})")

    # Keep a deterministic JSON dump for quick sanity checks if needed.
    print(json.dumps({"status": "ok", "projects": [p.get("id") for p in projects]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
