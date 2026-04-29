import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from src.utils.helpers import outputs_path

logger = logging.getLogger(__name__)


def univariate_analysis(df) -> None:
    """Histogram and boxplot of raw PM2.5 values."""
    logger.info("Running univariate analysis")

    plots_dir = outputs_path("plots")
    os.makedirs(plots_dir, exist_ok=True)

    plt.figure()
    sns.histplot(df["PM2_5_ugm3"], bins=100)
    plt.title("PM2.5 Distribution")
    plt.savefig(os.path.join(plots_dir, "pm25_distribution.png"))
    plt.close()

    plt.figure()
    sns.boxplot(x=df["PM2_5_ugm3"])
    plt.title("PM2.5 Boxplot")
    plt.savefig(os.path.join(plots_dir, "pm25_boxplot.png"))
    plt.close()


def log_distribution_plot(df) -> None:
    """Histogram of log-transformed PM2.5."""
    logger.info("Plotting log distribution")

    plots_dir = outputs_path("plots")
    os.makedirs(plots_dir, exist_ok=True)

    plt.figure()
    sns.histplot(np.log1p(df["PM2_5_ugm3"]), bins=100)
    plt.title("Log PM2.5 Distribution")
    plt.savefig(os.path.join(plots_dir, "pm25_log_distribution.png"))
    plt.close()


def wind_vs_pm(df) -> None:
    """Scatter plot of wind speed vs PM2.5."""
    logger.info("Plotting wind vs PM2.5")

    plots_dir = outputs_path("plots")
    os.makedirs(plots_dir, exist_ok=True)

    plt.figure()
    sns.scatterplot(
        x=df["Wind_Speed_10m_kmh"],
        y=df["PM2_5_ugm3"],
        alpha=0.3,
    )
    plt.title("Wind Speed vs PM2.5")
    plt.savefig(os.path.join(plots_dir, "wind_vs_pm25.png"))
    plt.close()


def humidity_vs_pm(df) -> None:
    """Scatter plot of humidity vs PM2.5."""
    logger.info("Plotting humidity vs PM2.5")

    plots_dir = outputs_path("plots")
    os.makedirs(plots_dir, exist_ok=True)

    plt.figure()
    sns.scatterplot(
        x=df["Humidity_Percent"],
        y=df["PM2_5_ugm3"],
        alpha=0.3,
    )
    plt.title("Humidity vs PM2.5")
    plt.savefig(os.path.join(plots_dir, "humidity_vs_pm25.png"))
    plt.close()


def correlation_heatmap(df) -> None:
    """Heatmap of correlations between PM2.5 and weather variables."""
    logger.info("Generating correlation heatmap")

    cols = [
        "PM2_5_ugm3",
        "Wind_Speed_10m_kmh",
        "Humidity_Percent",
        "Temp_2m_C",
    ]

    plots_dir = outputs_path("plots")
    os.makedirs(plots_dir, exist_ok=True)

    plt.figure(figsize=(8, 6))
    sns.heatmap(df[cols].corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.savefig(os.path.join(plots_dir, "correlation_matrix.png"))
    plt.close()


def seasonal_boxplot(df) -> None:
    """Boxplot of PM2.5 by season."""
    logger.info("Plotting seasonal boxplot")

    plots_dir = outputs_path("plots")
    os.makedirs(plots_dir, exist_ok=True)

    plt.figure(figsize=(8, 6))
    sns.boxplot(x="Season", y="PM2_5_ugm3", data=df)
    plt.title("Season vs PM2.5")
    plt.savefig(os.path.join(plots_dir, "season_boxplot.png"))
    plt.close()


def run_visualizations(df) -> None:
    """Run all visualization sub-routines."""
    logger.info("Starting visualization module")

    univariate_analysis(df)
    log_distribution_plot(df)
    wind_vs_pm(df)
    humidity_vs_pm(df)
    correlation_heatmap(df)
    seasonal_boxplot(df)

    logger.info("Visualization completed")
