from abc import ABC, abstractmethod
from pathlib import Path
from typing import List


class BookmarkManager(ABC):
    @abstractmethod
    def add_bookmark(self, path: Path, label: str):
        pass

    @abstractmethod
    def remove_bookmark(self, path: Path, label: str):
        pass

    @abstractmethod
    def get_bookmarks(self) -> List[Path]:
        pass
