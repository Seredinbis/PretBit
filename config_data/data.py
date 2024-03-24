from enum import Enum


class Position(Enum):
    LEAD_ENGINEER = 'Ведущий инженер'
    ENGINEER = 'Инженер'
    HEAD_CREW = 'Начальник осветительской службы'
    HEAD_DAY = 'Начальник смены'
    TECHNICAL = 'Техник'
    LIGHT = 'Осветитель'
    LIGHT_OPERATOR = 'Светооператор'


class MainMenu(Enum):
    TIMETABLE = 'График'
    SUMMARY = 'Выписки'
    TODAY = 'Сегодня'
    CALENDAR = 'Календарь'
    URLS = 'Ссылки'
    SETTINGS = 'Настройки пользователя'


class Month(Enum):
    JANUARY = 'Январь'
    FEBRUARY = 'Февраль'
    MARTH = 'Март'
    APRIL = 'Апрель'
    MAY = 'Май'
    JUNE = 'Июнь'
    JULY = 'Июль'
    AUGUST = 'Август'
    SEPTEMBER = 'Сентябрь'
    OCTOBER = 'Октябрь'
    NOVEMBER = 'Ноябрь'
    DECEMBER = 'Декабрь'
    ALL = 'За все отработанное время'


class Genre(Enum):
    BALELET = 'Балет'
    OPERA = 'Опера'
    MANUAL = 'Мануалы'


class ChoosePassport(Enum):
    PASSPORT = 'Паспорт спектакля'
    SHOW_ABSTRACT = 'Выписка спектакля'
    FOLLOW_POST = 'Выписка водящего'


class TimeTable(Enum):
    TIME_TABLE = 'Общий график'
    PERSONAL_TABLE = 'Персональный график'
    WORK_TIME = 'Количество отработанных часов'


class Settings(Enum):
    MASSAGE = 'Сколько последних сообщений оставлять'
    FILE = 'Через сколько часов удалять файлы'

