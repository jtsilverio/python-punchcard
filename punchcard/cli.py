from datetime import datetime
from typing import Annotated

import typer
from rich.box import ROUNDED
from rich.console import Console
from rich.table import Table
from rich.text import Text

from punchcard import cards
from punchcard.config import get_user_config, update_user_config
from punchcard.config.constants import DATE_FORMAT
from punchcard.exceptions import NotClockedOutError, PunchcardError
from punchcard.models import Punchcard
from punchcard.time import now

app = typer.Typer()


@app.command(name="in", short_help="Clock in a new punchcard")
def clockin():
    console = Console()
    try:
        cards.clockin()
        console.print("Successfully locked in", style="bold green")
    except NotClockedOutError as e:
        console.print(e, style="bold red")
        raise typer.Exit(1)


@app.command(name="out", short_help="Clock out the current punchcard")
def clockout():
    console = Console()
    try:
        card, _ = cards.clockout()
        console.print("Successfully clocked out", style="bold green")
        console.print(f"Duration: {card.duration()} hours", style="bold yellow")
        console.print(
            f"Balance: {card.balance()} hours",
            style=f"bold {'yellow' if card.balance() >= 0 else 'red'}",
        )
    except PunchcardError as e:
        console.print(e, style="bold red")
        raise typer.Exit(1)


@app.command(name="status", short_help="Get the current status")
def status():
    card = cards.get_punchcard(now()[0])
    console = Console()
    if card is None:
        console.print(
            "No punchcard found. You are not clocked in yet, use 'punchcard in' to clock in",
            style="bold yellow",
        )
        raise typer.Abort()

    entry = cards.get_last_entry(card)
    if entry.end_time is None:
        console.print("You are clocked in", style="bold magenta")
    else:
        console.print("You are clocked out", style="bold magenta")


@app.command(name="list", short_help="List punchcard duration and balance")
def list_punchcards():  # pylint: disable=redefined-builtin
    table = Table(show_header=True)
    table.add_column("ID", style="grey50")
    table.add_column("Date", style="cyan")
    table.add_column("Duration", style="bold yellow")
    table.add_column("Balance", style="bold yellow")

    for card in Punchcard.select().limit(30):  # pylint: disable=not-an-iterable
        table.add_row(
            str(card.id),
            card.date,
            f"{card.duration()}",
            f"{'[bold red]' if card.balance() < 0 else ''}{card.balance()}",
        )

    console = Console()
    console.print(table)


@app.command(name="entries", short_help="List punchcard's entries")
def list_entries(date: Annotated[str, typer.Argument()] = None):  # pylint: disable=redefined-builtin
    TABLE_SIZE = 40  # pylint: disable=invalid-name

    # List entries for a specific date
    table_entries = Table(show_header=True, width=TABLE_SIZE, box=ROUNDED)
    table_entries.add_column("ID", style="grey50")
    table_entries.add_column("Start", style="bold yellow")
    table_entries.add_column("End", style="bold yellow")

    if date is None:
        date_converted = now()[0]
    else:
        date_converted = datetime.strptime(date, DATE_FORMAT).date()

    card = cards.get_punchcard(date_converted)
    for entry in card.entries:
        table_entries.add_row(
            str(entry.id),
            entry.start_time,
            entry.end_time if entry.end_time is not None else "⏳",
        )

    summary = Text(
        f"Duration: {card.duration()} Balance: {card.balance()}",
    )

    # Container table
    table_container = Table(show_header=True, show_lines=True, box=ROUNDED)
    table_container.add_column(str(date_converted), justify="center")
    table_container.add_row(table_entries)
    table_container.add_row(summary)

    console = Console()
    console.print(table_container)


config_app = typer.Typer()
app.add_typer(config_app, name="config")


@config_app.command(name="list", short_help="Print configuration options")
def list_config():
    config = get_user_config()
    table = Table(show_header=True)
    table.add_column("Config", style="cyan")
    table.add_column("Value", style="cyan")

    for key, value in config.to_dict().items():
        table.add_row(key, str(value))

    console = Console()
    console.print(table)


@config_app.command(name="set", short_help="Print configuration options")
def set_config(config: str, value: int):
    update_user_config(config, value)


def main():
    app()


if __name__ == "__main__":
    main()
