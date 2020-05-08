import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class BookmarkingEventHandler(FileSystemEventHandler):
	def __init__(self, bookmarks, watch_folder):
		self.bookmarks = bookmarks
		self.watch_folder = watch_folder

	ROOT_FILES = ['.git', '.idea', '.vscode', 'package.json', 'requirements.txt']

	# TODO: implement activity tracker and cleanup

	def find_project_root(self, folder):
		if folder == self.watch_folder:
			return None
		is_root = len([file for file in folder.iterdir() if file.parts[-1] in self.ROOT_FILES])
		return folder if is_root else self.find_project_root(folder.parent)

	def on_modified(self, event):
		if not event.is_directory:
			project_path = self.find_project_root(Path(event.src_path).parent)
		else:
			project_path = self.find_project_root(Path(event.src_path))
		if project_path is not None and project_path not in self.bookmarks.keys():
			print("New project opened: {}".format(project_path))
			self.bookmarks[project_path] = 1


if __name__ == "__main__":
	bookmarks = {}
	path = '/home/benjamin/Projects/Dart/'
	event_handler = BookmarkingEventHandler(bookmarks, Path(path))
	observer = Observer()
	observer.schedule(event_handler, path, recursive=True)
	observer.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()