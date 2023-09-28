from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from sheets_api.gs_pandas import GetInfo
from sql_data.sql import session, Employee


choose_sn_kb = InlineKeyboardBuilder()
# используем Быкову из-за необходимости ввести в класс фамилию
employees = GetInfo().get_employees()
with session as ses:
    used_employees = ses.query(Employee.last_name).all()
for name in used_employees:
    if name in employees:
        del employees[name]
for sn in employees.keys():
    choose_sn_kb.row(InlineKeyboardButton(text=sn,
                                          callback_data=sn))
choose_sn_kb.row(InlineKeyboardButton(text='Круссер',
                                      callback_data='Круссер'))
choose_sn_kb.row(InlineKeyboardButton(text='Василевский',
                                      callback_data='Василевский'))
