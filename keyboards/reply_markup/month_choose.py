from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types
from datetime import datetime
from handlers.fltrs.all_filters import month


current_month = datetime.now().month

month_choose_kb = ReplyKeyboardBuilder()
for month_number in range(len(month)):
    month_choose_kb.add(types.KeyboardButton(text=month[month_number]))
    if current_month-1 == month_number:
        break
month_choose_kb.add(types.KeyboardButton(text='За все отработанное время'))
month_choose_kb.add(types.KeyboardButton(text='Назад'))
month_choose_kb.adjust(2)
