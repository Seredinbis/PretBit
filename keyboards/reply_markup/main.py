from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


mb1 = KeyboardButton(text='График')
mb2 = KeyboardButton(text='Выписки')
mb3 = KeyboardButton(text='Сегодня')
mb4 = KeyboardButton(text='Календарь')
mb5 = KeyboardButton(text='Ссылки')
mb6 = KeyboardButton(text='Настройки пользователя')

main_kb = ReplyKeyboardMarkup(keyboard=[[mb1, mb2],
                                        [mb3, mb4],
                                        [mb5, mb6]],
                              resize_keyboard=True)
