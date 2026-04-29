import logging
import os
from typing import Tuple

import numpy as np
import pandas as pd

from src.utils.helpers import outputs_path

logger = logging.getLogger(__name__)


def aggregate_time(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Aggregate PM2.5 to daily and monthly levels per city."""
    logger.info("Aggregating data to daily and monthly levels")

    df = df.copy()
    df["date"] = df["Datetime"].dt.date
    df["month_period"] = df["Datetime"].dt.to_period("M")

    daily = df.groupby(["City", "date"])["PM2_5_ugm3"].mean().reset_index()
    monthly = df.groupby(["City", "month_period"])["PM2_5_ugm3"].mean().reset_index()

    return daily, monthly


def rolling_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Add 24h rolling mean and std of PM2.5 per city."""
    logger.info("Computing rolling trend and volatility")

    df = df.copy()
    df = df.sort_values(["City", "Datetime"])

    df["rolling_mean_24"] = df.groupby("City")["PM2_5_ugm3"].transform(
        lambda x: x.rolling(24).mean()
    )

    df["rolling_std_24"] = df.groupby("City")["PM2_5_ugm3"].transform(
        lambda x: x.rolling(24).std()
    )

    return df


def lag_correlation(df: pd.DataFrame, max_lag: int = 48) -> pd.DataFrame:
    """Auto-correlation of PM2.5 for lags 1..max_lag."""
    logger.info("Computing lag correlation")

    city = df["City"].iloc[0]

    series = df[df["City"] == city]["PM2_5_ugm3"].dropna()

    correlations = {}

    for lag in range(1, max_lag + 1):
        corr = series.corr(series.shift(lag))
        correlations[lag] = corr

    result = pd.DataFrame(
        {"lag": list(correlations.keys()), "correlation": list(correlations.values())}
    )

    return result


def diurnal_pattern(df: pd.DataFrame) -> pd.DataFrame:
    """Mean PM2.5 by hour of day."""
    logger.info("Analyzing diurnal (hourly) patterns")

    hourly = df.groupby("hour")["PM2_5_ugm3"].mean().reset_index()

    return hourly


def seasonal_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Mean PM2.5 by season."""
    logger.info("Analyzing seasonal trends")

    seasonal = df.groupby(["Season"])["PM2_5_ugm3"].mean().reset_index()

    return seasonal


def volatility_regime(df: pd.DataFrame) -> pd.DataFrame:
    """Flag rows whose 24h rolling std exceeds the median."""
    logger.info("Detecting volatility regimes")

    df = df.copy()
    df["volatility_flag"] = df["rolling_std_24"] > df["rolling_std_24"].median()

    return df[["Datetime", "City", "rolling_std_24", "volatility_flag"]]


def temporal_analysis(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Run all temporal sub-analyses and persist CSVs."""
    logger.info("Starting temporal analysis")

    df = df.copy()
    outputs: dict[str, pd.DataFrame] = {}

    daily, monthly = aggregate_time(df)
    outputs["daily"] = daily
    outputs["monthly"] = monthly

    df = rolling_trend(df)

    outputs["diurnal"] = diurnal_pattern(df)
    outputs["seasonal"] = seasonal_trend(df)

    delhi_df = df[df["City"] == "Delhi"]
    outputs["lag"] = lag_correlation(delhi_df)

    outputs["volatility"] = volatility_regime(df)

    tables_dir = outputs_path("tables")
    os.makedirs(tables_dir, exist_ok=True)
    for name, table in outputs.items():
        path = os.path.join(tables_dir, f"{name}_temporal.csv")
        table.to_csv(path, index=False)
        logger.info("Saved: %s", path)

    logger.info("Temporal analysis completed")

    return outputs
