# Testing

The project uses **pytest** under `tests/`. Tests use **synthetic DataFrames** so you do not need the full national CSV to run them locally or in CI.

## Philosophy

- **Fast:** dozens of rows per fixture; full suite completes in seconds.
- **Isolated:** analysis and forecasting tests redirect `project_root()` to a temporary directory so real `outputs/` is not written during tests.

## Fixtures ([tests/conftest.py](../tests/conftest.py))

| Fixture | Role |
| --- | --- |
| `sample_raw_df` | ~50 hourly rows, two cities (`Delhi`, `Mumbai`), columns required by validation, cleaning, and features |
| `sample_clean_df` | `sample_raw_df` after `clean_data` |
| `sample_featured_df` | After `create_features`, plus **`baseline_pm25`** and **`event_delta`** (rolling baseline and deviation). These mirror what `event_analysis` / Tableau synthesis expect so `build_all_datasets` can run without mutating unrelated pipelines |

## Output isolation

The `tmp_outputs` fixture monkeypatches:

- `src.utils.helpers.project_root`
- `src.analysis.forecasting.project_root`

`run_forecast` binds `project_root` at import time in `src.analysis.forecasting`, so patching only `helpers` is not enough for model paths. If you add new modules that do `from src.utils.helpers import project_root` and write under the repo root, patch that module’s `project_root` attribute in tests the same way.

## Commands

```bash
source .venv/bin/activate
python -m pytest tests -v --tb=short
python -m pytest tests/test_cleaning.py -v
python -m pytest tests -k smoke -v
```

## See also

- [CONTRIBUTING.md](../CONTRIBUTING.md) — setup and PR expectations
- [README.md](../README.md) — `setup.sh` runs pytest automatically
