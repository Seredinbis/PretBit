import support_function
import asyncio

from aiogram.filters import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Router
from keyboards.reply_inline.how_del_pre_message import how_del_pre_message_kb
from keyboards.reply_inline.how_del_file import how_del_files_kb
from keyboards.reply_markup.user_setting import user_settings_kb
from keyboards.reply_markup.main import main_kb
from sql_data.sql import session
from sqlalchemy import text as rawreq

router_user_settings = Router()


# обработка кнопки в главном меню
@router_user_settings.message(Text('Настройки пользователя'))
async def get_settings(message: Message, state: FSMContext) -> None:
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    if await support_function.login_test.log_test(message=message,
                                                  state=state):
        msg = await message.answer(text='Меню пользовательских настроек!',
                                   reply_markup=user_settings_kb)
        await state.update_data(whitch_kb_was='main_kb')
        await message.delete()
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)


@router_user_settings.message(Text('Сколько последних сообщений оставлять'))
async def get_del_pre(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    if await support_function.login_test.log_test(message=message,
                                                  state=state):
        msg = await message.answer(text='Вы можете настроить количество сообщений, которые будут постоянное оставаться'
                                        ' в диалоговом окне',
                                   reply_markup=how_del_pre_message_kb.as_markup())
        await state.update_data(whitch_kb_was='main_kb')
        # следующий кусок кода, удаляет инлайн клавиатуру, после получения коллбэка, i_can_del служит флагом для
        # удаления сообщшения с клавиатурой
        while 'i_can_del_mess' not in user_data or not user_data['i_can_del_mess']:
            user_data = await state.get_data()
            await asyncio.sleep(1)
        if user_data['i_can_del_mess']:
            await msg.delete()
        await message.delete()
        await state.update_data(i_can_del_mess=False)


@router_user_settings.message(Text('Через сколько часов удалять файлы'))
async def get_del_files(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    if await support_function.login_test.log_test(message=message,
                                                  state=state):
        msg = await message.answer(text='Вы можете настроить через сколько часов вы бы хотели, чтобы файлы удалились!',
                                   reply_markup=how_del_files_kb.as_markup())
        await state.update_data(whitch_kb_was='main_kb')
        while 'i_can_del_file' not in user_data or not user_data['i_can_del_file']:
            user_data = await state.get_data()
            await asyncio.sleep(1)
        if user_data['i_can_del_file']:
            await msg.delete()
        await message.delete()
        await state.update_data(i_can_del_file=False)


@router_user_settings.message(Text(startswith='Запрос:'))
async def get_request(message: Message, state: FSMContext) -> None:
    if message.from_user.id == 327169698:
        await support_function.user_tracking.where_who(where=message.text,
                                                       state=state)
        if await support_function.login_test.log_test(message=message,
                                                      state=state):
            request = message.text.split(':')[1]
            try:
                with session as s:
                    result = s.execute(rawreq(request)).all()
                    res = ''
                    for que in result:
                        res += f'{que}\n'
                    msg = await message.answer(text=result,
                                               reply_markup=main_kb)
                    await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                              message_id=msg.message_id,
                                                                              state=state)
            except BaseException:
                text = 'Ошибка запроса, ваш запрос не прошел!'
                msg = await message.answer(text=text,
                                           reply_markup=main_kb)
                await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                          message_id=msg.message_id,
                                                                          state=state)


