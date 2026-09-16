import typer

from rich.console import Console
from rich.table import Table

from gaige import __version__
from gaige.logging_config import configure_logging
from gaige.saves import (
    find_save_directories,
    find_save_files,
)
from gaige.steam import find_steam_installations

app = typer.Typer(
    name="gaige",
    help="GaigeSaveEditor - Borderlands 2 save editor.",
)
console = Console()

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
    """
    List all detected Borderlands 2 save files.
    """
    installations = find_steam_installations()

    if not installations:
        console.print(
            "[yellow]No Steam installations found.[/yellow]"
        )
        raise typer.Exit(code=1)

    save_directories = find_save_directories(
        installations
    )

    if not save_directories:
        console.print(
            "[yellow]No Borderlands 2 save directories found.[/yellow]"
        )
        raise typer.Exit(code=1)

    saves = find_save_files(save_directories)

    if not saves:
        console.print(
            "[yellow]No Borderlands 2 save files found.[/yellow]"
        )
        raise typer.Exit(code=1)

    table = Table(
        title="Borderlands 2 Save Files"
    )

    table.add_column(
        "ID",
        justify="right",
        style="cyan",
        no_wrap=True,
    )

    table.add_column(
        "Steam ID",
        style="magenta",
        no_wrap=True,
    )

    table.add_column(
        "File",
        style="green",
        no_wrap=True,
    )

    table.add_column(
        "Path",
    )

    for save_id, save in enumerate(
        saves,
        start=1,
    ):
        table.add_row(
            str(save_id),
            save.steam_id,
            save.filename,
            str(save.path),
        )

    console.print(table)


@app.command("steam")
def show_steam_installations() -> None:
    """List detected Steam installations."""

    installations = find_steam_installations()

    if not installations:
        typer.echo("No Steam installations found.")
        raise typer.Exit(code=1)

    for installation in installations:
        typer.echo(
            f"[{installation.installation_type}] "
            f"{installation.path}"
        )