from typing import List
from Path import Flags, Path
from .BookmarkManager import BookmarkManager
import getpass
bookmark_path = f"/home/{getpass.getuser()}/.config/gtk-3.0/bookmarks"


class ThunarBookmarkManager(BookmarkManager):
	def read_file(self):
		file = open(bookmark_path, "r")
		return file.readlines()

	def write_file(self, content: str):
		file = open(bookmark_path, "w")
		file.write(content)
		file.close()

	def load_bookmarks(self, flag=Flags.NORMAL):
		bookmarks = self.read_file()
		paths = []

		for path in bookmarks:
			paths.append(Path(path, flag))
		return paths

	def paths_to_bookmark(self, paths: List[Path]):
		val = ""
		for path in paths:
			val += f"{path.path}\n"
		return val

	def save_bookmarks(self, paths: List[Path]):
		self.write_file(self.paths_to_bookmark(paths))

	def save_backup(self):
		self.save_bookmarks(self.paths_backup)

	def remove_bookmark(self, path: Path, label: str):
		found_path = None
		for p in self.paths:
			if p.path == path.path:
				found_path = p

		if found_path is not None:
			if found_path.is_removable():
				self.paths.remove(found_path)
				self.save_bookmarks(self.paths)

	def add_bookmark(self, path: Path, label: str):
		if path is None or path.path is "":
			return

		not_found = True
		for p in self.paths:
			if p.path == path.path:
				p.add_used_path(path.path)
				not_found = False
		if not_found:
			self.paths.append(path)
		self.save_bookmarks(self.paths)

	def __init__(self):
		self.paths_backup = self.load_bookmarks(Flags.LOCKED)
		self.paths = self.paths_backup.copy()
		# TODO create at the first startup a backup of the bookmarks file (bookmarks => bookmarks.bak)

	def __del__(self):
		pass
		# TODO find a way to save the path backup if the program shutdown
		# self.save_bookmarks(self.paths_backup)
