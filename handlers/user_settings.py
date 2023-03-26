import support_function

from aiogram.filters import Text
from aiogram.types import Message, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram import Router
from keyboards.reply_inline.how_del_pre_message import how_del_pre_message_kb
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from keyboards.reply_markup.user_setting import user_settings_kb


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
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    if await support_function.login_test.log_test(message=message,
                                                  state=state):
        msg = await message.answer(text='Вы можете настроить количество сообщений, которые будут постоянное оставаться'
                                        ' в диалоговом окне',
                                   reply_markup=how_del_pre_message_kb.as_markup())
        await state.update_data(whitch_kb_was='main_kb')
        await message.delete()
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)


@router_user_settings.message(Text('Автоматическая рассылка и оповещение'))
async def get_auto(message: Message, state: FSMContext) -> None:
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    if await support_function.login_test.log_test(message=message,
                                                  state=state):
        user_data = await state.get_data()
        # тут генерируем клавиатуру, включения/выключения автоматической рассылкb
        if 'auto_send_file' in user_data:
            if user_data['auto_send_file'] == 'enable':
                auto_send_kb = ReplyKeyboardBuilder()
                auto_send_kb.row(KeyboardButton(text='Выключить'))
                auto_send_kb.row(KeyboardButton(text='Назад'))
            elif user_data['auto_send_file'] == 'disable':
                auto_send_kb = ReplyKeyboardBuilder()
                auto_send_kb.row(KeyboardButton(text='Включить'))
                auto_send_kb.row(KeyboardButton(text='Назад'))
        else:
            auto_send_kb = ReplyKeyboardBuilder()
            auto_send_kb.row(KeyboardButton(text='Включить'))
            auto_send_kb.row(KeyboardButton(text='Назад'))
        await support_function.user_tracking.where_who(where=message.text,
                                                       state=state)
        msg = await message.answer(text='Автоматическая рассылка! Пожалуйста включите, либо выключите рассылку!'
                                        'Оповещение будет приходить за 2 часа до начала смены. Присланные файлы'
                                        ' удалятся через 10 часов, после оповещения.',
                                   reply_markup=auto_send_kb.as_markup())
        await state.update_data(whitch_kb_was='user_settings_kb')
        await message.delete()
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)


@router_user_settings.message(Text('Включить'))
async def enable_auto(message: Message, state: FSMContext) -> None:
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    if await support_function.login_test.log_test(message=message,
                                                  state=state):
        user_data = await state.get_data()
        await state.update_data(auto_send_file='enable')
        auto_send_kb = ReplyKeyboardBuilder()
        auto_send_kb.row(KeyboardButton(text='Выключить'))
        auto_send_kb.row(KeyboardButton(text='Назад'))
        msg = await message.answer(text='Вы включили автоматическую рассылку! Данная функция находится на тестирвании, '
                                        'могут быть ошибки!',
                                   reply_markup=auto_send_kb.as_markup())
        await state.update_data(whitch_kb_was='user_settings_kb')
        await message.delete()
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)
        await support_function.prepare_send(user_id=message.from_user.id,
                                            user_name=user_data['user_second_name'],
                                            condition=user_data['auto_send_file'])


@router_user_settings.message(Text('Выключить'))
async def disable_auto(message: Message, state: FSMContext) -> None:
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    if await support_function.login_test.log_test(message=message,
                                                  state=state):
        await state.update_data(auto_send_file='disable')
        auto_send_kb = ReplyKeyboardBuilder()
        auto_send_kb.row(KeyboardButton(text='Включить'))
        auto_send_kb.row(KeyboardButton(text='Назад'))
        msg = await message.answer(text='Вы выключили автоматическую рассылку! Данная функция находится на тестирвании,'
                                        ' могут быть ошибки!',
                                   reply_markup=auto_send_kb.as_markup())
        await state.update_data(whitch_kb_was='user_settings_kb')
        await message.delete()
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)
