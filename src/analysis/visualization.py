import matplotlib.pyplot as plt
import seaborn as sns
import logging
import numpy as np

logger = logging.getLogger(__name__)

# Univariate Analysis
def univariate_analysis(df):

    logger.info("Running univariate analysis")

    plt.figure()
    sns.histplot(df["PM2_5_ugm3"], bins=100)
    plt.title("PM2.5 Distribution")
    plt.savefig("outputs/plots/pm25_distribution.png")
    plt.close()

    plt.figure()
    sns.boxplot(x=df["PM2_5_ugm3"])
    plt.title("PM2.5 Boxplot")
    plt.savefig("outputs/plots/pm25_boxplot.png")
    plt.close()

# Log Distribution Plot
def log_distribution_plot(df):

    logger.info("Plotting log distribution")

    plt.figure()
    sns.histplot(np.log1p(df["PM2_5_ugm3"]), bins=100)
    plt.title("Log PM2.5 Distribution")
    plt.savefig("outputs/plots/pm25_log_distribution.png")
    plt.close()

# Bivariate Analysis
# Wind vs PM2.5 Scatter Plot
def wind_vs_pm(df):

    logger.info("Plotting wind vs PM2.5")

    plt.figure()
    sns.scatterplot(
        x=df["Wind_Speed_10m_kmh"],
        y=df["PM2_5_ugm3"],
        alpha=0.3
    )
    plt.title("Wind Speed vs PM2.5")
    plt.savefig("outputs/plots/wind_vs_pm25.png")
    plt.close()

# Humidity vs PM2.5 Scatter Plot
def humidity_vs_pm(df):

    logger.info("Plotting humidity vs PM2.5")

    plt.figure()
    sns.scatterplot(
        x=df["Humidity_Percent"],
        y=df["PM2_5_ugm3"],
        alpha=0.3
    )
    plt.title("Humidity vs PM2.5")
    plt.savefig("outputs/plots/humidity_vs_pm25.png")
    plt.close()

# Correlation Heatmap
def correlation_heatmap(df):

    logger.info("Generating correlation heatmap")

    cols = [
        "PM2_5_ugm3",
        "Wind_Speed_10m_kmh",
        "Humidity_Percent",
        "Temp_2m_C"
    ]

    plt.figure(figsize=(8,6))
    sns.heatmap(df[cols].corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.savefig("outputs/plots/correlation_matrix.png")
    plt.close()


# Seasonal Boxplot
def seasonal_boxplot(df):

    logger.info("Plotting seasonal boxplot")

    plt.figure(figsize=(8,6))
    sns.boxplot(x="Season", y="PM2_5_ugm3", data=df)
    plt.title("Season vs PM2.5")
    plt.savefig("outputs/plots/season_boxplot.png")
    plt.close()

# MasterFunction
def run_visualizations(df):

    logger.info("Starting visualization module")

    univariate_analysis(df)
    log_distribution_plot(df)
    wind_vs_pm(df)
    humidity_vs_pm(df)
    correlation_heatmap(df)
    seasonal_boxplot(df)

    logger.info("Visualization completed")