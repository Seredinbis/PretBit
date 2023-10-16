from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

work_position = ('Начальник осветительской службы', 'Начальник смены', 'Ведущий инженер', 'Инженер', 'Техник',
                 'Осветитель', 'Светооператор')
choose_work_pos = InlineKeyboardBuilder()
for sn in work_position:
    choose_work_pos.row(InlineKeyboardButton(text=sn,
                                             callback_data=sn))
