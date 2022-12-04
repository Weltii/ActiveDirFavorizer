import getpass
import re
from enum import Enum
from pathlib import Path
from typing import List

from .bookmark_manager import BookmarkManager


class Flags(Enum):
    LOCKED = "locked"
    NORMAL = "normal"


class Gtk3Bookmarker(BookmarkManager):
    def read_file(self):
        file = open(self.bookmark_path, "r")
        return file.readlines()

    def write_file(self, content: str):
        file = open(self.bookmark_path, "w")
        file.write(content)
        file.close()

    def load_bookmarks(self, flag=Flags.NORMAL):
        bookmarks = self.read_file()
        paths = dict()

        for path in bookmarks:
            paths[Path(path)] = flag
        return paths

    def paths_to_bookmark(self, paths: dict):
        val = ""
        for path in paths:
            path = str(path)
            if not re.search("[A-z]*:/", path):
                path = f"file://{path}"
            elif re.search("[A-z]*:/", path):
                split = re.split(":/", path)
                path = f"{split[0]}:///{split[1]}"
                pass

            val += f"{path}\n"
        return val

    def save_bookmarks(self, paths: dict):
        self.write_file(self.paths_to_bookmark(paths))

    def save_backup(self):
        self.save_bookmarks(self.paths_backup)

    def remove_bookmark(self, path: Path, label: str):
        if self.paths[path] == Flags.LOCKED:
            return
        self.paths.pop(path, None)
        self.save_bookmarks(self.paths)

    def add_bookmark(self, path: Path, label: str):
        if path is None or path == "":
            return

        self.paths[path] = Flags.NORMAL
        self.save_bookmarks(self.paths)

    def get_bookmarks(self) -> List[Path]:
        paths = []

        for value in self.paths.keys():
            paths.append(value)

        return paths

    def __init__(self, config):
        self.config = config
        if not self.config:
            raise Exception("Config not provided")

        if "path" not in self.config:
            raise Exception("path is missing in config")
        self.bookmark_path = Path(self.config["path"].format(user=getpass.getuser()))
        if not self.bookmark_path.is_file():
            raise Exception('Can\'t find dektop path "{}"'.format(self.bookmark_path))

        self.paths_backup = self.load_bookmarks(Flags.LOCKED)
        self.paths = self.paths_backup.copy()
        # TODO create at the first startup a backup of the bookmarks file (bookmarks => bookmarks.bak)

    def __del__(self):
        pass
        # TODO find a way to save the path backup if the program shutdown
        # self.save_bookmarks(self.paths_backup)
