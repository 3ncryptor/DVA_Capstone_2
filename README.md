# India AQI — exploratory analysis & forecasting

Capstone-style project for **exploratory data analysis (EDA)** on India air-quality data and a **separate prediction layer** that trains multi-horizon PM2.5 models per city. The entry point is a **Rich**-enhanced CLI: colorized logs, panels, and progress for a clear terminal experience.

---

## What this project does

1. **EDA pipeline** (`--stage …`)  
   Loads the configured raw CSV, validates and cleans it, engineers features, then runs **only the analysis blocks you select** (or everything with `full`).

2. **Prediction pipeline** (`--predict`)  
   A **dedicated, faster path**: chunked read filtered by **city**, same validation/cleaning/features, then **multi-horizon** Random Forest regressors with a **time-based train/test split**, test metrics (MAE, RMSE, R², MAPE), and **saved models** under `outputs/prediction/models/`.

Path resolution uses the **repository root** (not the shell’s current working directory), so you can run `python cli.py` from another directory if you pass the full path to `cli.py`.

---

## Repository layout (high level)

| Path | Role |
| --- | --- |
| `cli.py` | Main CLI: EDA via `--stage`, prediction via `--predict` |
| `config/config.yaml` | `data.raw_path` to the national CSV; tune paths here |
| `config/logging.yaml` | File logging; Rich console is attached in code |
| `data/raw/` | Place the raw AQI CSV (default name set in `config.yaml`) |
| `src/ingestion/` | Load + parse datetime |
| `src/preprocessing/` | Validation, cleaning, feature engineering |
| `src/analysis/` | Profiling, temporal, interactions, events, extremes, plots, Tableau-style exports, forecasting math |
| `src/prediction/` | City-filtered loader, training orchestration, Rich UI for predict |
| `src/pipelines/` | `run_eda` wires preprocessing to analysis stages |
| `outputs/tables/` | CSVs from EDA (profiling, temporal, etc.) |
| `outputs/plots/` | Figures when `--stage visual` or `full` |
| `outputs/Tables/Tableau/` | Dashboard-style CSVs when stage is `full` |
| `outputs/logs/app.log` | Full plain-text log (in addition to Rich console) |
| `outputs/prediction/` | `last_run.json`, and `models/<City>/<run_id>/` with `.joblib` + `manifest.json` |

---

## Requirements

- **Python 3.10+** (3.12+ recommended; the repo has been used with 3.14 in development).
- **Disk / memory**: the sample dataset is large (~800k+ hourly rows). Full EDA loads it into memory; prediction loads **only required columns** and **only the chosen city** in chunks, which is much lighter.
- A **64-bit** Python is assumed.

On macOS with **Homebrew Python**, the system may block global `pip install` (PEP 668). Use a **virtual environment** (see below).

---

## Installation

From the project root (the directory that contains `cli.py` and `config/`):

```bash
cd /path/to/DVA_Capstone_2

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
```

`requirements.txt` includes: `pandas`, `PyYAML`, `scikit-learn`, `joblib`, `matplotlib`, `seaborn`, `rich`, and `click` (kept for compatibility; the CLI is implemented with `argparse`).

---

## Data

1. Place your **India AQI** CSV (hourly, with expected columns used by the pipeline) under the path in `config/config.yaml`, e.g.:

   ```yaml
   data:
     raw_path: data/raw/INDIA_AQI_COMPLETE_20251126.csv
   ```

2. Required columns (at minimum) for preprocessing and features include, among others: `Datetime`, `City`, `PM2_5_ugm3`, `Humidity_Percent`, `Wind_Speed_10m_kmh`, and columns used in feature engineering and events (e.g. `Temp_2m_C`, `Festival_Period`, `Crop_Burning_Season`, `Season` as present in your file).

3. The **prediction** layer uses a **fixed list of columns** in `src/prediction/loader.py` for chunked I/O; if your file schema differs, update that list to match the CSV header.

---

## Configuration

- **`config/config.yaml`** — `data.raw_path` (absolute or relative to repo root).
- **`config/logging.yaml`** — file handler for `outputs/logs/app.log` (format includes time, level, logger name, message). The **Rich** console handler is added programmatically in `src/utils/logger.py`.

---

## Running the application

Always run from the project root (recommended):

```bash
source .venv/bin/activate
python cli.py --help
```

### EDA / analysis (`--stage`)

**Every** run loads data and runs: **ingestion → schema/range/duplicate validation → cleaning → feature engineering**. After that, **only the analysis steps matching `--stage`** run.

| Stage | What runs after preprocessing |
| --- | --- |
| `profiling` | Distributions, missingness, tail stats, etc. |
| `temporal` | Daily/monthly, diurnal, seasonal, lag, volatility |
| `interactions` | Wind/season, humidity, events, city-level effects |
| `events` | Festival / crop burning style event analysis + extremes module |
| `visual` | Matplotlib/Seaborn figures under `outputs/plots/` |
| `full` | All of the above **plus** Tableau-style dashboard CSVs and visualization |

**Aliases:** `interaction` → `interactions`.

**Examples**

```bash
# Default is profiling
python cli.py
python cli.py --stage profiling

# One analysis family
python cli.py --stage temporal

# Entire EDA + dashboard exports + plots (long run on full data)
python cli.py --stage full
```

Logs appear in the **terminal** (Rich) and in **`outputs/logs/app.log`**. Success and error **panels** are printed at the end of EDA runs.

### Prediction (`--predict`)

**Does not** run the full EDA profiling/temporal/… stack. It trains **per-horizon** models for PM2.5 (hours-ahead = row shifts on hourly data).

| Option | Default | Description |
| --- | --- | --- |
| `--city` | `Delhi` | City name as it appears in the `City` column |
| `--horizons` | `1,6,12,24,48` | Comma-separated hours (integer steps) |
| `--test-fraction` | `0.2` | Last fraction of the **time-ordered** index held out for **test** metrics |

**Examples**

```bash
python cli.py --predict --city Delhi
python cli.py --predict --city Mumbai --horizons 12,24,48
python cli.py --predict --city Delhi --horizons 1,6,12,24,48,72 --test-fraction 0.15
```

**Outputs:** metrics table in the console, `outputs/prediction/last_run.json`, and under `outputs/prediction/models/<City>/<timestamp>/` file(s) `rf_h{N}h.joblib` plus `manifest.json`.

**Loading a saved bundle in Python**

```python
import joblib
b = joblib.load("outputs/prediction/models/Delhi/<run_id>/rf_h24h.joblib")
model = b["model"]
feature_names = b["feature_names"]
# Build X with columns in the same order as feature_names
```

---

## Outputs reference

- **`outputs/tables/*`** — analysis-specific CSVs (suffixes like `_profiling`, `_temporal`, `_interaction`, `_events`, `_extremes`).
- **`outputs/Tables/Tableau/*`** — `*_dashboard.csv` when `full` (paths as logged).
- **`outputs/plots/*`** — PNGs when `visual` or `full` runs.
- **`outputs/prediction/models/`** — `joblib` models + `manifest.json` per run.
- **`outputs/prediction/last_run.json`** — last prediction run summary.
- **`outputs/logs/app.log`** — full session log (no Rich markup, plain text with timestamps).

---

## Testing and verification

There is no heavy automated test suite checked in. Recommended checks:

1. **CLI help**
   ```bash
   python cli.py --help
   ```

2. **Byte-compile (quick sanity)**
   ```bash
   python -m compileall -q src cli.py
   ```

3. **Short EDA stage** (still reads full raw file unless you use a small sample in config)
   ```bash
   python cli.py --stage profiling
   ```

4. **Prediction (lighter than full EDA for one city)**
   ```bash
   python cli.py --predict --city Delhi
   ```

5. **Optional:** add tests under `tests/` and run:
   ```bash
   python -m unittest discover -s tests -v
   ```

6. If imports fail, confirm the **venv is activated** and `pip install -r requirements.txt` completed without errors.

---

## Troubleshooting

| Issue | Suggestion |
| --- | --- |
| `No module named 'pandas'` / `sklearn` / `rich` | Activate `.venv` and `pip install -r requirements.txt` |
| `externally-managed-environment` (pip) | Use a venv; do not install into the system Python on macOS/Homebrew |
| `File not found` for raw CSV | Check `config/config.yaml` and that the file exists under the repo (or use an absolute `raw_path`) |
| `No rows for city` in `--predict` | Spelling of `--city` must match the `City` column in the data |
| Out of memory on `full` | Use a single `--stage` first, or sample the CSV; prediction is cheaper than loading all cities into one frame for training |
| Colors disabled | Some CI or `NO_COLOR=1` environments limit styling; Rich respects common conventions |

---

## License

This project is licensed under the **MIT License**; see [LICENSE.md](LICENSE.md).  
Replace the copyright name/year in that file if you publish under a different author or organization.

**Course / team attribution:** add your course name, team members, and institution here if your program requires it.

## Git and GitHub

- **Do not commit** large raw AQI files (`data/raw/*.csv` is gitignored) or generated **`outputs/`** (tables, logs, plots, models). An empty [`data/raw/.gitkeep`](data/raw/.gitkeep) keeps the `data/raw` folder in the repo.  
- **Optional:** add a `LICENSE` copy at the repo root (GitHub can detect `LICENSE` or `LICENSE.md` for the license badge).  
- **Before `git push`:** run `git status` and confirm no huge `.csv` or `outputs/prediction/models` paths are tracked. Use [Git LFS](https://git-lfs.com/) only if you intentionally need large binaries in the remote.  
- Keep **API keys and secrets** out of the repo (use env vars or private config; `.env` is already gitignored).

---

## Summary

- **Install:** venv + `pip install -r requirements.txt` + place AQI data per `config/config.yaml`.  
- **Analyze:** `python cli.py --stage <profiling|temporal|interactions|events|visual|full>`.  
- **Forecast:** `python cli.py --predict --city <Name> [--horizons ...] [--test-fraction ...]`.  
- **Monitor:** Rich terminal + `outputs/logs/app.log`; prediction artifacts under `outputs/prediction/`.
