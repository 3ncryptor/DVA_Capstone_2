# Air quality analysis system — production design document

This document describes the **analytical goals** and the **as-built architecture** of the repository. For install and run commands, see the main [README.md](../README.md).

---

## 1. Project overview

### Objective

To perform **deep, structured exploratory data analysis (EDA)** on Indian air quality data (2022–2025) to uncover:

* Temporal patterns
* Spatial inequalities and **city-level heterogeneity** (via profiling and cross-sectional summaries, not a separate `spatial.py` module in the current tree)
* Meteorological dependencies
* Event-driven pollution amplification
* Extreme pollution dynamics

The codebase adds a second objective:

* **Short-horizon PM2.5 forecasting** for a **single city at a time**, with proper **time-ordered train/test evaluation**, test metrics, and **persisted models** (isolated from the full EDA run).

### Core philosophy

This project is **not**:

* Random plotting
* Descriptive statistics dumping
* A single monolithic “run everything every time” script without staging

This project **is**:

> A **layered analytical system** (EDA + optional **prediction layer**) designed to uncover hidden structure in environmental data and to support **reproducible, modular** runs from the CLI.

### Two execution layers (current implementation)

| Layer | Entry | Role |
| --- | --- | --- |
| **EDA and analysis** | `python cli.py --stage <name>` | National (or full-file) load, shared preprocessing, then **selected** analysis blocks (`profiling` … `full`) |
| **Prediction** | `python cli.py --predict --city <City>` | Chunked read **for one city** only, same preprocessing and features as EDA, then **multi-horizon** Random Forest training, metrics, and **on-disk** artifacts under `outputs/prediction/` |

Path resolution is anchored to the **repository root** (`project_root()` in `src/utils/helpers.py`), not the shell’s current working directory.

---

## 2. Problem statements (final scope)

### P1 — Temporal pollution dynamics

* Multi-scale patterns (hourly, seasonal, yearly)
* Trend vs seasonality vs noise

### P2 — Distribution and tail risk

* Skewness and extreme events
* Mean vs median divergence
* Tail dominance

### P3 — City archetypes (behavioral clustering)

* Not ranking; grouping
* Stability vs volatility patterns (addressed in profiling and synthesis, not a dedicated clustering pipeline in v1)

### P4 — Meteorological interactions

* Non-linear dependencies: wind and season, humidity and related flags
* Conditional effects (see `src/analysis/interactions.py`)

### P5 — Event amplification (not just impact)

* Crop burning, festivals, amplification vs baseline (`src/analysis/events.py`)

### P6 — Extreme event mechanisms

* Conditions for severe pollution, conditional probabilities (`src/analysis/extremes.py`)

### P7 — Data reliability and bias

* AQI vs PM2.5 mismatch (where both exist in the data)
* Missingness patterns (`profiling` missingness output)

### P8 — Short-horizon PM2.5 predictability (operational add-on)

* For a fixed city, how well do lags, rolling PM2.5, and key weather fields predict **future** PM2.5 at 1, 6, 12, 24, 48 (and user-defined) **hour** horizons, under a **time-based holdout** (`src/analysis/forecasting.py`, `src/prediction/`)

---

## 3. System architecture (as built)

### Repository layout

```text
<repo root>/
  cli.py
  README.md
  requirements.txt
  LICENSE.md
  docs/
    devDoc.md
  config/
    config.yaml          # e.g. data.raw_path, analysis.default_stage
    logging.yaml         # file handler; Rich console added in code
  data/
    raw/                 # user-supplied CSV; large files gitignored, .gitkeep keeps folder
  src/
    ingestion/
      loader.py          # full-file load for EDA; paths via config
    preprocessing/
      cleaning.py
      feature_engineering.py
      validation.py
    analysis/
      profiling.py
      temporal.py
      interactions.py
      events.py
      extremes.py
      visualization.py   # matplotlib / seaborn figures (stages: visual, full)
      synthesis.py        # Tableau-style dashboard tables (full)
      forecasting.py     # time split, per-horizon RF, metrics, joblib, manifest
    pipelines/
      eda_pipeline.py    # run_eda: preprocess + gated analysis stages
    prediction/
      __init__.py
      loader.py          # chunked read + usecols + city filter
      pipeline.py        # predict orchestration, Rich progress and panels
    utils/
      helpers.py         # project_root, EDA stage registry
      logger.py          # file + RichHandler on stdout
      cli_screens.py     # EDA welcome / start / success / error panels
  outputs/
    tables/              # analysis CSVs (suffixes _profiling, _temporal, etc.)
    plots/                # from visualization
    logs/
      app.log
    Tables/Tableau/       # *_dashboard.csv when --stage full
    prediction/
      last_run.json
      models/<City>/<run_id>/
        manifest.json
        rf_h{N}h.joblib
```

**Note:** There is **no** `src/analysis/spatial.py` in the current tree. **City- and location-related** structure is covered via profiling (e.g. per-city tables), interaction outputs, and **synthesis** dashboard extracts.

---

## 4. Configuration

### Purpose

* Avoid hardcoding paths where possible
* Support reproducible runs (same config + same data file)

### Files

* **`config/config.yaml`** — at minimum `data.raw_path` (relative to repo root or absolute). Optional keys such as `analysis.default_stage` may appear.
* **`config/logging.yaml`** — `outputs/logs/app.log` and formatters. **Colored** terminal output is attached in **`src/utils/logger.py`** via **Rich** (`RichHandler`), not from YAML alone.

### Example shape (illustrative)

```yaml
data:
  raw_path: data/raw/INDIA_AQI_COMPLETE_20251126.csv

logging:
  log_file: outputs/logs/app.log

analysis:
  default_stage: profiling
```

---

## 5. Analytical framework (layered EDA model)

The following layers map to **code modules** and **CLI stages**; not every layer is a separate `--stage` (see section 7).

### Layer 1 — Data profiling and validation

**Modules:** `validation.py`, `profiling.py`  
**Goal:** Data integrity and distribution awareness.  
**Output:** `outputs/tables/*_profiling.csv` (when profiling runs)

### Layer 2 — Temporal decomposition

**Module:** `temporal.py`  
**Stage:** `temporal` or `full`  
**Output:** e.g. `daily_temporal.csv`, `seasonal_temporal.csv`, `lag_temporal.csv`, etc.

### Layer 3 — City heterogeneity and cross-sectional structure

**Modules:** `profiling.py` (city distributions), `synthesis.py` (aggregated dashboard tables for Tableau)  
**Insight:** Cities follow different **regimes**; avoid naive ranking without context.

### Layer 4 — Interaction analysis

**Module:** `interactions.py`  
**Stage:** `interactions` or `full`  
**Output:** `*_interaction.csv` under `outputs/tables/`

### Layer 5 — Event and extreme analysis

**Modules:** `events.py`, `extremes.py`  
**Stage:** `events` (both modules) or `full`  
**Output:** `*_events.csv`, `*_extremes.csv`

### Layer 6 — Presentation and handoff

**Modules:** `visualization.py`, `synthesis.py`  
**Stages:** `visual` (plots) and `full` (adds **Tableau**-oriented `*_dashboard.csv` under `outputs/Tables/Tableau/` and visualization)

### Layer 7 — Forecasting (prediction execution layer, not an EDA `--stage`)

**Modules:** `forecasting.py`, `prediction/loader.py`, `prediction/pipeline.py`  
**Entry:** `python cli.py --predict`  
**Behavior:**

* **Chunked** read with a **fixed column set** and **one city** (reduces I/O vs full EDA on the national file).
* Same **validation, cleaning, feature engineering** as EDA for that slice.
* **Multi-horizon** targets (default: 1, 6, 12, 24, 48 hours, hourly index).
* **Time-based** train/test split (index-based, avoiding label leakage for each horizon *h*).
* **Test metrics** per horizon: MAE, RMSE, MSE, R², MAPE; optional train metrics for reference.
* **Artifacts:** `joblib` bundles per horizon, `manifest.json`, and `last_run.json`.

**CLI options (prediction):** `--city`, optional `--horizons` (comma-separated hours), optional `--test-fraction`.

---

## 6. Hidden analytical angles (what many analyses still miss)

### Insight 1 — Mean is misleading

* PM2.5 is often heavily skewed; median and percentiles matter.

### Insight 2 — Pollution has memory

* Lags and rolling windows are first-class in **feature engineering** and in **forecasting** features.

### Insight 3 — Events are multipliers

* Framed in `events.py` and related interaction outputs.

### Insight 4 — Weather effects are conditional

* Framed in `interactions.py` and extreme-condition summaries.

### Insight 5 — Cities are not directly comparable

* Use regime thinking and per-city or grouped tables, not a single national rank without context.

### Insight 6 — Extreme events drive risk

* `extremes.py` and tail-focused profiling.

### Insight 7 — Holdout must respect time

* **Forecasting** uses time-ordered split and per-horizon test rows; in-sample R² alone is not the reporting target for generalization.

---

## 7. Pipeline design (implementation)

### EDA path (`run_eda` in `src/pipelines/eda_pipeline.py`)

For **every** run:

1. `load_data()` (full file as configured)
2. `validate_schema` / `validate_ranges` / `validate_duplicates`
3. `clean_data`
4. `create_features`

Then, **gated by `--stage`:**

* `profiling` / `full` → `run_profiling`
* `temporal` / `full` → `temporal_analysis`
* `interactions` / `full` → `interaction_analysis`
* `events` / `full` → `event_analysis` and `extreme_analysis`
* `full` only → `build_all_datasets` (synthesis)
* `visual` / `full` → `run_visualizations`

**Registered EDA stage names** (see `src/utils/helpers.py`, `EDA_STAGE_CHOICES`):  
`profiling`, `temporal`, `interactions`, `events`, `visual`, `full`.

### Prediction path (`run_prediction` in `src/prediction/pipeline.py`)

1. `load_city_data_for_forecast(city)` (chunked, filtered, limited columns)
2. Same three validation functions as EDA
3. `clean_data` → `create_features`
4. `run_forecast` in `forecasting.py` (per horizon: fit, test metrics, save `joblib`, write manifest)
5. Rich **progress** and **result table**; summary JSON at `outputs/prediction/last_run.json`

**Does not** run profiling, temporal plots, or synthesis unless the user also runs an EDA stage.

```text
EDA:
  raw load -> validate -> clean -> features -> (selected analysis + optional viz + optional synthesis)

Prediction:
  chunked city load -> validate -> clean -> features -> multi-horizon fit + time-split metrics + save models
```

---

## 8. CLI interface

### EDA and analysis

```bash
python cli.py --stage profiling
python cli.py --stage full
```

**Stages:** `profiling` | `temporal` | `interactions` | `events` | `visual` | `full`  
**Alias:** `interaction` → `interactions` (normalization in `helpers.py`).

**UX:** `src/utils/cli_screens.py` (banners) and `src/utils/logger.py` (Rich log stream). Plain file log: `outputs/logs/app.log`.

### Prediction

```bash
python cli.py --predict --city Delhi
python cli.py --predict --city Mumbai --horizons 12,24,48 --test-fraction 0.2
```

### Help

```bash
python cli.py --help
```

---

## 9. Outputs (where artifacts land)

| Area | Location | Typical contents |
| --- | --- | --- |
| EDA tables | `outputs/tables/` | `*_profiling.csv`, `*_temporal.csv`, `*_interaction.csv`, `*_events.csv`, `*_extremes.csv` |
| Plots | `outputs/plots/` | PNGs from `visualization.py` when `visual` or `full` |
| Dashboards | `outputs/Tables/Tableau/` | `*_dashboard.csv` when `full` (paths as logged) |
| Logs | `outputs/logs/app.log` | Full session log (text) |
| Prediction | `outputs/prediction/` | `last_run.json`; `models/<City>/<timestamp>/manifest.json` and `rf_h*h.joblib` |

**Git / GitHub:** Large raw CSVs and generated `outputs/` are **gitignored** in this repo; see [README.md](../README.md) and `.gitignore`.

---

## 10. Final analytical narrative (EDA)

If the EDA stack is used as intended, a defensible high-level message is still:

> Air pollution in India is a structured, state-dependent phenomenon driven by seasonal cycles, amplified by meteorological stagnation, and intensified by episodic events, with extreme events contributing disproportionately to overall risk.

### Final critical note

Shallow one-liners (“winter is worse”, “one city is bad”) are **not** the design target. Prefer mechanisms, defensible patterns, and honest limits of the data.

### Forecasting note

Short-horizon model metrics are **per horizon and per city**; they depend on the train/holdout split, label construction (shifted targets), and feature set. They support **operational follow-up** (calibration, more features, or other estimators), not a claim of universal national forecasting without further validation.

---

## 11. Roadmap and maintenance (post–v1)

The core pipeline, CLI, EDA stages, **synthesis**, **visualization**, and **prediction** path are in place. Reasonable next steps (project-specific) include:

* Adding or tuning **`spatial` analysis** (new module) if gridded or geo fields become first-class
* **External validation** of forecast models (other cities, other years, regime shifts)
* **Tests** under `tests/` and CI
* **Config-driven** forecast horizons and model IDs without code edits
* Tighter integration between **synthesis** outputs and a **Tableau** workbook path documented for stakeholders

For commands and file-level detail, the **source of truth** remains [README.md](../README.md) and the code under `src/`.
