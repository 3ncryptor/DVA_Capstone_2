import pandas as pd

from src.preprocessing.cleaning import clean_data


def test_clean_removes_duplicates(sample_raw_df):
    df = pd.concat([sample_raw_df, sample_raw_df.iloc[:5]], ignore_index=True)
    cleaned = clean_data(df)
    assert len(cleaned) <= len(sample_raw_df)


def test_clean_removes_negative_pm25(sample_raw_df):
    df = sample_raw_df.copy()
    df.loc[0, "PM2_5_ugm3"] = -99.0
    cleaned = clean_data(df)
    assert (cleaned["PM2_5_ugm3"] >= 0).all()


def test_clean_clips_humidity(sample_raw_df):
    df = sample_raw_df.copy()
    df.loc[0, "Humidity_Percent"] = 150.0
    cleaned = clean_data(df)
    assert cleaned["Humidity_Percent"].max() <= 100


def test_clean_fixes_negative_wind(sample_raw_df):
    df = sample_raw_df.copy()
    df.loc[0, "Wind_Speed_10m_kmh"] = -5.0
    cleaned = clean_data(df)
    assert (cleaned["Wind_Speed_10m_kmh"] >= 0).all()


def test_clean_sorts_by_city_datetime(sample_raw_df):
    cleaned = clean_data(sample_raw_df)
    cities = cleaned["City"].tolist()
    assert cities == sorted(cities)
