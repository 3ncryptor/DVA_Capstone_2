import logging
import os

import pandas as pd

from src.utils.helpers import outputs_path

logger = logging.getLogger(__name__)


def wind_season_interaction(df: pd.DataFrame) -> pd.DataFrame:
    """Mean PM2.5 by Season × low_wind combination."""
    logger.info("Analyzing Wind × Season interaction")

    result = df.groupby(["Season", "low_wind"])["PM2_5_ugm3"].mean().reset_index()

    return result


def humidity_season_interaction(df: pd.DataFrame) -> pd.DataFrame:
    """Mean PM2.5 by Season × high_humidity combination."""
    logger.info("Analyzing Humidity × Season interaction")

    result = df.groupby(["Season", "high_humidity"])["PM2_5_ugm3"].mean().reset_index()

    return result


def wind_humidity_interaction(df: pd.DataFrame) -> pd.DataFrame:
    """Mean PM2.5 by low_wind × high_humidity combination."""
    logger.info("Analyzing Wind × Humidity interaction")

    result = (
        df.groupby(["low_wind", "high_humidity"])["PM2_5_ugm3"].mean().reset_index()
    )

    return result


def event_season_interaction(df: pd.DataFrame) -> pd.DataFrame:
    """Mean PM2.5 by Season × festival × crop-burning combination."""
    logger.info("Analyzing Event × Season interaction")

    result = (
        df.groupby(["Season", "is_festival", "is_crop_burning"])["PM2_5_ugm3"]
        .mean()
        .reset_index()
    )

    return result


def severe_probability(df: pd.DataFrame) -> pd.DataFrame:
    """Conditional probability of severe pollution by weather/season group."""
    logger.info("Computing conditional probability of severe pollution")

    grouped = df.groupby(["low_wind", "high_humidity", "Season"])

    prob = grouped["is_severe"].mean().reset_index()

    prob.rename(columns={"is_severe": "severe_probability"}, inplace=True)

    return prob


def interaction_strength(df: pd.DataFrame) -> pd.DataFrame:
    """Variance reduction when grouping by low_wind × high_humidity."""
    logger.info("Evaluating interaction strength")

    overall_var = df["PM2_5_ugm3"].var()

    grouped_var = df.groupby(["low_wind", "high_humidity"])["PM2_5_ugm3"].var().mean()

    result = {
        "overall_variance": overall_var,
        "grouped_variance": grouped_var,
        "variance_reduction": overall_var - grouped_var,
    }

    return pd.DataFrame([result])


def city_interaction(df: pd.DataFrame) -> pd.DataFrame:
    """Mean PM2.5 by City × low_wind."""
    logger.info("Analyzing city-level interaction effects")

    result = df.groupby(["City", "low_wind"])["PM2_5_ugm3"].mean().reset_index()

    return result


def interaction_analysis(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Run all interaction sub-analyses and persist CSVs."""
    logger.info("Starting interaction analysis")

    outputs: dict[str, pd.DataFrame] = {}

    outputs["wind_season"] = wind_season_interaction(df)
    outputs["humidity_season"] = humidity_season_interaction(df)
    outputs["wind_humidity"] = wind_humidity_interaction(df)
    outputs["event_season"] = event_season_interaction(df)
    outputs["severe_prob"] = severe_probability(df)
    outputs["strength"] = interaction_strength(df)
    outputs["city_interaction"] = city_interaction(df)

    tables_dir = outputs_path("tables")
    os.makedirs(tables_dir, exist_ok=True)
    for name, table in outputs.items():
        path = os.path.join(tables_dir, f"{name}_interaction.csv")
        table.to_csv(path, index=False)
        logger.info("Saved: %s", path)

    logger.info("Interaction analysis completed")

    return outputs
