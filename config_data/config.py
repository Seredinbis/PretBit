from dataclasses import dataclass
from environs import Env


@dataclass()
class TgBot:
    token: str       # токен для телеграмм бота
    pass


@dataclass()
class YaDisc:
    token: str      # токен для яндекс диска
    pass


@dataclass()
class GooSheets:
    token: dict     # токен для гугл шиитс


#  этот датакласс не будет использоваться, лежит тут просто для примера
@dataclass
class DatabaseConfig:
    database: str         # Название базы данных
    db_host: str          # URL-адрес базы данных
    db_user: str          # Username пользователя базы данных
    db_password: str      # Пароль к базе данных


@dataclass
class Config:
    tg_bot: TgBot
    yandex_api: YaDisc
    google_sheets_api: GooSheets


def load_config(path) -> Config:

    env: Env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')),
                  yandex_api=YaDisc(token=env('YANDEX_TOKEN')),
                  google_sheets_api=GooSheets(token=env('GOOGLE_SHEETS_TOKEN')))
