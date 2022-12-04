import logging
from typing import List

from bookmark_manager.bookmark_manager import BookmarkManager
from config import dbus_service_name
from dasbus.server.interface import dbus_interface

logger = logging.getLogger()


@dbus_interface(dbus_service_name)
class DBusInterface:
    def __init__(self, bookmark_manager: BookmarkManager):
        logger.info("init {}".format(__file__))
        self.bookmark_manager = bookmark_manager

    def Start(self):
        logger.info("start service")

    def Stop(self):
        logger.info("stop service")

    def GetBookmarks(self) -> List[str]:
        path_strings = []
        for path in self.bookmark_manager.get_bookmarks():
            path_strings.append(str(path).strip())
        return path_strings
