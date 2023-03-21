from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router
from keyboards.reply_inline.choose_second_name import choose_second_name_kb


router = Router()
@router.message(Command(commands=["start"]))
async def start(message: Message, state: FSMContext):
    # await print_user(message.from_user.id, message.text)
    user_data = await state.get_data()
    if message.from_user.id not in user_data:
        await state.update_data(user_id=message.from_user.id)
        await message.answer(text='Пожайлуста, выберите свою фамилию из списка!',
                             reply_markup=choose_second_name_kb)

@router.callback_query()
async def set_user_second_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text='Выбор соответсвующей фамилии напрямую зависит на корректную работу бота!',
                          show_alert=True)
    await state.update_data(user_second_name=callback.data)
    print(await state.get_data())





