from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


how_del_pre_message_kb = InlineKeyboardBuilder()
for how_much in range(1, 20):
    how_del_pre_message_kb.row(InlineKeyboardButton(text=how_much,
                                                    callback_data=f'{how_much} DEL'))
how_del_pre_message_kb.row(InlineKeyboardButton(text='Назад',
                                                callback_data='Назад в выбор настроек'))
how_del_pre_message_kb.row(InlineKeyboardButton(text='В главное меню',
                                                callback_data='Вернуться в главное меню'))
