import pytest

from Path import Path, Flags
from .thunar_bookmark_manager import ThunarBookmarkManager


def read_file(self):
	return ["/home/user/top_of_a_table", "/home/user/table_top"]


def write_file(self, content: str):
	return content


def generate_thunar_manager():
	# overwrite the file system operations
	ThunarBookmarkManager.read_file = read_file
	ThunarBookmarkManager.write_file = write_file
	manager = ThunarBookmarkManager()
	return manager


def test_read_file():
	manager = generate_thunar_manager()
	assert manager.read_file() == ["/home/user/top_of_a_table", "/home/user/table_top"]


def test_write_file():
	manager = generate_thunar_manager()
	manager.add_bookmark(Path("home/user/dungeons_dungeons_and_more_dungeons", Flags.NORMAL), "")
	assert manager.write_file(manager.paths_to_bookmark(manager.paths)) == "/home/user/top_of_a_table\n/home/user/table_top\nhome/user" \
																 "/dungeons_dungeons_and_more_dungeons\n"


def test_load_bookmarks():
	manager = generate_thunar_manager()
	paths = manager.load_bookmarks(Flags.LOCKED)
	expected_paths = [
		Path("/home/user/top_of_a_table", Flags.LOCKED),
		Path("/home/user/table_top", Flags.LOCKED)
	]
	# TODO test the content of both lists, at the moment is it really imprecisely
	assert len(paths) == len(expected_paths)
	expected_paths.append(Path("/home/user/dungeons_dungeons_and_more_dungeons", Flags.LOCKED))
	assert len(paths) != len(expected_paths)


def test_paths_to_bookmark():
	manager = generate_thunar_manager()
	assert manager.paths_to_bookmark(manager.paths) == "/home/user/top_of_a_table\n/home/user/table_top\n"


def test_remove_bookmark():
	manager = generate_thunar_manager()
	manager.add_bookmark(Path("/home/user/dungeons_and_dragons", Flags.NORMAL), "")
	assert len(manager.paths) == 3
	manager.remove_bookmark(Path("/home/user/dungeons_and_dragons", Flags.NORMAL), "")
	assert len(manager.paths) == 2
	manager.remove_bookmark(Path("/home/user/top_of_a_table", Flags.NORMAL), "")
	assert len(manager.paths) == 2


def test_add_bookmark():
	manager = generate_thunar_manager()
	assert len(manager.paths) == 2
	manager.add_bookmark(Path("/home/user/dungeons_and_dragons", Flags.NORMAL), "")
	assert len(manager.paths) == 3
	manager.add_bookmark(Path("/home/user/dungeons_and_dragons", Flags.NORMAL), "")
	assert len(manager.paths) == 3


