# India AQI — exploratory analysis & forecasting

Capstone-style project for **exploratory data analysis (EDA)** on India air-quality data and a **separate prediction layer** that trains multi-horizon PM2.5 models per city. The entry point is a **Rich**-enhanced CLI: colorized logs, panels, and progress for a clear terminal experience.

Full design, problem framing, and architecture: **[docs/devDoc.md](docs/devDoc.md)**. Documentation index: **[docs/README.md](docs/README.md)**.

---

## What this project does

1. **EDA pipeline** (`--stage …`)  
   Loads the configured raw CSV, validates and cleans it, engineers features, then runs **only the analysis blocks you select** (or everything with `full`).

2. **Prediction pipeline** (`--predict`)  
   A **dedicated, faster path**: chunked read filtered by **city**, same validation/cleaning/features, then **multi-horizon** Random Forest regressors with a **time-based train/test split**, test metrics (MAE, RMSE, R², MAPE), and **saved models** under `outputs/prediction/models/`.

Paths for **data**, **logging**, and **EDA/prediction artifacts** resolve from the **repository root**, so you can run `python /path/to/repo/cli.py` from any working directory, or use [`scripts/run_eda.sh`](scripts/run_eda.sh) / [`scripts/run_predict.sh`](scripts/run_predict.sh) (they `cd` to the repo root first).

---

## Repository layout (high level)

| Path | Role |
| --- | --- |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Clone setup, pytest commands, links to architecture docs |
| [`setup.sh`](setup.sh) | Idempotent clone → venv → deps → import check → `compileall` → **pytest** → `cli.py --help` → optional prediction smoke (bash) |
| `cli.py` | Main CLI: EDA via `--stage`, prediction via `--predict` |
| `tests/` | **pytest** suite (synthetic data; no full CSV required); see [docs/testing.md](docs/testing.md) |
| `config/config.yaml` | `data.raw_path` to the national CSV; tune paths here |
| `config/logging.yaml` | File logging; Rich console is attached in code |
| `data/raw/` | Place the raw AQI CSV (default name set in `config.yaml`) |
| `DVA-focused-Portfolio/` | Portfolio narrative links (course deliverable; not used by code) |
| `DVA-oriented-Resume/` | Resume / CV materials (not used by code) |
| `docs/` | [Documentation hub](docs/README.md): design doc (`devDoc.md`), Tableau guide, testing, configuration |
| `notebooks/` | Jupyter: [`notebooks/pipeline.ipynb`](notebooks/pipeline.ipynb) — full narrated walkthrough of EDA + prediction pipelines |
| `reports/` | Human-written capstone reports (PDF/Markdown); pipeline does not write here |
| `scripts/` | Shell wrappers: `run_eda.sh`, `run_predict.sh` (invoke `cli.py` from repo root) |
| `tableau/` | [`dashboard_links.md`](tableau/dashboard_links.md) for published workbook URLs |
| `src/ingestion/` | Load + parse datetime |
| `src/preprocessing/` | Validation, cleaning, feature engineering |
| `src/analysis/` | Profiling, temporal, interactions, events, extremes, plots, Tableau-style exports, forecasting math |
| `src/prediction/` | City-filtered loader, training orchestration, Rich UI for predict |
| `src/pipelines/` | `run_eda` wires preprocessing to analysis stages |
| `outputs/tables/` | CSVs from EDA (profiling, temporal, etc.) |
| `outputs/plots/` | Figures when `--stage visual` or `full` |
| `outputs/tables/Tableau/` | Dashboard-style CSVs when stage is `full` |
| `outputs/logs/app.log` | Full plain-text log (in addition to Rich console) |
| `outputs/prediction/` | `last_run.json`, and `models/<City>/<run_id>/` with `.joblib` + `manifest.json` |

`outputs/` and `data/raw/*.csv` are **intended to be committed** so instructors can review data and artifacts. `reports/` is for narrative write-ups (PDF/Markdown) you add yourself. Very large files may require [Git LFS](https://git-lfs.com/) on GitHub.

---

## Requirements

- **Python 3.10+** (3.12+ recommended; the repo has been used with 3.14 in development).
- **Disk / memory**: the sample dataset is large (~800k+ hourly rows). Full EDA loads it into memory; prediction loads **only required columns** and **only the chosen city** in chunks, which is much lighter.
- A **64-bit** Python is assumed.

On macOS with **Homebrew Python**, the system may block global `pip install` (PEP 668). Use a **virtual environment** (see below).

---

## Installation

### Easiest: one script after clone (recommended for new contributors)

From the repository root (directory that contains `cli.py` and `setup.sh`):

```bash
cd /path/to/DVA_Capstone_2
chmod +x setup.sh    # once, if needed
./setup.sh
```

[`setup.sh`](setup.sh) is **idempotent**: it creates `.venv` if missing, installs/updates dependencies, checks imports, byte-compiles `src/` and `cli.py`, runs **`python -m pytest tests -v --tb=short`**, runs `cli.py --help`, and — if the CSV from `config/config.yaml` exists — runs a **short prediction smoke test**. Safe to run again after `git pull`. Requires **bash** (macOS, Linux, or **Git Bash** on Windows) and **Python 3.10+** as `python3` on your `PATH`.

### Manual install (same end state)

```bash
cd /path/to/DVA_Capstone_2

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
```

`requirements.txt` includes: `pandas`, `PyYAML`, `scikit-learn`, `joblib`, `matplotlib`, `seaborn`, `rich`, `pytest`, and `click` (kept for compatibility; the CLI is implemented with `argparse`).

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

From the project root (recommended):

```bash
source .venv/bin/activate
python cli.py --help
```

From any directory, you can use the repo’s scripts (they change to the repo root before invoking Python):

```bash
/path/to/DVA_Capstone_2/scripts/run_eda.sh --stage profiling
/path/to/DVA_Capstone_2/scripts/run_predict.sh --city Delhi
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
- **`outputs/tables/Tableau/*`** — `*_dashboard.csv` when `full`.
- **`outputs/plots/*`** — PNGs when `visual` or `full` runs.
- **`outputs/prediction/models/`** — `joblib` models + `manifest.json` per run.
- **`outputs/prediction/last_run.json`** — last prediction run summary.
- **`outputs/logs/app.log`** — full session log (no Rich markup, plain text with timestamps).

---

## Testing and verification

The repository includes a **pytest** suite under `tests/` using small synthetic DataFrames (no full national CSV needed). See [docs/testing.md](docs/testing.md) for fixtures and contributor notes.

1. **Automated tests (recommended after every change)**
   ```bash
   source .venv/bin/activate
   python -m pytest tests -v --tb=short
   ```
   Run one file: `python -m pytest tests/test_cleaning.py -v`. Filter tests: `python -m pytest tests -k smoke -v`.

2. **CLI help**
   ```bash
   python cli.py --help
   ```

3. **Byte-compile (quick sanity)**
   ```bash
   python -m compileall -q src cli.py
   ```

4. **Short EDA stage** (still reads full raw file unless you use a small sample in config)
   ```bash
   python cli.py --stage profiling
   ```

5. **Prediction (lighter than full EDA for one city)**
   ```bash
   python cli.py --predict --city Delhi
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
| `pytest` not found | Activate `.venv` and `pip install -r requirements.txt` (pytest is listed there) |

---

## License

This project is licensed under the **MIT License**; see [LICENSE](LICENSE).  
Replace the copyright name/year in that file if you publish under a different author or organization.

**Course / team attribution:** add your course name, team members, and institution here if your program requires it.

## Git and GitHub

- **Instructor review:** `data/raw/*.csv` and **`outputs/`** (tables, plots, logs, prediction models) are **not** listed in `.gitignore`, so you can commit them for grading. The raw folder still has [`.gitkeep`](data/raw/.gitkeep) when no CSV is present yet.  
- **Size limits:** GitHub warns above ~50 MB per file; use [Git LFS](https://git-lfs.com/) or a release attachment if the CSV or model artifacts exceed host limits.  
- The repo root includes **`LICENSE`** (GitHub detects it for the license badge).  
- Keep **API keys and secrets** out of the repo (use env vars or private config; `.env` is already gitignored).

---

## Summary

- **Install:** venv + `pip install -r requirements.txt` + place AQI data per `config/config.yaml` (or run [`./setup.sh`](setup.sh)).  
- **Test:** `python -m pytest tests -v` (see [docs/testing.md](docs/testing.md)).  
- **Analyze:** `python cli.py --stage <profiling|temporal|interactions|events|visual|full>`.  
- **Forecast:** `python cli.py --predict --city <Name> [--horizons ...] [--test-fraction ...]`.  
- **Monitor:** Rich terminal + `outputs/logs/app.log`; prediction artifacts under `outputs/prediction/`.
