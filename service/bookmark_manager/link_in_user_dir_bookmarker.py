import getpass
import logging
import os
from pathlib import Path
from typing import List

from .bookmark_manager import BookmarkManager


class LinkInUserDirBookmarker(BookmarkManager):
    def __init__(self, config):
        self.config = config
        if not self.config:
            raise Exception("Config not provided")

        if "path" not in self.config:
            raise Exception("path is missing in config")
        self.desktop_path = Path(self.config["path"].format(user=getpass.getuser()))
        if not self.desktop_path.exists() or self.desktop_path.is_file():
            raise Exception('Can\'t find dektop path "{}"'.format(self.desktop_path))

    def add_bookmark(self, path: Path, label: str):
        bookmark_path = self.desktop_path.joinpath(label)
        if not bookmark_path.exists():
            os.symlink(path, Path(self.desktop_path.joinpath(label)))

    def remove_bookmark(self, path: Path, label: str):
        bookmark_path = self.desktop_path.joinpath(label)
        if bookmark_path.is_symlink():
            os.unlink(self.desktop_path.joinpath(label))

    def get_bookmarks(self) -> List[Path]:
        logging.getLogger().info("deprecated!")
        return []
