import database
import typer

app = typer.Typer()


@app.command(name="in", short_help="Clock in for the day")
def clockin():
    typer.echo("Clocked in")


@app.command(name="out", short_help="Clock out for the day")
def clockout():
    typer.echo("Clocked out")


if __name__ == "__main__":
    app()
