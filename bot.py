import asyncio
import logging
import aioredis
import handlers
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

import support_function
from config_data.config import load_config
from sql_data.sql import session, Employee

# тут узнаем путь к файлу и получаем токен из него
abspath = os.path.abspath('.env')
config = load_config(abspath)
bot_token = config.tg_bot.token

# получение пользовательского логгера и установка уровня логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# настройка обработчика и форматировщика
handler = logging.FileHandler(f"{__name__}.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# добавление форматировщика к обработчику
handler.setFormatter(formatter)
# добавление обработчика к логгеру
logger.addHandler(handler)

# Инициализируем хранилище (создаем экземпляр класса RedisStorage)
storage = RedisStorage(redis=aioredis.Redis())

# Создаем экземпляр класса бот, чтобы уметь отправлять и удалять сообщения без ансвера и без зависимости с Мессадж
bot = Bot(token=bot_token, parse_mode='HTML')

# список, в котором будет порядок возникающих ошибок + трекинг пользователей
user_track = []
# Словарь, с привязкой к айди пользователя, для удаления предыдущих сообщений и файлов
# для удаления сообщений
message_id_dict = {}
# для удаления файлов
files_id_dict = {}
# для удаления файлов после авто-сообщений
for_delete = {}


# Тут роутеры находят новый дом
async def main() -> None:
    dp = Dispatcher(storage=storage)
    dp.include_router(handlers.router_today)
    dp.include_router(handlers.router_start)
    dp.include_router(handlers.router_url)
    dp.include_router(handlers.router_statement)
    dp.include_router(handlers.router_lebedki)
    dp.include_router(handlers.router_calendar)
    dp.include_router(handlers.router_back)
    dp.include_router(handlers.router_callbacks)
    dp.include_router(handlers.router_time_table)
    dp.include_router(handlers.router_user_settings)
    dp.include_router(handlers.router_error)
    # чтобы не ловил апдейт, когда выключен, пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    await support_function.reuse_auto_send()
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Запуск бота
    try:
        logger.info(f"Запуск бота! {__name__}")
        asyncio.run(main())

    except Exception as ex:
        logger.error(f'Ошибка запуска бота {ex}', exc_info=True)
