from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


class ConfigError(Exception):
    """Raised when configuration is invalid or cannot be loaded."""


class ConfigLoader:
    """Loads and resolves unified process configuration."""

    def __init__(self, config_path: str | Path):
        self.config_path = Path(config_path).resolve()
        self._config: dict[str, Any] = {}
        self.load_and_validate()

    def load_and_validate(self) -> dict[str, Any]:
        if not self.config_path.exists():
            raise ConfigError(f"Config file not found: {self.config_path}")

        try:
            with self.config_path.open("r", encoding="utf-8") as f:
                loaded = json.load(f)
        except json.JSONDecodeError as exc:
            raise ConfigError(f"Invalid JSON in config: {exc}") from exc

        if not isinstance(loaded, dict):
            raise ConfigError("Configuration root must be a JSON object")

        projects = loaded.get("projects")
        if not isinstance(projects, list) or not projects:
            raise ConfigError("Configuration must include a non-empty 'projects' array")

        project_ids: set[str] = set()
        for project in projects:
            if not isinstance(project, dict):
                raise ConfigError("Each project entry must be an object")

            project_id = project.get("id")
            if not isinstance(project_id, str) or not project_id.strip():
                raise ConfigError("Each project must contain a non-empty string 'id'")

            project_id = project_id.strip()
            if project_id in project_ids:
                raise ConfigError(f"Duplicated project id found: {project_id}")
            project_ids.add(project_id)

            if "execution" not in project or not isinstance(project["execution"], dict):
                raise ConfigError(f"Project '{project_id}' requires object 'execution'")
            if "parameters" not in project or not isinstance(project["parameters"], dict):
                raise ConfigError(f"Project '{project_id}' requires object 'parameters'")

        self._resolution_context = self._build_resolution_context(loaded)
        self._config = self._resolve_env_vars(loaded)
        return self._config

    def reload(self) -> dict[str, Any]:
        return self.load_and_validate()

    def get_config(self) -> dict[str, Any]:
        return self._config

    def get_all_projects(self, enabled_only: bool = True) -> list[dict[str, Any]]:
        projects = self._config.get("projects", [])
        if not enabled_only:
            return projects
        return [p for p in projects if p.get("enabled", True)]

    def get_project(self, project_id: str) -> dict[str, Any]:
        project_id = project_id.strip().lower()
        for project in self._config.get("projects", []):
            if str(project.get("id", "")).lower() == project_id:
                return project
        raise ConfigError(f"Project not found: {project_id}")

    def get_parameters(self, project_id: str) -> dict[str, Any]:
        project = self.get_project(project_id)
        return project.get("parameters", {})

    def _resolve_env_vars(self, value: Any) -> Any:
        if isinstance(value, dict):
            return {k: self._resolve_env_vars(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._resolve_env_vars(v) for v in value]
        if isinstance(value, str):
            return self._resolve_env_in_string(value)
        return value

    def _resolve_env_in_string(self, text: str) -> str:
        resolved = text

        # Resolve ${VAR} and ${VAR}/suffix through environment variables first.
        for _ in range(5):
            start = resolved.find("${")
            if start < 0:
                break
            end = resolved.find("}", start)
            if end < 0:
                break
            token = resolved[start + 2 : end]
            replacement = self._resolution_context.get(token)
            if replacement is None:
                replacement = os.getenv(token)
            if replacement is None:
                replacement = ""
            resolved = resolved[:start] + replacement + resolved[end + 1 :]

        # Normalize local path separators for Windows runtime.
        if "/" in resolved and (":" in resolved or resolved.startswith(".")):
            resolved = str(Path(resolved))

        return resolved

    def _build_resolution_context(self, loaded: dict[str, Any]) -> dict[str, str]:
        context: dict[str, str] = dict(os.environ)
        project_root = self._default_project_root()
        context.setdefault("PROJECT_ROOT", str(project_root))

        configured_vars = loaded.get("environment_variables", {})
        if isinstance(configured_vars, dict):
            for _ in range(5):
                changed = False
                for key, raw_value in configured_vars.items():
                    if not isinstance(raw_value, str):
                        continue
                    resolved_value = self._resolve_string_with_context(raw_value, context)
                    if context.get(key) != resolved_value:
                        context[key] = resolved_value
                        changed = True
                if not changed:
                    break

        return context

    def _resolve_string_with_context(self, text: str, context: dict[str, str]) -> str:
        resolved = text
        for _ in range(5):
            start = resolved.find("${")
            if start < 0:
                break
            end = resolved.find("}", start)
            if end < 0:
                break
            token = resolved[start + 2 : end]
            replacement = context.get(token)
            if replacement is None:
                replacement = os.getenv(token, "")
            resolved = resolved[:start] + replacement + resolved[end + 1 :]

        if "/" in resolved and (":" in resolved or resolved.startswith(".")):
            resolved = str(Path(resolved))

        return resolved

    def _default_project_root(self) -> Path:
        parents = self.config_path.resolve().parents
        if len(parents) >= 4:
            return parents[3]
        return self.config_path.resolve().parent
