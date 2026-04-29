# Notebooks

Optional Jupyter exploration. The canonical pipeline runs from the repo root:

```bash
python cli.py --stage profiling
```

- **[`pipeline.ipynb`](pipeline.ipynb)** — **Full pipeline walkthrough for instructors:** narrated cells follow the same order as `src/pipelines/eda_pipeline.py` (ingestion → validation → cleaning → features → each analysis module) and documents the separate **prediction** path (`src/prediction/pipeline.py`). Set **`EDA_STAGE`** to the same values as `cli.py --stage` (`profiling` … `full`). In Part II, set **`RUN_PREDICTION = True`** when you want to train (optional; uses the prediction loader path). Install Jupyter: `pip install notebook` or `pip install jupyterlab`; start Jupyter with cwd = repo root or `notebooks/`.

Data path for notebooks: `../data/raw/<your_csv>.csv` (see `config/config.yaml` for the configured filename).

For automated checks after changing code, see [docs/testing.md](../docs/testing.md) or [CONTRIBUTING.md](../CONTRIBUTING.md).
