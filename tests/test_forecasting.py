import os

import numpy as np
import pandas as pd
import pytest

from src.analysis.forecasting import run_forecast


@pytest.fixture
def forecast_df():
    """100-row single-city DataFrame with all features needed for forecasting."""
    n = 100
    rng = np.random.default_rng(99)
    return pd.DataFrame(
        {
            "Datetime": pd.date_range("2024-01-01", periods=n, freq="h"),
            "City": "Delhi",
            "PM2_5_ugm3": rng.uniform(20, 200, n),
            "pm25_lag_1": rng.uniform(20, 200, n),
            "pm25_lag_24": rng.uniform(20, 200, n),
            "pm25_lag_168": rng.uniform(20, 200, n),
            "pm25_roll_24": rng.uniform(20, 200, n),
            "Wind_Speed_10m_kmh": rng.uniform(1, 25, n),
            "Humidity_Percent": rng.uniform(30, 80, n),
            "Temp_2m_C": rng.uniform(15, 35, n),
        }
    )


def test_run_forecast_produces_metrics(forecast_df, tmp_outputs):
    result = run_forecast(forecast_df, "Delhi", horizons=(1,), test_fraction=0.3)
    assert "1" in result["horizons"]
    assert "r2" in result["horizons"]["1"]["test_metrics"]


def test_run_forecast_saves_joblib(forecast_df, tmp_outputs):
    result = run_forecast(forecast_df, "Delhi", horizons=(1,), test_fraction=0.3)
    model_rel = result["horizons"]["1"]["model_path"]
    model_path = tmp_outputs / model_rel
    assert model_path.is_file()


def test_run_forecast_empty_city_raises(forecast_df, tmp_outputs):
    with pytest.raises(ValueError, match="No rows for city"):
        run_forecast(forecast_df, "Kolkata", horizons=(1,), test_fraction=0.3)
