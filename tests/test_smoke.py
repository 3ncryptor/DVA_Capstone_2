import subprocess
import sys

from src.utils.helpers import project_root


def test_imports():
    """Every public module can be imported without crashing."""
    import src.ingestion.loader  # noqa: F401
    import src.preprocessing.validation  # noqa: F401
    import src.preprocessing.cleaning  # noqa: F401
    import src.preprocessing.feature_engineering  # noqa: F401
    import src.analysis.profiling  # noqa: F401
    import src.analysis.temporal  # noqa: F401
    import src.analysis.interactions  # noqa: F401
    import src.analysis.events  # noqa: F401
    import src.analysis.extremes  # noqa: F401
    import src.analysis.synthesis  # noqa: F401
    import src.analysis.visualization  # noqa: F401
    import src.analysis.forecasting  # noqa: F401


def test_project_root_exists():
    import os

    root = project_root()
    assert os.path.isdir(root)
    assert os.path.isfile(os.path.join(root, "cli.py"))


def test_cli_help():
    result = subprocess.run(
        [sys.executable, "cli.py", "--help"],
        cwd=project_root(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
