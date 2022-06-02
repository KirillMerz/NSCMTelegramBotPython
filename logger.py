import logging
import os
from datetime import datetime

LOGS_DIR_NAME = 'logs'
LOG_FILE_NAME = f'{datetime.now().strftime("%m.%d.%Y")}.log'

if not os.path.exists(LOGS_DIR_NAME):
    os.mkdir(LOGS_DIR_NAME)

logging.basicConfig(
    filename=f'{LOGS_DIR_NAME}/{LOG_FILE_NAME}',
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S',
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
