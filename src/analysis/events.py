import logging
import os

import pandas as pd

from src.utils.helpers import outputs_path

logger = logging.getLogger(__name__)


def compute_baseline(df: pd.DataFrame) -> pd.DataFrame:
    """Add 24h rolling baseline and event_delta columns."""
    logger.info("Computing rolling baseline")

    df = df.copy()
    df = df.sort_values(["City", "Datetime"])

    df["baseline_pm25"] = df.groupby("City")["PM2_5_ugm3"].transform(
        lambda x: x.rolling(24).mean()
    )

    df["event_delta"] = df["PM2_5_ugm3"] - df["baseline_pm25"]

    return df


def festival_impact(df: pd.DataFrame) -> pd.DataFrame:
    """Mean PM2.5 and event_delta grouped by festival flag."""
    logger.info("Analyzing festival impact")

    result = (
        df.groupby("is_festival")
        .agg({"PM2_5_ugm3": "mean", "event_delta": "mean"})
        .reset_index()
    )

    return result


def crop_burning_impact(df: pd.DataFrame) -> pd.DataFrame:
    """Mean PM2.5 and event_delta by Season × crop-burning flag."""
    logger.info("Analyzing crop burning impact")

    result = (
        df.groupby(["Season", "is_crop_burning"])
        .agg({"PM2_5_ugm3": "mean", "event_delta": "mean"})
        .reset_index()
    )

    return result


def amplification_factor(df: pd.DataFrame) -> pd.DataFrame:
    """Delta amplification during festival vs non-festival periods."""
    logger.info("Calculating event amplification factor")

    event = df[df["is_festival"]]["event_delta"].mean()
    non_event = df[~df["is_festival"]]["event_delta"].mean()

    result = {
        "event_delta": event,
        "non_event_delta": non_event,
        "amplification": event - non_event,
    }

    return pd.DataFrame([result])


def event_severity(df: pd.DataFrame) -> pd.DataFrame:
    """Severe-pollution probability during festival vs non-festival periods."""
    logger.info("Analyzing severity during events")

    result = df.groupby("is_festival")["is_severe"].mean().reset_index()
    result.rename(columns={"is_severe": "severe_probability"}, inplace=True)

    return result


def event_analysis(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Run all event sub-analyses and persist CSVs."""
    logger.info("Starting event analysis")

    df = compute_baseline(df)

    outputs: dict[str, pd.DataFrame] = {}

    outputs["festival"] = festival_impact(df)
    outputs["crop"] = crop_burning_impact(df)
    outputs["amplification"] = amplification_factor(df)
    outputs["severity"] = event_severity(df)

    tables_dir = outputs_path("tables")
    os.makedirs(tables_dir, exist_ok=True)
    for name, table in outputs.items():
        path = os.path.join(tables_dir, f"{name}_events.csv")
        table.to_csv(path, index=False)
        logger.info("Saved: %s", path)

    logger.info("Event analysis completed")

    return outputs
