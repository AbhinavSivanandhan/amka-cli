from datetime import datetime

import typer

from amka import __version__
from amka.errors import InvalidScheduleError
from amka.notifier import notify_terminal
from amka.scheduler import wait_until
from amka.timeparse import parse_duration, resolve_local_time

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


@app.command("set")
def set_alarm(
    in_: str | None = typer.Option(None, "--in", help="Relative duration, such as 5s or 1h30m."),
    at: str | None = typer.Option(None, "--at", help="Local time, such as 07:30."),
    label: str | None = typer.Option(None, "--label"),
) -> None:
    """Set a foreground alarm."""
    try:
        if label is not None and len(label) > 200:
            raise InvalidScheduleError("Label must not exceed 200 characters.")
        now = datetime.now().astimezone()
        if in_ is None and at is None:
            raise InvalidScheduleError("Provide exactly one of --in or --at.")
        if in_ is not None and at is not None:
            raise InvalidScheduleError("Use only one of --in or --at.")

        if in_ is not None:
            duration = parse_duration(in_)
            scheduled_for = now + duration
            source = f"in {in_}"
        else:
            if at is None:
                raise InvalidScheduleError("Provide exactly one of --in or --at.")
            scheduled_for = resolve_local_time(at, now=now)
            source = f"at {at}"

        timezone = scheduled_for.tzname() or scheduled_for.strftime("%z")
        typer.echo(f"Alarm scheduled for {scheduled_for:%Y-%m-%d %H:%M:%S} {timezone} ({source}).")
        if label is not None:
            typer.echo(f"Label: {label}")
        wait_until(scheduled_for)
        notify_terminal(label)
    except InvalidScheduleError as error:
        typer.echo(f"Error: {error}", err=True)
        raise typer.Exit(1) from error
    except KeyboardInterrupt:
        typer.echo("Alarm cancelled.")
        raise typer.Exit(130) from None
