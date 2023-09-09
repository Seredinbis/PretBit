from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from handlers.fltrs.all_filters import work_position


choose_work_pos = InlineKeyboardBuilder()
for sn in work_position:
    choose_work_pos.row(InlineKeyboardButton(text=sn,
                                          callback_data=sn))

