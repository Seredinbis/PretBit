from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton(text='Опера')
b2 = KeyboardButton(text='Балет')
b3 = KeyboardButton(text='Назад')

choose_jenre_kb = ReplyKeyboardMarkup(keyboard=[[b1, b2],
                                                [b3]],
                                      resize_keyboard=True)

bu1 = KeyboardButton(text='Паспорт спектакля')
bu2 = KeyboardButton(text='Выписка спектакля')
bu3 = KeyboardButton(text='Выписка водящего')
bu4 = KeyboardButton(text='Назад')
bu5 = KeyboardButton(text='Вернуться в главное меню')

choose_what_need_kb = ReplyKeyboardMarkup(keyboard=[[bu1, bu2],
                                                    [bu3, bu4],
                                                    [bu5]],
                                          resize_keyboard=True)
