import logging

import pandas as pd

logger = logging.getLogger(__name__)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicates, fix invalid values, and sort by City + Datetime."""
    logger.info("Starting data cleaning")

    original_shape = df.shape

    df = df.drop_duplicates()
    logger.info("Removed duplicates: %s", original_shape[0] - len(df))

    negative_pm = (df["PM2_5_ugm3"] < 0).sum()
    if negative_pm > 0:
        logger.warning("Negative PM2.5 values found: %s", negative_pm)
        df = df[df["PM2_5_ugm3"] >= 0]

    invalid_humidity = (
        (df["Humidity_Percent"] < 0) | (df["Humidity_Percent"] > 100)
    ).sum()
    if invalid_humidity > 0:
        logger.warning("Invalid humidity values: %s", invalid_humidity)
        df["Humidity_Percent"] = df["Humidity_Percent"].clip(0, 100)

    negative_wind = (df["Wind_Speed_10m_kmh"] < 0).sum()
    if negative_wind > 0:
        logger.warning("Negative wind speed values: %s", negative_wind)
        df["Wind_Speed_10m_kmh"] = df["Wind_Speed_10m_kmh"].abs()

    df = df.sort_values(["City", "Datetime"])

    logger.info("Final dataset shape: %s", df.shape)
    logger.info("Rows removed: %s", original_shape[0] - df.shape[0])

    return df
