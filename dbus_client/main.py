from pprint import pprint

from dasbus.connection import SessionMessageBus
from dasbus.loop import EventLoop

dbus_service_name = "org.outlawraspberry.ActiveDirFavorizer"

loop = EventLoop()

bus = SessionMessageBus()

proxy = bus.get_proxy(dbus_service_name, f"/{dbus_service_name.replace('.', '/')}")

pprint(proxy.GetBookmarks())
