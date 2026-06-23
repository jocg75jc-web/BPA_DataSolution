from pathlib import Path

from core.execution_engine import ExecutionEngine


def test_execution_engine_lists_projects():
    config_path = Path(__file__).resolve().parents[1] / "config" / "processes.json"
    engine = ExecutionEngine(config_path)

    projects = engine.list_projects()
    ids = {p["id"] for p in projects}

    assert "titania" in ids
    assert "onnet" in ids
