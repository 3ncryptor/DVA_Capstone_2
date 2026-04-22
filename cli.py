import argparse
import logging
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.pipelines.eda_pipeline import run_eda
from src.utils.helpers import EDA_STAGE_CHOICES, normalize_eda_stage
from src.utils.logger import get_rich_console, setup_logger
from src.utils.cli_screens import (
    eda_done_banner,
    eda_error_banner,
    eda_start_banner,
    print_welcome_subtitle,
)

logger = logging.getLogger(__name__)


def _parse_horizons(s: str) -> tuple[int, ...]:
    if not s or not s.strip():
        from src.analysis.forecasting import DEFAULT_HORIZONS

        return DEFAULT_HORIZONS
    out: list[int] = []
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        h = int(part)
        if h < 1:
            raise argparse.ArgumentTypeError("horizon hours must be >= 1")
        out.append(h)
    if not out:
        raise argparse.ArgumentTypeError("no horizons parsed; use e.g. 1,6,12,24,48")
    return tuple(out)


def _parse_stage(value: str) -> str:
    s = normalize_eda_stage(value)
    if s not in EDA_STAGE_CHOICES:
        raise argparse.ArgumentTypeError(
            f"invalid choice {value!r} (use one of: {', '.join(sorted(EDA_STAGE_CHOICES))})"
        )
    return s


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Air quality project CLI: (1) EDA pipeline via --stage, or "
            "(2) the isolated prediction layer via --predict (no full EDA run). "
            "Log output is colorized in the terminal (Rich)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python cli.py --stage profiling\n"
            "  python cli.py --stage full\n"
            "  python cli.py --predict --city Delhi\n"
            "  python cli.py --predict --city Mumbai --horizons 12,24,48 --test-fraction 0.2\n"
        ),
    )
    parser.add_argument(
        "--predict",
        action="store_true",
        help="Run only the prediction execution layer (chunked load + train). Does not run profiling/temporal/etc.",
    )
    parser.add_argument(
        "--stage",
        type=_parse_stage,
        default="profiling",
        metavar="NAME",
        help=(
            "EDA analysis stage (ignored if --predict is set): "
            "profiling | temporal | interactions | events | visual | full."
        ),
    )
    parser.add_argument(
        "--city",
        type=str,
        default="Delhi",
        metavar="NAME",
        help="City to train on when using --predict (default: Delhi).",
    )
    parser.add_argument(
        "--horizons",
        type=_parse_horizons,
        default=None,
        metavar="H1,H2,...",
        help=(
            "Comma-separated forecast horizons in hours, e.g. 1,6,12,24,48. "
            "Default: 1,6,12,24,48 (hourly index steps; requires hourly data)."
        ),
    )
    parser.add_argument(
        "--test-fraction",
        type=float,
        default=0.2,
        metavar="F",
        help="Fraction of time-ordered rows held out for test metrics (default: 0.2).",
    )
    args = parser.parse_args()
    console = get_rich_console()

    if args.predict:
        setup_logger()
        print_welcome_subtitle(console)
        from src.prediction.pipeline import run_prediction

        run_prediction(
            args.city,
            model_id="rf_multih_rf",
            horizons=args.horizons,
            test_fraction=args.test_fraction,
        )
        return

    setup_logger()
    print_welcome_subtitle(console)
    stage = args.stage
    eda_start_banner(console, stage)

    try:
        run_eda(stage)
    except Exception:
        logger.exception("Pipeline failed during EDA run")
        eda_error_banner(
            console,
            "The EDA run failed. A traceback was printed to the [bold]log[/] above.",
        )
        return

    eda_done_banner(console, stage)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
