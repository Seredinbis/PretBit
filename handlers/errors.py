import os
import logging

from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Text
from aiogram.types import FSInputFile

router_error = Router()

# создаем логирование
login_er = logging.getLogger(__name__)
login_er.setLevel('DEBUG')
handler_er = logging.FileHandler(f"{__name__}.log", mode='w')
formater_er = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(message)s')
handler_er.setFormatter(formater_er)
login_er.addHandler(handler_er)


def get_log_files():
    login_er.debug(f'ищем файлы с расширением log по всему проекту! {__name__}')
    # 42 - на этом индексе заканчивается путь дор корня проекта
    project_path = os.path.dirname(os.path.abspath(__file__))[:42]
    login_er.debug(f'путь к файлам {project_path}')
    log_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(".log"):
                file_path = os.path.join(root, file)
                login_er.debug(f'file_path {file_path}')
                log_files.append(file_path)
    login_er.debug(f'вот эти файлы! {log_files}')
    return log_files


@router_error.message(Text('Ошибки'))
async def get_errors(message: Message) -> None:
    login_er.debug('поймали хэндлер ОШИБКИ, пробуем отправку файлов')
    try:
        error_files = get_log_files()
        for file in error_files:
            doc = FSInputFile(file)
            await message.answer_document(doc)
            login_er.debug(f'файл {doc} отправлен')
    except Exception:
        login_er.exception(f'ошибка отправки файлов')
