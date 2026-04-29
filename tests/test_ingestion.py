import pytest

from src.ingestion.loader import load_config


def test_load_config_reads_yaml():
    cfg = load_config()
    assert isinstance(cfg, dict)
    assert "data" in cfg
    assert "raw_path" in cfg["data"]


def test_load_data_missing_file_raises(tmp_path, monkeypatch):
    """FileNotFoundError when the configured CSV is absent."""
    _root = lambda: str(tmp_path)  # noqa: E731
    monkeypatch.setattr("src.utils.helpers.project_root", _root)
    monkeypatch.setattr("src.ingestion.loader.project_root", _root)

    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    (cfg_dir / "config.yaml").write_text(
        "data:\n  raw_path: data/raw/nonexistent.csv\n"
    )

    from src.ingestion.loader import load_data

    with pytest.raises(FileNotFoundError):
        load_data()
