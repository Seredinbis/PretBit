import yadisk
import os
import logging

from config_data.config import load_config

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


class AuthYandex:
    # тут узнаем путь к файлу и получаем токен из него
    __abspath = os.path.abspath('.env')
    __config = load_config(__abspath)
    __yandex_token = __config.yandex_api.token
    __Y_Token = __yandex_token
    __yan = yadisk.YaDisk(token=__Y_Token)

    @classmethod
    def get_token(cls):
        return cls.__yan


class Chain(AuthYandex):
    def __init__(self, show=None):
        self.show = show
        self.__yan = super().get_token()

    def get_files(self):
        try:
            logger.info('Запрос на файлы лебедок')
            return [(file['name'], file['file']) for file in list(self.__yan.listdir(f'disk:/Лебедки/{self.show}'))]
        except ConnectionError as ex:
            logger.exception(f'Ошибка {ex}')

    def get_folders(self) -> list:
        try:
            logger.info(f'Запрос списка файлов лебедок')
            return [folder for folder in list(self.__yan.listdir(f'disk:/Лебедки'))]
        except ConnectionError as ex:
            logger.exception(f'Ошибка {ex}')


class Passport(AuthYandex):
    def __init__(self, genre, show):
        self.genre = genre
        self.show = show
        self.__yan = super().get_token()
        self.__files_url = {}

    def get_files(self):
        try:
            logger.info(f'Запрос на паспорт {self.show}')
            # тут бегаем по папкам и ищем нужный файл
            path = list(self.__yan.listdir(f'disk:/{self.genre}/Паспорт спектакля'))
            for folder in path:
                if folder['name'].lower() in self.show.lower():
                    path = list(self.__yan.listdir(f'disk:/{self.genre}/Паспорт спектакля/{folder["name"]}'))
                    for i in path:
                        self.__files_url.update({i['name']: i['file']})
                    return self.__files_url
                return f'К сожалению, для {self.show} нет паспотра, в скором времени это исправится!' \
                       f' Попробуйте выбрать другой файл!'
        except ConnectionError as ex:
            logger.exception(f'Ошибка {ex}')


class Manual(AuthYandex):
    def __init__(self, device=None):
        self.device = device
        self.__yan = super().get_token()
        self.__files_url = {}

    def get_folders(self) -> list:
        try:
            logger.info(f'Запрос списка мануалов')
            return [folder for folder in list(self.__yan.listdir(f'disk:/Мануалы'))]
        except ConnectionError as ex:
            logger.exception(f'Ошибка {ex}')

    def get_file(self) -> dict:
        try:
            logger.info(f'Запрос на мануал {self.device}')
            return {files['name']: files['file'] for files in list(self.__yan.listdir(f'disk:/Мануалы/{self.device}'))}
        except ConnectionError as ex:
            logger.exception(f'Ошибка {ex}')
