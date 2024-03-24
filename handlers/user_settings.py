import support_function
import asyncio
import os

from aiogram.filters import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Router
from keyboards.reply_inline.inline_builder import SettingsInlineKeyboard
from keyboards.reply_markup.reply_builder import MultiKeyboard
from config_data.data import Settings
from keyboards.reply_markup.reply_builder import MainReplyKeyboard
from sql_data.sql import session
from sqlalchemy import text as rawreq
from config_data.secret import dev_id



router_user_settings = Router()


# обработка кнопки в главном меню
@router_user_settings.message(Text('Настройки пользователя'))
async def get_settings(message: Message, state: FSMContext) -> None:
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    if await support_function.login_test.log_test(message=message):
        keyboard = MultiKeyboard(Settings).build()
        msg = await message.answer(text='Меню пользовательских настроек!',
                                   reply_markup=keyboard.as_markup())
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
    if await support_function.login_test.log_test(message=message):
        keyboard = SettingsInlineKeyboard().build()
        msg = await message.answer(text='Вы можете настроить количество сообщений, которые будут постоянное оставаться'
                                        ' в диалоговом окне',
                                   reply_markup=keyboard.as_markup())
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
    if await support_function.login_test.log_test(message=message):
        keyboard = SettingsInlineKeyboard().build()
        msg = await message.answer(text='Вы можете настроить через сколько часов вы бы хотели, чтобы файлы удалились!',
                                   reply_markup=keyboard.as_markup())
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
    if message.from_user.id == dev_id:
        await support_function.user_tracking.where_who(where=message.text,
                                                       state=state)
        if await support_function.login_test.log_test(message=message):
            request = message.text.split(':')[1]
            keyboard = MainReplyKeyboard().build()
            try:
                with session as s:
                    result = s.execute(rawreq(request)).all()
                    res = ''
                    for que in result:
                        res += f'{que}\n'
                    msg = await message.answer(text=result,
                                               reply_markup=keyboard.as_markup())
                    await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                              message_id=msg.message_id,
                                                                              state=state)
            except BaseException:
                text = 'Ошибка запроса, ваш запрос не прошел!'
                msg = await message.answer(text=text,
                                           reply_markup=keyboard.as_markup())
                await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                          message_id=msg.message_id,
                                                                          state=state)


