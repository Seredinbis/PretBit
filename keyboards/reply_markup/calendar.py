from datetime import datetime
from calendar import monthrange

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

current_year = datetime.now().year
current_month = datetime.now().month

days = monthrange(current_year, current_month)[1]

calendar_kb = ReplyKeyboardBuilder()
for day_n in range(1, days+1):
    calendar_kb.add(types.KeyboardButton(text=str(day_n)))
calendar_kb.add(types.KeyboardButton(text='Назад'))
calendar_kb.adjust(7)


