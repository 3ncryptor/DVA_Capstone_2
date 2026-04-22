import logging
import os

import pandas as pd
import yaml

from src.utils.helpers import project_root

logger = logging.getLogger(__name__)

# Columns required for clean_data + create_features + forecasting (pruned I/O for one city).
FORECAST_USECOLS: tuple[str, ...] = (
    "City",
    "Datetime",
    "PM2_5_ugm3",
    "Humidity_Percent",
    "Wind_Speed_10m_kmh",
    "Temp_2m_C",
    "Festival_Period",
    "Crop_Burning_Season",
)


def _raw_path() -> str:
    cfg = os.path.join(project_root(), "config", "config.yaml")
    with open(cfg, "r", encoding="utf-8") as f:
        y = yaml.safe_load(f)
    p = y["data"]["raw_path"]
    return p if os.path.isabs(p) else os.path.join(project_root(), p)


def load_city_data_for_forecast(
    city: str,
    *,
    chunk_size: int = 200_000,
) -> pd.DataFrame:
    """
    Read only needed columns in chunks, keep rows for ``city`` only.
    Avoids loading the full national table into memory.
    """
    path = _raw_path()
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Raw data not found: {path}")

    parts: list[pd.DataFrame] = []
    total_in = 0
    total_kept = 0

    for chunk in pd.read_csv(
        path,
        usecols=list(FORECAST_USECOLS),
        chunksize=chunk_size,
        low_memory=False,
    ):
        total_in += len(chunk)
        sub = chunk[chunk["City"] == city]
        if len(sub):
            total_kept += len(sub)
            parts.append(sub)

    if not parts:
        raise ValueError(
            f"No rows found for city {city!r}. Check spelling against the dataset."
        )

    df = pd.concat(parts, ignore_index=True)
    df["Datetime"] = pd.to_datetime(df["Datetime"])
    logger.info(
        "Loaded %s city rows (scanned %s raw rows) from chunks",
        total_kept,
        total_in,
    )
    return df
