import logging

from dasbus.server.interface import dbus_interface

from config import dbus_service_name

logger = logging.getLogger()


@dbus_interface(dbus_service_name)
class DBusInterface:
    def __init__(self):
        logger.info("init {}".format(__file__))

    def start(self):
        logger.info("start service")

    def stop(self):
        logger.info("stop service")
