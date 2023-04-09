from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from sheets_api.g_sheets import ResultPrint

choose_sn_kb = InlineKeyboardBuilder()
# используем Быкову из-за необходимости ввести в класс фамилию
for sn in ResultPrint('Великанова').list_of_employees():
    choose_sn_kb.row(InlineKeyboardButton(text=sn,
                                          callback_data=sn))
choose_sn_kb.row(InlineKeyboardButton(text='Круссер',
                                      callback_data='Круссер'))
choose_sn_kb.row(InlineKeyboardButton(text='Василевский',
                                      callback_data='Василевский'))

