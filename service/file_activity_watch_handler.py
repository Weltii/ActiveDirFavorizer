import logging
import time
from datetime import datetime
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

from bookmark_manager.bookmark_manager import BookmarkManager

logger = logging.getLogger()


class FileActivityWatchHandler(FileSystemEventHandler):
    def __init__(self,
                 watch_path: Path,
                 project_root_identifying_filenames: list,
                 bookmark_manager: BookmarkManager,
                 inactivity_timeout: int):
        self.bookmarks = dict()
        self.watch_path = watch_path
        self.project_root_identifying_filenames = project_root_identifying_filenames
        self.bookmark_manager = bookmark_manager
        self.inactivity_timeout = inactivity_timeout

        self.observer = Observer()
        self.observer.schedule(self, str(self.watch_path), recursive=True)

    def find_project_root(self, folder: Path):
        if folder == self.watch_path:
            return None

        for file in folder.iterdir():
            if file.parts[-1] in self.project_root_identifying_filenames:
                return folder
        return self.find_project_root(folder.parent)

    def cleanup(self):
        del_keys = []
        for bookmark_path in self.bookmarks.keys():
            if datetime.now().timestamp() - self.bookmarks[bookmark_path] > self.inactivity_timeout:
                logging.info('Removing inactive project "{}"'.format(bookmark_path))
                self.bookmark_manager.remove_bookmark(bookmark_path,
                                                      bookmark_path.parts[-1])
                del_keys.append(bookmark_path)
        for key in del_keys:
            del self.bookmarks[key]

    def cleanup_in_bookmark_manager(self):
        for bookmark in self.bookmarks.keys():
            self.bookmark_manager.remove_bookmark(bookmark, bookmark.parts[-1])

    def on_modified(self, event: FileSystemEvent):
        event_path = Path(event.src_path)

        if not event_path.exists():
            return

        if event_path.is_dir():
            project_path = self.find_project_root(event_path)
        else:
            project_path = self.find_project_root(event_path.parent)

        if project_path is None:
            logging.info('Detected no project root for activity in "{}"'.format(event.src_path))
            return
        if project_path not in self.bookmarks.keys():
            self.bookmark_manager.add_bookmark(project_path, project_path.parts[-1])
            logging.info('Detected new active project: {}'.format(project_path))
        self.bookmarks[project_path] = datetime.now().timestamp()

    def start(self):
        self.observer.start()
        try:
            while True:
                time.sleep(1)
                self.cleanup()
        except KeyboardInterrupt:
            self.stop()
        finally:
            self.cleanup_in_bookmark_manager()
        self.observer.join()

    def stop(self):
        logger.info("Stop file activity watcher")
        self.observer.stop()
        self.observer.join()
