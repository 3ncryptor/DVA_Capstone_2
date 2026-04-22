import logging
import pandas as pd

logger = logging.getLogger(__name__)

def clean_data(df: pd.DataFrame):

    logger.info("Starting data cleaning")

    original_shape = df.shape

    # --- 1. Remove exact duplicates ---
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    logger.info(f"Removed duplicates: {before - after}")

    # --- 2. Handle negative PM2.5 ---
    negative_pm = (df["PM2_5_ugm3"] < 0).sum()
    if negative_pm > 0:
        logger.warning(f"Negative PM2.5 values found: {negative_pm}")
        df = df[df["PM2_5_ugm3"] >= 0]

    # --- 3. Fix humidity ---
    invalid_humidity = (
        (df["Humidity_Percent"] < 0) | (df["Humidity_Percent"] > 100)
    ).sum()

    if invalid_humidity > 0:
        logger.warning(f"Invalid humidity values: {invalid_humidity}")
        df["Humidity_Percent"] = df["Humidity_Percent"].clip(0, 100)

    # --- 4. Fix wind speed ---
    negative_wind = (df["Wind_Speed_10m_kmh"] < 0).sum()

    if negative_wind > 0:
        logger.warning(f"Negative wind speed values: {negative_wind}")
        df["Wind_Speed_10m_kmh"] = df["Wind_Speed_10m_kmh"].abs()

    # --- 5. Sort for temporal consistency ---
    df = df.sort_values(["City", "Datetime"])

    logger.info(f"Final dataset shape: {df.shape}")
    logger.info(f"Rows removed: {original_shape[0] - df.shape[0]}")

    return df