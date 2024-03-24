from abc import ABC, abstractmethod
from datetime import datetime
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from calendar import monthrange
from config_data.data import MainMenu
from enum import Enum
from config_data.fltrs import month


class Keyboard(ABC):

    @abstractmethod
    def build(self) -> ReplyKeyboardBuilder:
        pass


class CalendarReplyKeyboard(Keyboard):
    """СОбирает клавиатуру из кол-ва дней в текущем месяце"""

    def __init__(self):
        self.year = datetime.now().year
        self.month = datetime.now().month
        self.days = monthrange(self.year, self.month)[1]

    def build(self) -> ReplyKeyboardBuilder:
        keyboard = ReplyKeyboardBuilder()

        for day in range(1, self.days + 1):
            keyboard.add(KeyboardButton(text=str(day)))
        keyboard.add(KeyboardButton(text='Назад'))
        keyboard.adjust(7)

        return keyboard


class MainReplyKeyboard(Keyboard):
    """Собирает клавитуру главного экрана"""
    def __init__(self):
        self.main_position = MainMenu

    def build(self) -> ReplyKeyboardBuilder:
        keyboard = ReplyKeyboardBuilder()

        for position in self.main_position:
            keyboard.add(KeyboardButton(text=position.value))
        keyboard.adjust(3)

        return keyboard


class MonthKeyboard(Keyboard):
    """Собирает клавиатуру с месяцами"""

    def build(self) -> ReplyKeyboardBuilder:
        keyboard = ReplyKeyboardBuilder()

        for month_number in range(self.month_rage()):
            keyboard.add(KeyboardButton(text=month[month_number]))
        keyboard.add(KeyboardButton(text='За все отработанное время'))
        keyboard.add(KeyboardButton(text='Назад'))
        keyboard.adjust(2)

        return keyboard

    @staticmethod
    def month_rage() -> int:
        """Возвращает кол-во прошедших месяцев в текущем году"""

        current_month = datetime.now().month
        return current_month


class MultiKeyboard(Keyboard):
    """Собирает клавиатуру с enum, которые описаны в /config_data/data"""

    def __init__(self, keyboard: Enum):
        self.collect = keyboard

    def build(self) -> ReplyKeyboardBuilder:
        keyboard = ReplyKeyboardBuilder()

        for item in self.collect:
            keyboard.add(KeyboardButton(text=item.value))
        keyboard.add(KeyboardButton(text='Назад'))
        keyboard.add(KeyboardButton(text='Вернуться в главное меню'))
        keyboard.adjust(3)

        return keyboard
