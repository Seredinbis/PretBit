from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
from disk_api.yandex_ import Chain, Manual, Passport
from sheets_api.gs_pandas import GetInfo
from abc import ABC, abstractmethod
from sql_data.queries import QueriesGet
from typing import Union
from config_data.data import Position


class Keyboard(ABC):

    @abstractmethod
    def build(self) -> InlineKeyboardBuilder:
        pass


class DiskInlineKeyboard(Keyboard):
    """Класс постоения инлайн клавиатур с имен папок, с яндекс диска"""

    def __init__(self, disk_object: Union[Chain, Manual, Passport]):
        self.object = disk_object

    async def build(self) -> InlineKeyboardBuilder:
        shows = await self.object.get_folder()
        keyboard = InlineKeyboardBuilder()

        for show in shows:
            keyboard.row(InlineKeyboardButton(text=show, callback_data=show))

        keyboard.row(InlineKeyboardButton(text='Назад',
                                          callback_data='Назад к выбору жанра'))
        keyboard.row(InlineKeyboardButton(text='Вернуться в главное меню',
                                          callback_data='Вернуться в главное меню'))
        return keyboard


class FamilyInlineKeyboard(Keyboard):
    """Класс построения инлайн клавиатуры с фамилиями, которые еще не были авторизированны в боте"""

    def __init__(self, table_object: GetInfo):
        self.used_employees = table_object.get_employees()

    async def drop_user(self) -> list:
        users: list = await QueriesGet().get_users()

        no_auth_employees = [user for user in self.used_employees if user not in users]
        return no_auth_employees

    async def build(self) -> InlineKeyboardBuilder:
        shows = await self.drop_user()
        keyboard = InlineKeyboardBuilder()

        for show in shows:
            keyboard.row(InlineKeyboardButton(text=show, callback_data=show))

        keyboard.row(InlineKeyboardButton(text='Круссер',
                                          callback_data='Круссер'))
        keyboard.row(InlineKeyboardButton(text='Василевский',
                                          callback_data='Василевский'))
        return keyboard


class PositionsInlineKeyboard(Keyboard):
    """Класс построения инлайн клавиатуры, для выбора рабочей должности"""

    def build(self) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()

        for position in Position():
            keyboard.row(InlineKeyboardButton(text=position,
                                              callback_data=position))
        return keyboard


class SettingsInlineKeyboard(Keyboard):
    """Класс построения инлайн клавиатуры для настроек времени удаления файла и кол-ва оставляемых сообщений"""

    def build(self) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        for how_much in range(1, 10):
            keyboard.row(InlineKeyboardButton(text=how_much,
                                              callback_data=f'{how_much} DELF'))
        keyboard.row(InlineKeyboardButton(text='Назад',
                                          callback_data='Назад в выбор настроек'))
        keyboard.row(InlineKeyboardButton(text='В главное меню',
                                          callback_data='Вернуться в главное меню'))
        return keyboard
