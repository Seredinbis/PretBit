from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types
from datetime import datetime
from handlers.fltrs.all_filters import month


current_month = datetime.now().month
print(current_month)

m