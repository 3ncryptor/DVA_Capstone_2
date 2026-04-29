# Contributing

## Prerequisites

- **Python 3.10+** on your `PATH` as `python3` (the setup script probes several versioned names).
- **Bash** for [`setup.sh`](setup.sh) (macOS, Linux, or Git Bash on Windows).

## First-time setup

From the repository root (directory containing `cli.py` and `setup.sh`):

```bash
chmod +x setup.sh   # once, if needed
./setup.sh
```

This creates `.venv` if missing, installs dependencies from `requirements.txt`, runs import checks, byte-compiles sources, runs **pytest**, runs `cli.py --help`, and optionally runs a short prediction smoke test if the CSV configured in `config/config.yaml` is present.

Activate the environment in new terminals:

```bash
source .venv/bin/activate
```

## Running tests

Match what CI or `./setup.sh` does:

```bash
python -m pytest tests -v --tb=short
```

See [docs/testing.md](docs/testing.md) for fixtures, temporary output paths, and examples (single file, `-k` filter).

## Code layout

The EDA path is: load → validate → clean → features → gated analysis stages. The prediction path uses a chunked city load, then the same preprocess steps, then `run_forecast`. Full detail, stage names, and design rationale are in [docs/devDoc.md](docs/devDoc.md).

## Pull requests

- Run the test suite before opening or updating a PR.
- Keep changes scoped to one concern when possible.
- Update user-facing docs ([README.md](README.md) or under [docs/](docs/)) when behavior, flags, or defaults change.
