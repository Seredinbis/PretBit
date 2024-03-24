import os
import json

from dotenv import load_dotenv

load_dotenv()

yandex_token: str = os.getenv('YANDEX_TOKEN')
logs_path: str = os.getenv('LOGS_PATH')
bot_token: str = os.getenv('BOT_TOKEN')
google_token: dict = json.loads(os.getenv('GOOGLE_SHEETS_TOKEN'))
dev_id: str = os.getenv('DEV_ID')
sql_url: str = os.getenv('SQL_URL')
time_table_url = os.getenv('TIME_TABLE_URL')
spreadsheet_ID = os.getenv('SPREADSHEET_ID')