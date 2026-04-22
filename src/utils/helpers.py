import os
from typing import FrozenSet

EDA_STAGE_CHOICES: FrozenSet[str] = frozenset(
    {
        "profiling",
        "temporal",
        "interactions",
        "events",
        "visual",
        "full",
    }
)


def normalize_eda_stage(stage: str) -> str:
    """Lowercase, strip, and map common aliases (e.g. interaction → interactions)."""
    s = stage.strip().lower()
    aliases = {"interaction": "interactions"}
    return aliases.get(s, s)


def project_root() -> str:
    """Absolute path to the repository root (directory that contains ``config`` and ``src``)."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
