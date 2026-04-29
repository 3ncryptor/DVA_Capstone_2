import logging
import os

import numpy as np
import pandas as pd

from src.utils.helpers import outputs_path

logger = logging.getLogger(__name__)


def global_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Global PM2.5 distribution stats (mean, median, percentiles)."""
    logger.info("Running global distribution profiling")

    pm = df["PM2_5_ugm3"].dropna()

    stats = {
        "mean": pm.mean(),
        "median": pm.median(),
        "std": pm.std(),
        "skewness": pm.skew(),
        "kurtosis": pm.kurt(),
        "min": pm.min(),
        "max": pm.max(),
        "p95": np.percentile(pm, 95),
        "p99": np.percentile(pm, 99),
    }

    logger.info("Global stats: %s", stats)

    return pd.DataFrame([stats])


def mean_median_gap(df: pd.DataFrame) -> pd.DataFrame:
    """Mean-median divergence as a skewness indicator."""
    logger.info("Calculating mean-median divergence")

    mean_val = df["PM2_5_ugm3"].mean()
    median_val = df["PM2_5_ugm3"].median()

    gap = mean_val - median_val

    result = {
        "mean": mean_val,
        "median": median_val,
        "gap": gap,
        "gap_ratio": gap / mean_val if mean_val != 0 else 0,
    }

    logger.info("Mean-Median Gap: %s", result)

    return pd.DataFrame([result])


def tail_risk(df: pd.DataFrame) -> pd.DataFrame:
    """Fraction of records above the 250 µg/m³ severe threshold."""
    logger.info("Analyzing tail risk")

    pm = df["PM2_5_ugm3"]

    severe_threshold = 250

    total = len(pm)
    severe_count = (pm > severe_threshold).sum()

    result = {
        "total_records": total,
        "severe_count": severe_count,
        "severe_percentage": severe_count / total,
    }

    logger.info("Tail risk stats: %s", result)

    return pd.DataFrame([result])


def extreme_contribution(df: pd.DataFrame) -> pd.DataFrame:
    """Share of total PM2.5 mass contributed by >p95 values."""
    logger.info("Calculating contribution of extreme values")

    pm = df["PM2_5_ugm3"]

    threshold = np.percentile(pm, 95)

    extreme = pm[pm > threshold]

    contribution = extreme.sum() / pm.sum()

    result = {
        "p95_threshold": threshold,
        "extreme_contribution_ratio": contribution,
    }

    logger.info("Extreme contribution: %s", result)

    return pd.DataFrame([result])


def log_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Log-transformed PM2.5 summary (mean, std, skew)."""
    logger.info("Applying log transformation")

    pm = df["PM2_5_ugm3"]

    log_pm = np.log1p(pm)

    stats = {
        "log_mean": log_pm.mean(),
        "log_std": log_pm.std(),
        "log_skew": pd.Series(log_pm).skew(),
    }

    logger.info("Log distribution stats: %s", stats)

    return pd.DataFrame([stats])


def city_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Per-city PM2.5 descriptive statistics with coefficient of variation."""
    logger.info("Profiling distribution per city")

    city_stats = df.groupby("City")["PM2_5_ugm3"].agg(
        ["mean", "median", "std", "max"]
    )

    city_stats["cv"] = city_stats["std"] / city_stats["mean"]

    return city_stats.reset_index()


def missingness(df: pd.DataFrame) -> pd.DataFrame:
    """Per-column missing-value counts and ratios."""
    logger.info("Analyzing missing values")

    missing = df.isnull().sum()

    missing_ratio = missing / len(df)

    result = pd.DataFrame(
        {"missing_count": missing, "missing_ratio": missing_ratio}
    )

    result = result.reset_index().rename(columns={"index": "column"})

    return result.sort_values(by="missing_ratio", ascending=False)


def run_profiling(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Run all profiling sub-analyses and persist CSVs."""
    logger.info("Starting profiling analysis")

    outputs: dict[str, pd.DataFrame] = {}

    outputs["global"] = global_distribution(df)
    outputs["mean_median"] = mean_median_gap(df)
    outputs["tail"] = tail_risk(df)
    outputs["extreme"] = extreme_contribution(df)
    outputs["log"] = log_distribution(df)
    outputs["city"] = city_distribution(df)
    outputs["missing"] = missingness(df)

    tables_dir = outputs_path("tables")
    os.makedirs(tables_dir, exist_ok=True)
    for name, table in outputs.items():
        path = os.path.join(tables_dir, f"{name}_profiling.csv")
        table.to_csv(path, index=False)
        logger.info("Saved: %s", path)

    logger.info("Profiling completed")

    return outputs
