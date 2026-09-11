import typer

from gaige import __version__
from gaige.logging_config import configure_logging

app = typer.Typer(
    name="gaige",
    help="GaigeSaveEditor - Borderlands 2 save editor.",
)


@app.callback()
def main(
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose logging.",
    ),
) -> None:
    configure_logging(verbose)


@app.command()
def version() -> None:
    """Show GaigeSaveEditor version."""
    typer.echo(f"GaigeSaveEditor {__version__}")


@app.command("list")
def list_saves() -> None:
    """List Borderlands 2 save files."""
    typer.echo("Save discovery is not implemented yet.")