from pathlib import Path

from gaige.saves import (
    SaveDirectory,
    find_save_files,
)


def test_find_multiple_saves_and_steam_ids(
    tmp_path: Path,
) -> None:
    save_data = tmp_path / "SaveData"

    steam_id_1 = save_data / "76561198000000001"
    steam_id_2 = save_data / "76561198000000002"

    steam_id_1.mkdir(parents=True)
    steam_id_2.mkdir(parents=True)

    (steam_id_1 / "save0001.sav").write_bytes(b"save1")
    (steam_id_1 / "save0002.sav").write_bytes(b"save2")
    (steam_id_2 / "save0003.sav").write_bytes(b"save3")

    directory = SaveDirectory(
        path=save_data,
        steam_library=tmp_path,
        proton_prefix=tmp_path / "pfx",
        proton_user="steamuser",
    )

    saves = find_save_files([directory])

    assert len(saves) == 3

    filenames = {save.filename for save in saves}

    assert filenames == {
        "save0001.sav",
        "save0002.sav",
        "save0003.sav",
    }

    steam_ids = {save.steam_id for save in saves}

    assert steam_ids == {
        "76561198000000001",
        "76561198000000002",
    }
    
def test_ignore_non_save_files(
    tmp_path: Path,
) -> None:
    save_data = tmp_path / "SaveData"
    steam_id = save_data / "76561198000000001"

    steam_id.mkdir(parents=True)

    (steam_id / "save0001.sav").write_bytes(b"save")
    (steam_id / "profile.bin").write_bytes(b"profile")
    (steam_id / "notes.txt").write_text("test")

    directory = SaveDirectory(
        path=save_data,
        steam_library=tmp_path,
        proton_prefix=tmp_path / "pfx",
        proton_user="steamuser",
    )

    saves = find_save_files([directory])

    assert len(saves) == 1
    assert saves[0].filename == "save0001.sav"
    
def test_empty_save_directory(
    tmp_path: Path,
) -> None:
    save_data = tmp_path / "SaveData"
    save_data.mkdir()

    directory = SaveDirectory(
        path=save_data,
        steam_library=tmp_path,
        proton_prefix=tmp_path / "pfx",
        proton_user="steamuser",
    )

    assert find_save_files([directory]) == []