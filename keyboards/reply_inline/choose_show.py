import asyncio

from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
from disk_api.yandex_ import Chain, Manual, Passport



choose_lebedki_kb = InlineKeyboardBuilder()
for show in Chain().get_folders():
    choose_lebedki_kb.row(InlineKeyboardButton(text=show,
                                               callback_data=f'ЛЕБЕДКИ {show}'))

choose_lebedki_kb.row(InlineKeyboardButton(text='Назад',
                                           callback_data='Назад к выбору жанра'))
choose_lebedki_kb.row(InlineKeyboardButton(text='Вернуться в главное меню',
                                           callback_data='Вернуться в главное меню'))

choose_manual_kb = InlineKeyboardBuilder()
for device in Manual().get_folders():
    choose_manual_kb.row(InlineKeyboardButton(text=device,
                                              callback_data=f'МАНУАЛ {device}'))

choose_manual_kb.row(InlineKeyboardButton(text='Назад',
                                          callback_data='Назад к выбору жанра'))
choose_manual_kb.row(InlineKeyboardButton(text='Вернуться в главное меню',
                                          callback_data='Вернуться в главное меню'))
