import json
import logging
import os
from datetime import datetime, timezone
from typing import Any

from rich import box
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table

from src.analysis.forecasting import DEFAULT_HORIZONS, run_forecast
from src.preprocessing.cleaning import clean_data
from src.preprocessing.feature_engineering import create_features
from src.preprocessing.validation import (
    validate_duplicates,
    validate_ranges,
    validate_schema,
)
from src.utils.helpers import project_root
from src.utils.logger import get_rich_console

from .loader import load_city_data_for_forecast

logger = logging.getLogger(__name__)


def _write_result_artifact(payload: dict[str, Any]) -> str:
    out_dir = os.path.join(project_root(), "outputs", "prediction")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "last_run.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return path


def run_prediction(
    city: str,
    *,
    model_id: str = "rf_multih_rf",
    horizons: tuple[int, ...] | None = None,
    test_fraction: float = 0.2,
) -> dict[str, Any]:
    """
    Dedicated prediction path: no full-EDA (profiling, temporal, etc.).
    Expects :func:`src.utils.logger.setup_logger` to have been called (file + Rich).
    """
    console = get_rich_console()

    console.print()
    console.rule(
        "[bold bright_magenta]Predictive model · dedicated execution layer[/]",
        style="magenta",
    )
    sub = (
        f"[dim]Model[/]   [bold white]{model_id}[/]   [dim]·[/]   "
        f"[dim]City[/]  [bold cyan]{city}[/]   [dim]·[/]   "
        f"[dim]UTC[/]  [magenta]{datetime.now(timezone.utc).isoformat()}[/]"
    )
    console.print(
        Panel(
            sub,
            title="[bold]Prediction run[/]",
            border_style="bright_magenta",
            box=box.ROUNDED,
        )
    )
    console.print()

    hz = tuple(horizons) if horizons is not None else DEFAULT_HORIZONS
    result_summary: dict[str, Any] = {
        "layer": "prediction",
        "model_id": model_id,
        "city": city,
        "horizons": list(hz),
        "test_fraction": test_fraction,
        "started_utc": datetime.now(timezone.utc).isoformat(),
    }

    step_labels = [
        "1/5 [cyan]Load[/] raw (chunked, city filter)",
        "2/5 [yellow]Validate[/] schema + ranges + duplicates",
        "3/5 [green]Clean[/] data",
        "4/5 [blue]Feature[/] engineering",
        "5/5 [magenta]Train[/] multi-horizon models",
    ]

    with Progress(
        SpinnerColumn(style="magenta"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(
            complete_style="magenta",
            finished_style="bold bright_magenta",
        ),
        TextColumn("[bold]{task.fields[status]}[/]"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        ptask = progress.add_task(
            step_labels[0], total=len(step_labels), status="…"
        )
        df = load_city_data_for_forecast(city)
        progress.update(
            ptask, description=step_labels[1], advance=1, status="[green]ok[/]"
        )

        validate_schema(df)
        validate_ranges(df)
        validate_duplicates(df)
        progress.update(
            ptask, description=step_labels[2], advance=1, status="[green]ok[/]"
        )

        df = clean_data(df)
        progress.update(
            ptask, description=step_labels[3], advance=1, status="[green]ok[/]"
        )

        df = create_features(df)
        progress.update(
            ptask, description=step_labels[4], advance=1, status="[green]ok[/]"
        )

        out = run_forecast(
            df,
            city,
            horizons=hz,
            test_fraction=test_fraction,
        )
        progress.update(
            ptask, description=step_labels[4] + " [green]✓[/]", advance=1, status="[bold green]done[/]"
        )

    result_summary.update(
        {
            "finished_utc": datetime.now(timezone.utc).isoformat(),
            "split": "time_index (no label leakage: train targets before cut)",
            "model_dir": out.get("run_dir"),
            "manifest": out.get("manifest_path"),
            "metrics_by_horizon": {
                h: d.get("test_metrics", {})
                for h, d in out["horizons"].items()
                if isinstance(d, dict) and "test_metrics" in d
            },
            "features": out["features"],
        }
    )

    art_path = _write_result_artifact(result_summary)
    out_dir = os.path.relpath(os.path.dirname(art_path), project_root())

    table = Table(
        title="[bold]Test-set metrics[/] [dim](time holdout) · on-disk models[/]",
        box=box.ROUNDED,
        border_style="magenta",
        show_header=True,
        header_style="bold bright_magenta",
    )
    table.add_column("H", style="cyan", justify="right")
    table.add_column("n tr / te", style="white")
    table.add_column("R²", justify="right", style="green")
    table.add_column("MAE", justify="right")
    table.add_column("RMSE", justify="right")
    table.add_column("MAPE %", justify="right", style="dim")
    for hkey, block in out["horizons"].items():
        if not isinstance(block, dict) or "test_metrics" not in block:
            continue
        tm = block["test_metrics"]
        ntr, nte = block.get("n_train", 0), block.get("n_test", 0)
        r2c = "green" if tm["r2"] >= 0.4 else "yellow"
        table.add_row(
            f"{hkey}h",
            f"{ntr} / {nte}",
            f"[{r2c}]{tm['r2']:.4f}[/]",
            f"{tm['mae']:.2f}",
            f"{tm['rmse']:.2f}",
            f"{tm['mape']:.1f}",
        )
    table.add_row(
        "—",
        f"[dim]{out['run_dir']}/[/]",
        "",
        "",
        "",
        "[dim]artifact[/]",
    )
    table.add_row(
        "—",
        f"[dim]{out_dir}/last_run.json[/]",
        "",
        "",
        "",
        "[dim]summary[/]",
    )

    console.print()
    console.print(
        Panel(
            table,
            title="[bold white on magenta]  Final output  [/]",
            border_style="bright_magenta",
            box=box.HEAVY,
        )
    )
    console.print(
        "[dim]Extend: add new trainers under [bold cyan]src/prediction/[/] and call from [bold]run_prediction[/].[/]"
    )

    return result_summary
