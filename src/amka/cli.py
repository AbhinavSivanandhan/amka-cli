import typer

from amka import __version__

app = typer.Typer(
    name="amka",
    help="Create and manage local alarms.",
    no_args_is_help=True,
    add_completion=False,
    pretty_exceptions_enable=False,
)


@app.callback()
def main() -> None:
    """Create and manage local alarms."""


@app.command()
def version() -> None:
    """Show the installed Amka version."""
    typer.echo(f"amka {__version__}")
