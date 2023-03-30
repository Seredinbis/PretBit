from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton(text='Автоматическая рассылка и оповещение')
b2 = KeyboardButton(text='Сколько последних сообщений оставлять')
b3 = KeyboardButton(text='Через сколько часов удалять файлы')
b4 = KeyboardButton(text='Назад')


user_settings_kb = ReplyKeyboardMarkup(keyboard=[[b1], [b2], [b3], [b4]],
                                       resize_keyboard=True)
