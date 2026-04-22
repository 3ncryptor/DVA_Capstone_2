import logging
import pandas as pd

logger = logging.getLogger(__name__)

def aggregate_time(df: pd.DataFrame):

    logger.info("Aggregating data to daily and monthly levels")

    df["date"] = df["Datetime"].dt.date
    df["month_period"] = df["Datetime"].dt.to_period("M")

    daily = df.groupby(["City", "date"])["PM2_5_ugm3"].mean().reset_index()
    monthly = df.groupby(["City", "month_period"])["PM2_5_ugm3"].mean().reset_index()

    return daily, monthly

def rolling_trend(df: pd.DataFrame):

    logger.info("Computing rolling trend and volatility")

    df = df.sort_values(["City", "Datetime"])

    df["rolling_mean_24"] = df.groupby("City")["PM2_5_ugm3"].transform(
        lambda x: x.rolling(24).mean()
    )

    df["rolling_std_24"] = df.groupby("City")["PM2_5_ugm3"].transform(
        lambda x: x.rolling(24).std()
    )

    return df

import numpy as np

def lag_correlation(df: pd.DataFrame, max_lag=48):

    logger.info("Computing lag correlation")

    city = df["City"].iloc[0]  # assume filtered dataset

    series = df[df["City"] == city]["PM2_5_ugm3"].dropna()

    correlations = {}

    for lag in range(1, max_lag + 1):
        corr = series.corr(series.shift(lag))
        correlations[lag] = corr

    result = pd.DataFrame({
        "lag": list(correlations.keys()),
        "correlation": list(correlations.values())
    })

    return result

def diurnal_pattern(df: pd.DataFrame):

    logger.info("Analyzing diurnal (hourly) patterns")

    hourly = df.groupby("hour")["PM2_5_ugm3"].mean().reset_index()

    return hourly

def seasonal_trend(df: pd.DataFrame):

    logger.info("Analyzing seasonal trends")

    seasonal = df.groupby(["Season"])["PM2_5_ugm3"].mean().reset_index()

    return seasonal

def volatility_regime(df: pd.DataFrame):

    logger.info("Detecting volatility regimes")

    df["volatility_flag"] = df["rolling_std_24"] > df["rolling_std_24"].median()

    return df[["Datetime", "City", "rolling_std_24", "volatility_flag"]]


def temporal_analysis(df: pd.DataFrame):

    logger.info("Starting temporal analysis")

    outputs = {}

    daily, monthly = aggregate_time(df)
    outputs["daily"] = daily
    outputs["monthly"] = monthly

    df = rolling_trend(df)

    outputs["diurnal"] = diurnal_pattern(df)
    outputs["seasonal"] = seasonal_trend(df)

    # Use one major city for lag analysis (e.g., Delhi)
    delhi_df = df[df["City"] == "Delhi"]
    outputs["lag"] = lag_correlation(delhi_df)

    outputs["volatility"] = volatility_regime(df)

    # Save outputs
    for name, table in outputs.items():
        path = f"outputs/tables/{name}_temporal.csv"
        table.to_csv(path, index=False)
        logger.info(f"Saved: {path}")

    logger.info("Temporal analysis completed")

    return outputs