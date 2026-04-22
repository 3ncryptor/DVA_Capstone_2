import logging
import pandas as pd

logger = logging.getLogger(__name__)

# Baseline vs Event Analysis
def compute_baseline(df: pd.DataFrame) -> pd.DataFrame:
    """Add rolling baseline and event_delta to *df* in place (same object callers hold)."""
    logger.info("Computing rolling baseline")

    df.sort_values(["City", "Datetime"], inplace=True)

    df["baseline_pm25"] = df.groupby("City")["PM2_5_ugm3"].transform(
        lambda x: x.rolling(24).mean()
    )

    df["event_delta"] = df["PM2_5_ugm3"] - df["baseline_pm25"]

    return df

# Festival Impact Analysis
def festival_impact(df: pd.DataFrame):

    logger.info("Analyzing festival impact")

    result = df.groupby("is_festival").agg({
        "PM2_5_ugm3": "mean",
        "event_delta": "mean"
    }).reset_index()

    return result

# Crop Burning Impact Analysis
def crop_burning_impact(df: pd.DataFrame):

    logger.info("Analyzing crop burning impact")

    result = df.groupby(["Season", "is_crop_burning"]).agg({
        "PM2_5_ugm3": "mean",
        "event_delta": "mean"
    }).reset_index()

    return result

# Event Amplification Factor
def amplification_factor(df: pd.DataFrame):

    logger.info("Calculating event amplification factor")

    event = df[df["is_festival"] == True]["event_delta"].mean()
    non_event = df[df["is_festival"] == False]["event_delta"].mean()

    result = {
        "event_delta": event,
        "non_event_delta": non_event,
        "amplification": event - non_event
    }

    return pd.DataFrame([result])



# Event Frequency vs Severity Analysis
def event_severity(df: pd.DataFrame):

    logger.info("Analyzing severity during events")

    result = df.groupby("is_festival")["is_severe"].mean().reset_index()
    result.rename(columns={"is_severe": "severe_probability"}, inplace=True)

    return result

# MasterFunction
def event_analysis(df: pd.DataFrame):

    logger.info("Starting event analysis")

    df = compute_baseline(df)

    outputs = {}

    outputs["festival"] = festival_impact(df)
    outputs["crop"] = crop_burning_impact(df)
    outputs["amplification"] = amplification_factor(df)
    outputs["severity"] = event_severity(df)

    for name, table in outputs.items():
        path = f"outputs/tables/{name}_events.csv"
        table.to_csv(path, index=False)
        logger.info(f"Saved: {path}")

    logger.info("Event analysis completed")

    return outputs