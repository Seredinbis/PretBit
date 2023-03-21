from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton(text='Автоматическая рассылка и оповещение')
b2 = KeyboardButton(text='Назад')


user_settings_kb = ReplyKeyboardMarkup(keyboard=[[b1], [b2]],
                                       resize_keyboard=True)
