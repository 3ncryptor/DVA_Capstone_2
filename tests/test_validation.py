import pytest

from src.preprocessing.validation import (
    validate_duplicates,
    validate_ranges,
    validate_schema,
)


def test_validate_schema_passes(sample_raw_df):
    validate_schema(sample_raw_df)


def test_validate_schema_missing_col_raises(sample_raw_df):
    df = sample_raw_df.drop(columns=["PM2_5_ugm3"])
    with pytest.raises(ValueError):
        validate_schema(df)


def test_validate_ranges_counts_issues(sample_raw_df):
    df = sample_raw_df.copy()
    df.loc[0, "PM2_5_ugm3"] = -10.0
    issues = validate_ranges(df)
    assert issues["negative_pm25"] >= 1


def test_validate_duplicates_counts(sample_raw_df):
    import pandas as pd

    df = pd.concat([sample_raw_df, sample_raw_df.iloc[:3]], ignore_index=True)
    count = validate_duplicates(df)
    assert count >= 3
