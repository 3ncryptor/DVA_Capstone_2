import json
import logging
import os
import re
import time
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import joblib

from src.utils.helpers import project_root

logger = logging.getLogger(__name__)

FEATURES = [
    "pm25_lag_1",
    "pm25_lag_24",
    "pm25_lag_168",
    "pm25_roll_24",
    "Wind_Speed_10m_kmh",
    "Humidity_Percent",
    "Temp_2m_C",
]

# Horizons in hours = steps (hourly series)
DEFAULT_HORIZONS = (1, 6, 12, 24, 48)


def _target_col(h: int) -> str:
    return f"target_{h}h"


def _sanitize(name: str) -> str:
    s = re.sub(r"[^\w\-.]+", "_", name.strip(), flags=re.UNICODE)
    return s or "model"


def _mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    denom = np.maximum(np.abs(y_true), 1e-3)
    return float(np.mean(np.abs((y_true - y_pred) / denom)) * 100.0)


def _regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    mae = float(mean_absolute_error(y_true, y_pred))
    mse = float(mean_squared_error(y_true, y_pred))
    rmse = float(np.sqrt(mse))
    r2 = float(r2_score(y_true, y_pred))
    return {"mae": mae, "rmse": rmse, "mse": mse, "r2": r2, "mape": _mape(y_true, y_pred)}


def _add_targets(sub: pd.DataFrame, horizons: tuple[int, ...]) -> pd.DataFrame:
    for h in horizons:
        sub[_target_col(h)] = sub["PM2_5_ugm3"].shift(-h)
    return sub


def _time_index_split_masks(
    n: int,
    idx: np.ndarray,
    h: int,
    cut: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    idx: 0..n-1 positions. cut: first test position (0..n).
    Train row i if i < cut - h (target index i+h stays in [0, cut) — no test-label leak).
    Test row i if i >= cut and i + h < n.
    """
    m_train = (idx < cut - h) & (idx < n)
    m_test = (idx >= cut) & (idx + h < n)
    return m_train, m_test


def run_forecast(
    df: pd.DataFrame,
    city: str,
    *,
    horizons: tuple[int, ...] = DEFAULT_HORIZONS,
    test_fraction: float = 0.2,
) -> dict[str, Any]:
    """
    Per-horizon RandomForest with time-ordered index split, test metrics, saved models.
    """
    sub = df[df["City"] == city].copy()
    if sub.empty:
        raise ValueError(f"No rows for city: {city!r}")

    sub = sub.sort_values("Datetime").reset_index(drop=True)
    n = len(sub)
    sub = _add_targets(sub, horizons)

    if test_fraction <= 0 or test_fraction >= 0.5:
        raise ValueError("test_fraction should be in (0, 0.5)")

    max_h = max(horizons)
    if n <= max_h + 10:
        raise ValueError(
            f"Time series too short (n={n}) for max horizon {max_h}h; need more history."
        )

    cut = int(n * (1.0 - test_fraction))
    cut = max(1, min(n - 1, cut))
    # Ensure index cut - h is positive for the largest h (train rows 0..cut-h-1)
    cut = max(cut, max_h + 1)
    if cut >= n:
        cut = n - 1
    if cut - max_h < 1:
        raise ValueError("Cannot time-split: not enough pre-test rows; lower horizons or test_fraction.")

    idx = np.arange(n, dtype=int)

    out_dir = os.path.join(
        project_root(), "outputs", "prediction", "models", _sanitize(city)
    )
    run_id = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    run_path = os.path.join(out_dir, run_id)
    os.makedirs(run_path, exist_ok=True)

    per_horizon: dict[str, Any] = {}
    all_models: dict[int, Any] = {}

    for h in sorted(horizons):
        tcol = _target_col(h)
        complete = sub[FEATURES + [tcol]].notna().all(axis=1).to_numpy()
        m_train, m_test = _time_index_split_masks(n, idx, h, cut)
        m_train = m_train & complete
        m_test = m_test & complete

        n_train = int(m_train.sum())
        n_test = int(m_test.sum())
        if n_train < 30:
            logger.warning("Horizon %sh: few train rows (%s)", h, n_train)
        if n_test < 5:
            logger.warning("Horizon %sh: few test rows (%s)", h, n_test)

        if n_train < 5 or n_test < 1:
            logger.error("Horizon %sh: skipping (insufficient data after split)", h)
            per_horizon[str(h)] = {
                "horizon_hours": h,
                "status": "skipped",
                "reason": "insufficient_rows_after_time_split",
            }
            continue

        X_tr = sub.loc[m_train, FEATURES]
        y_tr = sub.loc[m_train, tcol]
        X_te = sub.loc[m_test, FEATURES]
        y_te = sub.loc[m_test, tcol]

        model = RandomForestRegressor(
            n_estimators=100, random_state=42, n_jobs=-1
        )
        model.fit(X_tr, y_tr)
        y_pred = model.predict(X_te)
        train_metrics = _regression_metrics(
            y_tr.to_numpy(), model.predict(X_tr)
        )
        test_metrics = _regression_metrics(y_te.to_numpy(), y_pred)

        all_models[h] = model
        fname = f"rf_h{h}h.joblib"
        fpath = os.path.join(run_path, fname)
        joblib.dump(
            {
                "model": model,
                "horizon_hours": h,
                "feature_names": list(FEATURES),
                "city": city,
            },
            fpath,
        )

        per_horizon[str(h)] = {
            "horizon_hours": h,
            "n_train": n_train,
            "n_test": n_test,
            "train_metrics": train_metrics,
            "test_metrics": test_metrics,
            "model_path": os.path.relpath(fpath, project_root()),
        }

        logger.info(
            "Horizon %sh | train %s / test %s | test R²=%.4f | test MAE=%.3f | test RMSE=%.3f",
            h,
            n_train,
            n_test,
            test_metrics["r2"],
            test_metrics["mae"],
            test_metrics["rmse"],
        )

    manifest: dict[str, Any] = {
        "city": city,
        "run_id": run_id,
        "horizons": [h for h in sorted(horizons)],
        "split": {
            "method": "time_index",
            "test_fraction": test_fraction,
            "n_rows_city": n,
            "cut_index": int(cut),
        },
        "features": list(FEATURES),
        "per_horizon": per_horizon,
    }
    mpath = os.path.join(run_path, "manifest.json")
    with open(mpath, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    total_train = sum(
        v.get("n_train", 0) for v in per_horizon.values() if isinstance(v, dict)
    )
    return {
        "city": city,
        "horizons": per_horizon,
        "run_dir": os.path.relpath(run_path, project_root()),
        "manifest_path": os.path.relpath(mpath, project_root()),
        "models": all_models,
        "features": list(FEATURES),
        "n_rows_city": n,
        "n_train_reported": total_train,
    }
