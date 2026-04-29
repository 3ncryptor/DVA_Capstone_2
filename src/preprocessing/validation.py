import logging

import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = [
    "Datetime",
    "City",
    "PM2_5_ugm3",
    "Humidity_Percent",
    "Wind_Speed_10m_kmh",
]


def validate_schema(df: pd.DataFrame) -> None:
    """Raise ValueError if any required column is missing from *df*."""
    logger.info("Validating schema")

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing_cols:
        logger.error("Missing required columns: %s", missing_cols)
        raise ValueError("Schema validation failed")

    logger.info("Schema validation passed")


def validate_ranges(df: pd.DataFrame) -> dict[str, int]:
    """Log counts of out-of-range values (negative PM2.5, bad humidity, negative wind)."""
    logger.info("Validating data ranges")

    issues: dict[str, int] = {}

    issues["negative_pm25"] = int((df["PM2_5_ugm3"] < 0).sum())
    issues["invalid_humidity"] = int(
        ((df["Humidity_Percent"] < 0) | (df["Humidity_Percent"] > 100)).sum()
    )
    issues["negative_wind"] = int((df["Wind_Speed_10m_kmh"] < 0).sum())

    logger.info("Validation issues summary: %s", issues)

    return issues


def validate_duplicates(df: pd.DataFrame) -> int:
    """Return the count of exact duplicate rows."""
    logger.info("Checking duplicate records")

    dup_count = int(df.duplicated().sum())

    logger.info("Duplicate rows: %s", dup_count)

    return dup_count
