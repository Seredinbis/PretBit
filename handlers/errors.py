from aiogram.types import Message, ErrorEvent
from aiogram.fsm.context import FSMContext
from aiogram import Router, exceptions
from bot import user_track
from aiogram.filters import Text
from keyboards.reply_markup.main import main_kb

import support_function

router_error = Router()


@router_error.errors()
async def er(er1: ErrorEvent, state: FSMContext) -> None:
    user_data = await state.get_data()
    user_track.append(f'БЫЛА ОШИБКА\nuser_id = {user_data["user_id"]}:{user_data["user_second_name"]}\n'
                      f' ошибка = {er1.exception}\n ошибка = {exceptions}')


@router_error.message(Text('Ошибки'))
async def get_lebedki(message: Message, state: FSMContext) -> None:
    text = ''.join(user_track)
    if len(text) > 4000:
        text = text[-4000:]
    msg = await message.answer(text=text,
                               reply_markup=main_kb)
    await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                              message_id=msg.message_id,
                                                              state=state)
