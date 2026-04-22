import logging
import os

import pandas as pd
import yaml

from src.utils.helpers import project_root

logger = logging.getLogger(__name__)


def load_config() -> dict:
    cfg_path = os.path.join(project_root(), "config", "config.yaml")
    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_data() -> pd.DataFrame:
    config = load_config()
    rel_path = config["data"]["raw_path"]
    abs_path = (
        rel_path
        if os.path.isabs(rel_path)
        else os.path.join(project_root(), rel_path)
    )

    logger.info("Loading data from %s", rel_path)

    if not os.path.isfile(abs_path):
        logger.error("File not found: %s", abs_path)
        raise FileNotFoundError(abs_path)

    try:
        df = pd.read_csv(abs_path)
    except Exception:
        logger.exception("Failed to read CSV")
        raise

    logger.info("Data loaded successfully | Shape: %s", df.shape)

    required_cols = ["Datetime", "PM2_5_ugm3", "City"]
    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        logger.error("Missing required columns: %s", missing)
        raise ValueError("Invalid dataset schema")

    try:
        df["Datetime"] = pd.to_datetime(df["Datetime"])
    except Exception:
        logger.exception("Datetime parsing failed")
        raise

    logger.info("Datetime parsing successful")

    return df
