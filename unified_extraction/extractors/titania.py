from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from .base import BaseExtractor
except ImportError:
    from extractors.base import BaseExtractor


class TitaniaExtractor(BaseExtractor):
    """Builds and executes Titania extraction commands."""

    def _resolved_paths(self) -> tuple[Path, Path, Path]:
        script = self.execution.get("script")
        if not script:
            raise ValueError("Titania extractor requires execution.script")

        workdir = Path(str(self.execution.get("workdir", Path(script).parent)))
        query_dir = Path(str(self.execution.get("query_dir", workdir / "Query")))
        credentials_file = Path(
            str(self.execution.get("credentials_file", query_dir / "Cred_Con.txt"))
        )
        output_dir = Path(
            str(self.project_definition.get("outputs", {}).get("directory", workdir / "output"))
        )
        return query_dir, credentials_file, output_dir

    def build_command(self, params: dict[str, Any]) -> list[str]:
        python_exe = self.execution.get("python", "python")
        script = self.execution.get("script")
        if not script:
            raise ValueError("Titania extractor requires execution.script")

        script_path = Path(str(script))
        bridge_script = script_path.parent / "export_queries_bridge.py"
        effective_script = bridge_script if bridge_script.exists() else script_path

        query_dir, credentials_file, output_dir = self._resolved_paths()

        if not query_dir.exists():
            raise ValueError(f"Titania query directory not found: {query_dir}")
        if not credentials_file.exists():
            raise ValueError(f"Titania credentials file not found: {credentials_file}")

        command = [str(python_exe), str(effective_script)]
        command.extend([
            "--query-dir",
            str(query_dir),
            "--output-dir",
            str(output_dir),
            "--credentials-file",
            str(credentials_file),
        ])

        query = params.get("query")
        if query and query != "all":
            command.extend(["--query", str(query)])

        database = params.get("database")
        if database:
            command.extend(["--database", str(database)])

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

        query_dir, _, output_dir = self._resolved_paths()
        selected_query = params.get("query")
        if selected_query and selected_query != "all":
            expected_files = [output_dir / f"{selected_query}.csv"]
        else:
            expected_files = [
                output_dir / f"{sql_path.stem}.csv"
                for sql_path in sorted(query_dir.glob("*.sql"))
                if sql_path.stem.lower() != "all"
            ]

        for file_path in expected_files:
            if not file_path.exists():
                raise ValueError(f"Titania no genero archivo esperado: {file_path}")
            if file_path.stat().st_size <= 0:
                raise ValueError(f"Titania genero archivo vacio: {file_path}")
            if file_path.stat().st_mtime < (started_at - 2):
                raise ValueError(f"Titania no actualizo archivo en esta corrida: {file_path}")

        # Algunas ejecuciones productivas registran solo a archivo y no siempre emiten marker a stderr.
        # Si los archivos esperados fueron actualizados en esta corrida, se considera ejecución válida.
        if not has_completion_marker:
            return
