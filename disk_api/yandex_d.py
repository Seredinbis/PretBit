import yadisk
import os

from config_data.config import load_config


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
    def __init__(self, show):
        self.show = show
        self.__yan = super().get_token()

    def get_files(self):
        return [(file['name'], file['file']) for file in list(self.__yan.listdir(f'disk:/Лебедки/{self.show}'))]


class Passport(AuthYandex):
    def __init__(self, genre, show):
        self.genre = genre
        self.show = show
        self.__yan = super().get_token()
        self.__files_url = {}

    def get_files(self):
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


class Manual(AuthYandex):
    def __init__(self, show=None):
        self.show = show
        self.__yan = super().get_token()
        self.__files_url = {}

    def get_manual_folders(self) -> list:
        return [folder for folder in list(self.__yan.listdir(f'disk:/Мануалы'))]

    def get_manual_file(self) -> dict:
        return {files['name']: files['file'] for files in list(self.__yan.listdir(f'disk:/Мануалы/{self.show}'))}
