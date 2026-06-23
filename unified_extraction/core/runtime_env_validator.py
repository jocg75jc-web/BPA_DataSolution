from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .config_loader import ConfigLoader


class RuntimeEnvContractError(Exception):
    """Raised when runtime environment contract validation fails."""


def _resolve_tokens(raw: str, context: dict[str, str]) -> str:
    resolved = raw
    for _ in range(10):
        start = resolved.find("${")
        if start < 0:
            break
        end = resolved.find("}", start)
        if end < 0:
            break
        token = resolved[start + 2 : end]
        replacement = context.get(token, os.getenv(token, ""))
        resolved = resolved[:start] + replacement + resolved[end + 1 :]
    return resolved


def validate_runtime_environment(
    config_path: str | Path,
    contract_path: str | Path | None = None,
) -> dict[str, Any]:
    config_path = Path(config_path)
    if contract_path is None:
        contract_path = Path(__file__).resolve().parents[1] / "config" / "runtime_env_contract.json"
    else:
        contract_path = Path(contract_path)

    if not contract_path.exists():
        raise RuntimeEnvContractError(f"Runtime env contract not found: {contract_path}")

    with contract_path.open("r", encoding="utf-8") as f:
        contract = json.load(f)

    loader = ConfigLoader(config_path)
    config = loader.get_config()
    config_env = config.get("environment_variables", {})
    if not isinstance(config_env, dict):
        config_env = {}

    context = dict(os.environ)
    context.update({k: str(v) for k, v in config_env.items() if v is not None})

    errors: list[str] = []
    warnings: list[str] = []

    for key in contract.get("required", []):
        value = os.getenv(key) or context.get(key)
        if value is None or str(value).strip() == "":
            errors.append(f"Missing required runtime variable: {key}")

    for key in contract.get("recommended", []):
        value = os.getenv(key) or context.get(key)
        if value is None or str(value).strip() == "":
            warnings.append(f"Missing recommended runtime variable: {key}")

    for raw_path in contract.get("paths_must_exist", []):
        if not isinstance(raw_path, str):
            continue
        resolved = _resolve_tokens(raw_path, context)
        if not resolved:
            errors.append(f"Path could not be resolved from contract: {raw_path}")
            continue
        path_obj = Path(resolved)
        if not path_obj.exists():
            errors.append(f"Required runtime path not found: {path_obj}")

    if errors:
        details = "\n".join([f" - {item}" for item in errors])
        raise RuntimeEnvContractError(
            "Runtime environment validation failed:\n" + details
        )

    return {
        "status": "ok",
        "required_checked": len(contract.get("required", [])),
        "recommended_missing": warnings,
        "paths_checked": len(contract.get("paths_must_exist", [])),
        "contract": str(contract_path.resolve()),
    }
