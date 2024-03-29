from pathlib import Path

import pytest

from bookmark_manager.gtk3_bookmarker import Gtk3Bookmarker, Flags


def read_file(self):
    return ["/home/user/top_of_a_table", "/home/user/table_top"]


def write_file(self, content: str):
    return content


def generate_thunar_manager():
    # overwrite the file system operations
    Gtk3Bookmarker.read_file = read_file
    Gtk3Bookmarker.write_file = write_file
    config = dict(path="/tmp/bookmarks.txt")
    file = Path(config["path"])
    file.write_text(("file:///home/user/top_of_a_table\nfile:///home/user/table_top\n"))
    manager = Gtk3Bookmarker(config)
    return manager


def test_read_file():
    manager = generate_thunar_manager()
    assert manager.read_file() == ["/home/user/top_of_a_table", "/home/user/table_top"]


@pytest.mark.skip
def test_write_file():
    manager = generate_thunar_manager()
    manager.add_bookmark(Path("/home/user/dungeons_dungeons_and_more_dungeons"), "")
    assert (
        manager.write_file(manager.paths_to_bookmark(manager.paths))
        == "file:///home/user/top_of_a_table\n"
        "file:///home/user/table_top\n"
        "file:///home/user/dungeons_dungeons_and_more_dungeons\n"
    )


def test_load_bookmarks():
    manager = generate_thunar_manager()
    paths = manager.load_bookmarks(Flags.LOCKED)
    expected_paths = [Path("/home/user/top_of_a_table"), Path("/home/user/table_top")]
    # TODO test the content of both lists, at the moment is it really imprecisely
    assert len(paths) == len(expected_paths)
    expected_paths.append(Path("/home/user/dungeons_dungeons_and_more_dungeons"))
    assert len(paths) != len(expected_paths)


def test_paths_to_bookmark():
    manager = generate_thunar_manager()
    assert (
        manager.paths_to_bookmark(manager.paths)
        == "file:///home/user/top_of_a_table\nfile:///home/user/table_top\n"
    )


def test_remove_bookmark():
    manager = generate_thunar_manager()

    manager.add_bookmark(Path("/home/user/dungeons_and_dragons"), "")
    assert len(manager.paths) == 3
    manager.remove_bookmark(Path("/home/user/dungeons_and_dragons"), "")
    assert len(manager.paths) == 2
    manager.remove_bookmark(Path("/home/user/top_of_a_table"), "")
    assert len(manager.paths) == 2


def test_add_bookmark():
    manager = generate_thunar_manager()
    assert len(manager.paths) == 2
    manager.add_bookmark(Path("/home/user/dungeons_and_dragons"), "")
    assert len(manager.paths) == 3
    manager.add_bookmark(Path("/home/user/dungeons_and_dragons"), "")
    assert len(manager.paths) == 3
