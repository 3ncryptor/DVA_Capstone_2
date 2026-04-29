import os

from src.analysis.events import event_analysis
from src.analysis.extremes import extreme_analysis
from src.analysis.interactions import interaction_analysis
from src.analysis.profiling import run_profiling
from src.analysis.synthesis import build_all_datasets
from src.analysis.temporal import temporal_analysis


def test_profiling_returns_7_tables(sample_featured_df, tmp_outputs):
    result = run_profiling(sample_featured_df)
    assert len(result) == 7


def test_profiling_writes_csvs(sample_featured_df, tmp_outputs):
    run_profiling(sample_featured_df)
    tables_dir = os.path.join(str(tmp_outputs), "outputs", "tables")
    csv_files = [f for f in os.listdir(tables_dir) if f.endswith("_profiling.csv")]
    assert len(csv_files) == 7


def test_temporal_returns_6_tables(sample_featured_df, tmp_outputs):
    result = temporal_analysis(sample_featured_df)
    assert len(result) == 6


def test_interaction_returns_7_tables(sample_featured_df, tmp_outputs):
    result = interaction_analysis(sample_featured_df)
    assert len(result) == 7


def test_event_returns_4_tables(sample_featured_df, tmp_outputs):
    result = event_analysis(sample_featured_df)
    assert len(result) == 4


def test_extreme_returns_3_tables(sample_featured_df, tmp_outputs):
    result = extreme_analysis(sample_featured_df)
    assert len(result) == 3


def test_synthesis_returns_6_dashboards(sample_featured_df, tmp_outputs):
    result = build_all_datasets(sample_featured_df)
    assert len(result) == 6
