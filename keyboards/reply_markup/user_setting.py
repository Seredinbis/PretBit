from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


b2 = KeyboardButton(text='Сколько последних сообщений оставлять')
b3 = KeyboardButton(text='Через сколько часов удалять файлы')
b4 = KeyboardButton(text='Назад')


user_settings_kb = ReplyKeyboardMarkup(keyboard=[[b2], [b3], [b4]],
                                       resize_keyboard=True)
