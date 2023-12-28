import yadisk

from config_data.secret import yandex_token, logs_path
from abc import ABC, abstractmethod
from loguru import logger

"""loging"""
logger.add(logs_path, format='{time} {level} {message}', level='INFO', mode='w')


class YandexAuth:
    @classmethod
    def get_token(cls):
        return yadisk.YaDisk(token=yandex_token)


class File(ABC):

    @abstractmethod
    def get_files(self): pass

    @abstractmethod
    def get_folder(self): pass


class BaseFile(File, YandexAuth):
    def __init__(self, path: str):
        self.path = path
        self.__yan = self.get_token()

    async def get_files(self) -> dict:
        try:
            logger.info(f'Запрос на файлы {self.path}')
            path = list(self.__yan.listdir(self.path))
            return {file['name']: file['file'] for file in path}
        except Exception as ex:
            logger.exception(f'Ошибка {ex}')

    async def get_folder(self) -> list:
        try:
            logger.info(f'Запрос списка файлов в {self.path}')
            path = list(self.__yan.listdir(self.path))
            return [folder['name'] for folder in path]
        except Exception as ex:
            logger.exception(f'Ошибка {ex}')


class Chain(BaseFile):
    """Класс получения папок и файлов о лебедках на яндекс диске """

    def __init__(self, show: str = None):
        if show is None:
            super().__init__(f'disk:/Лебедки')
        else:
            super().__init__(f'disk:/Лебедки/{show}')


class Manual(BaseFile):
    """Класс получния папок и файлов о мануалах на яндекс диске"""

    def __init__(self, device: str = None):
        if device is None:
            super().__init__(f'disk:/Мануалы')
        else:
            super().__init__(f'disk:/Мануалы/{device}')


class Passport(BaseFile):
    """Класс получения папок и файлов с паспортами спектаклей"""

    def __init__(self, genre: str, show: str = None):
        if show is None:
            super().__init__(f'disk:/{genre}/Паспорт спектакля')
        else:
            super().__init__(f'disk:/{genre}/Паспорт спектакля/{show}')
