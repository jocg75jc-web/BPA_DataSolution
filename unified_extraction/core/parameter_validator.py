from __future__ import annotations

from datetime import datetime
from typing import Any


class ParameterValidationError(Exception):
    """Raised when user parameters do not match project parameter definitions."""


class ParameterValidator:
    def __init__(self, parameters_definition: dict[str, Any]):
        self.parameters_definition = parameters_definition

    def validate(self, user_params: dict[str, Any] | None) -> tuple[bool, list[str], dict[str, Any]]:
        params = user_params or {}
        errors: list[str] = []
        cleaned: dict[str, Any] = {}

        for param_name, param_def in self.parameters_definition.items():
            required = bool(param_def.get("required", False))
            param_type = param_def.get("type", "text")
            default_value = param_def.get("default")

            if param_name not in params or params[param_name] in (None, ""):
                if required and default_value in (None, ""):
                    errors.append(f"Missing required parameter: {param_name}")
                    continue
                cleaned[param_name] = default_value
                continue

            raw_value = params[param_name]
            ok, converted, error = self._validate_type(param_name, param_type, raw_value, param_def)
            if not ok:
                errors.append(error)
                continue
            cleaned[param_name] = converted

        # Reject unknown parameters to avoid accidental command misuse.
        known = set(self.parameters_definition.keys())
        unknown = sorted([k for k in params.keys() if k not in known])
        for key in unknown:
            errors.append(f"Unknown parameter for project: {key}")

        return len(errors) == 0, errors, cleaned

    def validate_or_raise(self, user_params: dict[str, Any] | None) -> dict[str, Any]:
        ok, errors, cleaned = self.validate(user_params)
        if not ok:
            raise ParameterValidationError("; ".join(errors))
        return cleaned

    def _validate_type(
        self,
        name: str,
        param_type: str,
        value: Any,
        definition: dict[str, Any],
    ) -> tuple[bool, Any, str]:
        if param_type == "text":
            return True, str(value), ""

        if param_type == "number":
            try:
                num = float(value)
            except (ValueError, TypeError):
                return False, value, f"Parameter '{name}' must be a number"

            validation = definition.get("validation", {})
            if "min" in validation and num < validation["min"]:
                return False, value, f"Parameter '{name}' must be >= {validation['min']}"
            if "max" in validation and num > validation["max"]:
                return False, value, f"Parameter '{name}' must be <= {validation['max']}"
            return True, num, ""

        if param_type == "boolean":
            if isinstance(value, bool):
                return True, value, ""
            value_str = str(value).strip().lower()
            if value_str in {"1", "true", "yes", "y"}:
                return True, True, ""
            if value_str in {"0", "false", "no", "n"}:
                return True, False, ""
            return False, value, f"Parameter '{name}' must be boolean"

        if param_type == "date":
            value_str = str(value).strip()
            try:
                datetime.fromisoformat(value_str)
            except ValueError:
                return False, value, f"Parameter '{name}' must be ISO-8601 date"
            return True, value_str, ""

        if param_type in {"select", "multiselect"}:
            options = definition.get("options", {})
            if isinstance(options, dict):
                valid_values = set(options.keys())
            elif isinstance(options, list):
                valid_values = set(str(x) for x in options)
            else:
                valid_values = set()

            if param_type == "multiselect":
                values = value if isinstance(value, list) else [value]
                normalized = [str(v) for v in values]
                bad = [v for v in normalized if v not in valid_values]
                if bad:
                    return False, value, f"Parameter '{name}' has invalid option(s): {', '.join(bad)}"
                return True, normalized, ""

            normalized_value = str(value)
            if valid_values and normalized_value not in valid_values:
                return False, value, f"Parameter '{name}' invalid option: {normalized_value}"
            return True, normalized_value, ""

        return True, value, ""
