import yadisk
import os

from config_data.config import load_config


class FromYandex:
    def __init__(self, genre, show, what):
        # genre - жанр спектакля, Опера, либо Балет
        # show - название спектакля
        # what - что требуется: выписки, либо паспорта
        # check - флаг для выбора условия, если имя спекталкя совпадает с именем папки
        # clientID, client_secret, Redirect_URL, Y_token - данные выданные Yandex, для связи с RestApi

        # тут узнаем путь к файлу и получаем токен из него
        abspath = os.path.abspath('.env')
        config = load_config(abspath)
        yandex_token = config.yandex_api.token

        self.show = show
        self.what = what
        self.genre = genre
        self.clientID = '36a304f0b73340149d3d713adc45dac4'
        self.client_secret = 'bc0679779d5a49d584b5b9cc957b9271'
        self.Redirect_URL = 'yandexta://disk.yandex.ru'
        self.Y_Token = yandex_token
        self.yan = yadisk.YaDisk(token=self.Y_Token)
        self.check = False
        self.file_dict: dict = {}

    def get_files(self) -> [dict, str]:
        # тут бегаем по папкам и ищем нужный файл
        for folder in list(self.yan.listdir(f'disk:/{self.genre}/{self.what}')):
            if folder['name'].lower() in self.show.lower():
                self.check = True
                for i in list(self.yan.listdir(f'disk:/{self.genre}/{self.what}/{folder["name"]}')):
                    self.file_dict.update({i['name']: i['file']})
                return self.file_dict
        if not self.check:
            return f'К сожалению, для {self.show} нет {self.what}, в скором времени это исправится!' \
                   f' Попробуйте выбрать другой файл!'

    # данная функция возвращает список папок в папке лебедки
    def get_lebedki_show(self) -> list:
        show_list = []
        for folder in list(self.yan.listdir(f'disk:/{self.genre}')):
            show_list.append(folder)
        return show_list

    # данная функция возвращает список с именем файла и его урл
    def get_lebedki_file(self) -> list:
        file_list = []
        for file in list(self.yan.listdir(f'disk:/{self.genre}/{self.show}')):
            file_list = [file['name'], file['file']]
        return file_list

    # данная функция возвращает список папок в папке мануал
    def get_manual_show(self) -> list:
        show_list = []
        for folder in list(self.yan.listdir(f'disk:/{self.genre}')):
            show_list.append(folder)
        return show_list

    # данная функция возвращает словарь с именами фалйлов и их урл
    def get_manual_file(self) -> dict:
        for files in list(self.yan.listdir(f'disk:/{self.genre}/{self.show}')):
            self.file_dict.update({files['name']: files['file']})
        return self.file_dict

# Это для теста
# r = FromYandex('Опера', 'Севильский Цирюльник', 'Паспорт спектакля')
# print(r.get_files())
# r.get_files_name()
