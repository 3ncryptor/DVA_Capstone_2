import logging
import pandas as pd

logger = logging.getLogger(__name__)

# Wind X Season interaction
def wind_season_interaction(df: pd.DataFrame):

    logger.info("Analyzing Wind × Season interaction")

    result = df.groupby(["Season", "low_wind"])["PM2_5_ugm3"].mean().reset_index()

    return result

# Humidity X Season interaction
def humidity_season_interaction(df: pd.DataFrame):

    logger.info("Analyzing Humidity × Season interaction")

    result = df.groupby(["Season", "high_humidity"])["PM2_5_ugm3"].mean().reset_index()

    return result

# Wind X Humidity interaction
def wind_humidity_interaction(df: pd.DataFrame):

    logger.info("Analyzing Wind × Humidity interaction")

    result = df.groupby(
        ["low_wind", "high_humidity"]
    )["PM2_5_ugm3"].mean().reset_index()

    return result

# Event X Season interaction
def event_season_interaction(df: pd.DataFrame):

    logger.info("Analyzing Event × Season interaction")

    result = df.groupby(
        ["Season", "is_festival", "is_crop_burning"]
    )["PM2_5_ugm3"].mean().reset_index()

    return result

# Severe probability
def severe_probability(df: pd.DataFrame):

    logger.info("Computing conditional probability of severe pollution")

    grouped = df.groupby(["low_wind", "high_humidity", "Season"])

    prob = grouped["is_severe"].mean().reset_index()

    prob.rename(columns={"is_severe": "severe_probability"}, inplace=True)

    return prob

# Interaction strength
def interaction_strength(df: pd.DataFrame):

    logger.info("Evaluating interaction strength")

    overall_var = df["PM2_5_ugm3"].var()

    grouped_var = df.groupby(["low_wind", "high_humidity"])["PM2_5_ugm3"].var().mean()

    result = {
        "overall_variance": overall_var,
        "grouped_variance": grouped_var,
        "variance_reduction": overall_var - grouped_var
    }

    return pd.DataFrame([result])

# City-level interaction
def city_interaction(df: pd.DataFrame):

    logger.info("Analyzing city-level interaction effects")

    result = df.groupby(
        ["City", "low_wind"]
    )["PM2_5_ugm3"].mean().reset_index()

    return result



def interaction_analysis(df: pd.DataFrame):

    logger.info("Starting interaction analysis")

    outputs = {}

    outputs["wind_season"] = wind_season_interaction(df)
    outputs["humidity_season"] = humidity_season_interaction(df)
    outputs["wind_humidity"] = wind_humidity_interaction(df)
    outputs["event_season"] = event_season_interaction(df)
    outputs["severe_prob"] = severe_probability(df)
    outputs["strength"] = interaction_strength(df)
    outputs["city_interaction"] = city_interaction(df)

    # Save outputs
    for name, table in outputs.items():
        path = f"outputs/tables/{name}_interaction.csv"
        table.to_csv(path, index=False)
        logger.info(f"Saved: {path}")

    logger.info("Interaction analysis completed")

    return outputs