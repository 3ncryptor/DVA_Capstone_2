import logging
import pandas as pd

logger = logging.getLogger(__name__)

def build_overview(df):

    logger.info("Building overview dataset")

    summary = df.groupby("City").agg({
        "PM2_5_ugm3": ["mean", "max"],
        "is_severe": "mean",
        "Latitude": "first",
        "Longitude": "first"
    })

    summary.columns = ["avg_pm25", "max_pm25", "severe_pct", "lat", "lon"]

    return summary.reset_index()


def build_temporal(df):

    logger.info("Building temporal dataset")

    df["date"] = df["Datetime"].dt.date

    daily = df.groupby(["City", "date", "Season"]).agg({
        "PM2_5_ugm3": "mean",
        "pm25_roll_24": "mean"
    }).reset_index()

    daily.rename(columns={
        "PM2_5_ugm3": "pm25_avg",
        "pm25_roll_24": "rolling_pm25"
    }, inplace=True)

    return daily


def build_city_comparison(df):

    logger.info("Building city comparison dataset")

    stats = df.groupby("City").agg({
        "PM2_5_ugm3": ["mean", "median", "std"],
        "is_severe": "mean"
    })

    stats.columns = ["mean", "median", "std", "severe_pct"]

    stats["cv"] = stats["std"] / stats["mean"]

    return stats.reset_index()


def build_interactions(df):

    logger.info("Building interaction dataset")

    result = df.groupby(["Season", "low_wind", "high_humidity"]).agg({
        "PM2_5_ugm3": "mean",
        "is_severe": "mean"
    }).reset_index()

    result.rename(columns={
        "PM2_5_ugm3": "pm25_avg",
        "is_severe": "severe_probability"
    }, inplace=True)

    return result


def build_events(df):

    logger.info("Building event dataset")

    df["event_type"] = df.apply(
        lambda x: "Festival" if x["is_festival"] else (
            "Crop Burning" if x["is_crop_burning"] else "None"
        ),
        axis=1
    )

    result = df.groupby(["event_type", "Season"]).agg({
        "PM2_5_ugm3": "mean",
        "event_delta": "mean",
        "is_severe": "mean"
    }).reset_index()

    result.rename(columns={
        "PM2_5_ugm3": "pm25_avg",
        "is_severe": "severe_probability"
    }, inplace=True)

    return result



def build_extremes(df):

    logger.info("Building extreme dataset")

    extreme = df[df["is_severe"]]

    result = extreme.groupby(["City", "Season"]).size().reset_index(name="extreme_count")

    total = df.groupby(["City", "Season"]).size().reset_index(name="total_count")

    merged = result.merge(total, on=["City", "Season"])

    merged["extreme_probability"] = merged["extreme_count"] / merged["total_count"]

    return merged



def build_all_datasets(df):

    logger.info("Building all Tableau datasets")

    outputs = {
        "overview": build_overview(df),
        "temporal": build_temporal(df),
        "city": build_city_comparison(df),
        "interaction": build_interactions(df),
        "events": build_events(df),
        "extremes": build_extremes(df)
    }

    for name, table in outputs.items():
        path = f"outputs/Tables/Tableau/{name}_dashboard.csv"
        table.to_csv(path, index=False)
        logger.info(f"Saved: {path}")

    logger.info("All datasets ready for Tableau")

    return outputs