import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

LOGS_DIR_NAME = 'logs'

if not os.path.exists(LOGS_DIR_NAME):
    os.mkdir(LOGS_DIR_NAME)

handler = TimedRotatingFileHandler(
    f'{LOGS_DIR_NAME}/{datetime.now().strftime("%d.%m.%Y")}.log',
    when='midnight'
)

formatter = logging.Formatter(
    '[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S'
)

handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
