# Configuration

## `config/config.yaml`

Keys present in the default file:

| Key | Example | Read by code? |
| --- | --- | --- |
| `data.raw_path` | `data/raw/…csv` | **Yes** — [src/ingestion/loader.py](../src/ingestion/loader.py) (EDA full load) and [src/prediction/loader.py](../src/prediction/loader.py) (chunked city load for `--predict`) |
| `logging.log_file` | `outputs/logs/app.log` | **No** — reserved for documentation / future use; the active log path comes from `config/logging.yaml` (see below) |
| `analysis.default_stage` | `profiling` | **No** — the CLI default stage is set in [cli.py](../cli.py) (`argparse` default). Keep this key for team convention or future wiring |

Paths under `data.raw_path` may be absolute or relative to the **repository root** (`project_root()`).

## `config/logging.yaml`

- Defines the **file** handler (path, formatter, level).
- [src/utils/logger.py](../src/utils/logger.py) loads this file with `logging.config.dictConfig`, resolves relative `filename` under the repo root, ensures the log directory exists, then attaches a **Rich** stream handler on stdout (not defined in YAML).

## Prediction CSV columns

`--predict` reads only the columns listed in **`FORECAST_USECOLS`** in [src/prediction/loader.py](../src/prediction/loader.py). If your raw CSV headers differ, update that tuple (and any downstream code that assumes those names) so chunked reads stay aligned with the file.

## Related docs

- [README.md](../README.md) — quick config bullets
- [devDoc.md](devDoc.md) — architecture and outputs
