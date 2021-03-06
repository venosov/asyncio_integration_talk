# Copyright (C) 2019  Infobyte LLC (http://www.infobytesec.com/)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import logging.handlers

from dispatcher.config import DispatcherGlobals


MAX_LOG_FILE_SIZE = 5 * 1024 * 1024     # 5 MB
MAX_LOG_FILE_BACKUP_COUNT = 5
ROOT_LOGGER = u'pycon2020_dispatcher'
LOGGING_HANDLERS = []
LVL_SETTABLE_HANDLERS = []


def setup_logging():
    logger = logging.getLogger(ROOT_LOGGER)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s {%(threadName)s} [%(filename)s:%(lineno)s - %(funcName)s()]  '
            '%(message)s'
    )
    setup_console_logging(formatter)


def setup_console_logging(formatter):
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(DispatcherGlobals.LOGGING_LEVEL)
    console_handler.name = "CONSOLE_HANDLER"
    add_handler(console_handler)
    LVL_SETTABLE_HANDLERS.append(console_handler)


def add_handler(handler):
    logger = logging.getLogger(ROOT_LOGGER)
    for hldr in logger.handlers:
        if hldr.name == handler.name:
            logger.removeHandler(hldr)
    logger.addHandler(handler)
    LOGGING_HANDLERS.append(handler)


def get_logger(obj=None):
    """Creates a logger named by a string or an object's class name.
     Allowing logger to additionally accept strings as names
     for non-class loggings."""
    if obj is None:
        logger = logging.getLogger(ROOT_LOGGER)
        logger.setLevel(DispatcherGlobals.LOGGING_LEVEL)
    elif isinstance(obj, str):
        if obj != ROOT_LOGGER:
            logger = logging.getLogger(u'{}.{}'.format(ROOT_LOGGER, obj))
        else:
            logger = logging.getLogger(obj)
    else:
        cls_name = obj.__class__.__name__
        logger = logging.getLogger(u'{}.{}'.format(ROOT_LOGGER, cls_name))
    return logger


def set_logging_level(level):

    DispatcherGlobals.LOGGING_LEVEL = level
    for handler in LVL_SETTABLE_HANDLERS:
        handler.setLevel(level)
