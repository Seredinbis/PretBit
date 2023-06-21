import asyncio
import logging
import aioredis
import handlers
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from config_data.config import load_config


# тут узнаем путь к файлу и получаем токен из него
abspath = os.path.abspath('.env')
config = load_config(abspath)
bot_token = config.tg_bot.token

# Инициализируем хранилище (создаем экземпляр класса RedisStorage)
storage = RedisStorage(redis=aioredis.Redis())

# Создаем экземпляр класса бот, чтобы уметь отправлять и удалять сообщения без ансвера и без зависимости с Мессадж
bot = Bot(token=bot_token, parse_mode='HTML')

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
    # dp.include_router(handlers.router_error)
    # чтобы не ловил апдейт, когда выключен, пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Запуск бота
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
