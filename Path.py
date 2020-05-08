from enum import Enum


class Flags(Enum):
	LOCKED = "locked"
	NORMAL = "normal"


class Path:
	def __init__(self, path: str, flag: Flags):
		self.path = path.strip()
		self.flag = flag
		self.used_by_paths = []

	def add_used_path(self, path: str):
		if not self.used_by_paths.__contains__(path):
			self.used_by_paths.append(path)

	def remove_used_path(self, path: str):
		if self.used_by_paths.__contains__(path):
			self.used_by_paths.remove(path)

	def is_removable(self) -> bool:
		removable = len(self.used_by_paths) is 0 \
					 and self.flag is not Flags.LOCKED

		return removable

	def __str__(self):
		used_by = ""
		for path in self.used_by_paths:
			used_by += f"{path},"
		return f"Path: {self.path}; Flag: {self.flag}; Used by: [{used_by}]"
