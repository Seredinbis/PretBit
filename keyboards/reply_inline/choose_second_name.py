from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from sheets_api.gs import GS


choose_sn_kb = InlineKeyboardBuilder()
# используем Быкову из-за необходимости ввести в класс фамилию
for sn in GS().list_of_employees():
    choose_sn_kb.row(InlineKeyboardButton(text=sn,
                                          callback_data=sn))
choose_sn_kb.row(InlineKeyboardButton(text='Круссер',
                                      callback_data='Круссер'))
choose_sn_kb.row(InlineKeyboardButton(text='Василевский',
                                      callback_data='Василевский'))
