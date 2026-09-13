from pathlib import Path

from gaige.steam import (
    find_steam_installations,
    get_common_steam_paths,
    is_steam_installation,
)


def test_get_common_steam_paths(tmp_path: Path) -> None:
    paths = get_common_steam_paths(tmp_path)

    assert len(paths) == 3
    assert paths[0].path == tmp_path / ".local/share/Steam"
    assert paths[1].path == tmp_path / ".steam/steam"
    assert paths[2].path == tmp_path / ".var/app/com.valvesoftware.Steam/.local/share/Steam"

def test_is_steam_installation(tmp_path: Path) -> None:
    steam_path = tmp_path / ".local/share/Steam"

    steam_path.mkdir(parents=True)

    assert is_steam_installation(steam_path) is False

    (steam_path / "steamapps").mkdir()

    assert is_steam_installation(steam_path) is True


def test_find_native_steam_installation(tmp_path: Path) -> None:
    steam_path = tmp_path / ".local/share/Steam"

    (steam_path / "steamapps").mkdir(parents=True)

    installations = find_steam_installations(tmp_path)

    assert len(installations) == 1
    assert installations[0].path == steam_path.resolve()
    assert installations[0].installation_type == "native"


def test_find_multiple_steam_installations(tmp_path: Path) -> None:
    native = tmp_path / ".local/share/Steam"
    flatpak = tmp_path / ".var/app/com.valvesoftware.Steam/.local/share/Steam"

    (native / "steamapps").mkdir(parents=True)
    (flatpak / "steamapps").mkdir(parents=True)

    installations = find_steam_installations(tmp_path)

    assert len(installations) == 2

    paths = {installation.path for installation in installations}

    assert native.resolve() in paths
    assert flatpak.resolve() in paths


def test_ignore_missing_installations(tmp_path: Path) -> None:
    installations = find_steam_installations(tmp_path)

    assert installations == []


def test_ignore_duplicate_symlink(tmp_path: Path) -> None:
    main_steam = tmp_path / ".local/share/Steam"
    alternate_steam = tmp_path / ".steam/steam"

    (main_steam / "steamapps").mkdir(parents=True)

    alternate_steam.parent.mkdir(parents=True)
    alternate_steam.symlink_to(main_steam, target_is_directory=True)

    installations = find_steam_installations(tmp_path)

    assert len(installations) == 1
    assert installations[0].path == main_steam.resolve()