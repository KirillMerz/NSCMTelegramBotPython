import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
DB_FILENAME = 'NCMSTracker.sqlite3'
SUCCESS_RESPONSE = 'Готово'
