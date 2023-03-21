from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


b1 = KeyboardButton(text='Общий график')
b2 = KeyboardButton(text='Персональный график')
b3 = KeyboardButton(text='Количество отработанных часов')
b4 = KeyboardButton(text='Назад')

time_table_kb = ReplyKeyboardMarkup(keyboard=[[b1, b2],
                                              [b3, b4]],
                                    resize_keyboard=True)
