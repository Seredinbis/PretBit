import support_function

from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sheets_api.g_sheets import ResultPrint
from keyboards.reply_markup.main import main_kb


router_today = Router()


@router_today.message(Text('Сегодня'))
async def get_today(message: Message, state: FSMContext):
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    if await support_function.login_test.log_test(message=message,
                                                  state=state):
        user_data = await state.get_data()
        user_sn = user_data['user_second_name']
        if user_sn in ('Василевский', 'Крусcер'):
            msg = await message.answer(text='Для вас будет использоваться график Быковой Ангелины!')
            await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                      message_id=msg.message_id,
                                                                      state=state)
            # возможно будет изменения в if_work и [0] не будет
            await message.delete()
            msg2 = await message.answer(text='Идет загрузка данных...')
            msg1 = await message.answer(text=ResultPrint('Великанова').today_button()[0],
                                        reply_markup=main_kb)
            await state.update_data(whitch_kb_was='main_kb')
            await msg2.delete()
            await support_function.delete_pre_message.del_pre_message(chat_id=msg1.chat.id,
                                                                      message_id=msg1.message_id,
                                                                      state=state)
        else:
            await message.delete()
            msg1 = await message.answer(text='Идет загрузка данных...')
            msg = await message.answer(text=ResultPrint(user_sn).today_button()[0],
                                       reply_markup=main_kb)
            await state.update_data(whitch_kb_was='main_kb')
            await msg1.delete()
            await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                      message_id=msg.message_id,
                                                                      state=state)
