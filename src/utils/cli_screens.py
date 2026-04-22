"""Reusable Rich layouts for the main CLI (EDA and prediction)."""

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


def print_welcome_subtitle(c: Console) -> None:
    t = Text()
    t.append("India AQI  ", style="bold cyan")
    t.append("·", style="dim")
    t.append("  DVA capstone  ", style="white")
    t.append("·", style="dim")
    t.append("  Rich CLI  ", style="bold magenta")
    c.print(t, justify="center")
    c.print()


def eda_start_banner(c: Console, stage: str) -> None:
    c.print()
    c.rule("[bold green] EDA & analysis pipeline [/]", style="green")
    body = (
        f"[dim]Mode[/]  exploratory analysis  (batch + outputs under [cyan]outputs/[/])\n"
        f"[dim]Stage[/]  [bold bright_yellow]{stage}[/]\n"
        f"[dim]Logs  [/]  [magenta]outputs/logs/app.log[/]  [dim]·[/]  console below is colorized"
    )
    c.print(
        Panel(
            body,
            title="[bold white] run [/]",
            border_style="green",
            box=box.ROUNDED,
        )
    )
    c.print()


def eda_done_banner(c: Console, stage: str) -> None:
    c.print()
    c.print(
        Panel(
            f"[green]Pipeline finished.[/] Stage [bold yellow]{stage}[/] [dim]— see app.log for the full line history.[/]",
            title="[white on green]  OK  [/]",
            border_style="green",
            box=box.HEAVY,
        )
    )
    c.print()


def eda_error_banner(c: Console, err: str) -> None:
    c.print()
    c.print(
        Panel(
            f"[red]{err}[/]\n[dim]Details were logged above.[/]",
            title="[white on red]  FAILED  [/]",
            border_style="red",
            box=box.HEAVY,
        )
    )
    c.print()
