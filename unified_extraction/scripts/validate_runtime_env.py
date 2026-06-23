from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.runtime_env_validator import RuntimeEnvContractError, validate_runtime_environment


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate runtime environment contract")
    parser.add_argument("--config", default="config/processes.json", help="Path to processes.json")
    parser.add_argument(
        "--contract",
        default="config/runtime_env_contract.json",
        help="Path to runtime env contract JSON",
    )
    args = parser.parse_args()

    try:
        result = validate_runtime_environment(args.config, args.contract)
        print(json.dumps(result, ensure_ascii=True))
        return 0
    except RuntimeEnvContractError as exc:
        print(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
