import os

from dotenv import load_dotenv

load_dotenv()

yandex_token: str = os.getenv('YANDEX_TOKEN')
logs_path: str = os.getenv('LOGS_PATH')
bot_token: str = os.getenv('BOT_TOKEN')
google_token: dict = os.getenv('GOOGLE_SHEETS_TOKEN')
dev_id: str = os.getenv('DEV_ID')
sql_url: str = os.getenv('SQL_URL')
