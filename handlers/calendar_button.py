import support_function

from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.reply_markup.calendar import calendar_kb
from sheets_api.gs import GS

from .fltrs import day_number


router_calendar = Router()


@router_calendar.message(Text('Календарь'))
async def get_calendar(message: Message, state: FSMContext):
    if await support_function.login_test.log_test(message=message,
                                                  state=state):
        await support_function.user_tracking.where_who(where=message.text,
                                                       state=state)
        msg = await message.answer(text='Выберите пожалуйста желаемую дату текущего месяца',
                                   reply_markup=calendar_kb.as_markup())
        await state.update_data(whitch_kb_was='main_kb')
        await message.delete()
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)


@router_calendar.message(Text(day_number))
async def get_calendar(message: Message, state: FSMContext):
    if await support_function.login_test.log_test(message=message,
                                                  state=state):
        user_data = await state.get_data()
        user_sn = user_data['user_second_name']
        await support_function.user_tracking.where_who(where=message.text,
                                                       state=state)
        await message.delete()
        await state.update_data(whitch_kb_was='calendar_kb')
        msg = await message.answer(text='Идет загрузка...')
        msg1 = await message.answer(text=GS(family=user_sn, day=message.text).today_data_work()[0],
                                    reply_markup=calendar_kb.as_markup())
        await msg.delete()
        await support_function.delete_pre_message.del_pre_message(chat_id=msg1.chat.id,
                                                                  message_id=msg1.message_id,
                                                                  state=state)
