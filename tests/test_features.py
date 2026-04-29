from src.preprocessing.feature_engineering import create_features


def test_create_features_adds_expected_columns(sample_clean_df):
    df = create_features(sample_clean_df.copy())

    expected = [
        "year",
        "month",
        "hour",
        "pm25_lag_1",
        "pm25_roll_24",
        "pm25_category",
        "is_severe",
        "low_wind",
        "high_humidity",
        "is_festival",
        "is_crop_burning",
    ]
    for col in expected:
        assert col in df.columns, f"Missing column: {col}"


def test_severity_categories_correct(sample_clean_df):
    df = sample_clean_df.copy()
    df.loc[df.index[0], "PM2_5_ugm3"] = 20.0
    df.loc[df.index[1], "PM2_5_ugm3"] = 300.0

    df = create_features(df)

    assert df.loc[df.index[0], "pm25_category"] == "Good"
    assert df.loc[df.index[1], "pm25_category"] == "Severe"


def test_is_severe_flag(sample_clean_df):
    df = sample_clean_df.copy()
    df.loc[df.index[0], "PM2_5_ugm3"] = 100.0
    df.loc[df.index[1], "PM2_5_ugm3"] = 300.0

    df = create_features(df)

    assert df.loc[df.index[0], "is_severe"] is False or not df.loc[df.index[0], "is_severe"]
    assert df.loc[df.index[1], "is_severe"]
