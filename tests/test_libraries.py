from pathlib import Path

from gaige.libraries import (
    SteamLibrary,
    _parse_libraryfolders,
    find_library_for_app,
    find_proton_prefix_for_app,
)


def test_parse_libraryfolders() -> None:
    content = '''
"libraryfolders"
{
    "0"
    {
        "path"      "/home/user/.steam/debian-installation"
        "apps"
        {
            "123"   "1000"
        }
    }

    "1"
    {
        "path"      "/mnt/documents/SteamLibrary"
        "apps"
        {
            "49520" "16446971171"
            "730"   "123456"
        }
    }
}
'''

    libraries = _parse_libraryfolders(content)

    assert len(libraries) == 2

    assert libraries[0].path == Path(
        "/home/user/.steam/debian-installation"
    )
    assert libraries[0].apps == frozenset({"123"})

    assert libraries[1].path == Path(
        "/mnt/documents/SteamLibrary"
    )
    assert libraries[1].apps == frozenset(
        {"49520", "730"}
    )


def test_find_library_for_app() -> None:
    libraries = [
        SteamLibrary(
            path=Path("/home/user/.steam"),
            apps=frozenset({"123"}),
        ),
        SteamLibrary(
            path=Path("/mnt/documents/SteamLibrary"),
            apps=frozenset({"49520"}),
        ),
    ]

    library = find_library_for_app(
        libraries,
        "49520",
    )

    assert library is not None
    assert library.path == Path(
        "/mnt/documents/SteamLibrary"
    )


def test_find_library_for_missing_app() -> None:
    libraries = [
        SteamLibrary(
            path=Path("/steam"),
            apps=frozenset({"123"}),
        ),
    ]

    assert find_library_for_app(
        libraries,
        "49520",
    ) is None
    
def test_find_proton_prefix_for_app(tmp_path: Path) -> None:
    library_path = tmp_path / "SteamLibrary"

    prefix = (
        library_path
        / "steamapps"
        / "compatdata"
        / "49520"
        / "pfx"
    )

    prefix.mkdir(parents=True)

    libraries = [
        SteamLibrary(
            path=library_path,
            apps=frozenset({"49520"}),
        ),
    ]

    result = find_proton_prefix_for_app(
        libraries,
        "49520",
    )

    assert result == prefix
    
def test_missing_proton_prefix_returns_none(
    tmp_path: Path,
) -> None:
    libraries = [
        SteamLibrary(
            path=tmp_path / "SteamLibrary",
            apps=frozenset({"49520"}),
        ),
    ]

    result = find_proton_prefix_for_app(
        libraries,
        "49520",
    )

    assert result is None