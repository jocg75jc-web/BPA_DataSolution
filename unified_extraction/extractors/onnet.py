from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from .base import BaseExtractor
except ImportError:
    from extractors.base import BaseExtractor


class ONNETExtractor(BaseExtractor):
    """Builds and executes ONNET extraction commands."""

    def _resolved_paths(self) -> tuple[Path, Path]:
        script = self.execution.get("script")
        if not script:
            raise ValueError("ONNET extractor requires execution.script")

        workdir = Path(str(self.execution.get("workdir", Path(script).parent)))
        env_file = Path(str(self.execution.get("env_file", workdir / ".env")))
        output_dir = Path(
            str(self.project_definition.get("outputs", {}).get("directory", workdir / "output"))
        )
        return env_file, output_dir

    def build_command(self, params: dict[str, Any]) -> list[str]:
        python_exe = self.execution.get("python", "python")
        script = self.execution.get("script")
        if not script:
            raise ValueError("ONNET extractor requires execution.script")

        script_path = Path(str(script))
        bridge_path = script_path.parent / "export_onnet_bridge.py"
        runner_path = bridge_path if bridge_path.exists() else script_path

        env_file, output_dir = self._resolved_paths()

        if not env_file.exists():
            raise ValueError(f"ONNET env file not found: {env_file}")

        command = [str(python_exe), str(runner_path)]
        command.extend([
            "--output-dir",
            str(output_dir),
            "--env-file",
            str(env_file),
        ])

        model = params.get("model")
        if model and model != "all":
            command.extend(["--query", str(model)])

        return command

    def validate_execution_result(
        self,
        *,
        params: dict[str, Any],
        started_at: float,
        returncode: int,
        stdout: str,
        stderr: str,
    ) -> None:
        if returncode != 0:
            return

        combined_output = f"{stdout}\n{stderr}"
        has_completion_marker = "Proceso completado correctamente" in combined_output

        _, output_dir = self._resolved_paths()
        model = params.get("model")
        if model == "modelo3":
            expected_files = [output_dir / "1070_TRANSACCIONES_ONNET.csv"]
        elif model == "modelo4":
            expected_files = [output_dir / "1070_TRANSACCIONES_ONNET_ticketes.csv"]
        else:
            expected_files = [
                output_dir / "1070_TRANSACCIONES_ONNET.csv",
                output_dir / "1070_TRANSACCIONES_ONNET_ticketes.csv",
            ]

        for file_path in expected_files:
            if not file_path.exists():
                raise ValueError(f"ONNET no genero archivo esperado: {file_path}")
            if file_path.stat().st_size <= 0:
                raise ValueError(f"ONNET genero archivo vacio: {file_path}")
            if file_path.stat().st_mtime < (started_at - 2):
                raise ValueError(f"ONNET no actualizo archivo en esta corrida: {file_path}")

        if not has_completion_marker:
            return
