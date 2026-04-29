import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract year, month, hour, and day_of_week from Datetime."""
    logger.info("Adding time-based features")

    df["year"] = df["Datetime"].dt.year
    df["month"] = df["Datetime"].dt.month
    df["hour"] = df["Datetime"].dt.hour
    df["day_of_week"] = df["Datetime"].dt.dayofweek

    return df


def add_lag_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add per-city PM2.5 lag columns (1h, 24h, 168h)."""
    logger.info("Adding lag features")

    df = df.sort_values(["City", "Datetime"])

    df["pm25_lag_1"] = df.groupby("City")["PM2_5_ugm3"].shift(1)
    df["pm25_lag_24"] = df.groupby("City")["PM2_5_ugm3"].shift(24)
    df["pm25_lag_168"] = df.groupby("City")["PM2_5_ugm3"].shift(168)

    return df


def add_rolling_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add 24-hour rolling mean and std of PM2.5 per city."""
    logger.info("Adding rolling features")

    df["pm25_roll_24"] = df.groupby("City")["PM2_5_ugm3"].transform(
        lambda x: x.rolling(24).mean()
    )

    df["pm25_roll_std_24"] = df.groupby("City")["PM2_5_ugm3"].transform(
        lambda x: x.rolling(24).std()
    )

    return df


def add_baseline_deviation(df: pd.DataFrame) -> pd.DataFrame:
    """Compute deviation of PM2.5 from its 24h rolling mean."""
    logger.info("Calculating deviation from baseline")

    df["pm25_deviation"] = df["PM2_5_ugm3"] - df["pm25_roll_24"]

    return df


def add_severity_levels(df: pd.DataFrame) -> pd.DataFrame:
    """Assign Indian AQI-style category and is_severe boolean flag."""
    logger.info("Adding severity categories")

    conditions = [
        df["PM2_5_ugm3"] <= 30,
        df["PM2_5_ugm3"] <= 60,
        df["PM2_5_ugm3"] <= 90,
        df["PM2_5_ugm3"] <= 120,
        df["PM2_5_ugm3"] <= 250,
    ]
    choices = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor"]
    df["pm25_category"] = np.select(conditions, choices, default="Severe")

    df["is_severe"] = df["PM2_5_ugm3"] > 250

    return df


def add_weather_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Flag low-wind (<5 km/h) and high-humidity (>70%) conditions."""
    logger.info("Adding weather interaction flags")

    df["low_wind"] = df["Wind_Speed_10m_kmh"] < 5
    df["high_humidity"] = df["Humidity_Percent"] > 70

    return df


def add_event_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Convert Festival_Period and Crop_Burning_Season to boolean flags."""
    logger.info("Adding event flags")

    df["is_festival"] = df["Festival_Period"] == 1
    df["is_crop_burning"] = df["Crop_Burning_Season"] == 1

    return df


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Run the full feature engineering pipeline (time, lags, rolling, severity, flags)."""
    logger.info("Starting feature engineering")

    df = add_time_features(df)
    df = add_lag_features(df)
    df = add_rolling_features(df)
    df = add_baseline_deviation(df)
    df = add_severity_levels(df)
    df = add_weather_flags(df)
    df = add_event_flags(df)

    logger.info("Feature engineering completed")

    return df
