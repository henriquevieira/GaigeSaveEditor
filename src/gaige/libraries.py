from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path

from gaige.steam import SteamInstallation

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SteamLibrary:
    path: Path
    apps: frozenset[str]


_QUOTED_VALUE_RE = re.compile(r'^\s*"([^"]+)"\s+"([^"]*)"\s*$')


def find_steam_libraries(
    installation: SteamInstallation,
) -> list[SteamLibrary]:
    """
    Find all Steam libraries registered in libraryfolders.vdf.

    Each returned SteamLibrary contains:
    - the absolute path of the library;
    - the AppIDs registered under its ``apps`` section.

    Duplicate library paths are ignored.
    Invalid or inaccessible libraries are skipped.
    """
    steam_root = installation.path
    library_file = steam_root / "steamapps" / "libraryfolders.vdf"

    logger.debug("Reading Steam library file: %s", library_file)

    if not library_file.is_file():
        logger.warning(
            "Steam library configuration not found: %s",
            library_file,
        )
        return []

    try:
        content = library_file.read_text(
            encoding="utf-8",
            errors="replace",
        )
    except OSError as exc:
        logger.error(
            "Could not read Steam library configuration %s: %s",
            library_file,
            exc,
        )
        return []

    libraries = _parse_libraryfolders(content)

    valid_libraries: list[SteamLibrary] = []
    seen_paths: set[Path] = set()

    for library in libraries:
        path = library.path.expanduser()

        try:
            resolved_path = path.resolve()
        except OSError:
            logger.warning(
                "Could not resolve Steam library path: %s",
                path,
            )
            continue

        if resolved_path in seen_paths:
            logger.debug(
                "Ignoring duplicate Steam library: %s",
                resolved_path,
            )
            continue

        steamapps_path = resolved_path / "steamapps"

        if not steamapps_path.is_dir():
            logger.warning(
                "Ignoring invalid Steam library without steamapps/: %s",
                resolved_path,
            )
            continue

        seen_paths.add(resolved_path)

        valid_libraries.append(
            SteamLibrary(
                path=resolved_path,
                apps=library.apps,
            )
        )

    return valid_libraries


def find_library_for_app(
    libraries: list[SteamLibrary],
    app_id: str,
) -> SteamLibrary | None:
    """
    Return the Steam library containing the requested AppID.

    Returns None if the AppID is not found.
    """
    normalized_app_id = app_id.strip()

    for library in libraries:
        if normalized_app_id in library.apps:
            return library

    return None


def _parse_libraryfolders(content: str) -> list[SteamLibrary]:
    """
    Parse the relevant portions of Steam's libraryfolders.vdf.

    Only the following information is extracted:

    - library path;
    - AppIDs inside the ``apps`` block.

    This intentionally does not attempt to implement a complete VDF parser.
    """
    lines = content.splitlines()

    libraries: list[SteamLibrary] = []

    current_path: Path | None = None
    current_apps: set[str] = set()

    in_library = False
    in_apps = False

    brace_depth = 0
    library_depth: int | None = None
    apps_depth: int | None = None

    for line in lines:
        stripped = line.strip()

        # Detect numeric library entry:
        #
        # "0"
        # {
        #
        if (
            stripped.startswith('"')
            and stripped.endswith('"')
            and stripped[1:-1].isdigit()
            and not in_library
        ):
            in_library = True
            current_path = None
            current_apps = set()
            library_depth = brace_depth + 1
            continue

        if stripped == "{":
            brace_depth += 1
            continue

        if stripped == "}":
            if in_apps and apps_depth == brace_depth:
                in_apps = False
                apps_depth = None

            if in_library and library_depth == brace_depth:
                if current_path is not None:
                    libraries.append(
                        SteamLibrary(
                            path=current_path,
                            apps=frozenset(current_apps),
                        )
                    )

                in_library = False
                current_path = None
                current_apps = set()
                library_depth = None

            brace_depth -= 1
            continue

        if not in_library:
            continue

        match = _QUOTED_VALUE_RE.match(line)

        if match:
            key, value = match.groups()

            if key == "path":
                current_path = Path(value)

            elif in_apps and key.isdigit():
                current_apps.add(key)

            continue

        # Detect:
        #
        # "apps"
        # {
        #
        if stripped == '"apps"':
            in_apps = True
            apps_depth = brace_depth + 1

    return libraries

def find_proton_prefix_for_app(
    libraries: list[SteamLibrary],
    app_id: str,
) -> Path | None:
    """
    Find the Proton prefix associated with a Steam AppID.
    """
    library = find_library_for_app(
        libraries,
        app_id,
    )

    if library is None:
        return None

    prefix = (
        library.path
        / "steamapps"
        / "compatdata"
        / app_id
        / "pfx"
    )

    if not prefix.is_dir():
        return None

    return prefix