from datetime import datetime

import typer

from punchcard import database
from punchcard.models import Punchcard

app = typer.Typer()


@app.command(name="in", short_help="Clock in for the day")
def clockin():
    card = Punchcard(start=datetime.now())
    database.clockin(card)


@app.command(name="out", short_help="Clock out for the day")
def clockout():
    typer.echo("Clocked out")


if __name__ == "__main__":
    app()
