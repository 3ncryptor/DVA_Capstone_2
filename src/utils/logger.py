import logging
import logging.config
import os
from typing import Optional

import yaml
from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

from src.utils.helpers import project_root

# Shared console for progress bars, panels, and consistent styling across CLI/EDA/prediction
_rich_console: Optional[Console] = None
_rich_stream_handler_added: bool = False
_logging_configured: bool = False

CUSTOM_THEME = Theme(
    {
        "eda.title": "bold bright_cyan",
        "eda.stage": "bold yellow",
        "eda.dim": "dim",
        "pred.title": "bold bright_magenta",
        "ok": "green",
        "warn": "yellow",
        "err": "bold red",
        "log.level": "white",
    }
)


def get_rich_console() -> Console:
    global _rich_console
    if _rich_console is None:
        _rich_console = Console(theme=CUSTOM_THEME)
    return _rich_console


def setup_logger() -> Optional[Console]:
    """
    File logging to outputs/logs/app.log (plain text) + Rich colored logs on stdout.
    Safe to call more than once (adds the Rich stream handler only once).
    """
    global _rich_stream_handler_added
    root_dir = project_root()
    config_path = os.path.join(root_dir, "config", "logging.yaml")

    if not os.path.exists(config_path):
        raise FileNotFoundError("Logging config not found")

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    log_file = config["handlers"]["file"]["filename"]
    if not os.path.isabs(log_file):
        log_file = os.path.join(root_dir, log_file)
    config["handlers"]["file"]["filename"] = log_file

    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    global _logging_configured
    if not _logging_configured:
        logging.config.dictConfig(config)
        _logging_configured = True

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    if not _rich_stream_handler_added:
        console = get_rich_console()
        ch = RichHandler(
            console=console,
            show_time=True,
            show_path=False,
            show_level=True,
            rich_tracebacks=True,
            markup=True,
            level=logging.INFO,
        )
        root.addHandler(ch)
        _rich_stream_handler_added = True
        logging.getLogger(__name__).info(
            "Logger initialized (file + Rich console)"
        )

    return get_rich_console()
