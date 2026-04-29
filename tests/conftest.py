import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def sample_raw_df():
    """~50-row synthetic DataFrame with the columns used by the pipeline."""
    n = 50
    rng = np.random.default_rng(42)
    dates = pd.date_range("2024-01-01", periods=n, freq="h")
    cities = ["Delhi"] * 25 + ["Mumbai"] * 25
    return pd.DataFrame(
        {
            "Datetime": list(dates),
            "City": cities,
            "PM2_5_ugm3": rng.uniform(5, 300, n),
            "Humidity_Percent": rng.uniform(20, 90, n),
            "Wind_Speed_10m_kmh": rng.uniform(0, 30, n),
            "Temp_2m_C": rng.uniform(10, 40, n),
            "Season": rng.choice(
                ["Winter", "Summer", "Monsoon", "Post-Monsoon"], n
            ),
            "Festival_Period": rng.choice([0, 1], n),
            "Crop_Burning_Season": rng.choice([0, 1], n),
            "Latitude": [28.6] * 25 + [19.0] * 25,
            "Longitude": [77.2] * 25 + [72.8] * 25,
        }
    )


@pytest.fixture
def sample_clean_df(sample_raw_df):
    """sample_raw_df after cleaning."""
    from src.preprocessing.cleaning import clean_data

    return clean_data(sample_raw_df)


@pytest.fixture
def sample_featured_df(sample_clean_df):
    """sample_clean_df after feature engineering + baseline columns needed by synthesis."""
    from src.preprocessing.feature_engineering import create_features

    df = create_features(sample_clean_df.copy())
    df["baseline_pm25"] = df.groupby("City")["PM2_5_ugm3"].transform(
        lambda x: x.rolling(24, min_periods=1).mean()
    )
    df["event_delta"] = df["PM2_5_ugm3"] - df["baseline_pm25"]
    return df


@pytest.fixture
def tmp_outputs(tmp_path, monkeypatch):
    """Redirect project_root() to a temp directory so tests never touch real outputs/."""
    _root = lambda: str(tmp_path)  # noqa: E731
    monkeypatch.setattr("src.utils.helpers.project_root", _root)
    monkeypatch.setattr("src.analysis.forecasting.project_root", _root)
    return tmp_path
