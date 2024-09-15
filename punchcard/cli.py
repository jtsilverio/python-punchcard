import typer
from rich.console import Console
from rich.table import Table

from punchcard import cards
from punchcard.config import get_user_config, set_user_config, update_config
from punchcard.exceptions import PunchcardError
from punchcard.models import Punchcard

app = typer.Typer()
config_app = typer.Typer()
app.add_typer(config_app, name="config")


@app.command(name="in", short_help="Clock in a new punchcard")
def clockin():
    date, start_time = cards.now()
    card = Punchcard(date=date, start=start_time)

    console = Console()
    try:
        cards.clockin(card)
        console.print("Clocked in", style="bold green")
    except PunchcardError as e:
        console.print(e, style="bold red")
        raise typer.Exit(1)


@app.command(name="out", short_help="Clock out the current punchcard")
def clockout():
    card = cards.get_last_punchcard()
    console = Console()
    if card is None:
        console.print("There is no clocked in card open.", style="bold red")
        raise typer.Exit(1)

    try:
        cards.clockout(card)
        console.print("Clocked out", style="bold green")
        console.print(f"Duration: {card.duration()} hours", style="bold green")
    except PunchcardError as e:
        console.print(e, style="bold red")
        raise typer.Exit(1)


@app.command(name="status", short_help="Get the current status")
def status():
    card = cards.get_last_punchcard()
    console = Console()
    if card is None:
        console.print("No punchcard found", style="bold yellow")
        raise typer.Abort()

    if card.end is None:
        console.print("You are clocked in", style="bold magenta")
    else:
        console.print("You are clocked out", style="bold magenta")


@app.command(name="list", short_help="List all punchcards")
def list_punchcards():  # pylint: disable=redefined-builtin
    table = Table(show_header=True)
    table.add_column("ID", style="grey50")
    table.add_column("Date", style="cyan")
    table.add_column("Start", style="cyan")
    table.add_column("End", style="cyan")
    table.add_column("Duration", style="bold yellow")

    card_date = None
    for card in Punchcard.select().limit(10):  # pylint: disable=not-an-iterable
        if card_date is None:
            card_date = card.date

        if card.date != card_date:
            card_date = card.date
            table.add_row()

        duration = "⏳"
        end_date = card.end if card.end is not None else "-"
        if card.end is not None:
            duration = f"{card.duration()} hours"

        table.add_row(str(card.id), card_date, card.start, end_date, duration)

    console = Console()
    console.print(table)


@app.command(name="report", short_help="Report balance")
def report(show: int = 31):
    table = Table(show_header=True)
    table.add_column("Date", style="cyan")
    table.add_column("Duration")
    table.add_column("Balance")

    for date, duration, balance in report_list:
        table.add_row(str(date), str(duration), str(balance))

    console = Console()
    console.print(table)


@config_app.command(name="list", short_help="Print configuration options")
def list_config():
    config = get_user_config()
    table = Table(show_header=True)
    table.add_column("Config", style="cyan")
    table.add_column("Value", style="cyan")

    for key, value in config.items():
        table.add_row(key, str(value))

    console = Console()
    console.print(table)


@config_app.command(name="set", short_help="Print configuration options")
def set_config(config: str, value: int):
    update_config(config, value)


def main():
    app()


if __name__ == "__main__":
    main()
