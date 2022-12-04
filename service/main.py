import asyncio
import json
import logging
import os
import sys
from pathlib import Path

from dasbus.connection import SessionMessageBus
from dasbus.loop import EventLoop

from bookmark_manager.bookmark_manager import BookmarkManager
from bookmark_manager.gtk3_bookmarker import Gtk3Bookmarker
from config import dbus_service_name
from dbus.dbus_interface import DBusInterface
from file_activity_watch_handler import FileActivityWatchHandler
from logger import init_logging

DEFAULT_ACTIVITY_TIMEOUT = 300  # 5 * 60s = 5min
DEFAULT_CONFIG_FILE = 'config.json'

init_logging()

logger = logging.getLogger()


def init_bookmark() -> tuple[FileActivityWatchHandler, BookmarkManager]:
    config_path = sys.argv[1] if len(sys.argv) == 2 else DEFAULT_CONFIG_FILE
    with open(config_path, 'r') as config_file:
        config = json.loads(config_file.read())

    if 'watch_path' not in config:
        watch_path = Path(os.getcwd())
    else:
        watch_path = Path(config['watch_path'])
        if not watch_path.exists() or watch_path.is_file():
            logging.error('Can\'t find given watch_path "{}"'.format(config['watch_path']))
            sys.exit(1)

    if 'bookmark_manager_class' not in config:
        logging.error('config item "bookmark_manager_class" is required')
        sys.exit(1)
    try:
        bookmark_manager = Gtk3Bookmarker(config.get('bookmark_manager_config', None))
    except ImportError as e:
        logging.error('Can\'t import given bookmark_mananger_class "{}": {}'.format(
            config['bookmark_manager_class'], str(e)))
        sys.exit(1)
    except AttributeError as e:
        logging.error('Can\'t import given bookmark_mananger_class "{}": {}'.format(
            config['bookmark_manager_class'], str(e)))
        sys.exit(1)
    except Exception as e:
        logging.error('Can\'t instantiate bookmark_mananger_class "{}": {}'.format(
            config['bookmark_manager_class'], str(e)))
        sys.exit(1)

    if 'project_root_identifying_filenames' not in config:
        logging.error(
            'config item "project_root_identifying_filenames" is required, please provide a list '
            'with file or folder names that identifie a project root, e.g. ".git"')
        sys.exit(1)

    project_root_identifying_filenames = config['project_root_identifying_filenames']
    inactivity_timeout = config.get('inactivity_timeout', DEFAULT_ACTIVITY_TIMEOUT)

    watcher = FileActivityWatchHandler(watch_path,
                                       project_root_identifying_filenames,
                                       bookmark_manager,
                                       inactivity_timeout)

    logging.info('ActiveDirFavorizer is configured by "{}" \n'
                 'and is watching "{}"\n'
                 'using {} for project root detection\n'
                 'with {} and {} seconds for inativity detection\n'.format(
        config_path, str(watch_path), project_root_identifying_filenames,
        bookmark_manager.__class__.__name__, inactivity_timeout))
    logging.info('Use Ctrl+C to exit')

    return watcher, bookmark_manager


def init_dbus(bookmark_manager: BookmarkManager) -> EventLoop:
    bus = SessionMessageBus()
    bus.publish_object(f"/{dbus_service_name.replace('.', '/')}", DBusInterface(bookmark_manager))
    bus.register_service(dbus_service_name)

    return EventLoop()


if __name__ == '__main__':
    file_watcher_loop, bookmark_manager = init_bookmark()
    dbus_loop = init_dbus(bookmark_manager)
    asyncio_loop = asyncio.get_event_loop()
    future_dbus = asyncio_loop.run_in_executor(None, dbus_loop.run)
    future_file_watch = asyncio_loop.run_in_executor(None, file_watcher_loop.start)

    try:
        asyncio_loop.run_until_complete(future_dbus)
        asyncio_loop.run_until_complete(future_file_watch)
    except KeyboardInterrupt:
        # TODO stopping service is not smooth...

        logger.info("Stop services")
        dbus_loop.quit()
        file_watcher_loop.stop()

        future_dbus.cancel()
        future_file_watch.cancel()



