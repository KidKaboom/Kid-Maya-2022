# :coding: utf-8

# Project Modules
from kid.core.kobject import KObject

# Python Modules
import logging
import time

# logging.basicConfig()
LOGGER = logging.getLogger("KID")
# LOG_HANDLER = logging.StreamHandler()
# LOG_FORMAT = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# LOG_HANDLER.setFormatter(LOG_FORMAT)
# LOGGER.addHandler(LOG_HANDLER) 
LOGGER.setLevel(logging.DEBUG)


class KDebug(KObject):
    CURRENT_TIME = time.time()

    @staticmethod
    def log(message):
        LOGGER.debug(message)

    @staticmethod
    def debug(message):
        LOGGER.debug(message)

    @staticmethod
    def info(message):
        LOGGER.info(message)

    @staticmethod
    def warning(message):
        LOGGER.warning(message)

    @staticmethod
    def error(message):
        LOGGER.error(message)

    @staticmethod
    def critical(message):
        LOGGER.critical(message)

    @classmethod
    def update_time(cls):
        cls.CURRENT_TIME = time.time()

    @classmethod
    def log_elapsed_time(cls):
        cls.log("Time Elapsed: {} seconds.".format(time.time() - cls.CURRENT_TIME))
        cls.CURRENT_TIME = time.time()


if __name__ == '__main__':
    KDebug.error("test")
