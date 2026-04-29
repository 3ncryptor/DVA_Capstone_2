#!/usr/bin/env bash
# Idempotent first-time setup after `git clone`.
# Usage (from repository root):  chmod +x setup.sh && ./setup.sh
# Requires: bash 3.2+, Python 3.10+ on PATH as python3 (macOS/Linux/Git Bash on Windows).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

info() { printf '\033[0;32m[setup]\033[0m %s\n' "$*"; }
warn() { printf '\033[0;33m[setup]\033[0m %s\n' "$*"; }
err()  { printf '\033[0;31m[setup]\033[0m %s\n' "$*" >&2; }

info "Repository root: ${ROOT}"

# --- Pick a Python >= 3.10 ---
PY=""
for cand in python3.14 python3.13 python3.12 python3.11 python3.10 python3; do
  if command -v "$cand" >/dev/null 2>&1; then
    if "$cand" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
      PY="$cand"
      break
    fi
  fi
done

if [[ -z "${PY}" ]]; then
  err "No Python 3.10+ found. Install Python from https://www.python.org/downloads/ or use your OS package manager, then run this script again."
  exit 1
fi

info "Using interpreter: $(${PY} -c 'import sys; print(sys.executable)') ($(${PY} -c 'import sys; print("%d.%d.%d" % sys.version_info[:3])'))"

# --- Virtual environment (create if missing; never deleted) ---
if [[ ! -d "${ROOT}/.venv" ]]; then
  info "Creating virtual environment in .venv ..."
  "${PY}" -m venv "${ROOT}/.venv"
else
  info "Virtual environment .venv already exists (reusing)."
fi

# shellcheck source=/dev/null
source "${ROOT}/.venv/bin/activate"

info "Upgrading pip ..."
python -m pip install --upgrade pip

info "Installing project dependencies (idempotent) ..."
pip install -r "${ROOT}/requirements.txt"

info "Checking imports (pandas, sklearn, rich, yaml) ..."
python -c "import pandas, sklearn, rich, yaml; print('OK')"

info "Byte-compiling sources ..."
python -m compileall -q "${ROOT}/src" "${ROOT}/cli.py"

info "Running test suite ..."
python -m pytest "${ROOT}/tests" -v --tb=short

info "CLI smoke: --help ..."
python "${ROOT}/cli.py" --help >/dev/null

# --- Optional: end-to-end smoke if dataset is present ---
export SETUP_REPO_ROOT="${ROOT}"
if python - <<'PY'
import os
import sys
from pathlib import Path

import yaml

root = Path(os.environ["SETUP_REPO_ROOT"])
cfg_path = root / "config" / "config.yaml"
cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
rel = cfg["data"]["raw_path"]
path = Path(rel)
if not path.is_absolute():
    path = root / path
sys.exit(0 if path.is_file() else 1)
PY
then
  info "Dataset found at configured raw_path — running quick prediction test (Delhi, 1h horizon, ~10–60s depending on machine) ..."
  python "${ROOT}/cli.py" --predict --city Delhi --horizons 1 --test-fraction 0.3
  info "Smoke prediction finished. Check outputs/prediction/ under the repo."
else
  warn "No CSV at data.raw_path in config/config.yaml — skipped training smoke test."
  warn "After you add the file, run:  source .venv/bin/activate && python cli.py --predict --city Delhi --horizons 1"
fi

info "Done. Next steps:"
printf '  %s\n' "  source .venv/bin/activate   # each new terminal"
printf '  %s\n' "  python cli.py --stage profiling"
printf '  %s\n' "  python cli.py --predict --city Delhi"
printf '\n%s\n' "Re-run ./setup.sh anytime after pulling — it is safe to repeat."
