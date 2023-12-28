import os

from dotenv import load_dotenv

load_dotenv()

yandex_token: str = os.getenv('YANDEX_TOKEN')
logs_path: str = os.getenv('LOGS_PATH')