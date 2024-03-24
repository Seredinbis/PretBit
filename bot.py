import asyncio
import aioredis
import handlers

from loguru import logger
from config_data.secret import logs_path, bot_token
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

# Инициализируем хранилище (создаем экземпляр класса RedisStorage)
storage = RedisStorage(redis=aioredis.Redis())

# Создаем экземпляр класса бот, чтобы уметь отправлять и удалять сообщения без ансвера и без зависимости с Мессадж
bot = Bot(token=bot_token, parse_mode='HTML')

"""loging"""
logger.add(logs_path+'/bot.log', format='{time} {level} {message}', level='INFO', mode='w')


# Тут роутеры находят новый дом
async def main() -> None:
    logger.info('запуск event loop: успешно')
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
    # await support_function.reuse_auto_send()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logger.info(f"Запуск бота! {__name__}")
        asyncio.run(main())
    except Exception as ex:
        logger.error(f'Ошибка запуска бота {ex}', exc_info=True)
