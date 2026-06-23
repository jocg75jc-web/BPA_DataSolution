from __future__ import annotations

import argparse
import logging
import os
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Callable, Optional

PACKAGE_ROOT = Path(__file__).resolve().parents[1]

if __package__ in {None, ""}:
    sys.path.insert(0, str(PACKAGE_ROOT))

try:
    from .config_loader import ConfigLoader
    from .parameter_validator import ParameterValidator
    from .runtime_env_validator import validate_runtime_environment
    from ..extractors.registry import ExtractorRegistry
except ImportError:
    from core.config_loader import ConfigLoader
    from core.parameter_validator import ParameterValidator
    from core.runtime_env_validator import validate_runtime_environment
    from extractors.registry import ExtractorRegistry

logger = logging.getLogger(__name__)


def _default_config_path() -> str:
    return str(PACKAGE_ROOT / "config" / "processes.json")


class ExecutionEngine:
    """Coordinates configuration loading, parameter validation and extractor execution."""

    def __init__(self, config_path: str | Path):
        self.config_path = Path(config_path)
        self.config_loader = ConfigLoader(self.config_path)

        skip_validation = str(os.getenv("UNIFIED_SKIP_RUNTIME_ENV_VALIDATION", "")).lower() in {
            "1",
            "true",
            "yes",
        }
        if not skip_validation:
            validation = validate_runtime_environment(self.config_path)
            missing_recommended = validation.get("recommended_missing", [])
            for warning in missing_recommended:
                logger.warning(warning)

    def list_projects(self) -> list[dict[str, Any]]:
        return self.config_loader.get_all_projects(enabled_only=True)

    def execute(
        self,
        project_id: str,
        parameters: dict[str, Any] | None = None,
        log_callback: Optional[Callable[[str, str], None]] = None,
    ) -> dict[str, Any]:
        execution_id = str(uuid.uuid4())
        start = time.time()

        project = self.config_loader.get_project(project_id)
        param_definition = project.get("parameters", {})

        validator = ParameterValidator(param_definition)
        cleaned_params = validator.validate_or_raise(parameters)

        extractor_id = project.get("execution", {}).get("extractor") or project.get("id")
        extractor = ExtractorRegistry.create(str(extractor_id), project)

        result = extractor.execute(cleaned_params, log_callback=log_callback)

        duration_seconds = round(time.time() - start, 3)
        success = result.get("returncode", 1) == 0

        payload = {
            "execution_id": execution_id,
            "project_id": project_id,
            "status": "completed" if success else "failed",
            "success": success,
            "duration_seconds": duration_seconds,
            "parameters": cleaned_params,
            "result": result,
        }

        if success:
            logger.info("Execution %s completed for project %s", execution_id, project_id)
        else:
            logger.error("Execution %s failed for project %s", execution_id, project_id)

        return payload


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified extraction execution engine")
    parser.add_argument("--config", default=_default_config_path(), help="Path to processes configuration file")
    parser.add_argument("--project", help="Project id (e.g. titania, onnet)")
    parser.add_argument("--list", action="store_true", help="List enabled projects and exit")
    parser.add_argument("--param", action="append", default=[], help="Key=Value parameter pair. Can be repeated")
    return parser


def _parse_params(raw_params: list[str]) -> dict[str, Any]:
    params: dict[str, Any] = {}
    for item in raw_params:
        if "=" not in item:
            raise ValueError(f"Invalid param format '{item}'. Expected key=value")
        key, value = item.split("=", 1)
        params[key.strip()] = value.strip()
    return params


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
    parser = _build_arg_parser()
    args = parser.parse_args()

    try:
        engine = ExecutionEngine(args.config)
        if args.list:
            for project in engine.list_projects():
                print(f"{project.get('id')}: {project.get('name')}")
            return 0

        if not args.project:
            parser.error("--project is required unless --list is used")

        params = _parse_params(args.param)
        outcome = engine.execute(args.project, params)
        print(outcome)
        return 0 if outcome["success"] else 1
    except Exception as exc:  # pragma: no cover - CLI wrapper
        logger.exception("Execution failed: %s", exc)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
