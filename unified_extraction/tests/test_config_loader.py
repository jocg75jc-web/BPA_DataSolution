from pathlib import Path

from core.config_loader import ConfigLoader


def test_config_loader_reads_projects():
    config_path = Path(__file__).resolve().parents[1] / "config" / "processes.json"
    loader = ConfigLoader(config_path)
    projects = loader.get_all_projects(enabled_only=False)

    assert len(projects) >= 2
    ids = {p["id"] for p in projects}
    assert "titania" in ids
    assert "onnet" in ids
