from __future__ import annotations

import os
import subprocess
import threading
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Callable, Optional


class ExtractorExecutionError(Exception):
    """Raised when extractor execution fails."""


class BaseExtractor(ABC):
    def __init__(self, project_definition: dict[str, Any]):
        self.project_definition = project_definition
        self.execution = project_definition.get("execution", {})

    @abstractmethod
    def build_command(self, params: dict[str, Any]) -> list[str]:
        """Builds subprocess command."""

    def validate_execution_result(
        self,
        *,
        params: dict[str, Any],
        started_at: float,
        returncode: int,
        stdout: str,
        stderr: str,
    ) -> None:
        """Optional post-execution validation hook for extractor-specific checks."""

    def get_timeout_seconds(self) -> int:
        return int(self.execution.get("timeout_seconds", 1800))

    def _consume_stream(
        self,
        stream,
        sink: list[str],
        source: str,
        log_callback: Optional[Callable[[str, str], None]] = None,
    ) -> None:
        for raw_line in iter(stream.readline, ""):
            line = raw_line.rstrip("\r\n")
            sink.append(raw_line)
            if not line:
                continue
            if log_callback:
                level = "info" if source == "stdout" else "warning"
                log_callback(level, line)
        stream.close()

    def execute(
        self,
        params: dict[str, Any],
        log_callback: Optional[Callable[[str, str], None]] = None,
    ) -> dict[str, Any]:
        command = self.build_command(params)
        workdir = Path(self.execution.get("workdir", "."))
        timeout_seconds = self.get_timeout_seconds()
        started_at = time.time()

        popen_kwargs: dict[str, Any] = {
            "cwd": str(workdir),
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "text": True,
            "bufsize": 1,
        }

        # Modo estable por defecto: no desacoplar proceso hijo, para poder esperar su
        # finalización real y validar correctamente resultados/archivos.
        if os.name == "nt" and bool(self.execution.get("new_process_group", False)):
            popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
            popen_kwargs["stdin"] = subprocess.DEVNULL

        process = subprocess.Popen(
            command,
            **popen_kwargs,
        )

        stdout_chunks: list[str] = []
        stderr_chunks: list[str] = []

        stdout_thread = threading.Thread(
            target=self._consume_stream,
            args=(process.stdout, stdout_chunks, "stdout", log_callback),
            daemon=True,
        )
        stderr_thread = threading.Thread(
            target=self._consume_stream,
            args=(process.stderr, stderr_chunks, "stderr", log_callback),
            daemon=True,
        )

        stdout_thread.start()
        stderr_thread.start()

        try:
            process.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired as exc:
            process.kill()
            stdout_thread.join(timeout=2)
            stderr_thread.join(timeout=2)
            raise ExtractorExecutionError(
                f"Extractor timed out after {timeout_seconds}s: {' '.join(command)}"
            ) from exc

        stdout_thread.join(timeout=2)
        stderr_thread.join(timeout=2)

        stdout = "".join(stdout_chunks)
        stderr = "".join(stderr_chunks)

        self.validate_execution_result(
            params=params,
            started_at=started_at,
            returncode=process.returncode,
            stdout=stdout,
            stderr=stderr,
        )

        return {
            "returncode": process.returncode,
            "stdout": stdout,
            "stderr": stderr,
            "command": command,
            "workdir": str(workdir),
            "streamed": bool(log_callback),
        }
