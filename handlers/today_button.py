import support_function

from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sql_data.sql import session, Employee
from sheets_api.gs_pandas import LightPerson
from keyboards.reply_markup.main import main_kb


router_today = Router()


@router_today.message(Text('Сегодня'))
async def get_today(message: Message, state: FSMContext):
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    if await support_function.login_test.log_test(message=message,
                                                  state=state):
        with session as ses:
            user_sn = ses.query(Employee.last_name).filter(Employee.id == message.from_user.id).scalar()
        if user_sn in ('Василевский', 'Крусcер'):
            msg = await message.answer(text='Для вас эта функция пока не активна')
            await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                      message_id=msg.message_id,
                                                                      state=state)
            await message.delete()
        else:
            await message.delete()
            msg1 = await message.answer(text='Идет загрузка данных...')
            msg = await message.answer(text=LightPerson(last_name=user_sn).get_message(),
                                       reply_markup=main_kb,
                                       parse_mode='HTML')
            await state.update_data(whitch_kb_was='main_kb')
            await msg1.delete()
            await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                      message_id=msg.message_id,
                                                                      state=state)
