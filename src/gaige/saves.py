from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from gaige.libraries import find_steam_libraries
from gaige.steam import SteamInstallation

logger = logging.getLogger(__name__)

BORDERLANDS_2_APP_ID = "49520"

SAVE_RELATIVE_PATHS = (
    Path("Documents/My games/Borderlands 2/WillowGame/SaveData"),
    Path("My Documents/My games/Borderlands 2/WillowGame/SaveData"),
)


@dataclass(frozen=True)
class SaveDirectory:
    """
    A Borderlands 2 SaveData directory found inside a Proton prefix.
    """

    path: Path
    steam_library: Path
    proton_prefix: Path
    proton_user: str


@dataclass(frozen=True)
class SaveFile:
    """
    A Borderlands 2 character save file.
    """

    path: Path
    save_directory: SaveDirectory
    steam_id: str

    @property
    def filename(self) -> str:
        return self.path.name


def find_save_directories(
    installations: list[SteamInstallation],
    app_id: str = BORDERLANDS_2_APP_ID,
) -> list[SaveDirectory]:
    """
    Find every Borderlands 2 SaveData directory available through the
    supplied Steam installations.

    Multiple Steam installations, Steam libraries and Proton users are
    supported.
    """
    directories: list[SaveDirectory] = []
    seen_paths: set[Path] = set()

    for installation in installations:
        libraries = find_steam_libraries(installation)

        for library in libraries:
            if app_id not in library.apps:
                continue

            proton_prefix = (
                library.path
                / "steamapps"
                / "compatdata"
                / app_id
                / "pfx"
            )

            if not proton_prefix.is_dir():
                logger.debug(
                    "Proton prefix does not exist: %s",
                    proton_prefix,
                )
                continue

            users_directory = proton_prefix / "drive_c" / "users"

            if not users_directory.is_dir():
                logger.debug(
                    "Proton users directory does not exist: %s",
                    users_directory,
                )
                continue

            for user_directory in users_directory.iterdir():
                
                if not user_directory.is_dir():
                    continue

                for relative_path in SAVE_RELATIVE_PATHS:
                    
                    save_data = user_directory / relative_path

                    if not save_data.is_dir():
                        continue

                    resolved = save_data.resolve()

                    if resolved in seen_paths:
                        continue

                    seen_paths.add(resolved)

                    directories.append(
                        SaveDirectory(
                            path=resolved,
                            steam_library=library.path,
                            proton_prefix=proton_prefix,
                            proton_user=user_directory.name,
                        )
                    )

                    logger.debug(
                        "Borderlands 2 SaveData found: %s",
                        resolved,
                    )

    return directories


def find_save_files(
    directories: list[SaveDirectory],
) -> list[SaveFile]:
    """
    Find character save files inside all discovered SaveData directories.

    Borderlands 2 normally stores saves inside a directory named after the
    Steam account ID:

        SaveData/<SteamID>/Save0001.sav

    Multiple Steam IDs and multiple characters are supported.
    """
    saves: list[SaveFile] = []
    seen_paths: set[Path] = set()

    for save_directory in directories:
        for steam_id_directory in sorted(save_directory.path.iterdir(),key=lambda path: path.name,):
            
            if not steam_id_directory.is_dir():
                continue

            steam_id = steam_id_directory.name

            for save_path in sorted(
                steam_id_directory.glob("save*.sav")
            ):
                if not save_path.is_file():
                    continue

                resolved = save_path.resolve()

                if resolved in seen_paths:
                    continue

                seen_paths.add(resolved)

                saves.append(
                    SaveFile(
                        path=resolved,
                        save_directory=save_directory,
                        steam_id=steam_id,
                    )
                )

    return saves