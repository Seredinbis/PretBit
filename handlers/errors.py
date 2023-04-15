from aiogram.types import Message, ErrorEvent
from aiogram.fsm.context import FSMContext
from aiogram import Router, exceptions
from bot import bot


router_error = Router()


@router_error.errors()
async def er(er1: ErrorEvent, state: FSMContext) -> None:
    user_data = await state.get_data()
    await bot.send_message(chat_id=327169698,
                           text=f'БЫЛА ОШИБКА\nuser_id = {user_data["user_id"]}:{user_data["user_second_name"]}\n'
                                f'ошибка = {er1.exception}')