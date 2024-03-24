import os

from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Text
from aiogram.types import FSInputFile
from loguru import logger

router_error = Router()


def get_log_files():
    logger.debug(f'ищем файлы с расширением log по всему проекту! {__name__}')
    # 42 - на этом индексе заканчивается путь дор корня проекта
    project_path = os.path.dirname(os.path.abspath(__file__))[:42]
    logger.debug(f'путь к файлам {project_path}')
    log_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(".log"):
                file_path = os.path.join(root, file)
                logger.debug(f'file_path {file_path}')
                log_files.append(file_path)
    logger.debug(f'вот эти файлы! {log_files}')
    return log_files


@router_error.message(Text('Ошибки'))
async def get_errors(message: Message) -> None:
    logger.info('поймали хэндлер ОШИБКИ, пробуем отправку файлов')
    try:
        error_files = get_log_files()
        for file in error_files:
            doc = FSInputFile(file)
            await message.answer_document(doc)
            logger.info(f'файл {doc} отправлен')
    except Exception:
        logger.exception(f'ошибка отправки файлов')
