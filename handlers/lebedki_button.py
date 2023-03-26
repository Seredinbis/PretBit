import support_function

from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.reply_markup.main import main_kb
from keyboards.reply_inline.choose_show import choose_lebedki_kb


router_lebedki = Router()


@router_lebedki.message(Text('Лебедки'))
async def get_lebedki(message: Message, state: FSMContext) -> None:
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    if await support_function.login_test.log_test(message=message,
                                                  state=state):

        user_data = await state.get_data()
        user_sn = user_data['user_second_name']
        if user_sn not in ('Касырев', 'Глухов', 'Середин', 'Леонов'):
            msg = await message.answer(text='ДОСТУП ЗАПРЕЩЕН',
                                       reply_markup=main_kb)
            await state.update_data(whitch_kb_was='main_kb')
        else:
            msg = await message.answer(text='Пожалуйста выберите необходимы спектакль',
                                       reply_markup=choose_lebedki_kb.as_markup())
            await state.update_data(whitch_kb_was='main_kb')
        await message.delete()
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)