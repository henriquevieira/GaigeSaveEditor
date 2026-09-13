from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SteamInstallation:
    path: Path
    installation_type: str


def get_common_steam_paths(home: Path | None = None) -> list[SteamInstallation]:
    """
    Return common Steam installation paths on Linux.

    The paths are only candidates. Their existence and validity are checked
    separately by find_steam_installations().
    """
    home = home or Path.home()

    return [
        SteamInstallation(
            path=home / ".local/share/Steam",
            installation_type="native",
        ),
        SteamInstallation(
            path=home / ".steam/steam",
            installation_type="native",
        ),
        SteamInstallation(
            path=home / ".var/app/com.valvesoftware.Steam/.local/share/Steam",
            installation_type="flatpak",
        ),
    ]


def is_steam_installation(path: Path) -> bool:
    """
    Check whether a directory looks like a valid Steam installation.
    """
    if not path.is_dir():
        return False

    steamapps = path / "steamapps"

    return steamapps.is_dir()


def find_steam_installations(
    home: Path | None = None,
) -> list[SteamInstallation]:
    """
    Find all known Steam installations available for the current user.

    Duplicate installations are removed. This is important because paths such
    as ~/.steam/steam may be symbolic links to ~/.local/share/Steam.
    """
    installations: list[SteamInstallation] = []
    seen_paths: set[Path] = set()

    for candidate in get_common_steam_paths(home):
        if not is_steam_installation(candidate.path):
            continue

        resolved_path = candidate.path.resolve()

        if resolved_path in seen_paths:
            continue

        seen_paths.add(resolved_path)

        installations.append(
            SteamInstallation(
                path=resolved_path,
                installation_type=candidate.installation_type,
            )
        )

    return installations