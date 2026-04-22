from src.ingestion.loader import load_data
from src.preprocessing.validation import (
    validate_schema,
    validate_ranges,
    validate_duplicates,
)
from src.preprocessing.cleaning import clean_data
from src.preprocessing.feature_engineering import create_features
from src.analysis.profiling import run_profiling
from src.analysis.temporal import temporal_analysis
from src.analysis.interactions import interaction_analysis
from src.utils.helpers import EDA_STAGE_CHOICES, normalize_eda_stage
from src.analysis.events import event_analysis
from src.analysis.extremes import extreme_analysis
from src.analysis.synthesis import build_all_datasets

import logging

logger = logging.getLogger(__name__)


def run_eda(stage: str = "profiling"):
    stage = normalize_eda_stage(stage)
    if stage not in EDA_STAGE_CHOICES:
        raise ValueError(
            f"Unknown stage {stage!r}; expected one of {sorted(EDA_STAGE_CHOICES)}"
        )

    logger.info("Starting EDA pipeline (analysis stage=%s)", stage)
    logger.info(
        "Shared preprocessing always runs: load → validate → clean → feature engineering"
    )

    df = load_data()

    validate_schema(df)
    validate_ranges(df)
    validate_duplicates(df)

    df = clean_data(df)

    df = create_features(df)

    analysis_steps = []
    # Profiling
    if stage in ("profiling", "full"):
        analysis_steps.append("profiling")
        run_profiling(df)

    # Temporal
    if stage in ("temporal", "full"):
        analysis_steps.append("temporal")
        temporal_analysis(df)

    # Interactions
    if stage in ("interactions", "full"):
        analysis_steps.append("interactions")
        interaction_analysis(df)

    # Events + extremes (festival / crop burning + severe-event tables)
    if stage in ("events", "full"):
        analysis_steps.append("events")
        event_analysis(df)
        analysis_steps.append("extremes")
        extreme_analysis(df)

    # Build all datasets for Tableau
    if stage in ["full"]:
        build_all_datasets(df)

    # Visualizations (lazy import so matplotlib/seaborn are only required for this stage)
    if stage in ("visual", "full"):
        from src.analysis.visualization import run_visualizations

        analysis_steps.append("visual")
        run_visualizations(df)

    logger.info(
        "Analysis steps executed: %s",
        ", ".join(analysis_steps) if analysis_steps else "none",
    )
    logger.info("EDA pipeline completed")

    return df
