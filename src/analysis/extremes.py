import logging
import pandas as pd

logger = logging.getLogger(__name__)

# Extract Extreme Pollution Events
def extract_extremes(df: pd.DataFrame):

    logger.info("Extracting extreme pollution events")

    extreme = df[df["PM2_5_ugm3"] > 250]

    return extreme

# Extreme Conditions Analysis
def extreme_conditions(df: pd.DataFrame):

    logger.info("Analyzing conditions during extreme events")

    extreme = extract_extremes(df)

    summary = extreme[[
        "Wind_Speed_10m_kmh",
        "Humidity_Percent",
        "Temp_2m_C"
    ]].describe()

    return summary

# Extreme Event Distribution Analysis
def extreme_distribution(df: pd.DataFrame):

    logger.info("Analyzing extreme event distribution")

    extreme = extract_extremes(df)

    result = extreme.groupby(["City", "Season"]).size().reset_index(name="count")

    return result

# Extreme Probability Analysis
def extreme_probability(df: pd.DataFrame):

    logger.info("Computing probability of extreme events")

    grouped = df.groupby(["low_wind", "high_humidity", "Season"])

    prob = grouped["is_severe"].mean().reset_index()

    prob.rename(columns={"is_severe": "extreme_probability"}, inplace=True)

    return prob

# MasterFunction
def extreme_analysis(df: pd.DataFrame):

    logger.info("Starting extreme event analysis")

    outputs = {}

    outputs["conditions"] = extreme_conditions(df)
    outputs["distribution"] = extreme_distribution(df)
    outputs["probability"] = extreme_probability(df)

    for name, table in outputs.items():
        path = f"outputs/tables/{name}_extremes.csv"
        table.to_csv(path, index=False)
        logger.info(f"Saved: {path}")

    logger.info("Extreme analysis completed")

    return outputs