import logging
import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = [
    "Datetime",
    "City",
    "PM2_5_ugm3",
    "Humidity_Percent",
    "Wind_Speed_10m_kmh"
]

def validate_schema(df: pd.DataFrame):
    logger.info("Validating schema")

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing_cols:
        logger.error(f"Missing required columns: {missing_cols}")
        raise ValueError("Schema validation failed")

    logger.info("Schema validation passed")


def validate_ranges(df: pd.DataFrame):
    logger.info("Validating data ranges")

    issues = {}

    # PM2.5 should not be negative
    invalid_pm = df[df["PM2_5_ugm3"] < 0]
    issues["negative_pm25"] = len(invalid_pm)

    # Humidity should be between 0–100
    invalid_humidity = df[
        (df["Humidity_Percent"] < 0) | (df["Humidity_Percent"] > 100)
    ]
    issues["invalid_humidity"] = len(invalid_humidity)

    # Wind speed should not be negative
    invalid_wind = df[df["Wind_Speed_10m_kmh"] < 0]
    issues["negative_wind"] = len(invalid_wind)

    logger.info(f"Validation issues summary: {issues}")

    return issues


def validate_duplicates(df: pd.DataFrame):
    logger.info("Checking duplicate records")

    dup_count = df.duplicated().sum()

    logger.info(f"Duplicate rows: {dup_count}")

    return dup_count