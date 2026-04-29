import logging
import os

import pandas as pd

from src.utils.helpers import outputs_path

logger = logging.getLogger(__name__)


def extract_extremes(df: pd.DataFrame) -> pd.DataFrame:
    """Filter rows where PM2.5 exceeds the 250 µg/m³ severe threshold."""
    logger.info("Extracting extreme pollution events")

    extreme = df[df["PM2_5_ugm3"] > 250]

    return extreme


def extreme_conditions(df: pd.DataFrame) -> pd.DataFrame:
    """Descriptive stats of weather variables during extreme events."""
    logger.info("Analyzing conditions during extreme events")

    extreme = extract_extremes(df)

    summary = extreme[
        ["Wind_Speed_10m_kmh", "Humidity_Percent", "Temp_2m_C"]
    ].describe()

    return summary


def extreme_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Count of extreme events by City × Season."""
    logger.info("Analyzing extreme event distribution")

    extreme = extract_extremes(df)

    result = extreme.groupby(["City", "Season"]).size().reset_index(name="count")

    return result


def extreme_probability(df: pd.DataFrame) -> pd.DataFrame:
    """Conditional probability of severe events by weather/season group."""
    logger.info("Computing probability of extreme events")

    grouped = df.groupby(["low_wind", "high_humidity", "Season"])

    prob = grouped["is_severe"].mean().reset_index()

    prob.rename(columns={"is_severe": "extreme_probability"}, inplace=True)

    return prob


def extreme_analysis(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Run all extreme-event sub-analyses and persist CSVs."""
    logger.info("Starting extreme event analysis")

    outputs: dict[str, pd.DataFrame] = {}

    outputs["conditions"] = extreme_conditions(df)
    outputs["distribution"] = extreme_distribution(df)
    outputs["probability"] = extreme_probability(df)

    tables_dir = outputs_path("tables")
    os.makedirs(tables_dir, exist_ok=True)
    for name, table in outputs.items():
        path = os.path.join(tables_dir, f"{name}_extremes.csv")
        table.to_csv(path, index=False)
        logger.info("Saved: %s", path)

    logger.info("Extreme analysis completed")

    return outputs
