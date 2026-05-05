import logging
import os

import numpy as np
import pandas as pd

from src.utils.helpers import outputs_path

logger = logging.getLogger(__name__)


def build_overview(df: pd.DataFrame) -> pd.DataFrame:
    """City-level summary (mean/max PM2.5, severe %, coordinates)."""
    logger.info("Building overview dataset")

    summary = df.groupby("City").agg(
        {"PM2_5_ugm3": ["mean", "max"], "is_severe": "mean", "Latitude": "first", "Longitude": "first"}
    )

    summary.columns = ["avg_pm25", "max_pm25", "severe_pct", "lat", "lon"]

    return summary.reset_index()


def build_temporal(df: pd.DataFrame) -> pd.DataFrame:
    """Daily average PM2.5 and rolling mean per city/season."""
    logger.info("Building temporal dataset")

    df = df.copy()
    df["date"] = df["Datetime"].dt.date

    daily = (
        df.groupby(["City", "date", "Season"])
        .agg({"PM2_5_ugm3": "mean", "pm25_roll_24": "mean"})
        .reset_index()
    )

    daily.rename(
        columns={"PM2_5_ugm3": "pm25_avg", "pm25_roll_24": "rolling_pm25"},
        inplace=True,
    )

    return daily


def build_city_comparison(df: pd.DataFrame) -> pd.DataFrame:
    """Cross-city descriptive statistics with coefficient of variation."""
    logger.info("Building city comparison dataset")

    stats = df.groupby("City").agg(
        {"PM2_5_ugm3": ["mean", "median", "std"], "is_severe": "mean"}
    )

    stats.columns = ["mean", "median", "std", "severe_pct"]

    stats["cv"] = stats["std"] / stats["mean"]

    return stats.reset_index()


def build_interactions(df: pd.DataFrame) -> pd.DataFrame:
    """Mean PM2.5 and severe probability by weather/season combination."""
    logger.info("Building interaction dataset")

    result = (
        df.groupby(["Season", "low_wind", "high_humidity"])
        .agg({"PM2_5_ugm3": "mean", "is_severe": "mean"})
        .reset_index()
    )

    result.rename(
        columns={"PM2_5_ugm3": "pm25_avg", "is_severe": "severe_probability"},
        inplace=True,
    )

    return result


def build_events(df: pd.DataFrame) -> pd.DataFrame:
    """Event-type dataset for Tableau (festival / crop-burning / none)."""
    logger.info("Building event dataset")

    df = df.copy()

    if "event_delta" not in df.columns:
        from src.analysis.events import compute_baseline

        df = compute_baseline(df)

    conditions = [df["is_festival"], df["is_crop_burning"]]
    choices = ["Festival", "Crop Burning"]
    df["event_type"] = np.select(conditions, choices, default="None")

    result = (
        df.groupby(["event_type", "Season"])
        .agg({"PM2_5_ugm3": "mean", "event_delta": "mean", "is_severe": "mean"})
        .reset_index()
    )

    result.rename(
        columns={"PM2_5_ugm3": "pm25_avg", "is_severe": "severe_probability"},
        inplace=True,
    )

    return result


def build_extremes(df: pd.DataFrame) -> pd.DataFrame:
    """Extreme-event probability by City × Season."""
    logger.info("Building extreme dataset")

    extreme = df[df["is_severe"]]

    result = extreme.groupby(["City", "Season"]).size().reset_index(name="extreme_count")

    total = df.groupby(["City", "Season"]).size().reset_index(name="total_count")

    merged = result.merge(total, on=["City", "Season"])

    merged["extreme_probability"] = merged["extreme_count"] / merged["total_count"]

    return merged


def build_all_datasets(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Build and persist all Tableau-ready CSV datasets."""
    logger.info("Building all Tableau datasets")

    df = df.copy()

    outputs: dict[str, pd.DataFrame] = {
        "overview": build_overview(df),
        "temporal": build_temporal(df),
        "city": build_city_comparison(df),
        "interaction": build_interactions(df),
        "events": build_events(df),
        "extremes": build_extremes(df),
    }

    tableau_dir = outputs_path("tables", "Tableau")
    os.makedirs(tableau_dir, exist_ok=True)
    for name, table in outputs.items():
        path = os.path.join(tableau_dir, f"{name}_dashboard.csv")
        table.to_csv(path, index=False)
        logger.info("Saved: %s", path)

    logger.info("All datasets ready for Tableau")

    return outputs
